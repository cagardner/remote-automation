import config

def main_menu():
    flag = False
    while not flag:
        config_menu = config.ConfigurationMenu()
        config_menu.display_menu()
if __name__ == "__main__":
    main_menu()
