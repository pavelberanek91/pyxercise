# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:01:50 2020

@author: pberanek91
"""

import math
import random
import codecs
from xml.dom import minidom as md

from src.generators.txtgenerator import TxtGenerator
from src.generators.htmlgenerator import HtmlGenerator
from src.generators.pdfgenerator import PdfGenerator

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


def main():

    xmlPath = "priklady/termika.xml"
    studenti_soubor = "studenti/septima.txt"
    test_cesta = "testy/"
    reseni_cesta = "reseni/"
    styl_cesta = "../stylytestu/styl.css"
    nprikladu_typu = [2, 2, 1]

    studenti = []
    for radek in codecs.open(studenti_soubor, "r", encoding="utf8"):
        studenti.append(radek.strip())

    for student in studenti:
        data_testu = vygenerujZadani(xmlPath, student, nprikladu_typu)
        pdf_generator = PdfGenerator(
            exercise_data=data_testu,
            test_folder=test_cesta,
            solution_folder=reseni_cesta,
            style_file=styl_cesta
        )
        pdf_generator.generate_file('test')
        pdf_generator.generate_file('solution')

if __name__ == "__main__":
    main()