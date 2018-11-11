import tkinter as ttk
from tkinter import messagebox
import numpy as np
import pandas as pd
import pickle

class Attendance:
    def __init__(self):
        self.root = ttk.Tk()
        self.root.title("Attendance")
        self.last_action = ("", "", "a")
        self.names_list = []
        self.names_listbox = ttk.Listbox(self.root)
        self.email_list = []
        self.email_listbox = ttk.Listbox(self.root)
        self.name_entry = ttk.Entry(self.root)
        self.email_entry = ttk.Entry(self.root)
        self.name_entry.config(font=36)
        self.email_entry.config(font=36)
        self.meeting_type = ttk.StringVar()

        def edit_listbox():
            self.names_listbox.delete(0, ttk.END)
            for name in self.names_list:
                self.names_listbox.insert(ttk.END, name)
            self.email_listbox.delete(0, ttk.END)
            for name in self.email_list:
                self.email_listbox.insert(ttk.END, name)
            # make this into a loop don't be lazy

        def insert_name(name=None, email=None):
            if not name:
                email = self.email_entry.get()
                name = self.name_entry.get()
                if name != "":
                    self.last_action = (name, email, "i")
            if name != "":
                self.names_list.append(name)
                self.email_list.append(email)
                self.name_entry.delete(0, ttk.END)
                self.email_entry.delete(0, ttk.END)
                edit_listbox()

        def remove_name(name=None, email=None):
            if not name:
                nums = self.names_listbox.curselection()
                enums = self.email_listbox.curselection()
                names = []
                emails = []
                for x in nums:
                    names.append(self.names_list[x])
                    emails.append(self.email_list[x])
                for x in enums:
                    names.append(self.names_list[x])
                    emails.append(self.email_list[x])
                if len(nums)or len(enums):
                    self.last_action = (names, emails, "r")
                for num in nums:
                    self.names_list.pop(num)
                    self.email_list.pop(num)
                for num in enums:
                    self.names_list.pop(num)
                    self.email_list.pop(num)
            else:
                self.names_list.remove(name)
                self.email_list.remove(email)
            edit_listbox()

        def undo_action():
            if self.last_action[-1] == "r":
                for y in range(len(self.last_action[0])):
                    insert_name(self.last_action[0][y], self.last_action[1][y])
            elif self.last_action[-1] == "i":
                remove_name(self.last_action[0], self.last_action[1])

        self.add_button = ttk.Button(self.root, text="Add Entry", command=lambda: insert_name())
        self.remove_button = ttk.Button(self.root, text="Remove Entry", command=lambda: remove_name())
        self.undo_button = ttk.Button(self.root, text="Undo Last Action", command=lambda: undo_action())
        self.listbox_scrollbar = ttk.Scrollbar(self.root, orient=ttk.VERTICAL)
        self.listbox_scrollbar.config(command=self.names_listbox.yview)
        self.names_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.email_scrollbar = ttk.Scrollbar(self.root, orient=ttk.VERTICAL)
        self.email_scrollbar.config(command=self.email_listbox.yview)
        self.email_listbox.config(yscrollcommand=self.email_scrollbar.set)
        self.name_entry_label = ttk.Label(self.root, text="Type your name here:")
        self.email_entry_label = ttk.Label(self.root, text="Type your e-mail here. If I already have your e-mail, leave this section blank.")

        self.names_listbox.grid(row=0, column=0, rowspan=12, columnspan=2, sticky="NSEW")
        self.listbox_scrollbar.grid(row=0, column=2, rowspan=12, sticky="NSEW")
        self.email_listbox.grid(row=0, column=3, rowspan=12, columnspan=2, sticky="NSEW")
        self.email_scrollbar.grid(row=0, column=5, rowspan=12, sticky="NSEW")
        self.name_entry_label.grid(row=0, column=6, sticky="NSEW")
        self.name_entry.grid(row=0, column=7, sticky="NSEW")
        self.email_entry_label.grid(row=1, column=6, sticky="NSEW")
        self.email_entry.grid(row=1, column=7, sticky="NSEW")
        self.add_button.grid(row=2, column=6, columnspan=2, sticky="NSEW")
        self.remove_button.grid(row=3, column=6, columnspan=2, sticky="NSEW")
        self.undo_button.grid(row=4, column=6, columnspan=2, sticky="NSEW")

        self.year_label = ttk.Label(self.root, text="Year:")
        self.month_label = ttk.Label(self.root, text="Month:")
        self.day_label = ttk.Label(self.root, text="Day:")
        self.year_label.grid(row=5, column=6)
        self.month_label.grid(row=6, column=6)
        self.day_label.grid(row=7, column=6)

        self.year_spinbox = ttk.Spinbox(self.root, from_=2017, to=2018)
        self.month_spinbox = ttk.Spinbox(self.root, from_=1, to=12)
        self.day_spinbox = ttk.Spinbox(self.root, from_=1, to=31)
        self.year_spinbox.grid(row=5, column=7)
        self.month_spinbox.grid(row=6, column=7)
        self.day_spinbox.grid(row=7, column=7)

        ttk.Label(self.root, text="What meeting type?").grid(row=8, column=6)
        ttk.Radiobutton(self.root, text="Chemistry", variable=self.meeting_type, value="Chemistry").grid(row=8, column=7)
        ttk.Radiobutton(self.root, text="Physics", variable=self.meeting_type, value="Physics").grid(row=9, column=7)
        ttk.Radiobutton(self.root, text="Biology", variable=self.meeting_type, value="Biology").grid(row=10, column=7)
        ttk.Radiobutton(self.root, text="General", variable=self.meeting_type, value="General").grid(row=11, column=7)
        self.meeting_type.set("None")

        def ins_name(event):
            insert_name()

        def del_name(event):
            remove_name()

        def undo_name(event):
            undo_action()

        self.root.bind_all("<Return>", ins_name)
        self.names_listbox.bind("<BackSpace>", del_name)
        self.email_listbox.bind("<BackSpace>", del_name)
        self.root.bind_all("<Control-z>", undo_name)

        for x in range(8):
            self.root.rowconfigure(x, weight=1)
        for x in range(6):
            if x != 2:
                self.root.columnconfigure(x, weight=1)
        self.root.geometry("1000x500")

    def save_file(self):
        names_list_set = set(self.names_list)
        # names_series = pd.Series(self.names_list)
        date_name = (str(self.month_spinbox.get()) + "/" + str(self.day_spinbox.get() + "/" + str(self.year_spinbox.get())))

        meeting_type = self.meeting_type.get()
        if meeting_type == "Chemistry":
            files = ["I:\Attendance\chemistry.csv"]
        elif meeting_type == "Biology":
            files = ["I:\Attendance\\biology.csv"]
        elif meeting_type == "Physics":
            files = ["I:\Attendance\physics.csv"]
        else:
            files = ["I:\Attendance\chemistry.csv", "I:\Attendance\\biology.csv", "I:\Attendance\physics.csv"]

        for file in files:
            attendance_marks = []
            try:
                data = pd.read_csv(file, index_col=0)
                existing_names = list(data)

                for name in names_list_set:
                    if name not in existing_names:
                        data[name] = [0] * len(data)

                for name in list(data):
                    if name in names_list_set:
                        attendance_marks.append(1)
                    else:
                        attendance_marks.append(0)

                # date = pd.DataFrame(columns=names_list_set)

                try:
                    x = data.loc[date_name]
                    final_list = list(pd.Series(attendance_marks) + pd.Series(list(data.loc[date_name])))
                    for x in range(len(final_list)):
                        if final_list[x] > 1:
                            final_list[x] = 1
                    data.loc[date_name] = final_list
                except KeyError:
                    data.loc[date_name] = attendance_marks

            except pd.errors.EmptyDataError:
                data = pd.DataFrame(columns=names_list_set)
                data.loc[date_name] = [1] * len(names_list_set)

            data.to_csv(file)

    def save_email(self):
        try:
            data = pd.read_csv("I:\Attendance\emails.csv", index_col=0)
            new_names = []
            for x in range(len(self.names_list)):
                try:
                    y = data.loc[self.names_list[x]]
                    if x == "":
                        raise KeyError
                except KeyError:
                    new_names.append(x)
            for x in range(len(new_names)):
                data.loc[self.names_list[new_names[x]]] = [self.email_list[new_names[x]]]
        except pd.errors.EmptyDataError:
            data = pd.DataFrame(columns=["emails"])
            for x in range(len(self.names_list)):
                data.loc[self.names_list[x]] = [self.email_list[x]]
        data.to_csv("emails.csv")

    def on_close(self):
        if ttk.messagebox.askokcancel("Quit", "Save and Quit?"):
            self.save_file()
            self.save_email()
            att.root.destroy()

att = Attendance()
att.root.protocol("WM_DELETE_WINDOW", att.on_close)
att.root.mainloop()
