import tkinter as tk
from tkinter import messagebox
from db import Database

# Instanciate databse object
db = Database('students.db')

# Main Application/GUI class


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Student Manager')
        # Width height
        master.geometry("700x350")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # Part
        self.name_text = tk.StringVar()
        self.name_label = tk.Label(
            self.master, text='Student Name', font=('bold', 14), pady=20)
        self.name_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        self.name_entry = tk.Entry(self.master, textvariable=self.name_text)
        self.name_entry.grid(row=0, column=1)
        # Customer
        self.age_text = tk.StringVar()
        self.age_label = tk.Label(
            self.master, text='Student Age', font=('bold', 14))
        self.age_label.grid(row=0, column=2, sticky=tk.W)
        self.age_entry = tk.Entry(
            self.master, textvariable=self.age_text)
        self.age_entry.grid(row=0, column=3)
        # Retailer
        self.homeroom_teacher_text = tk.StringVar()
        self.homeroom_teacher_label = tk.Label(
            self.master, text='Homeroom Teacher', font=('bold', 14))
        self.homeroom_teacher_label.grid(row=1, column=0, sticky=tk.W, padx = 5)
        self.homeroom_teacher_entry = tk.Entry(
            self.master, textvariable=self.homeroom_teacher_text)
        self.homeroom_teacher_entry.grid(row=1, column=1)
        # Price
        self.avg_grade_text = tk.StringVar()
        self.avg_grade_label = tk.Label(
            self.master, text='Average Grade', font=('bold', 14))
        self.avg_grade_label.grid(row=1, column=2, sticky=tk.W)
        self.avg_grade_entry = tk.Entry(self.master, textvariable=self.avg_grade_text)
        self.avg_grade_entry.grid(row=1, column=3)

        # Parts list (listbox)
        self.names_list = tk.Listbox(self.master, height=8, width=100, border=1)
        self.names_list.grid(row=3, column=0, columnspan=4,
                             rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=4)
        # Set scrollbar to names
        self.names_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.names_list.yview)

        # Bind select
        self.names_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add Student", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Remove Student", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(
            self.master, text="Update Student", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.exit_btn = tk.Button(
            self.master, text="Clear Input", width=12, command=self.clear_text)
        self.exit_btn.grid(row=2, column=3)

    def populate_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.names_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.names_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.name_text.get() == '' or self.age_text.get() == '' or self.homeroom_teacher_text.get() == '' or self.avg_grade_text.get() == '':
            messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        # Insert into DB
        db.insert(self.name_text.get(), self.age_text.get(),
                  self.homeroom_teacher_text.get(), self.avg_grade_text.get())
        # Clear list
        self.names_list.delete(0, tk.END)
        # Insert into list
        self.names_list.insert(tk.END, (self.name_text.get(), self.age_text.get(
        ), self.homeroom_teacher_text.get(), self.avg_grade_text.get()))
        self.clear_text()
        self.populate_list()

    # Runs when item is selected
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.names_list.curselection()[0]
            # Get selected item
            self.selected_item = self.names_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, self.selected_item[1])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(tk.END, self.selected_item[2])
            self.homeroom_teacher_entry.delete(0, tk.END)
            self.homeroom_teacher_entry.insert(tk.END, self.selected_item[3])
            self.avg_grade_entry.delete(0, tk.END)
            self.avg_grade_entry.insert(tk.END, self.selected_item[4])
        except IndexError:
            pass

    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.name_text.get(
        ), self.age_text.get(), self.homeroom_teacher_text.get(), self.avg_grade_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.homeroom_teacher_entry.delete(0, tk.END)
        self.avg_grade_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
