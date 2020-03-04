# MongoDB & Flask

#Dependencies & setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

#Flask setup
app=Flask(__name__)

#PyMongo setup
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

#Flask route to q MongoDB & pass Mars data into HTML template: index.html to display
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#Scrape route to import `scrape_mars.py` script & call `scrape` function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

#define main
if __name__ == "__main__":
    app.run()