import re
import subprocess

import kivy
from kivy.uix.recycleview import RecycleView
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import ListProperty

kivy.require('2.1.0')


class RVScreen(Screen):
    pass


class RVLabel(Label):
    pass


class RV(RecycleView):
    # see video about passing variables link in description

    # what do we need for recycleview: list of dictionaries
    # [{'text': 'text for label 1 in RV'},{'text': 'text for label 2 in RV'},{'text': 'text for label 3 in RV'}]
    # number of dictionaries =  the number of items in your RV, which is not fixed
    rv_data_list = ListProperty([])

    # Let's look at 2 ways of passing variables between kv and Python
    #1. use instance properties
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.rv_data_list =[{'text': res} for res in self.get_rv_data()]
    #2. use kivy properties
    # -> remove self from function so it's no longer an instance function
    # -> remove self. in function call in list comprehension: there are no instances
    # -> move list comprehension to below the function for function to be recognised -> less OOP

    def get_rv_data() -> list:
        # see video link in description
        command = f'netsh wlan show profile'
        networks = subprocess.check_output(command, shell=True)
        network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks.decode())

        result = []
        for network_name in network_names_list:
            command = f'netsh wlan show profile {network_name} key=clear'
            current_result = subprocess.check_output(command, shell=True).decode()
            password = re.search("(?:\s*Key Content\s*:\s)(.*)", current_result).group(1)
            # print(f'network:{network_name[:-1]} - password:{password}') #remove \r
            result.append(f'network:{network_name[:-1]} - password:{password}')
        return result

    rv_data_list = [{'text': res} for res in get_rv_data()]

class MyApp(App):
    def build(self):
        self.title = 'Recover Network Passwords'
        return Builder.load_file('gui.kv')


if __name__ == '__main__':
    MyApp().run()


