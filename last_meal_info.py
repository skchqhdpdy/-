from lets_common_log import logUtils as log
import requests
from main import regex

def last_meal():
    URL = "https://open.neis.go.kr/portal/data/sheet/searchSheetData.do?page=1"

    HEADER = {
        "User-Agent": "python requests | https://github.com/skchqhdpdy/seongpo-highschool-meal/blob/main/last_meal_info.py",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    BODY = "rows=1&infId=OPEN17320190722180924242823&infSeq=1&ATPT_OFCDC_SC_CODE=J10&SCHUL_NM=%EC%84%B1%ED%8F%AC&MMEAL_SC_NM=&MLSV_YMD=&MLSV_YMD="

    r = requests.post(url=URL, headers=HEADER, data=BODY)
    r = r.json()

    last_meal = regex(r["data"][0]["DDISH_NM"])
    last_date = r["data"][0]["MLSV_YMD"]
    last_update = r["data"][0]["LOAD_DTM"]
    log.info(last_meal)
    log.info(last_date)
    log.info(last_update)

    return {"last_meal": last_meal, "last_date": last_date, "last_update": last_update}