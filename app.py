from flask import Flask, render_template, request, url_for, send_file, flash, redirect, make_response
import pickle
import numpy as np
import os
import json
import termcolor
import smtplib
import pickle
from werkzeug.utils import secure_filename
from prediction import check
import requests

app = Flask(__name__)



# For Coronavirus
with open("Coronavirus_logistic", "rb") as f:
    logisticRegression = pickle.load(f)





@app.route("/")
@app.route("/home")
def Homepage():
    return render_template("Homepage.html", feedback="False")

@app.route("/CoronavirusPrediction", methods=["POST", "GET"])
def Coronavirus():
    if request.method == "POST":
        # print(request.form)
        temperature = float(request.form.get("temperature").strip())
        age = int(request.form.get("age"))
        cough = int(request.form.get("cough"))
        cold = int(request.form.get("cold"))
        sore_throat = int(request.form.get("sore_throat"))
        body_pain = int(request.form.get("body_pain"))
        fatigue = int(request.form.get("fatigue"))
        headache = int(request.form.get("headache"))
        diarrhea = int(request.form.get("diarrhea"))
        difficult_breathing = int(request.form.get("difficult_breathing"))
        travelled14 = int(request.form.get("travelled14"))
        travel_covid = int(request.form.get("travel_covid"))
        covid_contact = int(request.form.get("covid_contact"))

        age = 2 if (age > 50 or age < 10) else 0
        temperature = 1 if temperature > 98 else 0
        difficult_breathing = 2 if difficult_breathing else 0
        travelled14 = 3 if travelled14 else 0
        travel_covid = 3 if travel_covid else 0
        covid_contact = 3 if covid_contact else 0

        model_inputs = [cough, cold, diarrhea,
                        sore_throat, body_pain, headache, temperature, difficult_breathing, fatigue, travelled14, travel_covid, covid_contact, age]
        prediction = logisticRegression.predict([model_inputs])[0]
     
        if prediction:
            return render_template("Infected.htm", disease="Coronavirus")
        else:
            return render_template("NonInfected.htm")

    return render_template("Coronavirus.htm", title="Coronavirus Prediction", navTitle="COVID-19 Detector", headText="Coronavirus Probability Detector", ImagePath="/static/VirusImage.png")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("PageNotFound.html")


@app.route("/about")
def About():
    return render_template("About.html")


@app.route("/infected")
def Infected():
    return render_template("Infected.htm", disease="Nothing")


@app.route("/noninfected")
def NonInfected():
    return render_template("NonInfected.htm")


@app.route("/xray")
def xRayPrediction():
    return render_template("xray.html")

@app.route("/report",methods=["GET","POST"])
def report():
    file = request.files['myfile']
    filename = secure_filename(file.filename)
    if file.filename != '':
            file.save("x-ray/{}".format(file.filename))
    prediction=check("x-ray/{}".format(file.filename))
    if prediction[0][0]<prediction[0][1]:
        report="Positive"
    else:
        report="Negative"
    details={
        "name":request.form.get("name"),
        "gender":request.form.get("gender"),
        "email":request.form.get("email"),
        "phone":request.form.get("phone"),
        "dist":request.form.get("dist"),
        "trival_history":request.form.get("trival_history"),
        "addres":request.form.get("addres"),
        "test":report
    }
    message="{} had a Covid-19 Test and report of test was {} He had the trival history to {}".format(details["name"],details["test"],details["trival_history"])
    contact="Contact Details \n {} \n {} \n {}".format(details["phone"],details["email"],details["addres"])
     
   # mail.send_message('Quick Covid-19 Test Report',
                          #sender=details["email"],
                          #recipients=['thorataniket777@gmail.com'],
                          #body=message + "\n\n" + contact
                          #)
    print(details)
    return render_template("report.html",details=details)


@app.route("/bedsforcovid")
def bedsforcovid():
    URL = "https://api.rootnet.in/covid19-in/hospitals/beds"
    r = requests.get(url = URL)
    data = r.json()
    data=data["data"]["regional"]
    return render_template("beads.html",data=data)



@app.route("/covidscases")
def covidscases():
    URL = "https://api.rootnet.in/covid19-in/stats/latest"
    r = requests.get(url = URL)
    data = r.json()
    data=data["data"]["regional"]
    return render_template("caseCount.html",data=data)


if __name__ == '__main__':
    app.run(debug=True)
