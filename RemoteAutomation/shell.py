import paramiko
import os

class ShellMenu:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def menu(self, ips):
        flag = False
        while not flag:
            print("--- SSH Connection Menu ---\
                \n1. Run a script remotely\
                \n2. Run a stable connection\
                \n3. Open multiple command prompt windows\
                \n4. Ping Host\
                \n5. Run a traceroute\
                \n6. Back")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.run_script()  # Call the method to run a script remotely
            elif choice == "2":
                ip = self.choose_hostname(ips)  # Choose a hostname from the provided IP addresses
                if ip is not None:
                    self.stable_connection(ip)  # Establish a stable SSH connection with the selected hostname
            elif choice == "3":
                num_windows = int(input("Enter the number of command prompt windows to open: "))
                self.open_command_prompt_windows(num_windows)  # Open multiple command prompt windows
            elif choice == "4":
                ip = self.choose_hostname(ips)  # Choose a hostname from the provided IP addresses
                os.system(f'ping {ip}')  # Ping the selected host
            elif choice == "5":
                ip = self.choose_hostname(ips)  # Choose a hostname from the provided IP addresses
                windows = f"tracert {ip}"
                linux = f"traceroute {ip}"
                if os.name == "posix":
                    os.system(linux)  # Run traceroute on Linux
                else:
                    os.system(windows)  # Run traceroute on Windows
            elif choice == "6":
                flag = True  # Exit the menu loop
            else:
                input("Invalid choice. Press Enter to continue...")  # Prompt for valid input

    def choose_hostname(self, ips):
        os.system("clear" if os.name == "posix" else "cls")
        for i, ip in enumerate(ips, start=1):
            print(f"{i}. {ip}")
        if not ips:
            print("No IP addresses available.")
            return None
        while True:
            choice = input(f"Enter the line number (1-{len(ips)})\nOr enter any letter to cancel: ")
            try:
                line_number = int(choice)
                if 1 <= line_number <= len(ips):
                    selected_ip = ips[line_number - 1]
                    print(f"\nAddress selected:\n{selected_ip}")
                    return selected_ip
                else:
                    print("\nInvalid line number. Please try again.\n")
            except ValueError:
                print("...")
                break

    def open_command_prompt_windows(self, num_windows):
        for _ in range(num_windows):
            os.system("terminal" if os.name == "posix" else "start cmd")  # Open a command prompt window
        input("Press Enter to continue...")  # Wait for user confirmation

    def run_script(self):
        # Update this method as per your requirement
        pass

    def stable_connection(self, hostname):
        username = input('Username: ')
        password = input('Password: ')

        try:
            self.client.connect(hostname=hostname, username=username, password=password)  # Establish SSH connection
            shell = self.client.invoke_shell()  # Create an interactive shell
            self.interact(shell)  # Start interacting with the shell
        except Exception as e:
            print(e)
        finally:
            self.client.close()  # Close the SSH connection
            print("SSH connection closed.\n\n")

    def interact(self, shell):
        while True:
            try:
                if shell.recv_ready():
                    data = shell.recv(1024)  # Receive data from the shell
                    print(data.decode(), end='')  # Print the received data

                if not shell.closed and not shell.exit_status_ready():
                    input_data = input()  # Get user input
                    shell.sendall(input_data + '\n')  # Send user input to the shell

            except (EOFError, KeyboardInterrupt):
                break  # Exit the interaction loop
