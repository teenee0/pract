import os
import re
import make_ini
from pathlib import Path
from colorama import init
from termcolor import colored
from shutil import rmtree, copy2, move
init()

def check(child):
    global root
    child_path = Path(os.path.join(pwd, child))
    return child_path.is_relative_to(root) or child == root

def create_dir(dirname):
    path = os.path.join(pwd, dirname)
    if check(path):
        os.mkdir(path)
        print(colored(f"Directory {path} was created successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory", "white", "on_red"))

def remove_dir(dirname):
    path = os.path.join(pwd, dirname)
    if check(path):
        try:
            os.rmdir(path)
            print(colored(f"Directory {path} was removed successfully", "white", "on_green"))
        except OSError:
            print(colored(f"This directory isn't empty. Do you want to delete {path} with all files inside? [y/n]"))
            if str(input()).lower() == 'y':
                rmtree(path)
                print(colored(f"Directory {path} with all files inside was removed successfully", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory", "white", "on_red"))

def change_dir(dirname):
    global root
    if dirname == '/':
        dirname = root
    if dirname == '..':
        dirname = os.path.abspath(pwd)
    path = os.path.join(pwd, dirname)
    if check(path):
        os.chdir(path)
        print(colored(f"Now your pwd is {path}", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory", "white", "on_red"))

def create_file(fname):
    path = os.path.join(pwd, fname)
    if check(path):
        with open(path, "w"):
            pass
            print(colored(f"File {path} was created successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory", "white", "on_red"))

def write(fname, text):
    path = os.path.join(pwd, fname)
    if check(path) and os.path.isfile(path):
        with open(path, "w") as file:
            file.write(text)
            print(colored(f"File {path} was edited successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory or file doesn't exists", "white", "on_red"))

def get_content(fname):
    path = os.path.join(pwd, fname)
    if check(path) and os.path.isfile(path):
        with open(path, "r") as file:
            for line in [line.rstrip() for line in file]:
                print(line)
            print(colored(f"----------THE-END----------", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory or file doesn't exists", "white", "on_red"))

def remove_file(fname):
    path = os.path.join(pwd, fname)
    if check(path) and os.path.isfile(path):
        os.remove(path)
        print(colored(f"File {path} was removed successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory or file doesn't exists", "white", "on_red"))

def copy_file(old, new):
    old_path = os.path.join(pwd, old)
    new_path = os.path.join(pwd, new)
    if os.path.isfile(old_path) and check(old_path) and check(new_path):
        copy2(old_path, new_path)
        print(colored(f"File {old_path} was copied successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory or file doesn't exists", "white", "on_red"))

def move_file(fname, dst):
    path = os.path.join(pwd, fname)
    dst_path = os.path.join(pwd, dst)
    if os.path.isfile(path) and check(path) and check(dst_path):
        move(path, dst_path)
        print(colored(f"File {path} was moved to {dst_path} successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory or file doesn't exists", "white", "on_red"))

def rename_file(fname, new_name):
    path = os.path.join(pwd, fname)
    new_path = os.path.join(pwd, new_name)
    if os.path.isfile(path) and \
       not os.path.isfile(new_path) and \
       check(path) and \
       check(new_path):
        os.rename(path, new_path)
        print(colored(f"File {path} was renamed to {new_path} successfuly", "white", "on_green"))
    else:
        print(colored("Oooops. Looks like this directory isn't relative to your root directory or file doesn't exists", "white", "on_red"))


if not os.path.isfile("settings.ini"):
    root = str(input("Hi! You are first time here! Please, enter your root dir: "))
    root = re.sub(r'/', r'\\', root)
    make_ini.make_ini(root)
root = make_ini.get_root()
pwd = root
funcs = {"change_dir" : change_dir,
         "create_dir" : create_dir,
         "remove_dir" : remove_dir,
         "create_file" : create_file,
         "write" : write,
         "get_content" : get_content,
         "remove_file" : remove_file,
         "copy_file" : copy_file,
         "move_file" : move_file,
         "rename_file" : rename_file}

print("\n\
      Hi! This is simple python file manager. Have fun using it\
      \n\
      \n\
      Usage: command [args]\
      \n\
      \n\
      \n\
      Commands:\
      \n\
      1.create_dir   \targs: dirname\n\
      2.change_dir   \targs: dirname\n\
      3.remove_dir   \targs: dirname\n\
      4.create_file  \targs: filename\n\
      5.write        \targs: filename text ;tip: use quotes(') for your text\n\
      6.get_content  \targs: filename\n\
      7.remove_file  \targs: filename\n\
      8.copy_file    \targs: old_filename new_filename\n\
      9.move_file    \targs: old_path new_path\n\
      10.rename_file \targs: old_name new_name\n\
      11.exit\
      ")
while True:
    s = str(input('What would you like to do?\n')) 
    if s == 'exit':
        print(colored("Bye! See you later", "white", "on_cyan"))
        break
    try:
        if len(s.split()) == 2:
            func, arg = s.split()
            funcs[func](arg)
        elif len(s.split()) == 3:
            func, arg1, arg2 = s.split()
            funcs[func](arg1, arg2)
        else:
            func, arg2, _ = s.split("'")
            func, arg1 = func.split()
            funcs[func](arg1, arg2)
    except ValueError:
        print(colored("Oooops! Looks like there is a syntax error in your comand. Please, try again", "white", "on_red"))
    except KeyError:
        print(colored("Oooops! Looks like there is a syntax error in your comand. Please, try again", "white", "on_red"))