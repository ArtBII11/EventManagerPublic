import sys
import csv
import os
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox

from tkinter import filedialog
import os
import docx
from Table_class import Table
from pathlib import Path
from Filling_window import Enter_win

# CSV_FILE_MEETTINGS = r"D:\EM\pythonEventManager\Data\мeetings.csv"
# CSV_FILE_MEETTINGS = Path(__file__).resolve().parent.parent / "Data" / "meetings.csv"
CSV_FILE_MEMBERS =Path(__file__).resolve().parent.parent/"Data"/"members.csv"
CSV_FILE_GUESTS = Path(__file__).resolve().parent.parent/"Data"/"guests.csv"
CSV_FILE_SPENDING =Path(__file__).resolve().parent.parent/"Data"/"spending.csv"


class Edit_window(ctk.CTkToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Event manager (Editing)")
        self.geometry("990x900")
   
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=1)   


        self.frame_g_m = ctk.CTkFrame(self)
        self.frame_g_m.grid(column=0,row=1,rowspan=2)
        self.frame_g_m.grid_rowconfigure(0, weight=1)  
        self.frame_g_m.grid_rowconfigure(1, weight=1)       
        self.frame_g_m.grid_columnconfigure(1, weight=1)
        self.frame_g_m.grid_columnconfigure(2, weight=0) 
        self.frame_g_m.grid_columnconfigure(0, weight=0)    

        self.tree_of_members = Table(self.frame_g_m,("name", "email","role"),("Имя","Email","Роль"),(140,160,80),CSV_FILE_MEMBERS,"Список участников")
        self.tree_of_guests = Table(self.frame_g_m,("name", "email"),("Имя","Email"),(180,200),CSV_FILE_GUESTS,"Список гостей")


        self.tree_of_guests.grid(column=1,row=0,padx=10,pady=5,ipadx=40,sticky="nsew")
        self.tree_of_members.grid(column=1,row=1,padx=10,pady=5,sticky="nsew")
        self.tree_of_guests.TreeviewSelect(self.fill_rows)
        self.tree_of_members.TreeviewSelect(self.fill_rows)

        self.frame_of_attach = ctk.CTkFrame(self)
        self.frame_of_attach.grid(column=0,row=3)

        self.btn_send = ctk.CTkButton(
            self, text="Разослать всем пользователям", command=self.send_emails,font=("Arial", 12, "bold"))

        self.btn_send.grid(column=2, row=4, pady=15, ipady=10)


        self.btn_attach_member = ctk.CTkButton(self.frame_of_attach,text="Прикрепить шаблон участника",command=lambda:self.attach_file_doc("member"),font=("Arial", 12, "bold"))
        self.btn_attach_member.grid(column=0, row=0, pady=15,padx=5, ipady=10)

        self.btn_attach_guest = ctk.CTkButton(self.frame_of_attach,text="Прикрепить шаблон гостя",command=lambda:self.attach_file_doc("guest"),font=("Arial", 12, "bold"))
        self.btn_attach_guest.grid(column=1, row=0, pady=15,padx=5, ipady=10)




        self.entry_name = ctk.CTkEntry(self,font=("Arial", 13),placeholder_text="Введите сюда название...")
        self.entry_name.grid(column=1,row=0,sticky="ew",ipady=10,ipadx=20,pady=20,padx=(0,15),columnspan=2)

        self.frame_DataTime = ctk.CTkFrame(self)
        self.frame_DataTime.grid(column=1,row=1,sticky="ns",pady=(60,60),padx=0,columnspan=2) # <<--- Фрейм соединяющий дату и время

        self.frame_DataTime.grid_rowconfigure(0,weight=0)
        self.frame_DataTime.grid_rowconfigure(1,weight=1) # <<--- Настройка фрейма соединяющий дату и время
        self.frame_DataTime.grid_rowconfigure(2,weight=0)

        self.entry_time = ctk.CTkEntry(self.frame_DataTime,placeholder_text="Время...")
        self.entry_time.grid(column=0,row=0,pady=5,ipady=5,sticky="nw",padx=10)

        self.entry_data = ctk.CTkEntry(self.frame_DataTime,placeholder_text="Дата...")
        self.entry_data.grid(column=0,row=2,pady=5,ipady=5,sticky="sw",padx=10)


        self.frame_budget_all = ctk.CTkFrame(self)
        self.frame_budget_all.grid(row=2, column=1,sticky="sewn",columnspan=2,padx=20)

        self.frame_budget_all.grid_columnconfigure(0,weight=1)
        self.frame_budget_all.grid_columnconfigure(1,weight=2)

        self.lable_budget = ctk.CTkLabel(self.frame_budget_all,text="Нет проблем с бюджетом",font=("Arial",12))
        self.lable_budget.grid(row=0,column=1)


        self.tree_of_spending =Table(self.frame_budget_all,("name", "sum", "cost","ry"),
                                     ("Название","Количество","Цена за один","Ответственный"),
                                     (120,50,100,130),
                                     CSV_FILE_SPENDING,
                                     "Список трат",
                                     self.fill_rows)
        
        self.tree_of_spending.grid(row=2,column=0,columnspan=2,sticky="ew")
        self.tree_of_spending.TreeviewSelect(lambda event: self.fill_rows(self.tree_of_spending,event))

        self.ProgressBar_budget= ctk.CTkProgressBar(self.frame_budget_all)
        self.ProgressBar_budget.grid(row=1,column=0,columnspan=3,sticky="ew",ipady=5,padx=2,pady=5)






        self.budget1_var= ctk.StringVar()
        self.budget1_var.trace_add("write",self.check_value)
        self.budget1_var.set(0)


        self.entry_limit = ctk.CTkEntry(self.frame_budget_all,textvariable=self.budget1_var,placeholder_text="Введите сумму бюджета")
        self.entry_limit.grid(column=0,row=0,padx=10,sticky="we",ipady=10)
        self.entry_limit.bind("<Return>",self.enter_function_input)

        

    def fill_rows(self,tree_data,event=None):
            if event == None:
                headers = tree_data.headers 
                row_values = None
                win = Enter_win(self,headers,row_values)
                self.wait_window(win)

                if win.result:
                    tree_data.create_row(win.result) # <--- СОХРАНЯЕМ!
                return


            else:  
            
                tree_w = event.widget
                selected = tree_w.selection()
                if selected:
                    clicked_id = selected[0]
                
                    columns = tree_w["columns"]

                    headers = []
                    for i in columns:
                        col = tree_w.heading(i,"text")
                        headers.append(col)
                    print(headers)

                    row_info = tree_w.item(clicked_id)
                    row_values = row_info["values"]

                    print(f"Полный состав: {row_values}")
                # ctk.CTkInputDialog(text="", title="")
                    win = Enter_win(self,headers,row_values)
                    self.wait_window(win)

                    if win.result:
                        tree_w.master.save_row(win.result,clicked_id)
                else:
                    return


    # def attach_file_doc(self,id_button): # <-- Функция находится в доработке

    def load_data_from_csv(self,csv_file):
        """Функция загрузки данных из CSV-файла."""
        if not os.path.exists(csv_file):
            self.create_test_csv(csv_file)

        data = []
        try:
            with open(csv_file, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f, delimiter=";")
                next(reader)  # Пропускаем заголовок

                for row in reader:
                    if row:  # Проверка на пустые строки
                        data.append(row)
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Не удалось прочитать файл {csv_file}:\n{e}"
            )
        return data


    # def create_test_csv(self,csv_file): #                  <-- Функция находится в доработке
    #     """Создает тестовый файл, если его не существует."""
    #     if csv_file == CSV_FILE_MEETTINGS:
    #         test_data = [
    #             ["id", "name", "email", "role"],
    #             ["1", "Алексей", "", "Админ"],  
    #         ]
    #     elif csv_file == CSV_FILE_MEMBERS:
    #         test_data = [
    #                 ["name_of_meet", "date", "time"],
    #                 ["Met", "02.04.26", "02.04.26"],  
    #                 ["et2", "02.04.26", "02.04.26"],
    #                 ["IRL", "02.04.26", "02.04.26"],
    #             ]
    #     elif csv_file == CSV_FILE_GUESTS:
    #         test_data = [
    #                     ["id", "name", "email"],
    #                     ["1", "Артём Бируля", ""],  
    #                 ]
    #     with open(csv_file, mode="w", encoding="utf-8-sig", newline="") as f:
    #         writer = csv.writer(f, delimiter=";")
    #         writer.writerows(test_data)

    def add_table(self,var): # <-- Функция находится в доработке
        pass

    def send_emails(self): # <-- Функция находится в доработке
        pass

    def enter_function_input(self,event): # <-- Функция находится в доработке
        pass

    def check_value(self,*args):
        try:


            
            limit = self.budget1_var.get().strip()
            limit = float(limit)

            all_data_spending = self.tree_of_spending.tree.get_children()

            spend = limit

            for i in range(0,len(self.tree_of_spending.tree.get_children())):
                fh = all_data_spending[i]
                name = self.tree_of_spending.tree.item(fh)["values"]
                quantity = name[1]
                price = name[2]
                spend -= (float(price)*float(quantity))
            
            print("Потрачено:", spend)
            print("Лимит:", limit)

            


            if limit == 0:
                self.lable_budget.configure(text="Введи бюджет больше нуля")
                self.ProgressBar_budget.configure(progress_color="#FCFDFB",fg_color="#8A8A8A")

            elif spend<0 :
                self.lable_budget.configure(text=f"Не хватает {round(abs(spend))} денег ")
                self.ProgressBar_budget.set(round(limit/(limit-spend),3))
                print(round(limit/(spend-limit),3))
                self.ProgressBar_budget.configure(progress_color="#42B32C",fg_color="#872222")
            elif spend>0:
                self.lable_budget.configure(text=f"В запасе на {round(spend)} денег ")
                self.ProgressBar_budget.set(round((limit-spend)/limit,3))
                print((spend-limit)/limit)
                self.ProgressBar_budget.configure(progress_color="#42B32C",fg_color="#2F821E")

            elif spend==0:
                        self.lable_budget.configure(text=f"Тютелька в тютельку!")
                        self.ProgressBar_budget.set(round(abs((limit-spend)/limit),3))
            
                
                
                
        except ValueError:
            if limit == "":
                self.lable_budget.configure(text="Вводите цифры, пожалуйста.")
            else:
                    self.lable_budget.configure(text="Вы вводите не цифры!")
            self.ProgressBar_budget.configure(progress_color="#FCFDFB",fg_color="#8A8A8A")
