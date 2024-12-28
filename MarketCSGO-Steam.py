import asyncio
from aiogram import Bot, types
from aiogram.filters import Command
from aiogram import Router, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

from ParserMarketCSGOSkinov import MarketCSGO  
from ParserSteamSkinov import Steam_data  

API_TOKEN = "YOUR_API_TOKEN"

# Создаем экземпляр бота с указанием режима парсинга HTML
bot = Bot(
    token=API_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML"),
)
router = Router()

# Глобальные переменные для управления состоянием мониторинга
monitoring_task = None
monitoring_task_running = False


@router.message(Command("start"))
async def start(message: types.Message):
    global monitoring_task, monitoring_task_running
    if not monitoring_task_running:
        monitoring_task_running = True
        await message.answer("Запуск мониторинга цен...")
        monitoring_task = asyncio.create_task(price_monitoring(message))
    else:
        await message.answer("Мониторинг уже запущен.")


@router.message(Command("stop"))
async def stop(message: types.Message):
    global monitoring_task, monitoring_task_running
    if monitoring_task_running:
        monitoring_task_running = False
        monitoring_task.cancel()
        await message.answer("Остановка мониторинга цен...")
        try:
            await monitoring_task
        except asyncio.CancelledError:
            print("Мониторинг был отменен.")
    else:
        await message.answer("Мониторинг не был запущен.")


async def price_monitoring(message: types.Message):
    item_index = 0
    current_page = 1
    while monitoring_task_running:
        try:
            result = MarketCSGO(current_page, item_index)
            if result is None:
                await message.answer("На всех страницах больше нет предметов.")
                break

            (
                item_name,
                item_price_MarketCSGO,
                item_link,
                current_page,
                item_index,
                item_image,
            ) = result
            if item_name is not None:
                item_price_Steam = Steam_data(item_name)
                print(item_name)
                print(item_price_MarketCSGO, item_price_Steam)
                # Проверка, чтобы убедиться, что цены не None
                if item_price_Steam is not None and item_price_MarketCSGO is not None:
                    checking_the_profit = (
                        (item_price_Steam * 0.87 - item_price_MarketCSGO)
                        / item_price_MarketCSGO
                        * 100
                    )

                    print(
                        item_name,
                        item_price_Steam,
                        checking_the_profit,
                    )
                    checking_the_profit = int(checking_the_profit * 100) / 100
                    if checking_the_profit >= 15:
                        response_text = (
                            f"<b>{item_name}</b>\n\n"
                            f"🛒 <b>CSGO-Market Price:</b> ${item_price_MarketCSGO}\n\n"
                            f"💸 <b>Steam Price:</b> ${item_price_Steam}\n\n"
                            f"📈 <b>Profit:</b> {checking_the_profit}%\n\n"
                            f"🔗 <b>Links: </b><a href='{item_link}'>CSGO-Market</a> ,  <a href='https://steamcommunity.com/market/listings/730/{item_name}'>Steam</a>"
                        )
                        await bot.send_photo(
                            message.chat.id, item_image, caption=response_text
                        )
                    else:
                        print("Нет подходящих предложений")
                else:
                    print("Цены не могут быть определены")
            else:
                await asyncio.sleep(
                    10
                )  # Добавляем задержку для предотвращения быстрого циклического выполнения
        except asyncio.CancelledError:
            print("Мониторинг был отменен.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await message.answer(f"Произошла ошибка: {e}")
            await asyncio.sleep(
                10
            )  # Добавляем задержку для предотвращения быстрого циклического выполнения

    print("Мониторинг остановлен")


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    # Удаление вебхука, если установлен, и запуск поллинга
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
