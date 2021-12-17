from bs4 import BeautifulSoup
import requests
import time
import aiohttp
import asyncio

#Проверять нужно последнию страницу на данный момент 438 

URL = "https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C438"
URL_CARD = "https://ros-bilet.ru"
FLIGHT_DATA = []

_err_str = ['Скидка', 'Акция!', 'Организованный', 'актуально']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/81.0.4044.96 YaBrowser/20.4.0.1461 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}

URL_TICKET_LIST = []


async def get_page_data(session, page):
    url_page = f"https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C{page}"
    async with session.get(url=url_page, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), "lxml")
        flight_items = soup.find_all("td", class_="views-field views-field-path")
        url_page_href = [fi.find("a").get('href') for fi in flight_items]
        url_ticket = [URL_CARD + i for i in url_page_href]

    for url_tic in url_ticket:
        async with session.get(url=url_tic, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            data_ticket_road_soup = soup.find_all('div', class_='bus-stantion-info-text')
            start_ticket_route = data_ticket_road_soup[0].text.split(',')[0]
            end_ticket_route = data_ticket_road_soup[1].text.split(',')[0]

            data_road_soup = soup.find('div',
                                       class_="field field-name-field-path-following field-type-text-long field-label-hidden").find(
                'div', class_="field-item even")
            start_road = data_road_soup.text.split(',')[0]
            end_road = data_road_soup.text.split(',')[-1]

            field_item_even = soup.find_all('div', class_="field-item")
            _bad_position = [field_item_even[3].text.strip().find(i) for i in _err_str if
                             field_item_even[3].text.strip().find(i) == 0]
            if len(field_item_even) == 8:
                price_adult = field_item_even[4].text.strip()
                price_children = field_item_even[5].text.strip()
            else:
                if _bad_position:
                    price_adult = field_item_even[4].text.strip()
                    price_children = field_item_even[5].text.strip()
                else:
                    price_adult = field_item_even[3].text.strip()
                    price_children = field_item_even[4].text.strip()

            time_default_soup = soup.find_all('div', class_="time-default")
            start_time_route = time_default_soup[0].text.strip()
            end_time_route = time_default_soup[1].text.strip()

            travel_time_soup = soup.find_all('div', class_="tline even")
            travel_time = travel_time_soup[1].find('div', class_='two tap').text.strip()

            _sts_start_route = start_ticket_route + ' - ' + end_ticket_route
            _str_price = price_adult + ' / ' + price_children
            _str_road = start_road + ' - ' + end_road
            FLIGHT_DATA.append(
                f"{_sts_start_route}, {start_time_route}, {end_time_route}, {travel_time}, {_str_price}, {_str_road}")
            with open('bus_route_asy.cvc', "a", encoding="utf-8") as file:
                for line in FLIGHT_DATA:
                    file.write(f"{line}\n")
            FLIGHT_DATA.clear()


async def gather_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(URL, headers=headers)

        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = int(soup.find("ul", class_="pager").find_all("a")[-1].text)
        tasks = []

        for page in range(0, pages_count):
            # for page in range(0, 5):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    tic = time.perf_counter()
    asyncio.run(gather_data())
    toc = time.perf_counter()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")


if __name__ == "__main__":
    main()

