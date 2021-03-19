import configparser
import os

config = configparser.ConfigParser(allow_no_value=True)

def read_config(config):
    # confirm config file exists
    if os.path.exists('manager.ini'):
        config.read('manager.ini')
    else:
        make_config(config)

def make_config(config):
    mod_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods')
    config['directories'] = {
        'mods': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mods'),
        'angband': None
    }
    with open('manager.ini', 'w') as configfile:
        config.write(configfile)
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
