from bs4 import BeautifulSoup
import requests
import time

URL = "https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C428"
URL_CARD = "https://ros-bilet.ru"
FLIGHT_DATA = []


def get_url(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")
    pages_count = int(soup.find("ul", class_="pager").find_all("a")[-1].text)

    for page in range(0, pages_count):
        url_page = f"https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C{page}"
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, "lxml")

        flight_items = soup.find_all("td", class_="views-field views-field-path")
        url_page_href = [fi.find("a").get('href') for fi in flight_items]
        url_ticket = [URL_CARD + i for i in url_page_href]
        for url_tic in url_ticket:
            response = requests.get(url_tic)
            soup = BeautifulSoup(response.text, "lxml")
            data_ticket_road_soup = soup.find_all('div', class_='bus-stantion-info-text')
            start_ticket_route = data_ticket_road_soup[0].text.split(',')[0]
            end_ticket_route = data_ticket_road_soup[1].text.split(',')[0]

            data_road_soup = soup.find('div',
                                       class_="field field-name-field-path-following field-type-text-long field-label-hidden").find(
                'div', class_="field-item even")
            start_road = data_road_soup.text.split(',')[0]
            end_road = data_road_soup.text.split(',')[-1]

            field_item_even = soup.find_all('div', class_="field-item")
            if len(field_item_even) == 8:
                price_adult = field_item_even[4].text.strip()
                price_children = field_item_even[5].text.strip()
            else:
                if 'Акция! Раннее бронирование' == field_item_even[3].text.strip():
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
            with open('bus_route.cvc', "a", encoding="utf-8") as file:
                for line in FLIGHT_DATA:
                    file.write(f"{line}\n")
            FLIGHT_DATA.clear()


def main():
    tic = time.perf_counter()
    get_url(URL)
    toc = time.perf_counter()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")


if __name__ == "__main__":
    main()
