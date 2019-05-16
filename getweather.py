import requests
import geocoder
import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

api_key = "759446d9a929bc4c607a3ec3f24084ef"
api ="http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang={lang}&APPID={key}"

k2c = lambda k: k- 273.15

t = datetime.now

def get_lat_lon(location):
    geo_address = location
    g = geocoder.osm(geo_address)
    #print(g.latlng)
    return(g.latlng)

def get_weather(location): # main ------------------------------------
    print(t().strftime("[ %H:%M:%S ] "),"<weather>start")
    lat,lon = get_lat_lon(location) #緯度と経度の取得
    url = api.format(lat=lat,lon=lon,lang="ja",key=api_key) #APIのアクセス先
    r = requests.get(url) #APIの結果
    weather_data = json.loads(r.text) #結果をjsonでパース
    return(print_weather(weather_data))
    #json.dump(weather_data,open("wdata.txt","w"),indent=4,sort_keys=True)

def print_weather(data):
    text = '```'
    text = text + "Location:" + data["city"]["name"] +"\n"
    count=1
    for wlist in data["list"]:
        time = datetime.fromtimestamp(int(wlist["dt"]))
        time = str(time)[5:16]
        #print("time=",time,"raw=",wlist["dt_txt"])
        if count==1 or wlist["dt_txt"][11:13]=="15":
            text = text + time
            #text = text + wlist["dt_txt"][5:16]
        else:
            dt = time[6:]
            text = text + "      " + dt
        tmp = str(Decimal(k2c(wlist["main"]["temp"])).quantize(Decimal(0),rounding="ROUND_HALF_UP"))
        text = text +" / "+tmp+"℃ , "+ wlist["weather"][0]["description"] + "\n"
        count += 1
    
    text = text + '```'
    print(t().strftime("[ %H:%M:%S ] "),"<weather>finished")
    return(text)
#print(get_weather("asahikawa"))