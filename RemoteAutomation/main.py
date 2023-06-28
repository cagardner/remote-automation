import app

def menu():
    flag = False
    while not flag:
        config_menu = app.ConfigurationMenu()
        config_menu.main_menu()

if __name__ == "__main__":
    menu()