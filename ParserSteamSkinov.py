import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def initialize_driver():
    chromedriver_autoinstaller.install()  # Автоматическая установка подходящей версии ChromeDriver

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_price_csgo_item(driver):
    try:
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")

        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(page_content)

        item_price_div = soup.find_all(
            "span", class_="market_commodity_orders_header_promote"
        )
        if item_price_div and len(item_price_div) > 1:
            item_price_text = item_price_div[1].text.strip()
            item_price_text = item_price_text.replace("$", "").replace(",", "").strip()
            try:
                item_price = float(item_price_text)
            except ValueError:
                print("Ошибка при преобразовании цены:", item_price_text)
                item_price = None
        else:
            item_price = None

        return item_price
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def Steam_data(item_name):
    item_name = item_name.replace(" ", "%20").replace("|", "%7C")
    url = f"https://steamcommunity.com/market/listings/730/{item_name}"
    driver = initialize_driver()
    try:
        driver.get(url)
        time.sleep(5)  # Подождите, пока страница загрузится

        item_price = get_price_csgo_item(driver)
        return item_price

    finally:
        driver.quit()


if __name__ == "__main__":
    item_name = "Glove Case"
    price = Steam_data(item_name)
    print(f"Цена: {price}")
