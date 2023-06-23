import os

class ConfigurationMenu:
    def __init__(self):
        self.connections = []
    
    def load_connections(self):
        file_path = r'C:\Users\code\Documents\WorkComputerTransfer\Programming\Python\Apps\Autossh\connections.txt'
        try:
            with open(file_path, "r") as file:
                self.connections = file.read().splitlines()
            print("Connections loaded successfully.")
        except FileNotFoundError:
            print("Connections file not found.")
    
    def print_connections(self):
        if self.connections:
            print("Connections:")
            for i, connection in enumerate(self.connections, start=1):
                print(f"{i}. {connection}")
        else:
            print("No connections available.")
  
    def choose_connection(self):
        if not self.connections:
            print("No connections available.")
            return None

        while True:
            self.print_connections()
            choice = input("Enter the line number of the connection (1-{}), or 'q' to cancel: ".format(len(self.connections)))
            try:
                line_number = int(choice)
                if 1 <= line_number <= len(self.connections):
                    selected_connection = self.connections[line_number - 1]
                    print(f"My connection: {selected_connection}")
                    return selected_connection
                else:
                    print("Invalid line number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid line number or 'q' to cancel.")

    def add_connection(self, new_connection):
        self.connections.append(new_connection)
        print("Connection added successfully.")

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)
            print("Connection removed successfully.")
        else:
            print("Connection not found.")

    def edit_connection(self, line_number, new_connection):
        if 1 <= line_number <= len(self.connections):
            self.connections[line_number - 1] = new_connection
            print("Connection edited successfully.")
        else:
            print("Invalid line number.")

    def save_connections(self):
        with open("connections.txt", "w") as file:
            for connection in self.connections:
                file.write(connection + "\n")
        print("Connections saved successfully.")

    def display_menu(self):
        self.load_connections()
        while True:
            print("\n=== Config Menu ===\
                    \n1. Make Connection\
                    \n2. Print connections\
                    \n3. Add connection\
                    \n4. Remove connection\
                    \n5. Edit connection\
                    \n6. Clear Screen\
                    \n7. Back")
            choice = int(input("Enter your choice (1-8): "))

            if choice == 1:
                self.choose_connection()
            elif choice == 2:
                self.print_connections()
            elif choice == 3:
                new_connection = input("Enter the new connection: ")
                self.add_connection(new_connection)
                self.save_connections()
            elif choice == 4:
                connection_to_remove = input("Enter the connection to remove: ")
                self.remove_connection(connection_to_remove)
                self.save_connections()
            elif choice == 5:
                self.print_connections
                line_number = int(input("Enter the line number to edit: "))
                new_connection = input("Enter the new connection: ")
                self.edit_connection(line_number, new_connection)
                self.save_connections()
            elif choice == 6:
                self.save_connections()
            elif choice == 7:
                os.system("cls")
            elif choice == 8:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
