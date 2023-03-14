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
patch_found = False
selected_command = None

today = date.today()
today = today.strftime('%d/%m/%Y')

commands_table = [['1. Patch VSCode with a custom CSS stylesheet (File)', '2. Remove custom CSS patch', '3. Patch VSCode with custom JS (File, NOT YET IMPLEMENTED)'],
                  ['4. Quick patches (NOT YET IMPLEMENTED)', '5. Patch product.json (NOT YET IMPLEMENTED)', '6. Reload CSS backup']]

vscode_css_path = ''
vscode_css = ''
vscode_css_backup_path_file = ''
user_css_path = ''
user_css_file = ''
user_css_content = ''

config_file = ''
config_data = ''


def vs_patcher():
    global selected_command
    config_loader()
    vscode_css_retriever()
    print(f'{Back.CYAN + Fore.BLACK} VSPatch is ready to patch {Back.RESET + Fore.RESET}')
    commands_prompt()
    if selected_command == '1':
        custom_css_patch()
    if selected_command == '2':
        remove_existing_patch()
    if selected_command in ['3', '4', '5']:
        print('Not yet Implemented')
    if selected_command == '6':
        reload_backup()


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
            vscode_css_path = os.path.expanduser(
                '~') + "\AppData\Local\Programs\Microsoft VS Code\\resources\\app\out\\vs\workbench\workbench.desktop.main.css"
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
        if selected_command in ['1', '2', '3', '4', '5', '6']:
            valid = True
    valid = False


def custom_css_patch():
    user_css_path_prompt()
    user_css_loading()
    vscode_css_backup()
    user_css_inject()


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
    global vscode_css_backup_path_file
    vscode_css_backup_path = f'{Path(vscode_css_path).parent}\\backup (Generated by VSPatcher)'
    vscode_css_backup_path_file = f'{Path(vscode_css_path).parent}\\backup (Generated by VSPatcher)\\{Path(vscode_css_path).name}'
    try:
        file_status_msg('Creating a backup of', Path(vscode_css_path).name)
        os.mkdir(vscode_css_backup_path)
        shutil.copyfile(vscode_css_path, vscode_css_backup_path_file)
        success_msg()
    except FileExistsError:
        print(f'{Fore.CYAN} Backup already exists{Fore.RESET}')


def reload_backup():
    global vscode_css_path, vscode_css_backup_path_file
    vscode_css_retriever()
    vscode_css_backup_path_file = f'{Path(vscode_css_path).parent}\\backup (Generated by VSPatcher)\\{Path(vscode_css_path).name}'
    try:
        file_status_msg('Removing', Path(vscode_css_path).name)
        os.remove(vscode_css_path)
        success_msg()
    except FileNotFoundError:
        failure_msg()
    try:
        file_status_msg('Reloading the backup of', Path(vscode_css_path).name)
        shutil.copyfile(vscode_css_backup_path_file, Path(vscode_css_path))
        success_msg()
    except FileExistsError:
        print(f'{Fore.CYAN} Backup already exists{Fore.RESET}')


def user_css_inject():
    global vscode_css
    vscode_css = open(vscode_css_path, 'r+')
    vscode_css_content = vscode_css.read()
    file_status_msg('Injecting the custom CSS into', Path(vscode_css_path).name)
    if '\n/* PATCH */\n' in vscode_css_content:
        print(f'{Fore.CYAN} Already patched{Fore.RESET}')
        replace_existing_patch_prompt()
    else:
        vscode_css.write('\n/* PATCH */\n')
        vscode_css.write(user_css_content)
        success_msg()
    vscode_css.close()


def replace_existing_patch_prompt():
    global valid
    new_line()
    while not valid:
        replace_patch = input('Replace existing patch ?\n Y: yes\n N: no\n>>> ')
        if replace_patch in ['y', 'Y']:
            remove_existing_patch_prompt()
            user_css_inject()
            valid = True
        elif replace_patch in ['n', 'N']:
            valid = True
    valid = False


def remove_existing_patch_prompt():
    global valid
    new_line()
    while not valid:
        remove_patch = input('Remove existing patch ?\n Y: yes\n N: no\n>>> ')
        if remove_patch in ['y', 'Y']:
            valid = True
            remove_existing_patch()
        elif remove_patch in ['n', 'N']:
            valid = True
    valid = False


def remove_existing_patch():
    global vscode_css, patch_found
    vscode_css = open(vscode_css_path, 'r')
    vscode_css_content = vscode_css.readlines()
    output = open(f'{Path(vscode_css_path).parent}\\temp.txt', 'w')
    print('Finding the patch...', end='')
    for line in vscode_css_content:
        if '/* PATCH */' in line:
            patch_found = True
            success_msg()
            break
        else:
            output.write(line)
    if not patch_found:
        failure_msg()
        print(f'{Fore.YELLOW}No patch was found{Fore.RESET}')
    vscode_css.close()
    output.close()
    if patch_found:
        file_status_msg('Removing', 'the patch')
        os.replace(f'{Path(vscode_css_path).parent}\\temp.txt', f'{Path(vscode_css_path).parent}\\{Path(vscode_css_path).name}')
        success_msg()
    try:
        os.remove(f'{Path(vscode_css_path).parent}\\temp.txt')
    except FileNotFoundError:
        pass
    patch_found = False


if __name__ == '__main__':
    while not done:
        os.system('cls')
        valid = False
        done = False
        print(start.renderText('VSPatcher'))
        new_line()
        vs_patcher()
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
