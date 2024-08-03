# ParserCS2
Простенький парсер скинов marketcsgo -> steam

### 1. Что умеет данный бот?
Скрипт заходит на сайт https://market-old.csgo.com/, парсирует html код и получает оттуда теги с нужными мне элементами. Далее заходит в steam для сравнении цены. Если выяснится, что при покупки данного скина пользователь сможет получить +15% от стоимости товара на marketcsgo, приходит оповещение в телеграм боте.

### 2. Как это выглядит?
![image](https://github.com/user-attachments/assets/86663a54-0c17-4fc6-926c-2def4a7e645d)

### 3. Что нужно для запуска?
Выполните следующие команды для установки всех необходимых библиотек:
* pip install requests
* pip install beautifulsoup4
* pip install DrissionPage
* pip install selenium
* pip install webdriver-manager
* pip install aiogram
* pip install aiohttp
  
Для использования selenium с Chrome вам потребуется установить Google Chrome и соответствующий ChromeDriver. Библиотека webdriver-manager автоматизирует этот процесс, поэтому вам не нужно вручную скачивать и устанавливать ChromeDriver.

