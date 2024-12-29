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
import base64
from colorama import Fore
import random
mouse = Controller()

WIND = 0.2 # Сдвиг окна


star_templates_10s = [
    ('6', cv2.imread('6.png', cv2.IMREAD_COLOR)),
]


def click(xs, ys):
    mouse.position = (xs, ys)
    mouse.press(Button.left)
    mouse.release(Button.left)


def choose_window_gui():
    root = tk.Tk()
    root.withdraw()
    windows = gw.getAllTitles()
    if not windows:
        return None
    choice = simpledialog.askstring(f"{Fore.LIGHTWHITE_EX}Выбор окна Telegram", "Введите номер окна:\n" + "\n".join(
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
    click(center_x + region_left, center_y + region_top + 4)

def process_template(template_data, screenshot, scale_factor, region_left, region_top, click_counts):
    template_name, template = template_data
    if template is None:
        print(f"{Fore.LIGHTRED_EX}Ошибка загрузки {template_name}")
        return template_name, None
    position = find_template_on_screen(template, screenshot, scale_factor=scale_factor)
    if position:
        template_height, template_width, _ = template.shape
        if template_name == '6' and click_counts['6'] > 1:
            click_on_screen(position, template_width, template_height, region_left, region_top)
            click_counts['6'] -= 1


        return template_name, position
    return template_name, None

def color_range(r, g, b):
    return (
            (r in range(84, 98) and g in range(114, 121) and b in range(116, 123)) or
            (r in range(98, 98) and g in range(50, 50) and b in range(14, 14)) or
            (r in range(220, 223) and g in range(118, 120) and b in range(70, 71)) or

            (r in range(113, 115) and g in range(111, 113) and b in range(107, 109)) or
            #(r in range(254, 255) and g in range(248, 251) and b in range(241, 244)) or

            (r in range(250, 255) and g in range(135, 190) and b in range(0, 1)) or

            (r in range(200, 255) and g in range(34, 65) and b in range(184, 200)) or
            (r in range(87, 129) and g in range(160, 203) and b in range(23, 60)) or
            (r in range(209, 239) and g in range(0, 14) and b in range(149, 167)) or
            (r in range(234, 234) and g in range(250, 251) and b in range(120, 122)) or
            (r in range(132, 180) and g in range(56, 88) and b in range(7, 38)) or
            (r in range(43, 58) and g in range(88, 111) and b in range(24, 36)) or
            (r in range(176, 183) and g in range(236, 242) and b in range(250, 255)) or
            (r in range(196, 255) and g in range(15, 32) and b in range(172, 195)) or

            (r in range(240, 255) and g in range(0, 15) and b in range(120, 200)) or
            (r in range(130, 180) and g in range(50, 80) and b in range(0, 20)) or
            (r in range(230, 240) and g in range(85, 160) and b in range(70, 140)) or
            (r in range(90, 120) and g in range(35, 50) and b in range(0, 5))
            )

def bomb(r, g, b):
    return ((r in range(240, 255) and g in range(170, 200) and b in range(20, 80)) or
            (r in range(74, 255) and g in range(0, 203) and b in range(0, 136)) or
            (r in range(160, 255) and g in range(0, 123) and b in range(0, 127))
            )

window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)
encoded = b'LS0tLS0tLS0tLdCa0J7QlCDQndCQ0KXQntCU0JjQotCh0K8g0JIg0J7QotCa0KDQq9Ci0J7QnCDQlNCe0KHQotCj0J/QlSwg0JvQrtCR0JDQryDQn9Cg0J7QlNCQ0JbQkCAtINCX0JDQn9Cg0JXQqdCV0J3QkCEhIS0tLS0tLS0tLS0KLS0tLS0tLS0tLS0tLS0tLS0t0J7QoNCY0JPQmNCd0JDQm9Cs0J3Qq9CZINCa0J7QlDogaHR0cHM6Ly9naXRodWIuY29tL21lS3J5enRhbC9CbHVtLWNsaWNrZXIgLS0tLS0tLS0tLS0tLS0tLS0t'
print(f"{Fore.LIGHTYELLOW_EX}{base64.b64decode(encoded).decode('utf-8')}")

if not check:
    print(f"{Fore.LIGHTRED_EX}\nОкно {window_name} не найдено!\nПожалуйста, выберите другое окно.")
    window_name = choose_window_gui()

if not window_name or not gw.getWindowsWithTitle(window_name):
    print(f"{Fore.LIGHTRED_EX}\nНе удалось найти указанное окно!\nЗапустите Telegram, после чего перезапустите бота!")
else:
    print(f"{Fore.LIGHTBLUE_EX}\nОкно {window_name} найдено\n")
    num = input(f"{Fore.LIGHTYELLOW_EX}Укажите количество игр, что нужно отыграть:\n")
    click_counts = {'6': int(num)}
    print(f"{Fore.LIGHTBLUE_EX}Нажмите 'S' для старта.")

telegram_window = gw.getWindowsWithTitle(window_name)[0]
paused = True
last_check_time = time.time()
last_blue_check_time = time.time()
last_pause_time = time.time()
last_check_time_10s = time.time()
last_check_time_5s = time.time()
end_time = None

while True:
    if keyboard.is_pressed('S') and time.time() - last_pause_time > 0.1:
        paused = not paused
        last_pause_time = time.time()
        if paused:
            print(f'{Fore.LIGHTBLUE_EX}Пауза')
        else:
            print(f'{Fore.LIGHTBLUE_EX}Работаю')
            print(f"{Fore.LIGHTBLUE_EX}Для паузы нажми 'S'")
        time.sleep(0.2)

    window_rect = (
        telegram_window.left+int(telegram_window.width*0.05),
        telegram_window.top+int(telegram_window.height*WIND),
        telegram_window.width-int(telegram_window.width*0.12),
        int(telegram_window.height*(0.92-WIND))
    )


    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    if not paused and click_counts['6'] > 0:
        screenshot = grab_screen(window_rect)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            current_time = time.time()

            if current_time - last_check_time_10s >= 12:
                futures += [executor.submit(process_template, template_data, screenshot, 0.5, (telegram_window.left+int(telegram_window.width*0.05)), (telegram_window.top+int(telegram_window.height*WIND)), click_counts) for template_data in star_templates_10s]
                last_check_time_10s = current_time

            for future in concurrent.futures.as_completed(futures):
                template_name, position = future.result()

        screenshot_pix = pyautogui.screenshot(region=window_rect)
        width, height = screenshot_pix.size
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = screenshot_pix.getpixel((x, y))

                if color_range(r, g, b):
                    if bomb(r, g, b):
                        break
                    else:
                        click(x+window_rect[0], y+window_rect[1])
                        #time.sleep(0.01)
                        break




    if click_counts['6'] == 1:
        if not end_time:
            end_time = time.time() + 50
            print(f'{Fore.LIGHTWHITE_EX}Достигнуто заданное количество игр')


    if end_time and time.time() >= end_time:
        break

print(f'{Fore.LIGHTRED_EX}Стоп')
