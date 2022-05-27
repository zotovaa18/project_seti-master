import textwrap
import time
import requests
import threading
import tkinter as tk
from loguru import logger
from tkinter.messagebox import showinfo
from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters

import core.default_values as def_values


old_user_fio = None


def begin_work():
    global window_detecting

    window_detecting = tk.Toplevel()
    window_detecting.title("Титруемся")
    window_detecting.resizable(False, False)
    window_detecting.geometry("800x300")

    img = tk.PhotoImage(file=def_values.BACKGROUND_PATH)
    limg = tk.Label(window_detecting, image=img)
    limg.place(x=0, y=0)
    btn_back = tk.Button(window_detecting, text="Назад", command=back2main)
    btn_back.place(x=0, y=0)

    img_setup = tk.PhotoImage(file=def_values.SETUP_OBS_IMG_PATH)
    limg_setup = tk.Label(window_detecting, image=img_setup)
    limg_setup.place(x=200, y=130)

    setup_text = tk.Label(
        window_detecting,
        text="Включите, что надо включить, а что не надо не включайте",
    )
    setup_text.place(x=200, y=100)

    btn_next = tk.Button(window_detecting, text="Далее", command=process_stream)
    btn_next.place(x=230, y=250)
    window_detecting.mainloop()


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return

            res = detect_user()
            if res.status_code == 201 and not self.stopped():
                user = res.json()

                fio, role = user.get("name"), user.get("info")
                # if old_user_fio != fio:
                logger.info(f"Detected user: {fio}")
                showinfo("Найден пользователь", fio)
                # image_text = fio + "\n" + role
                image_text = role
                img = Image.new("RGB", (800, 200), color="red")
                unicode_font = ImageFont.truetype(def_values.TEXT_FONT, 35)
                output_image = ImageDraw.Draw(img)
                avg_char_width = sum(unicode_font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
                max_char_count = int(img.size[0] * .98 / avg_char_width)
                image_text = textwrap.fill(text=image_text, width=max_char_count)
                image_text = fio + "\n" + image_text
                output_image.text(
                    (10, 10), image_text, fill=(255, 255, 0), font=unicode_font
                )
                img.save(def_values.RESULT_IMAGE)

                # old_user_fio = fio

            elif res.status_code == 500:
                logger.error("Backend error")
                break

            time.sleep(1)


def detect_user(file_path: str = def_values.STREAM_SCREENSHOT_PATH) -> dict:
    extention = file_path.split(".")[-1]
    with open(file_path, "rb") as f:
        chunk = f.read(15 * 1024 * 1024)  # 50 MB

        res = requests.post(
            f"{def_values.BACKEND_URL}/detect_user",
            params={"extention": extention},
            files={"file_data": chunk},
        )

        return res


def process_stream():
    global loop
    global label
    global frames
    global frameCnt
    global window_detecting

    window_detecting.destroy()

    window_detecting = tk.Toplevel()
    window_detecting.title("Титруемся")
    window_detecting.resizable(False, False)
    window_detecting.geometry("800x300")

    label = tk.Label(window_detecting)
    frameCnt = 41
    frames = [
        tk.PhotoImage(file=def_values.PROCESSING_GIF, format="gif -index %i" % (i))
        .zoom(2)
        .subsample(3)
        for i in range(frameCnt)
    ]
    label.pack()

    btn_back = tk.Button(window_detecting, text="Назад", command=back2main)
    btn_back.place(x=0, y=0)

    logger.info("Starting users detection process...")

    loop = MyThread()
    loop.start()

    window_detecting.after(0, run_gif, 0)
    window_detecting.mainloop()


def run_gif(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    window_detecting.after(40, run_gif, ind)


def back2main():
    loop.stop()
    window_detecting.destroy()
