import configparser
import os

# import kivy
# kivy.require('2.0.0')
# from kivy.app import App
# from kivy.uix.label import Label

config = configparser.ConfigParser(allow_no_value=True)
mod_list = []

def read_config(config):
    # confirm config file exists
    if os.path.exists('manager.ini'):
        config.read('manager.ini')
    else:
        make_config(config)

def save_config(config):
    with open('manager.ini', 'w') as configfile:
        config.write(configfile)

def make_config(config):
    mod_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods')
    config['directories'] = {
        'mods': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods'),
        'angband': None
    }
    save_config(config)

def list_mods(config):
    mods = [x[0] for x in os.walk(config['directories']['mods'])]
    # is this sorted?
    # at some point going to want to verify these all have manifests or not
    return mods

def startup(config):
    # confirm config file exists
    read_config(config)
    # confirm mod folder exists
    if not os.path.exists(config['directories']['mods']):
        os.mkdir(config['directories']['mods'])

# class MyApp(App):
#     def build(self):
#         return Label(text='Hello world')

if __name__ == '__main__':
    # MyApp().run()
