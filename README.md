# 5letterwords_bot
Удобный бот, позволяющий отгадывать слово из пяти букв на основании следующей информации:  
1. Буквы, которые точно есть, но неизвестна из позиция в слове
2. Буквы, которые точно есть и их позиция в слове известа
3. Буквы, которых точно нет в слове

### Схема поиска
Отправить боту сообщение состоящее из либо одного элемента, либо трех, отделенных запятыми:

> **Important**
> Первый элемент представляет собой набор из 5 символов, где каждый символ кириллицы принимается как известная буква с известной позицией в слове  
> Второй элемент представляет собой набор любого количества символов, которыми будет пополнен текущий массив букв, которые ДОЛЖНЫ присутствовать в слове  
> Третий Элекмент представляет собой набор любого количества символов, которыми будет пополнен текущий массив букв, которые НЕ ДОЛЖНЫ присутсовать в слове 


### Примеры:  
> #### Запрос
> _Хочу найти слово в котором вторая буква - О, а пследние две - КА. Известно, что в слове точно должны быть буквы К и Ж, и точно не должно быть букв Г и М:_
> ```
> _о$ка, кж, гм  
> ```
> #### Ответ
> ```
> ложка
> ножка
> ```

> #### Запрос
> _Хочу найти слово в котором две последние буквы - ОК, и известно, что в этом слове нет буквы Б, Ы и Ч:_
> ```
> 888ок,,быч  
> ```
> #### Ответ
> ```
> валок
> венок
> весок
> вилок
> висок
> виток
> возок
> волок
> впрок
> давок
> жевок
> зевок
> кивок
> севок
> совок
> ```

### Команды бота  
**/restart** - чтоыб сбросит все данные поиска  
**/status** - чтобы посмотреть по каким параметрам ведется поиск

### Стэк  
|**TECHNOLOGY**|**NAME**|
|----|-----|
|Telegram framework|[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)|
|ORM|SQLAlchemy|
|Database|SQLite    |
|Tests|pytest    |

## Деплой
### SYSTEMD service config file пример 
Запусти следующую команду, чтобы создать сервисный файл systemd:  
```
cd /etc/systemd/system; sudo vi 5lw_bot.service
```

Заполни открывшийся файл по образцу:
```
[Unit]
Description=5 letter words bot
After=network.target
Requires=network.target
StartLimitIntervalSec=360
StartLimitBurst=12

[Service]
Type=simple
WorkingDirectory=/path/to/bot's/directory/

User=username
Group=username

ExecStart=/path/to/venv/bin/python /path/to/5lw_bot/server.py --start
ExecReload=/path/to/venv/bin/python /path/to/5lw_bot/server.py --restart
TimeoutSec=900
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
```

### Запускаем systemd service
```
sudo systemctl daemon-reload; sudo systemctl start 5lw_bot.service
```
