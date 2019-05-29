import folium
import os
from selenium import webdriver
import PIL.Image

def saveMap(r, c, name):
    map_osm = folium.Map(location=[r, c], zoom_start=15)
    folium.Marker([r, c], popup=name).add_to(map_osm)
    map_osm.save('osm.html')

    fn = 'osm.html'
    tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=fn)
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(tmpurl)
    browser.save_screenshot('map.png')




