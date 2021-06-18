import sqlite3
import tkinter as tk
import tkinter.ttk as ttk

def update():
    with sqlite3.connect('Main_base.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        data = (row for row in cursor.fetchall())
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.after(1000, update)

class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

def update(self):
    global root, table, conn1, cur1, data
    conn1 = sqlite3.connect('Main_base.db')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM users")
    data = (row for row in cur1.fetchall())
    conn1.commit()
    table = Table(root, headings=('Userid', 'Username', 'Status', 'Date'), rows=data)
    # table.pack(expand=tk.YES, fill=tk.BOTH)
    self.Treeview.insert(parent='', index = tk.END, values=tuple(data))
    print("check")
    root.after(1000, update)




# data = ( , )
conn1 = sqlite3.connect('Main_base.db')
cur1 = conn1.cursor()
cur1.execute("SELECT * FROM users")
data = (row for row in cur1.fetchall())
conn1.commit()
root = tk.Tk()
table = Table(root, headings=('Userid', 'Username', 'Status', 'Date'), rows=data)
table.pack(expand=tk.YES, fill=tk.BOTH)
root.after(1000, update)
root.mainloop()
