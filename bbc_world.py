# coding=utf-8
from bs4 import BeautifulSoup
import lxml
import csv
import requests

outfile = 'bbc_world.csv'

with open(outfile, 'wb') as csvfile:
    fieldnames = ['title','url','desc','pubdate','lat','lng']
    writer = csv.DictWriter(csvfile, delimiter=',',fieldnames=fieldnames)

    writer.writeheader()
    r  = requests.get("http://api.geonames.org/rssToGeoRSS?feedUrl=http://news.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml&username=icrcopassist")
    data = r.text

    soup = BeautifulSoup(r.content, ['lxml', 'xml'])
    soup_list = soup.findChildren()

    #Getting a clean file out off the rss mess
    for i, element in enumerate(soup):
        elmt_item = element.findChildren()
        if len(elmt_item) >1:
            # a clean file !
            itm1 = elmt_item[0]

	#Working now on this clean file
	itm = str(itm1)
    soup2 = BeautifulSoup(itm)
    item2 = soup2.find_all("item")

    for i in item2:
        info = str(i)
        soup3 = BeautifulSoup(info)

        title  = soup3.find_all('title')
        url = soup3.find_all('guid')
        desc = soup3.find_all('description')
        pubdate = soup3.find_all('pubdate')
        lat  = soup3.find_all('geo:lat')
        lng = soup3.find_all('geo:long')

		#Cleaning the result
        title_clean = str(title).replace('<title>','').replace('</title>','').replace('[','').replace(']','').replace(',','')
        url_clean = str(url).replace('<guid ispermalink="false">','').replace('</guid>','').replace('[','').replace(']','')
        desc_clean =str(desc).replace('<description>','').replace('</description>','').replace('[','').replace(']','').replace('"','').replace(',','')
        pubdate_clean = str(pubdate).replace('<pubdate>','').replace('</pubdate>','').replace('[','').replace(']','').replace(',','')
        lat_clean = str(lat).replace('<geo:lat>','').replace('</geo:lat>','').replace('[','').replace(']','')
        lng_clean = str(lng).replace('<geo:long>','').replace('</geo:long>','').replace('[','').replace(']','')

        #Write the code to get the country here !

		#For each row:
        writer.writerow({'desc':desc,'title':title_clean,'url':url_clean,'desc':desc_clean,'pubdate':pubdate_clean,'lat':lat_clean,'lng':lng_clean})
