# ГАЙД
https://telegra.ph/Avtoklikker-dlya-BLUM-GAJD-05-29

![photo_2024-07-07_11-47-59](https://github.com/meKryztal/Blum-clicker/assets/47853767/eb7aa1ce-408f-49bb-8532-37c96ff7ea03)



# Делать выбор нажимать или нет на заморозку не получилось сделать

# Про требования к железу:
Скрипт делает скриншоты окна для поиска пикселей и чем выше у вас разрешение экрана, тем мощнее нужно железо

Поэтому если у вас пропуски и мало набирает, то снижайте разрешение экрана с 2к на fullhd или с fulhd на hd



# Если вы используете в другом окне и чтоб постоянно его не выбирать, сделайте так:

![photo_2024-07-07_12-03-47](https://github.com/meKryztal/Blum-clicker/assets/47853767/8294b22f-b6db-4bb6-bab1-9750bbca3a8e)

Замените имя "TelegramDesktop" на свое, например "NoxPlayer"


# Изначально установлены настройки для окна в telegram desktop, на других окнах нужны свои настройки, что б не тригерился по краям, вот для эмулятора:

![photo_2024-07-07_12-13-17](https://github.com/meKryztal/Blum-clicker/assets/47853767/f872f2b7-e2ef-4552-8c1c-161aaa73d629)

Заменить эти строки на:
```
window_rect = (
        telegram_window.left + 10,
        telegram_window.top + 200,
        telegram_window.width - 60,
        telegram_window.height - 210
    )
```

Если вдруг у вас все таки тригериться на края, индивидуальные проблемы могут быть, вот инструкция как сделать под себя:
https://telegra.ph/Podbor-razmerov-okna-07-07
