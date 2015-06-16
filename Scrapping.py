# coding=utf-8
from bs4 import BeautifulSoup
import lxml
import csv
import urllib2

outfile = 'bbc_world.csv'

with open(outfile, 'wb') as csvfile:
    fieldnames = ['title','url','desc','pubdate','lat','lng','country']
    writer = csv.DictWriter(csvfile, delimiter=',',fieldnames=fieldnames)

    writer.writeheader()
    r  = urllib2.urlopen("http://api.geonames.org/rssToGeoRSS?feedUrl=http://news.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml&username=icrcopassist")
    data = r.read()

    soup = BeautifulSoup(data)
    #soup_list = data.findChildren()

    item2 = soup.find_all("item")
   
    for i in item2:
        itm =str(i)
        soup3 = BeautifulSoup(itm)
        title  = soup3.find('title')
        url = soup3.find('guid')
        desc = soup3.find('description')
        pubdate = soup3.find('pubdate')
        lat  = soup3.find('geo:lat')
        lng= soup3.find('geo:long')
 
	#Cleaning the result
        title_clean = str(title).replace('<title>','').replace('</title>','').replace('[','').replace(']','').replace(',','')
        url_clean = str(url).replace('<guid ispermalink="false">','').replace('</guid>','').replace('[','').replace(']','')
        desc_clean =str(desc).replace('<description>','').replace('</description>','').replace('[','').replace(']','').replace('"','').replace(',','')
        pubdate_clean = str(pubdate).replace('<pubdate>','').replace('</pubdate>','').replace('[','').replace(']','').replace(',','')
        lat_clean = str(lat).replace('<geo:lat>','').replace('</geo:lat>','').replace('[','').replace(']','')
        lng_clean = str(lng).replace('<geo:long>','').replace('</geo:long>','').replace('[','').replace(']','')

        #Write the code to get the country here !
        nearByPlace = urllib2.urlopen("http://ws.geonames.org/findNearbyPlaceName?lat="+lat_clean+"&lng="+lng_clean+"&username=icrcopassist")
        placeResult=nearByPlace.read();
        soupresult=BeautifulSoup(placeResult)
        country = soupresult.find_all("countryname")
        print country
        country_clean = str(country).replace('<countryname>','').replace('</countryname>','').replace('[','').replace(']','')

	#For each row:
        writer.writerow({'desc':desc,'title':title_clean,'url':url_clean,'desc':desc_clean,'pubdate':pubdate_clean,'lat':lat_clean,'lng':lng_clean,'country':country_clean})
