import urllib.request
import datetime
import os
import csv
import pycountry

from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    currentRows = []
    todaysDate = datetime.datetime.now().strftime("%Y-%m-%d")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
    fileName = "vaccinations.csv"
    urllib.request.urlretrieve(url, fileName)
    with open('vaccinations.csv') as csvfile:
        vaccreader = list(csv.DictReader(csvfile))
        firstHeader = vaccreader[0]["location"]
        latestDate = "";
        for i in range(len(vaccreader)):
            if (i > 0):
                if (vaccreader[i]["location"] != vaccreader[i-1]["location"]):
                    country = pycountry.countries.get(alpha_3=vaccreader[i-1]["iso_code"])
                    if (country != None):
                        vaccreader[i-1]["alpha_2"] = country.alpha_2
                    else:
                        continue;
                    vaccreader[i-1]["total_vaccinations"] = formatNumbers(vaccreader, i, "total_vaccinations")
                    vaccreader[i-1]["daily_vaccinations"] = formatNumbers(vaccreader, i, "daily_vaccinations")

                    currentRows.append(vaccreader[i-1])
    return render_template("index.html", data=currentRows)

def formatNumbers(reader, i, k):
    if (reader[i-1][k] != ""):
        return format(int(reader[i-1][k]), ",d")
    else:
        return 0
