import requests
from bs4 import BeautifulSoup
import json
import sqlite3

# names = ['baghdad', 'mesan', 'mohana', 'nainoa', 'najaf',
#          'basra', 'karkok', 'karbala', 'thekar', 'hela', 'dhoke']


def scrape():

    weather = {}
    cities = ['https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A8%D8%BA%D8%AF%D8%A7%D8%AF/54/iq?ref=all-locations-page',
              'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D9%85%D9%8A%D8%B3%D8%A7%D9%86/201033294/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D9%85%D8%AB%D9%86%D9%89-/201033251/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D9%86%D9%8A%D9%86%D9%88%D9%89/201033252/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D9%86%D8%AC%D9%81/190/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D8%A8%D8%B5%D8%B1%D8%A9/100/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D9%83%D8%B1%D9%83%D9%88%D9%83/250/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D9%83%D8%B1%D8%A8%D9%84%D8%A7%D8%A1/171/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%B0%D9%8A-%D9%82%D8%A7%D8%B1-/201033291/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D8%AD%D9%84%D8%A9/148/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%AF%D9%87%D9%88%D9%83/230/iq?ref=all-locations-page', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A3%D8%B1%D8%A8%D9%8A%D9%84/241/iq', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D8%B3%D9%84%D9%8A%D9%85%D8%A7%D9%86%D9%8A%D8%A9/258/iq', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%B5%D9%84%D8%A7%D8%AD-%D8%A7%D9%84%D8%AF%D9%8A%D9%86/244/iq', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%AF%D9%8A%D8%A7%D9%84%D9%8A/201033292/iq', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D9%88%D8%A7%D8%B3%D8%B7/107/iq', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D8%AF%D9%8A%D9%88%D8%A7%D9%86%D9%8A%D8%A9/134/iq', 'https://www.arabiaweather.com/ar/%D8%AA%D9%88%D9%82%D8%B9%D8%A7%D8%AA-%D8%A7%D9%84%D8%B7%D9%82%D8%B3/%D8%A7%D9%84%D8%A3%D9%86%D8%A8%D8%A7%D8%B1/201032583/iq']
    names = ['baghdad', 'mesan', 'mothana', 'nainoa', 'najaf',
             'basra', 'karkok', 'karbala', 'thekar', 'hela', 'dhoke', 'erbeel', 'alsulamaneea', 'slah aldeen', 'deala', 'wast', 'dewanea', 'anbar']
    for z in zip(cities, names):

        source = requests.get(f'{z[0]}').text

        soup = BeautifulSoup(source, 'lxml')

        a = soup.find('div', id="homepage-weather-widget-desktop")
        b = a.find('div', class_="homepage-day-card-rows")

        c = b.find('div', class_="homepage-day-card-row active")
        d = c.find('div', class_="temp-container ltr").text

        e = c.findNextSibling()
        f = e.find('div', class_="temp-container ltr").text

        g = e.findNextSibling()
        h = g.find('div', class_="temp-container ltr").text

        i = g.findNextSibling()
        j = i.find('div', class_="temp-container ltr").text

        k = i.findNextSibling()
        l = k.find('div', class_="temp-container ltr").text
        dec = {"first": d, "second": f, "therd": h, "forth": j, "fifth": l}
        weather[z[1]] = dec
        if z[1] == 'anbar':
            # print(json.dumps(weather))
            return weather

        # suber_weather =
        # print(suber_weather)
        # return json.dumps(dec)

# with open('D:\\PYTHON_PROJECTS\\Flask for adobe\\flask\\json.json', 'w') as jsons:
#     jsons.write(scrape())
#     jsons.close()
