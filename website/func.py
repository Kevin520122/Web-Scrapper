from bs4 import BeautifulSoup as soup
import string
import requests
import wikipedia
import json

def formatStr(content):
    capWords = string.capwords(content)
    wordList = capWords.split()
    content = "_".join(wordList)
    return content


def access_car_wiki(brand):
    wikiURL = "https://en.wikipedia.org/wiki/"+brand
    data = requests.get(wikiURL)
    #Returns an array containing all the html code
    contents = soup(data.content, "html.parser")
    #Returns an array containing infobox html code
    info = contents("td", {"class":"infobox-image"})[0]
    #Find all image tag in html, return type: array
    img = info.find_all("img")[0]
    return img


def write_cars_json(brand, img):
    cars = {}
    cars["path"] = "C:\OSU\CS361\WebScrapper\car.json"
    cars["img"] = "https:"+img["src"]
    cars["brand"] = brand

    json_car = json.dumps(cars, indent=len(cars))
    with open("car.json", "w") as f:
        f.write(json_car)

    return cars


def write_summary_json(context):
    summary = {}
    #Fulfill the summary of specific content
    summary["context"] = context
    summary["path"] = "C:\OSU\CS361\WebScrapper\input.json"

    #Converts info to json format
    json_summary = json.dumps(summary, indent=len(summary))

    #Transfer paragraphs to Michille
    with open("summary.json", "w") as f:
        f.write(json_summary)

    return summary

def update_summary(summary, language):
    summary.update({"language": language})
    json_updated_summary = json.dumps(summary, indent=len(summary))
    with open("summary.json", "w") as f:
        f.write(json_updated_summary)
    return summary

def write_image_json(img):
    images = {}
    images["links"] = img
    images["path"] = "C:\OSU\CS361\WebScrapper\image.json"

        
    #Converts info to json format
        
        
    json_image = json.dumps(images, indent=len(images))
        
    #Transfer images
    with open("image.json", "w") as f:
        f.write(json_image)

    return images




