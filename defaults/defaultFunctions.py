from colorama import Fore


def new_line():
    print('')


def success_msg():
    print(f'{Fore.GREEN} Success{Fore.RESET}')


def failure_msg():
    print(f'{Fore.RED} Failed{Fore.RESET}')


def file_status_msg(action, file_name):
    print(f'{action} {file_name}...', end='')
