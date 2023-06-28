import os
import shell
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class ConfigurationMenu:
    def __init__(self):
        self.ips = []  # Initialize the list of IP addresses

    def select_file(self):
        self.clear_screen()
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Display custom message
        messagebox.showinfo("Remote Automation", "Please select a text file to store IP addresses.")

        file_path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        print("Selected file:", file_path)
        return file_path

    def start_connection(self):
        ips = self.ips
        shell.ShellMenu().menu(ips)  # Start a connection using the IP addresses

    def load_ip_addresses(self):
        path = self.select_file()
        try:
            with open(path, "r") as file:
                self.ips = file.read().splitlines()  # Read IP addresses from a file and store them in the list
                return path
            print("IPs loaded successfully.")
        except FileNotFoundError:
            print("File not found.")

    def print_ip_addresses(self):
        if self.ips:
            print("IPs:")
            for i, ip in enumerate(self.ips, start=1):
                print(f"{i}. {ip}")  # Print the list of IP addresses
        else:
            print("No IP addresses available.")

    def add_ip_address(self, new_ip):
        if new_ip in self.ips:
            print("IP address already exists.")
        else:
            self.ips.append(new_ip)  # Add a new IP address to the list
            print("IP added successfully.")

    def remove_ip_address(self, line_number):
        if 1 <= line_number <= len(self.ips):
            removed_ip = self.ips.pop(line_number - 1)  # Remove the IP address at the specified line number
            print(f"IP '{removed_ip}' removed successfully.")
        else:
            print("Invalid line number.")

    def edit_ip_address(self, line_number, new_ip):
        if 1 <= line_number <= len(self.ips):
            self.ips[line_number - 1] = new_ip  # Replace the IP address at the specified line number with the new IP
            print("IP edited successfully.")
        else:
            print("Invalid line number.")

    def save_ip_addresses(self, path):
        self.ips.sort()  # Sort the IP addresses in ascending order
        with open(path, "w") as file:
            file.writelines(ip + "\n" for ip in self.ips)  # Write the IP addresses to a file
        print("IPs saved successfully.")

    def clear_screen(self):
        os.system("clear" if os.name == "posix" else "cls")

    def main_menu(self):
        path = self.load_ip_addresses()  # Load IP addresses from a file
        self.clear_screen()
        while True:
            print("\n=== Config Menu ===\
                    \n1. Start Connection\
                    \n2. Print IPs\
                    \n3. Add IP\
                    \n4. Remove IP\
                    \n5. Edit IP\
                    \n6. Clear Screen\
                    \n7. Exit")
            choice = int(input("Enter your choice (1-7): "))  # Prompt the user for a menu choice
            if choice == 1:
                self.clear_screen()
                self.start_connection()  # Start a connection using the IP addresses
            elif choice == 2:
                self.clear_screen()
                self.print_ip_addresses()  # Print the list of IP addresses
            elif choice == 3:
                self.clear_screen()
                new_ip = input("Enter the new IP address: ")
                self.add_ip_address(new_ip)  # Add a new IP address to the list
                self.save_ip_addresses(path)  # Save IP addresses to a file
            elif choice == 4:
                self.clear_screen()
                self.print_ip_addresses()
                line_number = int(input("Enter the line number of the IP address to remove: "))
                self.remove_ip_address(line_number)  # Remove an IP address from the list
                self.save_ip_addresses(path)  # Save IP addresses to a file
            elif choice == 5:
                self.clear_screen()
                self.print_ip_addresses()
                line_number = int(input("Enter the line number of the IP address to edit: "))
                new_ip = input("Enter the new IP address: ")
                self.edit_ip_address(line_number, new_ip)  # Edit an IP address in the list
                self.save_ip_addresses(path)  # Save IP addresses to a file
            elif choice == 6:
                self.clear_screen()
            elif choice == 7:
                self.save_ip_addresses(path)  # Save IP addresses to a file
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
