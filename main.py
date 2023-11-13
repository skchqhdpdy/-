from lets_common_log import logUtils as log
import config
import requests
import time
import json
import sys
#import dico

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

""" def regex_old(menu):
    #필터링 ?
    menu += "<br/>"
    log.debug(menu) 
    
    arr = []
    txt = ""
    for i in menu:
        #if i != " ":
        #log.error(i != " " or i != "<" or i != "b" or i != "r" or i != "/" or i != ">")
        if i == "<" or i == "b" or i == "r" or i == "/" or i == ">":
            if i == ">":
                arr.append(txt)
                txt = ""
        #elif i == "(" or i == "." or i == ")" or i.isdigit():
        #    txt += i
        else:
            txt += i
    return arr """

def regex(menu):
    regexedMenu = []
    while True:
        if menu.find("<br/>") == -1 and menu == "":
            return regexedMenu
        else:
            num = menu.find("<br/>")
            if num != -1:
                regexedMenu.append(menu[:num])
                menu = menu[num + 5:]
            else:
                regexedMenu.append(menu)
                menu = ""

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
    #inputDate = input("오늘 기준 으로 +, - 입력 : ")
    dateNow = time.strftime('%Y%m%d', time.localtime(time.time()))

    date = request.args.get('date')
    isjson = request.args.get('isjson')
    if date is None or date == "":
        #date = dateNow
        log.info(f"date Default set {dateNow} & Redirect")
        return redirect(url_for("home", date=dateNow, isjson=isjson))

    if isjson is None or isjson == "":
        return redirect(url_for("home", date=date, isjson=0))
    elif isjson == "1" or isjson == 1:
        isjson = 1
    else:
        isjson = 0

    menu = get_menu(date)

    if request.headers.get("User-Agent") == "meal discord":
        return jsonify(menu)
    elif isjson == 1:
        return Response(json.dumps(menu, indent=2, ensure_ascii=False), content_type='application/json')
    else:
        return render_template("main.html", title="오늘의 급식", txt=json.dumps(menu, ensure_ascii=False))

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
