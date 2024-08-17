import paramiko


class Connectivity:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                allow_agent=False,
                look_for_keys=False,
            )
            self.connection = ssh_client
        except:
            raise Exception("Something went wrong!")

    def show_command(self, command):
        outputs = []
        stdin, stdout, stderr = self.connection.exec_command(command=command)
        stdout = stdout.read().decode("ascii").strip()
        outputs.append(stdout)
        return outputs

    def check_arp(self, ip_to_find):
        self.connect()
        arp = self.show_command("show ip arp")
        for k in arp:
            if ip_to_find in k:
                return True
        return False
    
    def count_arp_entries(self):
        self.connect()
        arp = self.show_command("show ip arp")
        return len(arp[0].split("\n"))-1



        



if __name__ == "__main__":
    h1 = Connectivity("10.10.100.1", "admin", "cisco123")
    print(h1.check_arp("10.10.100.12"))
    print(h1.count_arp_entries())
