#!usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Surveillance d'un flux RSS contenant le programme du jour de la TNT.
'''

import os
from datetime import date
import time
from urllib.request import urlopen
import xml.etree.ElementTree as ET

MOTS_CLES = ["sport", "auto", "informatique", "finance", "film"]

CHAINES_NON_RECUES = ["Canal+", "RTL 9"]

URL_RSS = 'http://webnext.fr/epg_cache/programme-tv-rss_'+str(date.today())+'.xml'
contenu = urlopen(URL_RSS).read().decode('utf-8')
while contenu.find("<title>Webnext.fr - Programme Tv rss xml</title>") == -1:
	PAGE_GENERANT_LE_RSS = urlopen("http://webnext.fr/programme-tv-rss")
	time.sleep(3)
	contenu = urlopen(URL_RSS).read().decode('utf-8')
	
	
RACINE = ET.fromstring(contenu)
CHANNEL = RACINE.find("channel")

JOUR_FICHIER_AVANT = 0
if os.access("tnt.html", os.F_OK):
	JOUR_FICHIER_AVANT = int(os.stat("tnt.html").st_mtime/86400)
	
HEURE_EN_COURS = time.localtime().tm_hour

resultats = open("tnt.html","w")
resultats.write('<!DOCTYPE html> \n <html> \n <head> <meta charset="UTF-8" /> <head> \n')

'''
resultats.write('<body> <a href="'+URL_RSS+'">'+URL_RSS+'</a> <br /> <br /> \n')
'''

for item in CHANNEL.findall('item'):
	title = item.find('title').text
	chaine, horaire, titre = title.split(" | ")
	if chaine in CHAINES_NON_RECUES:
		continue
		
	heure_emission = int(horaire.split(":")[0])
	if heure_emission >= HEURE_EN_COURS:
		description = item.find('description').text
		for mot in MOTS_CLES:
			if (titre.find(mot) != -1) | (description.find(mot) != -1):
				description = description.replace("<strong>", "").replace("</strong>", "")
				description = description.replace(mot,"<strong>"+mot+"<strong>")
				titre = titre.replace(mot, "<em>"+mot+"</em>")
				resultats.write("<h2>"+titre+"</h2>\n")
				resultats.write(horaire+" sur "+chaine+"<br /> \n")
				resultats.write(description+"<hr />\n")
				break
				
resultats.write("</ body> \n </html> \n")
resultats.close()

JOUR_FICHIER_APRES = int(os.stat("tnt.html").st_mtime / 86400)
if (JOUR_FICHIER_AVANT != JOUR_FICHIER_APRES):
	os.system("firefox tnt.html &")
