import tkinter as tk
from tkinter import ttk

my_dict = {}

root = tk.Tk()

str_var = tk.StringVar()

entry = ttk.Entry(state='readonly', textvariable=str_var)
my_dict['entry'] = entry

entry.pack()
for n in my_dict.values():
    print(n)

str_var.set('опа')

root.mainloop()