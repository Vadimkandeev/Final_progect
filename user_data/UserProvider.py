import configparser

global_config = configparser.ConfigParser()
global_config.read('user_config.ini')

class UserProvider:
    def __init__(self) -> None:
        self.config = global_config

    def get(self, section: str, prop: str):
        return self.config[section].get(prop)

    def getint(self, section: str, prop: str):
        return self.config[section].getint(prop)
    
    def get_user_token(self):
        return self.config["user"].get("token")
    
    def get_user_username(self):
        return self.config["user"].get("username")
    
    def get_user_email(self):
        return self.config["user"].get("email")
    
    def get_user_password(self):
        return self.config["user"].get("password")