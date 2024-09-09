# view/evtx_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET
import Evtx.Evtx as evtx

def clean_tag(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag

def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    headers = set()
    data = {}

    for child in root:
        clean_child_tag = clean_tag(child.tag)
        if clean_child_tag not in data:
            data[clean_child_tag] = child.text
        for sub_child in child:
            clean_sub_child_tag = clean_tag(sub_child.tag)
            headers.add(clean_sub_child_tag)
            data[clean_sub_child_tag] = sub_child.text

    return headers, data

def get_evtx_data(file_path):
    data = []
    headers = set()
    with evtx.Evtx(file_path) as log:
        for record in log.records():
            record_headers, record_data = parse_xml(record.xml())
            headers.update(record_headers)
            data.append(record_data)
    return headers, data

def display_evtx_data(file_path):
    headers, data = get_evtx_data(file_path)

    root = tk.Tk()
    root.title("EVTX Viewer")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(headers), show="headings")
    tree.grid(row=0, column=0, sticky='nsew')

    x_scroll = tk.Scrollbar(frame, orient='horizontal', command=tree.xview)
    x_scroll.grid(row=1, column=0, sticky='ew')
    tree.configure(xscrollcommand=x_scroll.set)

    y_scroll = tk.Scrollbar(frame, orient='vertical', command=tree.yview)
    y_scroll.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=y_scroll.set)

    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=150)

    for record in data:
        values = [record.get(header, '') for header in headers]
        tree.insert("", tk.END, values=values)

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Exit", command=root.quit)

    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Undo", command=undo_action)
    edit_menu.add_command(label="Redo", command=redo_action)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    root.mainloop()

def open_file():
    messagebox.showinfo("File", "Open file functionality")

def undo_action():
    messagebox.showinfo("Edit", "Undo action")

def redo_action():
    messagebox.showinfo("Edit", "Redo action")

def show_about():
    messagebox.showinfo("Help", "EVTX Viewer v1.0\nCreated by YourName")

