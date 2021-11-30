from bs4 import BeautifulSoup
import requests

URL = "https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C428"
dop_url = "https://ros-bilet.ru/"
persons_url = []
list_bus = []
ticket_list = []


def get_url(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")
    pages_count = int(soup.find("ul", class_="pager").find_all("a")[-1].text)

    # for page in range(0, pages_count):
    for page in range(0, 1):
        url_page = f"https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C{page}"
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, "lxml")

        # flight_items = soup.find('table', class_='views-table cols-9').find_all('tr')
        flight_items = soup.find_all("td", class_="views-field views-field-path")
        for fi in flight_items:
            links_page = fi.find("a").get('href')
            # url_bilet = dop_url + links_page
            url_bilet = "https://ros-bilet.ru/reys/yalta/novocherkassk-5124586"
            response = requests.get(url_bilet)
            soup = BeautifulSoup(response.text, "lxml")
            otkyda = soup.find('div', class_='bus-stantion-info-text').text
            print(otkyda)


            # road = soup.find('h1')
            # field_item_even = soup.find_all('div', class_="field-item even")
            # start_time = field_item_even[0].text.strip()
            # end_time = field_item_even[1].text.strip()
            # price_adult = field_item_even[4].text.strip()
            # price_children = field_item_even[5].text.strip()

            # time_default = soup.find_all('div', class_="time-default")
            # start_time = time_default[0].text.strip()
            # end_time = time_default[1].text.strip()
            #TODO не могу определить время в пути
            # travel_time = soup.find_all('div', class_="tline even")
            # print(travel_time[0].find_all('div', class_="time-default"))

            # start_road = field_item_even[6].text.split(',')[0]
            # end_road = field_item_even[6].text.split(',')[-1]


            break
            # flight_date = fi.find_all("td")

            # print(flight_date)
            # try:
            #     flight_nember = flight_date[8].text.strip()
            # except:
            #     flight_nember = 'NO'
            # print(flight_nember)
            # try:
            #     flight_nember = flight_date[0].text.strip()
            # except:
            #     flight_nember = 'NO'
            # try:
            #     beginning_route = flight_date[1].text.rstrip()
            # except:
            #     beginning_route = 'NO'
            #
            # try:
            #     end_route = flight_date[3].text.strip()
            # except:
            #     end_route = 'NO'
            #
            # try:
            #     sending_time = flight_date[2].text.strip()
            # except:
            #     sending_time = 'NO'
            #
            # try:
            #     arrival_time = flight_date[4].text.strip()
            # except:
            #     arrival_time = 'NO'
            #
            # try:
            #     bus = flight_date[5].text.strip()
            # except:
            #     bus = 'NO'
            #
            # try:
            #     money = flight_date[6].text.rstrip('\n')
            # except:
            #     money = 'NO'

            # list_bus.append((flight_nember, beginning_route, end_route, sending_time, arrival_time, bus, money))
    # with open('chek.txt', "a", encoding="utf-8") as file:
    #     for line in list_bus:
    #         file.write(f"{line}\n")


def main():
    get_url(URL)


if __name__ == "__main__":
    main()
