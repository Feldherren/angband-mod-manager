import configparser
import os

config = configparser.ConfigParser(allow_no_value=True)

def read_config(config):
    # confirm config file exists
    if os.path.exists('manager.ini'):
        config.read('manager.ini')
    else:
        make_config(config)
        # config_object.read('manager.ini')

def make_config(config):
    mod_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods')
    config['directories'] = {
        'mod_folder': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods'),
        'angband_folder': None
        'mods': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods'),
        'angband': None
    }
    with open('manager.ini', 'w') as configfile:
        config.write(configfile)

def startup():
    this_path = os.path.dirname(os.path.realpath(__file__))
def startup(config):
    # confirm config file exists
    # if not os.path.exists(os.path.join(this_path, 'mods'))
    read_config(config)
    # confirm mod folder exists

read_config(config)

print(config.sections())
    if not os.path.exists(config['directories']['mods']):
        os.mkdir(config['directories']['mods'])
