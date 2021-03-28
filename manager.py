import configparser
import os
import shutil
import logging

# import kivy
# kivy.require('2.0.0')
# from kivy.app import App
# from kivy.uix.label import Label

config = configparser.ConfigParser(allow_no_value=True)
logging.basicConfig(level=logging.DEBUG)

mod_list = []

def read_config(config):
    # confirm config file exists
    if os.path.exists('manager.ini'):
        config.read('manager.ini')
    else:
        #  it didn't exist, so making basic config
        make_basic_config(config)
    # todo: check if config contains everything

def save_config(config, file):
    with open(file, 'w') as configfile:
        config.write(configfile)

def make_basic_config(config):
    mod_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods')
    config['directories'] = {
        'mods': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods'),
        'angband': None
    }
    save_config(config, 'manager.ini')

# may want to store this in a variable and watch for changes in the mod directory at some point, if it starts taking time to scan directory
def list_mods():
    mods = [os.path.basename(os.path.normpath(f.path)) for f in os.scandir(config['directories']['mods']) if f.is_dir()]
    # is this sorted?
    # at some point going to want to verify these all have manifests or not
    # print(mods)
    return mods

def get_angband_folder():
    # todo: prompt player to select Angband folder, instead of just hardcoding it for me
    return r"G:\angband-4.2.1"

def startup():
    # confirm config file exists
    read_config(config)
    # confirm mod folder exists
    if not os.path.exists(config['directories']['mods']):
        os.mkdir(config['directories']['mods'])

    # todo: get angband folder here
    # for now just setting it for testing purposes
    if config['directories']['angband'] is None:
        config['directories']['angband'] = get_angband_folder()
        # save_config(config)

    # todo: prompt user if they want to save out current gamedata folder as vanilla
    if not 'vanilla' in list_mods(config):
        make_mod('vanilla', os.path.join(config['directories']['angband'], 'lib', 'gamedata'))

# takes a name and a location, copies contents as mod
# probably want a better name for this; 'make_mod_from_preexisting'
def make_mod(id, location):
    if name not in list_mods(config):
        if os.path.exists(location):
            os.mkdir(os.path.join(config['directories']['mods'], id))
            os.mkdir(os.path.join(config['directories']['mods'], id, 'gamedata'))
            for file in os.scandir(location):
                shutil.copy(file, os.path.join(config['directories']['mods'], id, 'gamedata'))
        else:
            logging.error("%s does not exist", location)
    else:
        logging.warning("mod '%s' already exists", id)

# checks if mod in manager folder is set up correctly, doesn't have detectable errors
def validate_mod(id):
    is_valid = True
    # check if directory for mod exists
    if not os.path.exists(os.path.join(config['directories']['mods'], id)):
        is_valid = False
        logging.warning("mod '%s' does not exist", id)
    # check if has gamedata folder
    if not os.path.exists(os.path.join(config['directories']['mods'], id, 'gamedata')):
        is_valid = False
        logging.warning("mod '%s' has no gamedata folder", id)
    # check if has any files in gamedata
    # check if has manifest.xml
    # check if manifest.xml is properly formatted
    return is_valid

# class MyApp(App):
#     def build(self):
#         return Label(text='Hello world')

if __name__ == '__main__':
    # MyApp().run()
    startup(config)
