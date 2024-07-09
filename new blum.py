import pyautogui
import cv2
import numpy as np
import concurrent.futures
import time
import keyboard
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog

mouse = Controller()


def get_window(window):
    windows = pyautogui.getWindowsWithTitle(window)
    if windows:
        window = windows[0]
        region_left = window.left
        region_top = window.top
        region_width = window.width
        region_height = window.height
        return region_left, region_top, region_width, region_height
    else:
        raise Exception(f"Окно '{window}' не найдено.")


star_templates_10s = [
    ('6', cv2.imread('6.png', cv2.IMREAD_COLOR)),
]

# Удалить эти три строки, если не нужна заморозка и внизу скрипта удалить
star_templates_5s = [
    ('4', cv2.imread('4.png', cv2.IMREAD_COLOR)),
    ('5', cv2.imread('5.png', cv2.IMREAD_COLOR)),
]

star_templates = [
    ('1', cv2.imread('1.png', cv2.IMREAD_COLOR)),
    ('2', cv2.imread('2.png', cv2.IMREAD_COLOR)),
    ('3', cv2.imread('3.png', cv2.IMREAD_COLOR)),
]


def click(xs, ys):
    mouse.position = (xs, ys)
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(0.0001)


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


def grab_screen(region, scale_factor=0.5):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    new_width = int(screenshot.shape[1] * scale_factor)
    new_height = int(screenshot.shape[0] * scale_factor)
    resized_screenshot = cv2.resize(screenshot, (new_width, new_height))
    return resized_screenshot


def find_template_on_screen(template, screenshot, step=0.7, scale_factor=0.5):
    new_width = int(template.shape[1] * scale_factor)
    new_height = int(template.shape[0] * scale_factor)
    resized_template = cv2.resize(template, (new_width, new_height))
    result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= step:
        return (int(max_loc[0] / scale_factor), int(max_loc[1] / scale_factor))
    return None


def click_on_screen(position, template_width, template_height, region_left, region_top):

    center_x = position[0] + template_width // 2
    center_y = position[1] + template_height // 2
    click(center_x + region_left, center_y + region_top+4)



def process_template(template_data, screenshot, scale_factor, region_left, region_top):

    template_name, template = template_data
    if template is None:
        print(f"Ошибка загрузки {template_name}")
        return template_name, None
    position = find_template_on_screen(template, screenshot, scale_factor=scale_factor)
    if position:
        template_height, template_width, _ = template.shape
        click_on_screen(position, template_width, template_height, region_left, region_top)

        return template_name, position
    return template_name, None


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
last_pause_time = time.time()

last_check_time_10s = time.time()
last_check_time_5s = time.time()

while True:

    if keyboard.is_pressed('S') and time.time() - last_pause_time > 0.1:
        paused = not paused
        last_pause_time = time.time()
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'S'")
        time.sleep(0.2)

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    if not paused:

        screenshot = grab_screen(window_rect)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            current_time = time.time()

            if current_time - last_check_time_10s >= 5:
                futures += [executor.submit(process_template, template_data, screenshot, 0.5, telegram_window.left, telegram_window.top) for template_data in star_templates_10s]
                last_check_time_10s = current_time

            # Удалить эти три строки, если не нужна заморозка и вверху скрипта удалить
            if current_time - last_check_time_5s >= 1:
                futures += [executor.submit(process_template, template_data, screenshot, 0.5, telegram_window.left, telegram_window.top) for template_data in star_templates_5s]
                last_check_time_5s = current_time


            futures += [executor.submit(process_template, template_data, screenshot, 0.5, telegram_window.left, telegram_window.top) for template_data in star_templates]

            for future in concurrent.futures.as_completed(futures):
                template_name, position = future.result()



print('Стоп')
