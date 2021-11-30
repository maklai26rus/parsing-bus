from bs4 import BeautifulSoup
import requests

URL = "https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C428"
dop_url = "https://ros-bilet.ru"
persons_url = []
list_bus = []
ticket_list = []


def get_url(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")
    pages_count = int(soup.find("ul", class_="pager").find_all("a")[-1].text)

    for page in range(0, pages_count):
    # for page in range(0, 1):
        url_page = f"https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C{page}"
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, "lxml")

        flight_items = soup.find_all("td", class_="views-field views-field-path")
        for fi in flight_items:
            links_page = fi.find("a").get('href')
            url_bilet = dop_url + links_page
            print(url_bilet)
            # url_bilet = "https://ros-bilet.ru/reys/abinsk/aleksandrovskoe-5192458"
            response = requests.get(url_bilet)
            soup = BeautifulSoup(response.text, "lxml")
            road_bilet = soup.find_all('div', class_='bus-stantion-info-text')

            start_bilet = road_bilet[0].text.split(',')[0]
            end_bilet = road_bilet[1].text.split(',')[0]

            # field_item_even = soup.find_all('div', class_="field-item even")
            field_item_even = soup.find_all('div', class_="field-item")
            if len(field_item_even) != 6:
                price_adult = field_item_even[4].text.strip()
                price_children = field_item_even[5].text.strip()
                start_road = field_item_even[6].text.split(',')[0]
                end_road = field_item_even[6].text.split(',')[-1]
            else:
                price_adult = field_item_even[3].text.strip()
                price_children = field_item_even[4].text.strip()
                start_road = field_item_even[5].text.split(',')[0]
                end_road = field_item_even[5].text.split(',')[-1]

            time_default = soup.find_all('div', class_="time-default")
            start_time = time_default[0].text.strip()
            end_time = time_default[1].text.strip()

            travel_time_soup = soup.find_all('div', class_="tline even")
            travel_time = travel_time_soup[1].find('div', class_='two tap').text.strip()

            ticket_list.append(
                f"{start_bilet}, '-', {end_bilet}, {start_time}, {end_time}, {travel_time}, {price_adult}, '/',{price_children}, {start_road}, '-', {end_road}")
            with open('test.cvc', "a", encoding="utf-8") as file:
                for line in ticket_list:
                    file.write(f"{line}\n")

            # print(start_bilet, '-', end_bilet, start_time, end_time, travel_time, price_adult, '/', price_children, start_road, '-',
            #       end_road)
            #
            # break


def main():
    get_url(URL)


if __name__ == "__main__":
    main()
