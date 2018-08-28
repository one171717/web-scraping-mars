# Dependencies
from flask import Flask, jsonify, render_template, request
import pymongo
import Mars_scrape

app = Flask(__name__)

conn = "mongodb://admin:password@ds147265.mlab.com:47265/heroku_jggh81rx"
client = pymongo.MongoClient(conn)
db = client.heroku_jggh81rx
mars = db.mars

@app.route("/")
def index():
    mars_info = db.mars.find_one()

    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    mars_info = db.mars
    mars_data = mars_info.scrape()
    mars_info.update(
        {},
        mars_data,
        upsert = True
    )

    return index()

if __name__ == "__main__":
    app.run(debug=False)

