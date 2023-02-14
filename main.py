# -*- coding: utf-8 -*-
import json
import os
import time
import random

import requests
import io
import zipfile
import shutil

from defaults.defaultFunctions import new_line, file_status_msg, success_msg, failure_msg

from datetime import date
from tabulate import tabulate
from pyfiglet import Figlet
from colorama import Fore, Back, init
from pathlib import Path

init(convert=True)

start = Figlet(font='univers', width=120)

done = False
valid = False
selected_mode = None

today = date.today()
today = today.strftime('%d/%m/%Y')

commands_table = [['1. Patch VSCode with a custom CSS stylesheet (File)', '2. Patch VSCode with custom JS (File, NOT YET IMPLEMENTED)', '3. Quick patches (NOT YET IMPLEMENTED)'],
                  ['4. Reload CSS backup (NOT YET IMPLEMENTED)']]

vscode_css_path = ''
vscode_css = ''
user_css_path = ''
user_css_file = ''
user_css_content = ''

config_file = ''
config_data = ''


def vscode_patcher():
    global selected_command
    config_loader()
    vscode_css_retriever()
    print(f'{Back.CYAN + Fore.BLACK} VSPatch is now ready to patch {Back.RESET + Fore.RESET}')
    commands_prompt()
    if selected_command == '1':
        custom_css_patch()
    if selected_command == '2':
        print('Not yet Implemented')
    if selected_command == '3':
        print('Not yet Implemented')
    if selected_command == '4':
        print('Not yet Implemented')



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


def commands_prompt():
    global valid, selected_command
    new_line()
    print(tabulate(commands_table, tablefmt="presto"))
    while not valid:
        selected_command = str(input('>>> '))
        if selected_command == '1':
            valid = True
        if selected_command == '2':
            valid = True
        if selected_command == '3':
            valid = True
        if selected_command == '4':
            valid = True
    valid = False


def custom_css_patch():
    user_css_path_prompt()
    user_css_loading()
    vscode_css_backup()


def user_css_path_prompt():
    global user_css_path, user_css_file, valid
    while not valid:
        new_line()
        user_css_path = str(input('Put the path to your CSS patch file >>> '))
        try:
            file_status_msg('Searching', 'your CSS file')
            user_css_file = open(user_css_path)
            user_css_file.close()
            success_msg()
            valid = True
        except (FileNotFoundError, PermissionError):
            print(f' {Fore.RED}File not found{Fore.RESET}')
    valid = False
    new_line()


def user_css_path_update_config():
    global config_file, config_data
    file_status_msg('Updating', 'config.json')
    config_data['user_css_path'] = user_css_path
    config_file = open('config.json', 'w')
    json.dump(config_data, config_file, indent=4)
    config_file.close()
    success_msg()


def user_css_loading():
    global user_css_file, user_css_content
    user_css_path_update_config()
    user_css_file_name = Path(user_css_path).name
    file_status_msg('Opening', user_css_file_name)
    user_css_file = open(user_css_path)
    success_msg()
    file_status_msg('Loading the contents of', user_css_file_name)
    user_css_content = user_css_file.read()
    success_msg()


def vscode_css_backup():
    vscode_css_backup_path = f'{Path(vscode_css_path).parent}\\backup (Generated by VSPatch)'
    vscode_css_backup_path_file = f'{Path(vscode_css_path).parent}\\backup (Generated by VSPatch)\\{Path(vscode_css_path).name}'
    try:
        file_status_msg('Creating a backup of', Path(vscode_css_path).name)
        os.mkdir(vscode_css_backup_path)
        shutil.copyfile(vscode_css_path, vscode_css_backup_path_file)
        success_msg()
    except FileExistsError:
        print(f'{Fore.CYAN} Backup already exists{Fore.RESET}')


if __name__ == '__main__':
    while not done:
        os.system('cls')
        valid = False
        done = False
        print(start.renderText('VSPatcher'))
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
