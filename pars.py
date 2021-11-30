from bs4 import BeautifulSoup
import requests

URL = "https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C428"
dop_url = "https://ros-bilet.ru/"
persons_url = []
list_bus = []


def get_url(url):
    # html = requests.get(url)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")
    pages_count = int(soup.find("ul", class_="pager").find_all("a")[-1].text)

    # for page in range(0, pages_count):
    for page in range(0, 1):
        url_page = f"https://ros-bilet.ru/perevozchik/evrotrans-ip-yacunov-sp?field_city_tid=&field_city_arrival_tid=&page=0%2C{page}"
        response = requests.get(url_page)
        soup = BeautifulSoup(response.text, "lxml")

        flight_items = soup.find('table', class_='views-table cols-9').find_all('tr')
        for fi in flight_items:
            flight_date = fi.find_all("td")
            # print(flight_date)
            try:
                flight_nember = flight_date[0].text.strip()
            except:
                flight_nember = 'NO'
            try:
                beginning_route = flight_date[1].text.rstrip()
            except:
                beginning_route = 'NO'

            try:
                end_route = flight_date[3].text.strip()
            except:
                end_route = 'NO'

            try:
                sending_time = flight_date[2].text.strip()
            except:
                sending_time = 'NO'

            try:
                arrival_time = flight_date[4].text.strip()
            except:
                arrival_time = 'NO'

            try:
                bus = flight_date[5].text.strip()
            except:
                bus = 'NO'

            try:
                money = flight_date[6].text.rstrip('\n')
            except:
                money = 'NO'

            list_bus.append((flight_nember, beginning_route, end_route, sending_time, arrival_time, bus, money))
    with open('chek.txt', "a", encoding="utf-8") as file:
        for line in list_bus:
            file.write(f"{line}\n")


# with open("index.html", "w", encoding='utf-8') as file:
#     for line in soup:
#         file.write(line)
# link_a_table = soup.find("table", class_="views-table cols-9").find_all("a", rel='nofollow')
# for url_a in link_a_table:
#     persons_avto_url = url_a.get("href")
#     persons_url.append(f"{persons_avto_url}{url_a}")

# with open("bus_a.txt", "a", encoding="utf-8") as file:
#     for line in persons_url:
#         file.write(f"{line}\n")


get_url(URL)
