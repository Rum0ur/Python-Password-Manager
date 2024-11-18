import tkinter
import sqlite3

import random
import threading


## CSS

colour1 = "#020f12"
colour2 = "#05d7ff"
colour3 = "#65e7ff"
colour4 = "BLACK"

def btn_enter(event):
    # button.config(highlightbackground=colour3)
    button.config(highlightbackground="red")
    button.config(background=colour2)
    button.config(fg="WHITE")


def btn_leave(event):
    button.config(highlightbackground=colour2)
    button.config(background=colour1)

## CSS - END


def generatePassword():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    s = [",", ".", "/", '@', "]", "[", "{", "}", "!", "#", "$", "%", "^",
         "&", "*", "(", ")", "_", "-", "+"]
    d = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d",
         "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]

    pw = ""
    for i in range(5):
        broj = random.choices(a)[0]
        char = random.choices(s)[0]
        bukva = random.choices(d)[0]
        pw += f"{broj}{char}{bukva}"

    password.delete(0, tkinter.END)
    password.insert(tkinter.END, pw)

def emptyLabel():
    label.config(text="")
def addPassword():
    web = website.get()
    user = email.get()
    pw = password.get()

    conn = sqlite3.connect("my_db_password.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS pass_manager (id INTEGER primary key autoincrement, website TEXT, username TEXT, password TEXT)")
    cursor.execute(f"INSERT INTO pass_manager (website,username,password) VALUES (?,?,?)", [web, user, pw])

    lista = cursor.execute("SELECT * FROM pass_manager")
    for i in lista:
        print(i)

    ## TRUNCATE TABLE
    cursor.execute(f"DELETE FROM pass_manager;")
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='pass_manager';")
    ## TRUNCATE TABLE END

    conn.commit()
    conn.close()

    website.delete(0, tkinter.END)
    email.delete(0, tkinter.END)
    password.delete(0, tkinter.END)
    label.config(text="Success!")

    ## after 3 seconds empty the success text from label
    timer = threading.Timer(3.0, emptyLabel)
    timer.start()


screen = tkinter.Tk()
screen.title('Password Manager')
screen.iconbitmap("image.ico")
screen.geometry("475x475")
screen.wm_minsize(width=475, height=475)


frame = tkinter.Frame(screen, bg=colour1)
frame.pack(fill=tkinter.BOTH, expand=True)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)


frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(7, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(4, weight=1)


canvas = tkinter.Canvas(frame, bg=colour1, border=0)
img = tkinter.PhotoImage(file="image.png")
canvas.config(width=200, height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(row=1, column=1, columnspan=3)

labelWebsite = tkinter.Label(frame, text="Website:", width=10, anchor="w", bg=colour1, fg="WHITE")
labelWebsite.grid(row=2, column=1, pady=5)

website = tkinter.Entry(frame, font=("default", 12), width=30, bg=colour1, fg="WHITE")
website.grid(row=2, column=2, columnspan=2, pady=5, sticky="we")

labelEmail = tkinter.Label(frame, text="Username:", width=10, anchor="w", bg=colour1, fg="WHITE")
labelEmail.grid(row=3, column=1, pady=5)

email = tkinter.Entry(frame, font=("default", 12), width=30, bg=colour1, fg="WHITE")
email.grid(row=3, column=2, pady=5, columnspan=2, sticky="we")

labelPassword = tkinter.Label(frame, text="Password:", width=10, anchor="w", bg=colour1, fg="WHITE")
labelPassword.grid(row=4, column=1, pady=5)

password = tkinter.Entry(frame, font=("default", 12), width=20, bg=colour1, fg="WHITE")
password.grid(row=4, column=2, pady=5, sticky="we")

btnGeneratePassword = tkinter.Button(frame, font=("default", 7), text="Generate Password", command=generatePassword, width=10)
btnGeneratePassword.grid(row=4, column=3, padx=(10, 0), pady=5, ipadx=1, ipady=1, sticky="we")

# Create a frame to act as a border
border_frame = tkinter.Frame(
    frame,
    bg=colour2,  # Border color
    bd=1,         # Border width
    relief="groove"  # Type of border
)
border_frame.grid(row=5, column=2, pady=5, columnspan=2, sticky="we")

button = tkinter.Button(
    border_frame,
    background=colour1,
    foreground=colour2,
    activebackground=colour3,
    activeforeground=colour4,
    highlightthickness=2,
    highlightbackground=colour2,
    highlightcolor="WHITE",
    cursor="hand2",
    font=("default", 10, 'bold'),
    text="Add",
    command=addPassword,
    width=40,
    height=2,
    border=0,
    borderwidth=0,  # Set to 0 to avoid any default button border
    relief="flat"   # Flat relief for the button
)

button.pack(padx=2, pady=2)

label = tkinter.Label(frame, text="", width=40, bg=colour1, fg="WHITE")
label.grid(row=6, column=2, pady=5, columnspan=2, sticky="we")


button.bind('<Enter>', btn_enter)
button.bind('<Leave>', btn_leave)


screen.mainloop()
