from flask import Flask,redirect, url_for, render_template,request, session, Blueprint
from bs4 import BeautifulSoup as soup
import string
import requests
import wikipedia
import json
from pprint import pprint
from website import func
import PIL.Image


from wikipedia.wikipedia import summary


#from transformer into translate

views = Blueprint('views', __name__)
#Global variables

infobox={}
images={}




#@views.route('/')
@views.route("/", methods=["POST", "GET"])
def getInput():
    if request.method == 'POST':
        #Retrieve the seraching target
        aim = request.form['content']
        section = request.form["section"]
        session["section"] = section
        #Store it in session
        session["content"] = aim
        return redirect(url_for("views.scrape"))
    else:
        return render_template("search.html")
    


#Home page
@views.route("/home")
def displayHome():
    return render_template("home.html")

#Car service
@views.route("/car", methods=["POST", "GET"])
def car():
    if request.method == 'POST':
        #Store car brand in the session
        session["car"] = request.form["car"]
        #Go to scrape_car
        return redirect(url_for("views.scrape_car"))
    else:
        return render_template("car.html")

#Scraping car images
@views.route("/scrape_car", methods=["POST", "GET"])
def scrape_car():
    cars = {}
    if request.method == "POST":
        pass
    else:
        if "car" in session:
            #Retrieve the car brand
            brand = session["car"]
        else:
            return redirect(url_for("car"))


        #Format the input
        brand = func.formatStr(brand)
        #Retrieve image tag from infobox html 
        img = func.access_car_wiki(brand)

        brand = func.formatStr(brand)
        wikiURL = "https://en.wikipedia.org/wiki/"+brand
        data = requests.get(wikiURL)
        #Returns an array containing all the html code
        contents = soup(data.content, "html.parser")
        #Returns an array containing infobox html code
        info = contents("td", {"class":"infobox-image"})[0]
        #print(info)
        img = info.find_all("img")[0]
    

        cars["path"] = "C:\OSU\CS361\WebScrapper\car.json"
        cars["img"] = "https:"+img["src"]
        cars["brand"] = brand

        json_car = json.dumps(cars, indent=len(cars))
        with open("car.json", "w") as f:
            f.write(json_car)


        cars = func.write_cars_json(brand, img)
        return render_template("scrape_car.html", name=brand, img=cars["img"])
        



@views.route("/scrape", methods=["POST", "GET"])
def scrape():
    summary = {}
    if request.method == 'POST':
        #Retrieve the language from the user's request
        language = request.form['language']
        #Store the language at the session temporarily
        session["language"] = language
        #Update the summary json file by adding language
        summary = func.update_summary(summary, language)
    
        return render_template("scrape.html", part = session["section"], summary=summary["context"], content=infobox, language=language)

    else:
        content = ""
        if "content" in session and "section" in session:
            content = session["content"]
            section = session["section"]
        else:
            return redirect(url_for("getInput"))
        
        #Get all the content from Wikipedia
        search_result = wikipedia.page(wikipedia.search(content)[0])
        #Retrieve the scraping summary
        summary = func.write_summary_json(search_result.summary)
        #Retrieve the scraping images
        images = func.write_image_json(search_result.images)

        return render_template("scrape.html",   part=section, summary=summary["context"], images=images["links"])



@views.route("/transform", methods=["POST", "GET"])
def transform():
    if request.method == "POST":
        if "language" in session:
            language = session["language"]
        
            #Translate via my partner's service in the backend
            #Support other language
            with open("output.txt", "r", encoding="utf8") as f:
                #Retrieve scraping data(dictionary)
                translated_content = f.read()
            #Go to a separate web page to display translated content
            return render_template("transform.html", language=language,  content=translated_content)
        else:
            return redirect(url_for("views.scrape"))


@views.route("/carImage", methods=["POST", "GET"])
def showImage():
    if request.method == "POST":

        imgSrc = "sijun_service/pic/CONTOUR.jpg"
        carImage = PIL.Image.open(imgSrc)
        carImage.show()
        carImage.save("modified.jpg")
        return render_template("carImage.html")

    else:
        return redirect(url_for("views.scrape_car"))



