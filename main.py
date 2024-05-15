from lets_common_log import logUtils as log
import config
import requests
import time
import json
import sys
#import dico
from last_meal_info import last_meal
from rgx import regex

#This file is responsible for running the web server and (mostly nothing else)
from flask import Flask, render_template, session, redirect, url_for, request, send_from_directory, jsonify, Response
from colorama import Fore, init
import os
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

conf = config.config("config.ini")
if not conf.checkConfig():
    conf.generateDefaultConfig()
    sys.exit("config.ini 재설정")

HOST = conf.config["server"]["host"]
PORT = conf.config["server"]["port"]
DEBUG = True if conf.config["server"]["debug"] == "True" else False
apikey = conf.config["api"]["apikey"]

def get_menu(date):

    """ try:
        date = int(date) + int(inputDate)
        log.info(f"{inputDate}일 뒤 데이터 조회")
    except:
        log.info("당일 데이터 조회") """

    log.info(f"date = {date}")

    header = {
        "User-Agent": "python requests | https://github.com/skchqhdpdy/seongpo-highschool-meal/blob/main/main.py",
    }

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?key={apikey}&type=json&pIndex=1&pSize=1&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7530765&MLSV_FROM_YMD={date}"
    try:
        response = requests.get(url, headers=header)
        result = response.json()
        meal_date = result["mealServiceDietInfo"][1]["row"][0]["MLSV_YMD"]
        menu = result["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        menu = regex(menu)
        log.debug(menu)
    except:
        meal_date = ""
        menu = result
        log.debug(url)
        log.debug(result)
    
    return {"date": meal_date, "menu": menu}


app = Flask(__name__)
app.secret_key = os.urandom(24) #encrypts the session cookie

@app.route("/")
def home():
    return render_template("index.html", title="메인 페이지")

@app.route("/discordbot")
def discordbot():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=1109007342458114108&permissions=8&scope=bot+applications.commands")

@app.route("/email")
def email():
    return render_template("email.html", title="Email")

@app.route("/meal")
def meal():
    #inputDate = input("오늘 기준 으로 +, - 입력 : ")
    dateNow = time.strftime('%Y%m%d', time.localtime(time.time()))

    date = request.args.get('date')
    isjson = request.args.get('isjson')
    if date is None or date == "":
        #date = dateNow
        log.info(f"date Default set {dateNow} & Redirect")
        return redirect(url_for("meal", date=dateNow, isjson=isjson))

    if isjson is None or isjson == "":
        return redirect(url_for("meal", date=date, isjson=0))
    elif isjson == "1" or isjson == 1:
        isjson = 1
    else:
        isjson = 0

    menu = get_menu(date)

    if menu["date"] == "" and type(menu["menu"]) is dict:
        NoData = last_meal()
    else:
        NoData = False

    if request.headers.get("User-Agent") == "meal discord":
        return jsonify(menu)
    elif isjson == 1:
        return Response(json.dumps({"meal_info": menu, "last_meal_info": NoData}, indent=2, ensure_ascii=False), content_type='application/json')
    else:
        return render_template("meal.html", title="오늘의 급식", txt=json.dumps(menu, ensure_ascii=False), ND=NoData)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
