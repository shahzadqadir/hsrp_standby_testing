#!/usr/bin/python3

from connectivity import Connectivity
from getpass import getpass

def check_standby(hostname: str, username: str, password: str) -> dict:
    """Check Standby status and returns it as a Dict.

    Args:
        hostname (str): hostname or IP Address of host in string format
        username (str): username of host

    Returns:
        dict: Format {'group': [priority, status]}
    """

    cpe_host = Connectivity(hostname, username, password)
    cpe_host.connect()
    raw_output = cpe_host.show_command("show standby brief")
    results_dict = dict()
    for line in raw_output[0].split('\n')[3:]:
        results_dict[f"group-{line.split()[1]}"] = [line.split()[2], line.split()[4]]
    return results_dict   


def compare_standby_groups(host1: list, host2: list) -> dict:
    """Takes two hosts and compare their standby outputs to determine if there is anything wrong in the configs
    or Physical state of the network.

    Args:
        host1 (dict): Format: ["hostname or ip", "username", "password"]
        host2 (dict): Format: ["hostname or ip", "username", "password"]

    Returns:
        dict: TODO: PROVIDE FORMAT OF OUTPUT
    """
    results = dict()
    results["hsrp_results"] = []
    results["hsrp_results"].append({"CE1":[]})
    results["hsrp_results"].append({"CE2":[]})

    
    if type(host1) != list or type(host2) != list or len(host1) < 3 or len(host2) < 3:
        raise Exception("input format expected: ['ip_address', 'username', 'password']")
    
    try:
        cpe1 = check_standby(host1[0], host1[1], host1[2])
        cpe2 = check_standby(host2[0], host2[1], host2[2])

        for group in cpe1.keys():        
            if cpe1[group][0] > cpe2[group][0]:
                if cpe1[group][1] == 'Active':
                    results["hsrp_results"][0]["CE1"].append({group.capitalize(): "Pass"})
                else:
                    results["hsrp_results"][0]["CE1"].append({group.capitalize(): "No longer Active"})
                if cpe2[group][1] == 'Standby':
                    results["hsrp_results"][1]["CE2"].append({group.capitalize(): "Pass"})
                else:
                    results["hsrp_results"][1]["CE2"].append({group.capitalize(): "No longer Standby"})
            else:
                if cpe2[group][1] == 'Active':
                    results["hsrp_results"][1]["CE2"].append({group.capitalize(): "Pass"})
                else:
                    results["hsrp_results"][1]["CE2"].append({group.capitalize(): "No longer Active"})
                if cpe1[group][1] == 'Standby':
                    results["hsrp_results"][0]["CE1"].append({group.capitalize(): "Pass"})
                else:
                    results["hsrp_results"][0]["CE1"].append({group.capitalize(): "No longer Standby"})      
    except:
        raise Exception("Something went wrong, detailed exception handing in progress!")
    return results



if __name__ == "__main__":
    result = compare_standby_groups(["10.10.100.1", "admin", "cisco123"], ["10.10.100.2", "admin", "cisco123"])
    print(result)
