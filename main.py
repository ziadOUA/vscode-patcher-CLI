# -*- coding: utf-8 -*-
import json
import os
import time
import random

import requests
import io
import zipfile
import shutil

from defaults.defaultFunctions import new_line

from datetime import date

from pyfiglet import Figlet
from colorama import Fore, Back, init

init(convert=True)

start = Figlet(font='univers', width=120)

done = False
valid = False

today = date.today()
today = today.strftime('%d/%m/%Y')

vscode_css_path = ''
vscode_css = ''
user_css_path = ''

config_file = ''
config_data = ''


def vscode_patcher():
    config_loader()
    vscode_css_retriever()


def config_loader():
    global config_file
    try:
        file_status_msg('Opening', 'config.json')
        config_file = open('config.json')
        config_file.close()
        success_msg()
    except FileNotFoundError:
        failure_msg()
        print("Couldn't load the configuration file (config.json)")


def vscode_css_retriever():
    global valid, vscode_css, config_data
    global config_file, vscode_css_path
    config_file = open('config.json', 'r')
    config_data = json.load(config_file)
    config_file.close()
    if config_data['vscode_css_path'] is None:
        try:
            file_status_msg('Searching', 'workbench.desktop.main.css')
            vscode_css_path = os.path.expanduser('~') + "\AppData\Local\Programs\Microsoft VS Code\\resources\\app\out\\vs\workbench\workbench.desktop.main.css"
            vscode_css = open(vscode_css_path)
            vscode_css.close()
            success_msg()
            config_data['vscode_css_path'] = vscode_css_path
            config_file = open('config.json', 'w')
            json.dump(config_data, config_file, indent=4)
            config_file.close()
        except FileNotFoundError:
            failure_msg()
            print(f"{Fore.RED}Couldn't automatically fetch the VSCode CSS file{Fore.RESET}")
            new_line()
            vscode_css_new_path()
    else:
        vscode_css_path = config_data['vscode_css_path']
        while not valid:
            vscode_css_open()
            valid = True
        valid = False


def vscode_css_open():
    global vscode_css, vscode_css_path
    file_status_msg('Opening', 'workbench.desktop.main.css')
    try:
        vscode_css = open(vscode_css_path)
        vscode_css.close()
        success_msg()
    except FileNotFoundError:
        failure_msg()
        vscode_css_new_path()


def vscode_css_new_path():
    global valid, vscode_css, vscode_css_path
    while not valid:
        try:
            vscode_css_path = str(input("Input the path to the VSCode CSS file (workbench.desktop.main.css) >>> "))
            new_line()
            file_status_msg('Searching', 'workbench.desktop.main.css')
            vscode_css = open(vscode_css_path)
            vscode_css.close()
            success_msg()
            vscode_css_path_update_config()
            valid = True
        except FileNotFoundError:
            print(f' {Fore.RED}File not found{Fore.RESET}')
    valid = False


def vscode_css_path_update_config():
    global config_file, config_data
    file_status_msg('Updating', 'config.json')
    config_data['vscode_css_path'] = vscode_css_path
    config_file = open('config.json', 'w')
    json.dump(config_data, config_file, indent=4)
    config_file.close()
    success_msg()


# TERMINAL STATUS MESSAGES


def success_msg():
    print(f'{Fore.GREEN} Success{Fore.RESET}')


def failure_msg():
    print(f'{Fore.RED} Failed{Fore.RESET}')


def file_status_msg(action, file_name):
    print(f'{action} {file_name}...', end='')


# ---


if __name__ == '__main__':
    while not done:
        os.system('cls')
        valid = False
        done = False
        print(start.renderText('VSPatcher'))
        # try:
        #     # LOAD PATCHES LIST
        #     print('OK')
        # except zipfile.BadZipfile:
        #     # ERROR
        #     print('NOT OK')
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

new_line()
print('VSPatcher Copyright (C) 2023 ziadOUA')
time.sleep(3)
