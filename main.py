import tkinter
from tkinter import messagebox
import random
import json

FONT = ("Verdana", 10, "normal")
DEFAULT_USERNAME = "someone@hotmail.com"


# ---------------------------- PASSWORD SEARCH ___------------------------------- #


def search_password():
    search_item = website_entry.get()
    if len(search_item) == 0:
        messagebox.showinfo(title=f"Empty search field", message=f"You have not provided what to search for.\n"
                                                                 f"Please fill in the Website field.")
    else:
        try:
            with open(file="./database", mode="r") as database:
                data = json.load(fp=database)
            found_entry = data[search_item]
        except FileNotFoundError:
            messagebox.showinfo(title=f"Database is empty", message=f"There are no entries in the database.\n"
                                                                    f"Please add something before trying to search.")
        except KeyError:
            messagebox.showinfo(title=f"{search_item} not found", message=f"{search_item} not found in database.\n"
                                                                          f"Check for typos please.")
        else:
            password_entry.insert(0, string=f"{found_entry['password']}")
            password_entry.clipboard_clear()
            password_entry.clipboard_append(string=password_entry.get())
            password_entry.delete(0, tkinter.END)
            messagebox.showinfo(title=f"Found data on {search_item}!",
                                message=f"Here's what we have on {search_item}:\n\n"
                                        f"Username: {found_entry['email']}\n"
                                        f"Password: {found_entry['password']}\n\n"
                                        f"(Note: Password has been copied to clipboard.)")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for char in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for char in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for char in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, tkinter.END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    database_entry = [website_entry.get(), username_entry.get(), password_entry.get()]
    new_data = {
        database_entry[0]: {
            "email": database_entry[1],
            "password": database_entry[2],
        }
    }
    if len(database_entry[0]) == 0 or len(database_entry[1]) == 0 or len(database_entry[2]) == 0:
        messagebox.showinfo(title="Don't leave fields blank!", message="Can't save entry with blank fields.\n"
                                                                       "Please fill in all the fields.")
        empty_fields_exist = True
        user_confirmed = False
    else:
        user_confirmed = messagebox.askokcancel(title=database_entry[0] + ": Confirm Entry",
                                                message=f"You are going to save these:\n\n"
                                                        f"Website: {database_entry[0]}\n"
                                                        f"Username: {database_entry[1]}\n"
                                                        f"Password: {database_entry[2]}\n\n"
                                                        f"OK to save?")
        empty_fields_exist = False
    if user_confirmed and not empty_fields_exist:
        try:
            with open(file="./database", mode="r") as database:
                data = json.load(fp=database)
        except FileNotFoundError:
            pass
        else:
            new_data.update(data)
        finally:
            with open(file="./database", mode="w") as database:
                json.dump(obj=new_data, fp=database, indent=4)  # This writes a JSON to the file
            website_entry.delete(0, tkinter.END)
            password_entry.clipboard_clear()
            password_entry.clipboard_append(string=password_entry.get())
            password_entry.delete(0, tkinter.END)
        messagebox.showinfo(title=database_entry[0] + ": Entry Saved",
                            message="The entry you have provided has been saved.\n"
                                    "The password has been copied to the clipboard.")
    elif not user_confirmed and not empty_fields_exist:
        messagebox.showinfo(title="Entry save canceled",
                            message="Make changes if necessary, then press Add to Database again.")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title(string="Password Manager")
window.config(padx=40, pady=40)

canvas = tkinter.Canvas(width=200, height=200)
lock_img = tkinter.PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = tkinter.Label()
website_label.config(text="Website:", font=FONT)
website_label.grid(column=0, row=1)

username_label = tkinter.Label()
username_label.config(text="Email/Username:", font=FONT)
username_label.grid(column=0, row=2)

password_label = tkinter.Label()
password_label.config(text="Password:", font=FONT)
password_label.grid(column=0, row=3)

website_entry = tkinter.Entry()
website_entry.config(width=25, font=FONT, justify="left", highlightthickness=0)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2, sticky="w")

username_entry = tkinter.Entry()
username_entry.config(width=42, font=FONT, justify="left", highlightthickness=0)
username_entry.insert(0, string=DEFAULT_USERNAME)
username_entry.grid(column=1, row=2, columnspan=2, sticky="w")

password_entry = tkinter.Entry()
password_entry.config(width=25, font=FONT, justify="left", highlightthickness=0)
password_entry.grid(column=1, row=3, sticky="w")

generate_button = tkinter.Button()
generate_button.config(width=16, height=1, font=FONT, text="Generate Password", highlightthickness=0,
                       command=generate_password)
generate_button.grid(column=2, row=3, sticky="e")

search_button = tkinter.Button()
search_button.config(width=16, height=1, font=FONT, text="Search", highlightthickness=0,
                     command=search_password)
search_button.grid(column=2, row=1, sticky="e")

add_button = tkinter.Button()
add_button.config(width=42, height=1, font=FONT, text="Add to Database", highlightthickness=0, command=save)
add_button.grid(column=1, row=4, sticky="e", columnspan=2)

window.mainloop()
