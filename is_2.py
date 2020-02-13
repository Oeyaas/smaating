import requests
import csv
import re
from bs4 import BeautifulSoup

def GetRecipe(URL):
        #Parsing requested page
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        #Finding the recipe-row
        crafting_box = soup.find(class_="tabbertab", title=re.compile("Normal mode"))
        recipe_row = crafting_box.find(class_="infobox-vrow-value")
        recipe_icons = recipe_row.find_all(class_="factorio-icon")

        #Defining output name and output multiplier
        output_name = recipe_icons[-1].find("a")["href"].strip().replace("/","")
        output_mult = float(recipe_icons[-1].find(class_="factorio-icon-text").get_text())

        #Preparing empty recipe for the loOoOooOp
        recipe = {"input":{}, "name":output_name, "mult":output_mult}

        #Iterating over input
        for icon in recipe_icons[:-1]:
            input_name = icon.find("a")["href"].strip().replace("/","")  #Fungerer et parset tag som et dict?
            input_number = float(icon.find(class_="factorio-icon-text").get_text())
            recipe["input"][input_name] = input_number

        return recipe

def NavScraper(URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        #List of links to pass to GetRecipe
        link_list = []

        #Finding all links in tables with class "navbox-inner"
        navboxes = soup.find_all(class_="navbox-inner")
        for navbox in navboxes:
            for link in navbox.find_all("a"):
                try:
                    if link["href"] not in link_list:
                        link_list.append(link["href"])
                    else:
                        print("error: duplicate entry")
                except:
                    print("error: bad link")

        #Passing all links to GetRecipe
        print("Writing")
        with open("temp.csv", "a+") as outfile:
            writer = csv.DictWriter(
                outfile,
                fieldnames=["mult","name", "input"])
            for link in link_list:
                try:
                    writer.writerow(GetRecipe("https://wiki.factorio.com{link}".format(link=link)))
                    print("succes: line {cur} out of {tot} scraped".format(
                            cur=link_list.index(link),
                            tot=len(link_list)))
                except:
                    print("error: when trying to scrape: ", link)
            outfile.close()




NavScraper("https://wiki.factorio.com/Factorio:Navigation")
