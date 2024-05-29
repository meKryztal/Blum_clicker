import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw


mouse = Controller()
time.sleep(0.5)


def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)


check = gw.getWindowsWithTitle("TelegramDesktop")
if not check:
    print(f"Окно BLUM не найдено!\nЗапустите Telegram и окно BLUM, после чего перезапустите бота!")

else:
    print(f"Окно BLUM найдено\nНажмите 'F1' для старта.")

telegram_window = check[0]
paused = True

while True:
    if keyboard.is_pressed('F1'):
        paused = not paused
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'F1'")
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False
    if pixel_found == True:
        break

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))
            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y + 3
                click(screen_x, screen_y)
                time.sleep(0.001)
                pixel_found = True
                break

print('Стоп')
