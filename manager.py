import configparser
import os
import shutil

from lxml import etree

import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.logger import Logger, LOG_LEVELS
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

config = configparser.ConfigParser(allow_no_value=True)
Logger.setLevel(LOG_LEVELS["debug"])

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
    # if not 'angband' in list_mods():
        # make_mod(os.path.join(config['directories']['angband'], 'lib', 'gamedata'), 'angband', 'Angband 4.2.1', 'Angband', '4.2.1', target_versions=['4.2.1'])

    # run the UI
    ManagerApp().run()

# takes a name and a location, copies contents as mod
# probably want a better name for this; 'make_mod_from_preexisting'
# also, check that the location isn't IN the mods folder in the first place; if it's correctly placed, no copying of files is necessary
def make_mod(location, identifier, name, author, version, target_versions=None):
    if name not in list_mods():
        if os.path.exists(location):
            os.mkdir(os.path.join(config['directories']['mods'], identifier))
            os.mkdir(os.path.join(config['directories']['mods'], identifier, 'gamedata'))
            for file in os.scandir(location):
                shutil.copy(file, os.path.join(config['directories']['mods'], identifier, 'gamedata'))
            make_manifest(os.path.join(config['directories']['mods'], identifier), identifier, name, author, version, target_versions=target_versions)
        else:
            Logger.error("%s does not exist", location)
    else:
        Logger.warning("mod '%s' already exists", identifier)

# all of these are text except target_versions, which is a list of text
def make_manifest(location, identifier, name, author, version, target_versions=[], compatible_with=[],
                    incompatible_with=[], load_before=[], load_after=[]):
    # create manifest XML here
    if os.path.exists(os.path.join(config['directories']['mods'], identifier)):
        root = etree.Element("manifest")
        identifier_node = etree.SubElement(root, "identifier")
        identifier_node.text = identifier
        name_node = etree.SubElement(root, "name")
        name_node.text = name
        author_node = etree.SubElement(root, "author")
        author_node.text = author
        version_node = etree.SubElement(root, "version")
        version_node.text = version
        target_versions_node = etree.SubElement(root, "target_versions")
        for target_version in target_versions:
            c = etree.SubElement(target_versions_node, "target_version")
            c.text = target_version
        compatible_with_node = etree.SubElement(root, "compatible_with")
        for mod in compatible_with:
            c = etree.SubElement(compatible_with_node, "identifier")
            c.text = mod
        incompatible_with_node = etree.SubElement(root, "incompatible_with")
        for mod in incompatible_with:
            c = etree.SubElement(incompatible_with_node, "identifier")
            c.text = mod
        load_before_node = etree.SubElement(root, "load_before")
        for mod in load_before:
            c = etree.SubElement(load_before_node, "identifier")
            c.text = mod
        load_after_node = etree.SubElement(root, "load_after")
        for mod in load_after:
            c = etree.SubElement(load_after_node, "identifier")
            c.text = mod

        et = etree.ElementTree(root)
        et.write(os.path.join(location, 'manifest.xml'), pretty_print=True)
    # else: error

# checks if mod in manager folder is set up correctly, doesn't have detectable errors
def validate_mod(identifier):
    is_valid = True
    # check if directory for mod exists
    if not os.path.exists(os.path.join(config['directories']['mods'], identifier)):
        is_valid = False
        Logger.warning("mod '%s' does not exist", identifier)
    # check if has gamedata folder
    if not os.path.exists(os.path.join(config['directories']['mods'], identifier, 'gamedata')):
        is_valid = False
        Logger.warning("mod '%s' has no gamedata folder", identifier)
    # check if has any files in gamedata; needs at least one?
    # check if has manifest.xml
    # check if manifest.xml is properly formatted
    return is_valid

# Kivy stuff

class ManagerWindow(AnchorLayout):
    pass

class ModlistScreen(Screen):
    pass

class PreferenceScreen(Screen):
    pass

class ManagerApp(App):
    def build(self):
        manager_window = ManagerWindow()
        sm = ScreenManager()
        sm.add_widget(PreferenceScreen(name='preferences'))
        sm.add_widget(ModlistScreen(name='mod_list'))
        manager_window.add_widget(sm)
        return ManagerWindow()
    # def build(self):
    #     # Create the screen manager
    #     sm = ScreenManager()
    #     sm.add_widget(ModlistScreen(name='mod_list'))
    #     sm.add_widget(PreferenceScreen(name='preferences'))
    #
    #     return sm

if __name__ == '__main__':
    startup()
