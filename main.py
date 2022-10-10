# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:01:50 2020

@author: pberanek91
"""
import math
import random
import os
from xml.dom import minidom as md
import pdfkit
import codecs

#vygeneruje nahodne zadani pro studenta ve dvou verzich - s resenim a bez
def vygenerujZadani(xmlPath, student, nprikladu_typu):
    
    data_testu = {
        "student": student,
        "zadani": [],
        "reseni": [],
        "nazev":"",
        "uvod":"",
        "zaver":""
        }
    
    xmldoc = md.parse(xmlPath)
    
    testname_element = xmldoc.getElementsByTagName("nazev")[0]
    testname = testname_element.firstChild.nodeValue if testname_element.firstChild else ""
    data_testu["nazev"] = testname
    
    header_element = xmldoc.getElementsByTagName("uvod")[0]
    header = header_element.firstChild.nodeValue if header_element.firstChild else ""
    data_testu["uvod"] = header
    
    footer_element = xmldoc.getElementsByTagName("zaver")[0]
    footer = footer_element.firstChild.nodeValue if footer_element.firstChild else ""
    data_testu["zaver"] = footer
    
    priklady = xmldoc.getElementsByTagName("priklad")
    #ziska slovnik <typ prikladu: seznam prikladu daneho typu>
    typy_prikladu = {}
    for priklad in priklady:
        if priklad.getAttribute("typ") not in typy_prikladu.keys():
            typy_prikladu[priklad.getAttribute("typ")] = [priklad]
        else:
            typy_prikladu[priklad.getAttribute("typ")].append(priklad)

    #vylosuje nahodne priklady pro kazdy typ o pozadovanem poctu
    priklady = []
    for typ_prikladu in typy_prikladu.keys():
        for i in range(nprikladu_typu[int(typ_prikladu)-1]):
            random.shuffle(typy_prikladu[typ_prikladu])
            priklady.append(typy_prikladu[typ_prikladu].pop())

    #vygeneruje zadani pro studenta bez reseni a s resenim
    for i in range(len(priklady)):
        vyplneny_priklad = vygenerujPriklad(priklady[i])
        data_testu["zadani"].append(upravaZadani(vyplneny_priklad[0]))
        data_testu["reseni"].append(upravaZadani(vyplneny_priklad[1]))

    return data_testu
        

#vygeneruje nahodny priklad pro studenta (lze zvolit s resenim/bez reseni)
def vygenerujPriklad(priklad):

    #ziskej veskere informace o promennych v priklade
    promenne_element = priklad.getElementsByTagName("promenna")
    vyhodnocene_promenne = vygenerujPromenne(promenne_element)

    #ziskani zadani a nahrazeni znacek nazvy a hodnotami
    zadani_element = priklad.getElementsByTagName("zadani")[0]
    zadani = zadani_element.firstChild.nodeValue
    print("test: " + zadani)
    for promenna in vyhodnocene_promenne:
        zadani = zadani.replace("{"+promenna[0]+"}","{} {} {}".format(promenna[1], promenna[3], promenna[2]))
    print("test OK")

    #ziskani reseni prikladu
    vysledky_element = priklad.getElementsByTagName("vysledek")
    reseni = ziskejReseni(vysledky_element, vyhodnocene_promenne)
    zadani_reseni = zadani + "\n" + reseni + "\n"
        
    return [zadani, zadani_reseni]


#vygeneruje nahodne promenne do zadani
def vygenerujPromenne(promenne_element):
    vyhodnocene_promenne = []
    for promenna in promenne_element:

        #znacka - pouziva se pro identifikaci mista promenne v zadani
        znacka_element = promenna.getElementsByTagName("znacka")[0]
        znacka = znacka_element.firstChild.nodeValue if znacka_element.firstChild else ""

        #nazev - pouziva se pro nahrazeni znacky v zadani
        nazev_element = promenna.getElementsByTagName("nazev")[0]
        nazev = nazev_element.firstChild.nodeValue + " =" if nazev_element.firstChild else ""

        #jednotka - pouziva se za nazev pri nahrazovani znacky v zadani
        jednotka_element = promenna.getElementsByTagName("jednotka")[0]
        jednotka = jednotka_element.firstChild.nodeValue if jednotka_element.firstChild else ""

        #min a max - hodnoty pro vygenerovani nahodnych hodnot promennych
        min_element = promenna.getElementsByTagName("min")[0]
        min_hodnota = float(min_element.firstChild.nodeValue) if min_element.firstChild else 0
        max_element = promenna.getElementsByTagName("max")[0]
        max_hodnota = float(max_element.firstChild.nodeValue) if max_element.firstChild else 0

        #desetiny - na kolik desetinnych mist se ma hodnota vygenerovat
        desetiny_element = promenna.getElementsByTagName("desetiny")[0]
        desetiny = int(desetiny_element.firstChild.nodeValue) if desetiny_element.firstChild else 0

        #generovani hodnoty a zapis do seznamu pro nahrazeni v zadani
        rand_hodnota = round(min_hodnota + random.random()*(max_hodnota-min_hodnota),desetiny)
        vyhodnocene_promenne.append((znacka, nazev, jednotka, rand_hodnota))

    return vyhodnocene_promenne


#vrati retezec s vypocitanymi vysledky
def ziskejReseni(vysledky_element, vyhodnocene_promenne):

    #retezec, do ktereho se postupne ukladani vsechny pozadovane vysledky
    reseni = ""

    #vysledku muze byt vice (vsechny veliciny, jenz chceme spocitat)
    for vysledek_element in vysledky_element:

        #nazev se pouzije pred cislo: nazev = vysledna hodnota
        nazev_element = vysledek_element.getElementsByTagName("nazev")[0]
        nazev = nazev_element.firstChild.nodeValue if nazev_element.firstChild else ""

        #vzorec s promennymi se nahradi konkretnimi vygenerovanymi cisly
        vzorec_element = vysledek_element.getElementsByTagName("vzorec")[0]
        vzorec = vzorec_element.firstChild.nodeValue if vzorec_element.firstChild else ""
        for promenna in vyhodnocene_promenne:
             vzorec = vzorec.replace("{"+promenna[0]+"}", str(promenna[3]))

        #vzorec s cisly se vyhodnoti a vysledek se pripise do reseni
        if vzorec:
            reseni += "{} = {}\n".format(nazev, eval(vzorec))

    return reseni


#upravi graficky zadani
def upravaZadani(zadani):

    #smaze desetinna mista, pokud je promenna celociselna
    zadani = zadani.replace(".0 ", " ")
    zadani = zadani.replace(".0\n", "\n")

    #nahradi dve mezery jednou, vznikajici absenci nazvu promenne v zadani
    zadani = zadani.replace("  ", " ")

    return zadani

#vygeneruje zadani a reseni testu do souboru typu .txt
def vygenerujTXT(data_testu, test_cesta, reseni_cesta):

    if not os.path.exists(test_cesta):
        os.mkdir(test_cesta)
    soubor = codecs.open(test_cesta+data_testu["student"]+".txt", 
                         "w", encoding = "utf-8")    
    soubor.write("Test z fyziky: {}\n\n".format(data_testu["nazev"]))
    soubor.write("Student: {}\n\n".format(data_testu["student"]))  
    soubor.write(data_testu["uvod"] + "\n")
    for izadani, zadani in enumerate(data_testu["zadani"]):
        soubor.write("Pr. "+str(izadani+1)+":")
        soubor.write(zadani+"\n")
    soubor.write(data_testu["zaver"] + "\n")
    soubor.close()

    if not os.path.exists(reseni_cesta):
        os.mkdir(reseni_cesta)
    soubor = codecs.open(reseni_cesta+data_testu["student"]+"_reseni.txt", 
                         "w", encoding = "utf-8")
    soubor.write("Test z fyziky: {}\n\n".format(data_testu["nazev"]))
    soubor.write("Student: {}\n\n".format(data_testu["student"]))
    soubor.write(data_testu["uvod"] + "\n")
    for ireseni, reseni in enumerate(data_testu["reseni"]):
        soubor.write("Pr. "+str(ireseni+1)+":")
        soubor.write(reseni+"\n")
    soubor.write(data_testu["zaver"] + "\n")
    soubor.close()


#vygeneruje zadani a reseni testu do souboru typu .html
def vygenerujHTML(data_testu, test_cesta, reseni_cesta, css_cesta):

    hlavicka = "<!DOCTYPE html>\n<html>\n<head>\n"
    css_link = '<link rel="stylesheet" href="' + css_cesta + '">\n'
    title = "<title>Fyzika Test</title>\n"
    meta_charset = '<meta charset="utf-8">\n'
    body_start = "</head>\n<body>\n"
    zapati = "</body>\n</html>"

    html_zahlavi = "<h1>Test z fyziky: " + data_testu["nazev"] + "</h1>"     
    html_student = "<h2>Student: "+data_testu["student"]+"</h2>\n"
    
    html_uvod = '<p id="uvod">'+ data_testu["uvod"] +'</p>'
    html_zaver = '<hr>\n<p id="zaver">'+ data_testu["zaver"] +'</p>'
    
    html_zadani = hlavicka + css_link + title + meta_charset + body_start
    html_zadani += html_zahlavi
    html_zadani += html_student
    html_zadani += html_uvod
    html_reseni = html_zadani
    
    for izadani, zadani in enumerate(data_testu["zadani"]):
        html_zadani += "<hr>"
        html_zadani += "<h3>Příklad: "+str(izadani+1)+"</h3>\n"
        html_zadani += "<p>"+zadani.replace("\n","<br>")+"</p>\n"
    
    for ireseni, reseni in enumerate(data_testu["reseni"]):
        html_reseni += "<hr>"
        html_reseni += "<h3>Příklad: "+str(ireseni+1)+"</h3>\n"
        html_reseni += "<p>"+reseni.replace("\n","<br>")+"</p>\n" 
        
    html_zadani += html_zaver
    html_reseni += html_zaver
    html_zadani += zapati
    html_reseni += zapati
    
    zadani_soubor_html = os.getcwd()+"\\"+test_cesta+data_testu["student"]+".html"
    reseni_soubor_html = os.getcwd()+"\\"+reseni_cesta+data_testu["student"]+"_reseni.html"
    zadani_soubor_pdf = os.getcwd()+"\\"+test_cesta+data_testu["student"]+".pdf"
    reseni_soubor_pdf = os.getcwd()+"\\"+reseni_cesta+data_testu["student"]+"_reseni.pdf"
    
    if not os.path.exists(test_cesta):
        os.mkdir(test_cesta)
    soubor = codecs.open(zadani_soubor_html, "w", encoding="utf8")
    soubor.write(html_zadani)
    soubor.close()

    if not os.path.exists(reseni_cesta):
        os.mkdir(reseni_cesta)
    soubor = open(reseni_soubor_html, "w", encoding="utf8")
    soubor.write(html_reseni)
    soubor.close()

    path_wkthmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf = path_wkthmltopdf)
    options = {'enable-local-file-access': None}
    pdfkit.from_url(zadani_soubor_html, zadani_soubor_pdf, 
                    configuration=config, options=options)
    pdfkit.from_url(reseni_soubor_html, reseni_soubor_pdf, 
                    configuration=config, options=options)


def main():

    xmlPath = "priklady\\termika.xml"
    studenti_soubor = "studenti\\2A.txt"
    test_cesta = "testy\\"
    reseni_cesta = "reseni\\"
    nprikladu_typu = [2, 2, 1]

    studenti = []
    for radek in codecs.open(studenti_soubor, "r", encoding="utf8"):
        studenti.append(radek.strip())

    for student in studenti:
        data_testu = vygenerujZadani(xmlPath, student, nprikladu_typu)
        vygenerujTXT(data_testu, test_cesta, reseni_cesta)
        vygenerujHTML(data_testu, test_cesta, reseni_cesta, "styl.css")

if __name__ == "__main__":
    main()