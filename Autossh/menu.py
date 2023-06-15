from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
import connect


def create_table():
    conn = sqlite3.connect("connections.db")
    c = conn.cursor()

    # Check if the table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='connections'")
    table_exists = c.fetchone()

    if not table_exists:
        # Create a new table
        c.execute("""
            CREATE TABLE connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT,
                username TEXT
            )
        """)
    conn.commit()
    conn.close()

def insert_connection(connection):
    conn = sqlite3.connect("connections.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO connections (hostname, username)
        VALUES (?, ?)
    """, (connection["hostname"], connection["username"]))
    conn.commit()
    conn.close()

def update_connection(connection):
    conn = sqlite3.connect("connections.db")
    c = conn.cursor()
    c.execute("""
        UPDATE connections SET
        hostname = ?,
        username = ?
        WHERE id = ?
    """, (connection["hostname"], connection["username"], connection["id"]))
    conn.commit()
    conn.close()

# Function to delete a connection from the database
def delete_connection(connection_id):
    conn = sqlite3.connect("connections.db")
    c = conn.cursor()
    c.execute("DELETE FROM connections WHERE id = ?", (connection_id,))
    conn.commit()
    conn.close()


# Function to retrieve all connections from the database
def get_connections():
    conn = sqlite3.connect("connections.db")
    c = conn.cursor()
    c.execute("SELECT * FROM connections")
    connections = c.fetchall()
    conn.close()
    return connections

class ConnectionPage(QWidget):
    def __init__(self, connections):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setGeometry(600, 200, 400, 400)

        # Create a QTableWidget
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Add one column for checkboxes
        self.table.setHorizontalHeaderLabels(["", "ID", "Hostname", "Username"])

        self.layout.addWidget(self.table)

        # Create buttons for "Reset Moxa" and "Stable Connection"
        self.reset_button = QPushButton("Reset Moxa")
        self.stable_button = QPushButton("Stable Connection")

        # Connect the reset_button clicked signal to the functions
        self.reset_button.clicked.connect(self.reset_moxa)
        self.stable_button.clicked.connect(self.stable_connection)

        # Set button labels and font size
        self.reset_button.setText("Reset Moxa")
        self.stable_button.setText("Stable Connection")
        self.reset_button.setStyleSheet("font-size: 16px;")
        self.stable_button.setStyleSheet("font-size: 16px;")

        # Password
        self.layout.addWidget(QLabel.setStyleSheet("Password:"))
        self.password_edit = QLineEdit()

        # Add the buttons to the layout
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.stable_button)


        self.back_button = QPushButton("Back")
        self.layout.addWidget(self.back_button)

        self.back_button.clicked.connect(self.go_to_main_menu)

        # Initialize the table with data
        self.populate_table(connections)

    def populate_table(self, connections):
        # Set the number of rows in the table
        self.table.setRowCount(len(connections))

        # Populate the table with connection data
        for row, connection in enumerate(connections):
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            self.table.setCellWidget(row, 0, checkbox)

            for column, value in enumerate(connection):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, column + 1, item)

        # Resize the columns to fit the contents
        self.table.resizeColumnsToContents()
        # Resize the rows to fit the contents
        self.table.resizeRowsToContents()


    def reset_moxa(self):
        password = self.password_edit.text()
        checked_rows = []

        for row in range(self.table.rowCount()):
            checkbox_item = self.table.cellWidget(row, 0)
            if isinstance(checkbox_item, QCheckBox) and checkbox_item.isChecked():
                connection_id = int(self.table.item(row, 1).text())
                hostname = self.table.item(row, 2).text()
                username = self.table.item(row, 3).text()

                checked_rows.append({
                    "connection_id": connection_id,
                    "hostname": hostname,
                    "username": username
                })

        if checked_rows:
            # Create a dropdown menu
            dropdown = QComboBox()
            dropdown.addItems(["Option 1", "Option 2", "Option 3"])

            # Show the dropdown menu
            choice = dropdown.exec_()
            selected_option = dropdown.currentText()

            print("Selected Option:", selected_option)
            # Perform actions with the selected connections based on the dropdown choice
            # connect.run_script(hostname, username, password, selected_option)
        else:
            print("No connections selected.")

    # ...

        # connect.run_script(checked_rows[0]["hostname"], checked_rows[0]["username"], password)


    def stable_connection(self):
        password = self.password_edit.text()
        checked_rows = []
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.cellWidget(row, 0)
            if isinstance(checkbox_item, QCheckBox) and checkbox_item.isChecked():
                connection_id = int(self.table.item(row, 1).text())
                hostname = self.table.item(row, 2).text()
                username = self.table.item(row, 3).text()
                checked_rows.append({
                    "connection_id": connection_id,
                    "hostname": hostname,
                    "username": username
                })
        # for x in checked_rows:
        #     print(x)
        connect.stable_connection(checked_rows[0]["hostname"], checked_rows[0]["username"])


    def go_to_main_menu(self):
        main_menu.show()
        self.close()



class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setGeometry(600, 200, 400, 400)

        self.schedule_button = QPushButton("Connect")
        self.database_button = QPushButton("Edit Database")

        self.layout.addWidget(self.schedule_button)
        self.layout.addWidget(self.database_button)

        self.schedule_button.clicked.connect(self.open_connections_page)
        self.database_button.clicked.connect(self.open_database_page)

    def open_database_page(self):
        self.database_page = ConnectionManagement()  # Create an instance variable to keep the reference
        self.database_page.show()
        self.hide()  # Hide the current window
    
    def open_connections_page(self):
        connections = get_connections()
        self.connections_page = ConnectionPage(connections)
        self.connections_page.show()
        self.hide()
    


class ConnectionManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connection Database")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setGeometry(600, 200, 400, 400)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Hostname", "Username"])

        self.layout.addWidget(self.table)

        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_widget.setLayout(self.form_layout)

        self.hostname_label = QLabel("Client's IP Address:")
        self.hostname_edit = QLineEdit()

        self.username_label = QLabel("Client's Username:")
        self.username_edit = QLineEdit()

        self.add_button = QPushButton("Add connection")
        self.update_button = QPushButton("Update connection")
        self.delete_button = QPushButton("Delete connection")

        # set button size
        self.add_button.setFixedSize(150, 50)
        self.update_button.setFixedSize(150, 50)
        self.delete_button.setFixedSize(150, 50)

        self.form_layout.addWidget(self.hostname_label)
        self.form_layout.addWidget(self.hostname_edit)
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_edit)

        self.form_layout.addWidget(self.add_button)
        self.form_layout.addWidget(self.update_button)
        self.form_layout.addWidget(self.delete_button)

        

        self.layout.addWidget(self.form_widget)

        
        self.add_button.clicked.connect(self.add_connection)
        self.update_button.clicked.connect(self.update_connection)
        self.delete_button.clicked.connect(self.delete_connection)
        self.table.clicked.connect(self.row_clicked)

        self.refresh_table()
        self.back_button = QPushButton("Back")
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.go_to_main_menu)

    def go_to_main_menu(self):
        main_menu.show()
        self.close()

    def resize_table_columns(self):
        self.table.resizeColumnsToContents()

    # Slot function to handle row clicks in the table
    def row_clicked(self, index):
        row = index.row()
        connection_id = int(self.table.item(row, 0).text())
        hostname = self.table.item(row, 1).text()
        username = self.table.item(row, 2).text()

        self.hostname_edit.setText(hostname)
        self.username_edit.setText(username)

    def refresh_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        database = get_connections()

        for connection in database:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, value in enumerate(connection):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_position, column, item)
        # Resize the columns to fit the contents
        self.table.resizeColumnsToContents()

    def add_connection(self):
        hostname = self.hostname_edit.text().strip()
        username = self.username_edit.text().strip()

        if not hostname:
            QMessageBox.warning(self, "Error", "Please enter a Hostname.")
            return

        if not username:
            QMessageBox.warning(self, "Error", "Please enter a Username.")
            return

        connection = {
            "hostname": hostname,
            "username": username
        }
        insert_connection(connection)

        self.refresh_table()
        self.hostname_edit.clear()
        self.username_edit.clear()

    def update_connection(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "No connection selected.")
            return

        connection_id = int(self.table.item(row, 0).text())
        hostname = self.hostname_edit.text().strip()
        username = self.username_edit.text().strip()

        if not hostname:
            QMessageBox.warning(self, "Error", "Please enter a Hostname.")
            return

        if not username:
            QMessageBox.warning(self, "Error", "Please enter a Username.")
            return

        connection = {
            "id": connection_id,
            "hostname": hostname,
            "username": username
        }
        update_connection(connection)
        self.refresh_table()
        self.hostname_edit.clear()
        self.username_edit.clear()

    def delete_connection(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "No connection selected.")
            return

        connection_id = int(self.table.item(row, 0).text())
        delete_connection(connection_id)

        self.refresh_table()
        self.hostname_edit.clear()
        self.username_edit.clear()

    def select_date(self):
        dialog = QDialog(self)
        calendar = QCalendarWidget(dialog)
        calendar.setGridVisible(True)
        calendar.clicked.connect(lambda date: self.set_date(date, dialog))

        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(calendar)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def set_date(self, date, dialog):
        self.username_edit.setText(date.toString(Qt.ISODate))
        dialog.close()

def get_connection_rows():
    conn = sqlite3.connect("connections.db")
    c = conn.cursor()
    c.execute("SELECT * FROM connections")
    return c.fetchall()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    create_table()

    main_menu = MainMenu()
    main_menu.show()

    sys.exit(app.exec_())
