import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageEnhance, ImageTk
import cv2
import numpy as np

mouse = Controller()
time.sleep(0.5)


def click(xs, ys):
    mouse.position = (xs, ys + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)


def choose_window_gui():
    root = tk.Tk()
    root.withdraw()

    windows = gw.getAllTitles()
    if not windows:
        return None

    choice = simpledialog.askstring("Выбор окна Telegram", "Введите номер окна:\n" + "\n".join(
        f"{i}: {window}" for i, window in enumerate(windows)))

    if choice is None or not choice.isdigit():
        return None

    choice = int(choice)
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        return None


def find_image_on_screen(screenshot, template_path, threshold=0.7):
    template = cv2.imread(template_path, cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc
    return None


window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)

if not check:
    print(f"\nОкно {window_name} не найдено!\nПожалуйста, выберите другое окно.")
    window_name = choose_window_gui()

if not window_name or not gw.getWindowsWithTitle(window_name):
    print("\nНе удалось найти указанное окно!\nЗапустите Telegram, после чего перезапустите бота!")
else:
    print(f"\nОкно {window_name} найдено\nНажмите 'S' для старта.")

telegram_window = gw.getWindowsWithTitle(window_name)[0]
paused = True
last_check_time = time.time()
last_blue_check_time = time.time()

root = tk.Tk()
root.withdraw()

while True:
    if keyboard.is_pressed('S'):
        paused = not paused
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'S'")
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left + 10,
        telegram_window.top + 140,
        telegram_window.width - 30,
        telegram_window.height - 200
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))
    #scrn.save("screenshot.png")
    template_path = '7.png'
    found_location = find_image_on_screen(scrn, template_path)

    if found_location:
        screen_x, screen_y = found_location[0] + window_rect[0], found_location[1] + window_rect[1]
        click(screen_x, screen_y)
        time.sleep(0.002)


    width, height = scrn.size


    for xq in range(0, width, 10):
        for yq in range(0, height, 10):
            r, g, b = scrn.getpixel((xq, yq))
            if (b in range(50, 255)) and (r in range(150, 255)) and (g in range(0, 255)):
                if not (r > 240 and g > 240 and b > 240):
                    screen_xq = window_rect[0] + xq
                    screen_yq = window_rect[1] + yq
                    click(screen_xq, screen_yq)
                    break
print('Стоп')








