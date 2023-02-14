# -*- coding: utf-8 -*-
import json
import os
import time
import random

import requests
import io
import zipfile
import shutil

from defaults.defaultFunc import new_line

from datetime import date

from pyfiglet import Figlet
from colorama import Fore, Back, init

init(convert=True)

start = Figlet(font='univers')

done = False
valid = False

today = date.today()
today = today.strftime('%d/%m/%Y')

vscode_css_path = ''
user_css_path = ''

config_file = ''


def vscode_patcher():
    print('OK')
    home_directory = os.path.expanduser('~') + "\AppData\Local\Programs\Microsoft VS Code\\resources\\app\out\\vs\workbench"
    print(home_directory)
    config_loader()
    vscode_css_retriever()


def config_loader():
    global config_file
    try:
        config_file = open('config.json')
        config_file.close()
    except FileNotFoundError:
        print("Couldn't load the configuration file (config.json)")


def vscode_css_retriever():
    global config_file, vscode_css_path
    config_file = open('config.json', 'r')
    config_data = json.load(config_file)
    config_file.close()
    if config_data['vscode_css_path'] is None:
        try:
            vscode_css_path = os.path.expanduser('~') + "\AppData\Local\Programs\Microsoft VS Code\\resources\\app\out\\vs\workbench\workbench.desktop.main.css"
            vscode_css = open(vscode_css_path)
            print('OK')
            config_data['vscode_css_path'] = vscode_css_path
            config_file = open('config.json', 'w')
            json.dump(config_data, config_file, indent=4)
            config_file.close()
        except FileNotFoundError:
            print("Couldn't fetch automatically the VSCode CSS file")


if __name__ == '__main__':
    while not done:
        os.system('cls')
        valid = False
        done = False
        print(start.renderText('VSCode Patcher'))
        try:
            # LOAD PATCHES LIST
            print('OK')
        except zipfile.BadZipfile:
            # ERROR
            print('NOT OK')
        new_line()
        vscode_patcher()
        new_line()
        while not valid:
            is_user_done = input('Leave ?\n Y: yes\n N: no\n>>> ')
            if is_user_done in ['y', 'Y']:
                valid = True
                done = True
            elif is_user_done in ['n', 'N']:
                valid = True
                done = False
