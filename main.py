import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.ttk import *
import requests
import requests
import tkinter as tk

from core.worker import begin_work
from core.adding_users import upload_new
from core.default_values import BACKGROUND_PATH


def detect_user():
    global root

    def back_to_main():

        root3.destroy()
        root.deiconify()

    def select_file2():
        filetypes = [
            ("all files", ".*"),
            ("text files", ".txt"),
            ("image files", ".png"),
            ("image files", ".jpeg"),
            ("image files", ".jpg"),
        ]

        filename = fd.askopenfilename(
            title="Open a file", initialdir="/", filetypes=filetypes
        )

        entry_photo_detect.insert(0, filename)

        showinfo(title="Selected File", message=filename)

    def detect():
        extention = entry_photo_detect.get().split(".")[-1]
        url = "http://51.250.8.218:8000"
        with open(entry_photo_detect.get(), "rb") as f:
            chunk = f.read(15 * 1024 * 1024)
            res = requests.post(
                f"{url}/detect_user",
                params={"extention": extention},
                files={"file_data": chunk},
            )
        t = tk.Text(root3, height=20, width=100)
        t.insert("insert", res.text)
        t.pack()
        # t=tk.Label(root3, text=res.text)
        # t.place(x=100,y=100)

    root3 = tk.Toplevel()
    root3.title("Проверить")
    root3.resizable(False, False)
    root3.geometry("800x300")
    img = tk.PhotoImage(file=BACKGROUND_PATH)
    limg = tk.Label(root3, image=img)
    limg.place(x=0, y=0)

    entry_photo_detect = tk.Entry(root3, width=30)
    open_button_detect = ttk.Button(
        root3,
        text="Открыть файл",
        command=select_file2,
    )
    detect_button = tk.Button(root3, text="Найти", command=detect)
    button_back = tk.Button(root3, text="Назад", command=back_to_main)
    entry_photo_detect.place(x=150, y=100)
    open_button_detect.place(x=450, y=100)
    detect_button.place(x=300, y=150)
    button_back.place(x=300, y=200)

    root3.mainloop()


def main():

    global root

    # create the root window
    root = tk.Tk()
    root.title("Титровалка")
    root.resizable(True, True)
    root.geometry("800x300")

    # background
    img = tk.PhotoImage(file=BACKGROUND_PATH)
    limg = tk.Label(root, image=img)
    limg.place(x=0, y=0)
    btn1 = tk.Button(
        text="Добавить новых пользователей", width=30, height=3, command=upload_new
    )
    btn2 = tk.Button(
        text="Начать распознование", width=30, height=3, command=begin_work
    )

    btn1.place(x=100, y=150)
    btn2.place(x=400, y=150)

    root.mainloop()


if __name__ == "__main__":
    main()
