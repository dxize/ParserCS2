import re
import time
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage
import requests


def get_exchange_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        exchange_rate = data["rates"]["RUB"]  # курс RUB за 1 USD
        print(f"Курс обмена USD -> RUB: {exchange_rate}")
        return exchange_rate
    except Exception as e:
        print(f"Ошибка при получении курса обмена: {e}")
        return None


def initialize_driver():
    page = ChromiumPage()
    return page


def get_next_csgo_item(page, item_index, exchange_rate):
    try:
        # Получаем содержимое страницы
        page_content = page.html
        soup = BeautifulSoup(page_content, "html.parser")
        item_elements = soup.find_all("a", attrs={"class": "item", "href": True})

        if item_index >= len(item_elements):
            return None, None, None, None

        item_element = item_elements[item_index]
        item_link = "https://market-old.csgo.com" + item_element["href"]
        item_name = item_element.find("div", class_="name").text.strip()
        item_price_div = item_element.find("div", class_="price")
        item_image_div = item_element.find("div", class_="image")["style"]

        url_pattern = re.compile(r"url\((https?://[^\)]+)\)")
        match = url_pattern.search(item_image_div)
        item_image_url = match.group(1) if match else None
        item_image_url = re.sub(r"/100\.png$", "/300.png", item_image_url)

        if item_price_div:
            # Извлекаем текст из элемента
            item_price_text = item_price_div.text.strip()
            print("Текст цены:", item_price_text)
            # Удаляем возможные символы валюты и пробелы, и преобразуем текст в число
            item_price_text = (
                re.sub(r"[^\d.]", "", item_price_text).replace(",", ".").strip()
            )
            print("Обработанный текст цены:", item_price_text)
            try:
                item_price_rub = float(item_price_text)
                item_price_usd = (
                    item_price_rub / exchange_rate
                )  # делим на курс RUB за 1 USD
                print(
                    f"Цена в рублях: {item_price_rub}, Цена в долларах: {item_price_usd}"
                )
            except ValueError:
                print("Ошибка при преобразовании цены:", item_price_text)
                item_price_usd = None
        else:
            item_price_usd = None

        return (
            item_name,
            round(item_price_usd, 2) if item_price_usd is not None else None,
            item_link,
            item_image_url,
        )
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None, None, None, None


def MarketCSGO(current_page, item_index):
    base_url = "https://market-old.csgo.com/?lang=en"
    page = initialize_driver()

    exchange_rate = get_exchange_rate()
    if exchange_rate is None:
        print("Не удалось получить курс обмена валют.")
        return None, None, None, current_page, item_index

    try:
        while True:
            # Переходим на нужную страницу
            page.get(
                (f"{base_url}&p={current_page}&rs=0;500000&sd=desc")
                # f"{base_url}/?s=pop&t=all&p={current_page}&rs=2500;500000&sd=desc"
            )  # (f"{base_url}&p={current_page}&rs=2500;500000&sd=desc")
            time.sleep(5)  # Подождите, пока страница загрузится

            item_name, item_price, item_link, item_image = get_next_csgo_item(
                page, item_index, exchange_rate
            )
            if item_name is None:
                print(f"На странице {current_page} больше нет предметов.")
                current_page += 1
                item_index = 0
                continue
            item_index += 1

            return (
                item_name,
                item_price,
                item_link,
                current_page,
                item_index,
                item_image,
            )

    finally:
        page.close()


if __name__ == "__main__":
    current_page = 1
    item_index = 0
    item_name, item_price, item_link, current_page, item_index, item_image = MarketCSGO(
        current_page, item_index
    )
    print(f"Название: {item_name}")
    print(f"Цена в долларах: {item_price}")
    print(f"Ссылка: {item_link}")
    print(f"Текущая страница: {current_page}")
    print(f"Индекс предмета: {item_index}")
    print(f"URL изображения: {item_image}")
