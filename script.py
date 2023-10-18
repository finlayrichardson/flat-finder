import requests
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime
from utils import send_email, next_steps


def notify(key, email):
    match key:
        case 'alba':
            agent = "Alba"
            link = "https://www.albastandrews.co.uk/properties/"
        case 'bradburne':
            agent = "Bradburne & Co"
            link = "https://www.bradburne.co.uk/search-results-to-let"
        case 'inchdairnie':
            agent = "Inchdairnie"
            link = "https://www.standrewsletting.com/for-rent/?per_page=12&property_type=rental_property_property&address&area=St%20Andrews&price_min&price_max&bedrooms_min=2&hide_under_offer=0"
        case 'rollos':
            agent = "Rollos"
            link = "https://www.rolloslettings.co.uk/letting-agents/lettings/"
        case 'dja':
            agent = "DJ Alexander"
            link = "https://www.djalexander.co.uk/property/to-rent/in-ky16/2-and-more-bedrooms/"
        case 'gumtree':
            agent = "Gumtree"
            link = "https://www.gumtree.com/property-to-rent/st-andrews-fife"
    subject = f"A new letting has been advertised with {agent}!"
    body = f"Check {link} to see if it is to your liking.\n The next steps are:\n\n"
    for step in next_steps[key]:
        body += f"{step}\n"
    send_email(subject, body, [email])


def write_number(bedroom_num, key, number):
    f = open("numbers.json", 'r')
    data = json.loads(f.read())
    f.close()
    if data[str(bedroom_num)][key] < number:
        if bedroom_num == 2:
            email = ""
        elif bedroom_num == 3:
            email = ""
        time = datetime.now().strftime("%H:%M")
        if time != "10:30":
            notify(key, email)
    data[str(bedroom_num)][key] = number
    f = open("numbers.json", "w")
    f.write(json.dumps(data))


def check_alba():
    url = "https://www.albastandrews.co.uk/properties/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    number = len(soup.find_all("div", {"id": re.compile("(post-...)")}))
    write_number(2, "alba", number)
    write_number(3, "alba", number)


def check_bradburne(bedroom_num):
    url = "https://www.bradburne.co.uk/search-results-to-let"
    data = {'area': 'St. Andrews', 'type': '', 'bedrooms': str(bedroom_num),
            'price_min': '', 'price_max': '', 'submit': 'Search'}
    response = requests.post(url, data)
    soup = BeautifulSoup(response.text, 'html.parser')
    number = len(soup.find_all("div", {"class": "price_all_properties"}))
    write_number(bedroom_num, "bradburne", number)


def check_inchdairnie(bedroom_num):
    url = f"https://www.standrewsletting.com/for-rent/?per_page=12&property_type=rental_property_property&address&area=St%20Andrews&price_min&price_max&bedrooms_min={bedroom_num}&hide_under_offer=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    number = int(
        soup.find("p", {"class": "properties-found-count"}).find("span").string)
    write_number(bedroom_num, "inchdairnie", number)


def check_rollos(bedroom_num):
    url = "https://www.rolloslettings.co.uk/wp-content/plugins/Property/ajax/"
    data = {'page': '1',
            'search_filter': '',
            'selected_bedrooms[]': str(bedroom_num),
            'selected_sort_choice': 'Price High - Low',
            'selected_min_price': '',
            'selected_max_price': ''}
    response = requests.post(url, data)
    data = json.loads(response.text)
    number = len(data['properties'])
    write_number(bedroom_num, "rollos", number)


def check_dja(bedroom_num):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://www.djalexander.co.uk',
        'Referer': 'https://www.djalexander.co.uk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = '{"requests":[{"indexName":"prod_properties","params":"facets=%5B%22price%22%2C%22bedroom%22%2C%22building%22%2C%22mustInclude%22%2C%22furnishing%22%5D&filters=publish%3Atrue%20AND%20search_type%3Alettings%20AND%20department%3Aresidential%20AND%20(status%3A%22To%20Let%22%20OR%20status%3A%22Let%22)&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=20&maxValuesPerFacet=10&numericFilters=%5B%22bedroom%3E%3D' + str(
        bedroom_num) + '%22%5D&page=0&query=%22ky16%22&tagFilters="},{"indexName":"prod_properties","params":"analytics=false&clickAnalytics=false&facets=bedroom&filters=publish%3Atrue%20AND%20search_type%3Alettings%20AND%20department%3Aresidential%20AND%20(status%3A%22To%20Let%22%20OR%20status%3A%22Let%22)&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=10&page=0&query=%22ky16%22"}]}'

    response = requests.post(
        'https://3ax0bnlm21-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.11.3)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(6.39.0)&x-algolia-api-key=85b8fda7e815b64198bbe481b9557e6d&x-algolia-application-id=3AX0BNLM21',
        headers=headers,
        data=data,
    )

    data = json.loads(response.text)
    number = data['results'][1]['nbHits']
    write_number(bedroom_num, "dja", number)


def check_gumtree(bedroom_num):
    headers = {
        'authority': 'www.gumtree.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'referer': 'https://www.gumtree.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://www.gumtree.com/property-to-rent/st-andrews-fife', headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    header = soup.find("h2", {"class": "ads-count"}).string
    number = int(re.findall(r'\d+', header)[0])
    write_number(2, "gumtree", number)
    write_number(3, "gumtree", number)


if __name__ == "__main__":
    print("[*] Checking Alba for properties...")
    check_alba()
    print("[*] Checking Bradburne & Co for properties...")
    check_bradburne(2)
    check_bradburne(3)
    print("[*] Checking Inchdairnie for properties...")
    check_inchdairnie(2)
    check_inchdairnie(3)
    print("[*] Checking Rollos for properties...")
    check_rollos(2)
    check_rollos(3)
    print("[*] Checking DJ Alexander for properties...")
    check_dja(2)
    check_dja(3)
    print("[*] Checking Gumtree for properties...")
    check_gumtree(2)
    check_gumtree(3)
