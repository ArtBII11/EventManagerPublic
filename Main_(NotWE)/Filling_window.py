import customtkinter as ctk
# from Filling_window import Enter_win
# from tkinter import messagebox

class Enter_win(ctk.CTkToplevel):
    #,clicked_id
    #,on_save=None
    #self.clicked_id=clicked_id
    #self.on_save = on_save
    def __init__(self,master,headers,data=None):
            
            super().__init__(master)
            self.title("Event manager (Filling)")
            self.geometry("500x350")
            self.resizable(False,False)

            self.transient(master)
            self.grab_set()

            self.result = None
            
            self.headers = headers
            self.data = data

            frame_entry = ctk.CTkFrame(self)
            self.grid_columnconfigure(0, weight=0)  
            self.grid_columnconfigure(1, weight=2) 
            self.grid_columnconfigure(2, weight=0)
            self.grid_rowconfigure(0, weight=2)
            self.grid_rowconfigure(1, weight=1)

            frame_entry.grid(column=1,row=0)

            self.entries = []

            for i,head in enumerate(headers):
                frame_entry.grid_columnconfigure(0, weight=1)  
                frame_entry.grid_columnconfigure(1, weight=1) 
                frame_entry.grid_columnconfigure(2, weight=1) 
                frame_entry.grid_rowconfigure(0,weight=1) # <------------------------------------------------------- Сделать по короче
                frame_entry.grid_rowconfigure(1,weight=1)
                frame_entry.grid_rowconfigure(2,weight=1)
                frame_entry.grid_rowconfigure(3,weight=1)
                frame_entry.grid_rowconfigure(4,weight=1)

                entry = ctk.CTkEntry(frame_entry,placeholder_text=head)
                lable = ctk.CTkLabel(frame_entry,text=head)
                if i >= 3:
                    
                    lable.grid(column = i-3, row = 2)
                    entry.grid(column = i-3,row = 3)

                else:
                    lable.grid(column = i, row = 0)
                    entry.grid(column = i ,row = 1)
                
                if data:
                    entry.insert(0,str(data[i]))

                self.entries.append(entry)

            self.button = ctk.CTkButton(self,text="Сохранить",command=self.save)
            self.button.grid(column=1,row=1)
            

    def save(self):
        values = []
        for i in self.entries:
            values.append(i.get())

        if not values[0].strip():
            return

        self.result = values
        
        # self.on_save(values,self.clicked_id)
        self.destroy()
        



