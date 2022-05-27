import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from core.default_values import BACKGROUND_PATH


def upload_new():
    def back2main():
        window_upload_new.destroy()

    def select_file(filetype, entry_photo):
        def upload_archive():
            print(filetype)
            # Даня, пиши сюда

        if filetype == 1:
            filetypes = [
                ("all files", ".*"),
                ("text files", ".txt"),
                ("image files", ".png"),
                ("image files", ".jpeg"),
                ("image files", ".jpg"),
            ]
        if filetype == 2:

            filetypes = [("zips", ".zip")]

        filename = fd.askopenfilename(
            title="Open a file", initialdir="/", filetypes=filetypes
        )

        entry_photo.insert(0, filename)
        btn_upload = ttk.Button(
            window_upload_new, text="Загрузить файл", command=upload_archive
        )
        btn_upload.place(x=250, y=250)

        showinfo(title="Selected File", message=filename)

    def package():
        entry_photo = tk.Entry(window_upload_new, width=30)
        open_button = ttk.Button(
            window_upload_new,
            text="Открыть файл",
            command=lambda: select_file(2, entry_photo),
        )
        entry_photo.place(x=150, y=200)
        open_button.place(x=450, y=200)

    def oneandonly():
        entry_photo = tk.Entry(window_upload_new, width=30)
        open_button = ttk.Button(
            window_upload_new,
            text="Открыть файл",
            command=lambda: select_file(1, entry_photo),
        )
        entry_photo.place(x=150, y=200)
        open_button.place(x=450, y=200)

    window_upload_new = tk.Toplevel()
    window_upload_new.title("Добавление новых пользователей")
    window_upload_new.resizable(False, False)
    window_upload_new.geometry("800x300")
    img = tk.PhotoImage(file=BACKGROUND_PATH)
    limg = tk.Label(window_upload_new, image=img)
    limg.place(x=0, y=0)
    btn_back = tk.Button(window_upload_new, text="Назад", command=back2main)
    btn_package = tk.Button(
        window_upload_new, text="Пакетная загрузка", width=15, height=3, command=package
    )
    btn_one = tk.Button(
        window_upload_new, text="По одному", width=15, height=3, command=oneandonly
    )
    btn_package.place(x=400, y=120)
    btn_one.place(x=150, y=120)
    btn_back.place(x=0, y=0)
    window_upload_new.mainloop()
