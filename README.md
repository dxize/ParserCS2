# ParserCS2 (Counter-Strike 2)
Простенький парсер скинов marketcsgo -> steam. 
Если есть идеи для проектов пишите сюда -> [telegram](https://t.me/princeinthedarkness)

### 1. Что умеет данный бот?
Скрипт заходит на сайт https://market-old.csgo.com/ (проходит капчу), парсирует html код и получает оттуда теги с нужными мне элементами. Далее заходит в steam для сравнения цены. Если выяснится, что при покупки данного скина пользователь сможет получить >= +15% от стоимости товара на marketcsgo, приходит оповещение в телеграм боте.

### 2. Как это выглядит?
![image](https://github.com/user-attachments/assets/86663a54-0c17-4fc6-926c-2def4a7e645d)

### 3. Что нужно для запуска?
1) Выполните следующие команды для установки всех необходимых библиотек:
* pip install requests
* pip install beautifulsoup4
* pip install DrissionPage
* pip install selenium
* pip install webdriver-manager
* pip install aiogram
* pip install aiohttp
  
Для использования selenium с Chrome вам потребуется установить Google Chrome и соответствующий ChromeDriver. Библиотека webdriver-manager автоматизирует этот процесс, поэтому вам не нужно вручную скачивать и устанавливать ChromeDriver.

2) Нужно создать бота в [телеграме](https://t.me/BotFather) (там ничего сложного) и вставить апи ключ

### 4. Дополнительно...
Если хотите, чтобы парсировались цены с определённого ценового диапазона, меняйте ссылку f"{base_url}&p={current_page}&rs=0;500000&sd=desc"(0 в данной ссылке означает от скольки, а 500000 - до скольки) в ParserMarketCSGOSkinov.py

