import re
import subprocess

import kivy
from kivy.uix.recycleview import RecycleView
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

kivy.require('2.1.0')


class RVScreen(Screen):
    pass


class PWScreen(Screen):
    pass


class RVButton(Button):
    def on_release(self):
        sm = App.get_running_app().root.ids.sm
        sm.get_screen('pw_screen').ids.lbl_network.text = self.text
        sm.get_screen('pw_screen').ids.lbl_pw.text = self.text_pw
        sm.current = 'pw_screen'




class RV(RecycleView):
    # see video about passing variables link in description

    # what do we need for recycleview: list of dictionaries
    # [{'text': 'text for label 1 in RV'},{'text': 'text for label 2 in RV'},{'text': 'text for label 3 in RV'}]
    # number of dictionaries =  the number of items in your RV, which is not fixed
    # rv_data_list = ListProperty([])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rv_data_list = [{'text': res[0], 'text_pw': res[1]} for res in self.get_rv_data()]

    def get_rv_data(self) -> list:
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
            result.append([network_name[:-1], password[:-1]])
        return result


class MyApp(App):
    def build(self):
        self.title = 'Recover Network Passwords'
        return Builder.load_file('gui_rec.kv')


if __name__ == '__main__':
    MyApp().run()
