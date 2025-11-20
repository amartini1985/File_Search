import os
import re
import tkinter

from docx import Document
from tkinter import ttk

from constants import DRIVES
from utils import (
    clean_listbox,
    create_list_dir,
    insert_listbox,
    show_dir,
    walk_to_dir
    )


def click_back() -> None:
    current_dir = lable.cget('text')
    clean_listbox(dirs_listbox)
    if current_dir not in DRIVES:
        current_dir_list = current_dir.split('\\')
        if len(current_dir_list) == 1:
            current_dir = drives_combobox.get()
        else:
            current_dir = '\\'.join(current_dir_list[:-1])
    lable.config(text=current_dir)
    insert_listbox(listbox=dirs_listbox, list_dir=create_list_dir(lable=lable))


def selected(event) -> None:
    lable.config(text=dirs_listbox.get(
        dirs_listbox.curselection())
    )
    show_dir(dirs_listbox, lable)


def selected_combobox(event) -> None:
    lable.config(text=drives_combobox.get())
    show_dir(dirs_listbox, lable)


def check_type_files() -> set:
    files_type = set()
    enabled_files_type = {
        'txt': enabled_txt.get(),
        'docx': enabled_docx.get()
    }
    for key, value in enabled_files_type.items():
        if value == 1:
            files_type.add(key)
        else:
            files_type.discard(key)
    return files_type


def get_result() -> None:
    result_files = []
    files_type = check_type_files()
    files = walk_to_dir(current_dir=lable.cget('text'), files=list())
    find_word = find_word_entry.get()
    for file in files:
        try:
            file_type = file.split('.')[1]
            if file_type == 'txt' and file_type in files_type:
                with open(file, 'r') as file_open:
                    content = file_open.read()
                    if re.search(find_word, content):
                        result_files.append(file)
            elif file_type == 'docx' and file_type in files_type:
                document = Document(file)
                for paragraph in document.paragraphs:
                    if re.search(find_word, paragraph.text):
                        result_files.append(file)
                        break
        except Exception:
            continue
    clean_listbox(result_listbox)
    insert_listbox(result_listbox, result_files)


def selected_result(event) -> None:
    os.startfile(result_listbox.get(result_listbox.curselection()))


if __name__ == '__main__':
    # создание окна
    root = tkinter.Tk()
    root.title('File_Search')
    root.geometry('400x300')

    focus_disk = tkinter.StringVar(value=DRIVES[0])
    enabled_txt, enabled_docx = tkinter.IntVar(), tkinter.IntVar()

    ttk_button_up = ttk.Button(text='↑', width=3, command=click_back)
    lable = ttk.Label(text=DRIVES[0])

    list_dir = create_list_dir(lable=lable)
    list_dir_var = tkinter.Variable(value=list_dir)

    find_word_entry = ttk.Entry()
    dirs_listbox = tkinter.Listbox(listvariable=list_dir_var, width='200')
    result_listbox = tkinter.Listbox(listvariable=[], width='200')
    drives_combobox = ttk.Combobox(values=DRIVES, textvariable=focus_disk)
    txt_checkbutton = ttk.Checkbutton(
        text='.txt',
        variable=enabled_txt,
        command=check_type_files
    )
    docx_checkbutton = ttk.Checkbutton(
        text='.docx',
        variable=enabled_docx,
        command=check_type_files
    )
    dirs_listbox.bind('<<ListboxSelect>>', selected)
    result_listbox.bind('<<ListboxSelect>>', selected_result)
    drives_combobox.bind('<<ComboboxSelected>>', selected_combobox)
    button_result = ttk.Button(text='Result', command=get_result)

    # устанавливаем виджиты в окне
    lable.pack()
    ttk_button_up.pack()
    drives_combobox.pack()
    find_word_entry.pack()
    dirs_listbox.pack()
    txt_checkbutton.pack()
    docx_checkbutton.pack()
    result_listbox.pack()
    button_result.pack()

    # выставляем иконку от сглаза!!!!
    icon = tkinter.PhotoImage(file='smile.ico')
    root.iconphoto(False, icon)

    root.mainloop()
