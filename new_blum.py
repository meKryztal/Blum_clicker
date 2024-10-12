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
        raise Exception(f"{Fore.LIGHTRED_EX}Окно '{window}' не найдено.")

star_templates_10s = [
    ('6', cv2.imread('6.png', cv2.IMREAD_COLOR)),
    ('7', cv2.imread('7.png', cv2.IMREAD_COLOR)),
]

# Удалить эти строки, если не нужна заморозка и внизу скрипта удалить
star_templates_5s = [
    ('4', cv2.imread('4.png', cv2.IMREAD_COLOR)),
    ('5', cv2.imread('5.png', cv2.IMREAD_COLOR)),
]
########################################################


star_templates = [
    ('1', cv2.imread('1.png', cv2.IMREAD_COLOR)),
    ('2', cv2.imread('2.png', cv2.IMREAD_COLOR)),
    ('3', cv2.imread('3.png', cv2.IMREAD_COLOR)),
    ('10', cv2.imread('10.png', cv2.IMREAD_COLOR)),
    #('11', cv2.imread('11.png', cv2.IMREAD_COLOR)),
]

star_templates_p = [
    ('8', cv2.imread('8.png', cv2.IMREAD_COLOR))
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
            
        elif template_name == '7' and click_counts['6'] > 1:
            center_x = telegram_window.left + telegram_window.width // 2
            center_y = telegram_window.top + telegram_window.height // 2
            mouse.position = (center_x, center_y)
            time.sleep(0.3)
            #mouse.scroll(0, 2)
            mouse.scroll(0, -200)
            time.sleep(0.3)

            position_8 = find_template_on_screen(star_templates_p[-1][1], screenshot, scale_factor=scale_factor)
            if position_8:
                click_on_screen(position_8, template_width, template_height, region_left, region_top)
                click_counts['6'] -= 1
        elif template_name == '9':
            click_on_screen(position, template_width, template_height, region_left, region_top)        

        elif template_name != '6':
            click_on_screen(position, template_width, template_height, region_left, region_top)
        return template_name, position
    return template_name, None

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
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
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

            if current_time - last_check_time_10s >= 5:
                futures += [executor.submit(process_template, template_data, screenshot, 0.5, telegram_window.left, telegram_window.top, click_counts) for template_data in star_templates_10s]
                last_check_time_10s = current_time

            # Удалить эти три строки, если не нужна заморозка и вверху скрипта удалить
            if current_time - last_check_time_5s >= 1:
                futures += [executor.submit(process_template, template_data, screenshot, 0.5, telegram_window.left, telegram_window.top, click_counts) for template_data in star_templates_5s]
                last_check_time_5s = current_time
            ############################################################################################################################################
            
            futures += [executor.submit(process_template, template_data, screenshot, 0.5, telegram_window.left, telegram_window.top, click_counts) for template_data in star_templates]

            for future in concurrent.futures.as_completed(futures):
                template_name, position = future.result()

    if click_counts['6'] == 1:
        if not end_time:
            end_time = time.time() + 50
            print(f'{Fore.LIGHTWHITE_EX}Достигнуто заданное количество игр')

    if end_time and time.time() >= end_time:
        break

print(f'{Fore.LIGHTRED_EX}Стоп')
