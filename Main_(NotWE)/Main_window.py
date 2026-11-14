import sys
import csv
import os
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from Table_class import Table

from Edit_window import Edit_window
from pathlib import Path

from Edit_window import *

CSV_FILE_MEETTINGS = Path(__file__).resolve().parent.parent / "Data" / "meetings.csv"

root = ctk.CTk()
root.title("Event manager")
root.geometry("550x350")

root.grid_columnconfigure(0, weight=0)  
root.grid_columnconfigure(1, weight=2) 
root.grid_columnconfigure(2, weight=0) 
root.grid_rowconfigure(1,weight=1)

def clicked(*args):
    Edit_window(root)

tree_of_meetings = Table(root,("name_of_meet", "date", "time"),
                         ("Название мероприятия","Дата мероприятия","Время мероприятия"),
                         (120,110,120),
                         CSV_FILE_MEETTINGS,
                         "Список запланированных мероприятий",
                         clicked)



tree_of_meetings.grid(column=1,row=1,padx=10,pady=5,ipadx=40,sticky="news")

tree_of_meetings.change_theme()


def fill_rows(event):
        tree_w = event.widget
        selected = tree_w.selection()
        if selected:
            clicked_id = selected[0]
            print(tree_w)
            columns = tree_w["columns"]

            headers = []
            for i in columns:
                col = tree_w.heading(i,"text")
                headers.append(col)
            print(headers)

            row_info = tree_w.item(clicked_id)
            row_values = row_info["values"]

            win = Enter_win(root,headers,row_values)
            root.wait_window(win)

            if win.result:
                tree_w.master.save_row(win.result,clicked_id)
        else:
            return

tree_of_meetings.TreeviewSelect(fill_rows)



root.mainloop()