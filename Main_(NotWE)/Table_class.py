import sys
import csv
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
from Filling_window import Enter_win

class Table(ctk.CTkFrame):
    def __init__(self,master,columns,headers,width,csv_file_I, name_lable = str,ac_creat=None):
        super().__init__(master)

        self.csv_file_I = csv_file_I

        self.ac_creat = ac_creat

        self.headers = headers
        self.columns = columns

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=0)    

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.scrollbar = ctk.CTkScrollbar(self,orientation="vertical",command=self.tree.yview)

        self.tree.configure(yscrollcommand=self.scrollbar)

        self.scrollbar.grid(column=1,row=1,sticky="w")

        self.text_name = ctk.CTkLabel(self,text=name_lable)
        self.text_name.grid(column=0,row=0, sticky="ew")

        self.frame_but = ctk.CTkFrame(self)
        self.frame_but.grid(column = 0,row=2)

        

        self.button_c = ctk.CTkButton(self.frame_but,text="Создать",)

        self.button_c.configure(command=lambda: ac_creat(self))

        self.button_c.grid(column=0,row=0)

        self.button_d = ctk.CTkButton(self.frame_but,text="Удалить",command=self.delete_row)
        self.button_d.grid(column=1,row=0)

        for colum,header,wih in zip(columns,headers,width):
            
            self.tree.heading(column=colum, text=header)
            self.tree.column(column=colum, width=wih)


        data = self.load_data_from_csv(csv_file_I)

        self.tree.grid(column=0,row=1,sticky="nsew")

        self.theme = ctk.get_appearance_mode()

    def load_data_from_csv(self,csv_file):
        # if not os.path.exists(csv_file):
        #     return
        #     # messagebox.showinfo(
        #     #             f"Не найден файл {csv_file}", "Заменить файл шаблоном?"
        #     #         )
        #     # answer = messagebox.askyesno(f"Не найден файл {csv_file}", "Заменить файл шаблоном?")
        #     # if answer:
        #     #     pass
        #     # else:
        #     #     pass

        data = []

        try:
            with open(csv_file, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f, delimiter=";")

                next(reader)  # Пропускаем заголовок

                for row in reader:
                    if row: 
                        print(row) # Проверка на пустые строки
                        data.append(row)

            for item in data:
                 self.tree.insert("", tk.END, values=item)
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Не удалось прочитать файл {csv_file}:\n{e}"
            )
        return data


        

    def TreeviewSelect(self,action):
        self.tree.bind("<Double-1>",action)

    # def create_test_file(self,csv_file):
    #     if csv_file == CSV_FILE_MEETTINGS:
    #         est_data = [
    #             ["id", "name", "email", "role"],
    #             ["1", "Алексей", "", "Админ"],  
    #             ]
    #     elif csv_file == CSV_FILE_MEMBERS:
    #         test_data = [
    #                     ["name_of_meet", "date", "time"],
    #                     ["Met", "02.04.26", "02.04.26"],  
    #                     ["et2", "02.04.26", "02.04.26"],
    #                     ["IRL", "02.04.26", "02.04.26"],
    #                 ]
    #     elif csv_file == CSV_FILE_GUESTS:
    #         test_data = [
    #                         ["id", "name", "email"],
    #                         ["1", "Артём Бируля", ""],  
    #                     ]
    #     with open(csv_file, mode="w", encoding="utf-8-sig", newline="") as f:
    #         writer = csv.writer(f, delimiter=";")
    #         writer.writerows(test_data)

    
    def change_theme(self):
        if self.theme == "Dark":
            style = ttk.Style()
            style.theme_use("clam")

            style.configure("Treeview",
                background="#2b2b2b",      
                foreground="#ffffff",      
                fieldbackground="#2b2b2b",
                rowheight=25,
                borderwidth=0)
            style.configure("Treeview.Heading",
                background="#1f1f1f",      
                foreground="#ffffff",
                relief="flat"
            )
            style.map("Treeview", 
                background=[('selected', "#246391")])
            style.map("Treeview.Heading", 
                background=[('active', "#2285d2")]     
            )
            style.map("Sc")
        else:
            style = ttk.Style()
            style.theme_use("clam")

            style.configure("Treeview",
                background="#2b2b2b",      
                foreground="#ffffff",      
                fieldbackground="#2b2b2b",
                rowheight=25,
                borderwidth=0)
            style.configure("Treeview.Heading",
                background="#1f1f1f",      
                foreground="#ffffff",
                relief="flat"
            )
            style.map("Treeview", 
                background=[('selected', "#246391")])
            style.map("Treeview.Heading", 
                background=[('active', "#2285d2")])

    def save_row(self, values,item):
        """Добавляет строку в таблицу И сразу сохраняет в файл."""
        self.tree.item(item=item,value=values)
        self.save_to_csv() 
        
    def save_to_csv(self):
        """Перезаписывает CSV-файл всеми данными из таблицы."""
        all_data = []
        print(f"Вся дата до:{all_data}")
        for item in self.tree.get_children():
            all_data.append(self.tree.item(item, "values"))
        print(f"Вся дата после:{all_data}")
        with open(self.csv_file_I, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.columns) # Записываем шапку
            writer.writerows(all_data)    # Записываем строки

    def delete_row(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Внимание!","Выделите строку для удаления!")
            return

        if messagebox.askyesno("Удаление",f"Удалить {len(selected)} строки?"):
            for item in  selected:
                self.tree.delete(item)
            self.save_to_csv()

    def create_row(self,values):

        # self.tree.insert("", "end", values=values)

        empty_values = [""] * len(self.columns)
        self.tree.insert("", "end", values=empty_values)
    
        self.save_to_csv()