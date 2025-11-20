'''Функции для очистки и заполнения Listboxs'''
import os


def clean_listbox(listbox):
    size = listbox.size()
    listbox.delete(0, size)


def insert_listbox(listbox, list_dir):
    for dir in list_dir:
        listbox.insert(0, dir)


def walk_to_dir(current_dir, files):
    files_and_dirs = os.listdir(current_dir)
    for file_or_dir in files_and_dirs:
        path_dir = os.path.join(current_dir, file_or_dir)
        if os.path.isdir(path_dir):
            walk_to_dir(path_dir, files)
        elif os.path.isfile(path_dir):
            files.append(path_dir)
    return files


def create_list_dir(lable) -> list:
    current_dir = lable.cget('text')
    list_dir = []
    for dir in os.listdir(current_dir):
        path_dir = os.path.join(current_dir, dir)
        if os.path.isdir(path_dir):
            list_dir.append(path_dir)
    return sorted(list_dir, reverse=True)


def show_dir(listbox, lable) -> None:
    clean_listbox(listbox)
    insert_listbox(listbox, create_list_dir(lable))
