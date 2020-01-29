import requests
import csv
from bs4 import BeautifulSoup
import dateutil.parser as parser

## Funktion til at skrabe hvert enkelt objekt i itemlist
def item_scraper(item):
    title = item.find(class_="title").get_text().strip()
    subtitle = item.find(class_="dek").get_text().strip()
    date = item.find(class_="date").get_text().strip()
    link = item.find("a")["href"].strip()
    return {"title": title,
            "subtitle": subtitle,
            "date": parser.parse(date, ignoretz=True),
            "link": "https://www.cbsnews.com"+link}

## Funktion til at skrabe én URL
def URL_scraper(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="media-list content-list result-list")
    itemlist = results.find_all("li")
    scraped_itemlist = []
    for item in itemlist:
        scraped_itemlist.append(item_scraper(item))
    return scraped_itemlist

## Funktion til eksport som CSV
def CSV_writer(scraped_itemlist):
    with open("temp.csv", "a+") as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=["date","title", "subtitle", "link"])
        for item in scraped_itemlist:
            writer.writerow(item)
        outfile.close()

## Sammensat funktion. Tager args "keyword" som er emnet, du ønsker at søge på samt "start" og "end" som hhv. angiver første og sidste side af resultater, der skal medtages i skrabet
def CBS_scraper(keyword, start, end):
    for i in range(start, end):
        URL = "https://www.cbsnews.com/search/?q={keyword}&p={pagenumber}".format(keyword = keyword, pagenumber = i)
        CSV_writer(URL_scraper(URL))

CBS_scraper("Iraq", 3600, 4100)
