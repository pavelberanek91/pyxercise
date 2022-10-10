# Pyxercise

Python exercise generator

## 1. Popis projektu

Projekt Pyxercise ma za úkol vytvořit webovou aplikaci schopnou generovat unikátní příklady pro žáky základních a středních škol. Program vznikl během dvou nocí při online výuce v době pandemie. Aplikace dokáže ze souborů v XML formátu generovat PDF soubory se zadáním, které je v určitých místech nahrazeno dynamicky generovaným obsahem. Uživateli se vygenerují dvě verze PDF souboru - bez řešení a s řešením. Aplikaci lze použít pro procvičování příkladů a pro generování písemek s rychlou opravou učitelem.

První noc vznikla aplikace v zadáním testu v obyčejné textové podobě.
<img src="demo/verze0.1.png">

Druhou noc byl dodán design zadání s využitím kaskádových stylů a html kódu.
<img src="demo/verze0.2.png">

## 2. Instalace aplikace

Pro správnou funkčnost je aktuálně nutné mít nainstalovanou aplikace wkhtmltopdf.

* MacOS: ```brew install homebrew/cask/wkhtmltopdf```
* Linux: ```sudo apt-get install wkhtmltopdf```
* Windows: Nainstalovat z tohoto odkazu: [ZDE](https://wkhtmltopdf.org/downloads.html)

Dále je nutné si nainstalovat potřebné závislosti z requirements souboru:
```python -m pip install -r requirements.txt```

Do souboru s kódem aplikace *main.py* je nutné vyplnit cestu k aplikaci wkhtmltopdf. Na MacOS a Linux lze zjistit cestu k aplikaci pomocí příkazu: ```which wkhtmltopdf```. Příklady cesty:
* Windows: PATH_WKHTMLTOPDF = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
* MacOS: PATH_WKHTMLTOPDF = "/usr/local/bin/wkhtmltopdf"

## 3. Návod k použití

Do adresáře příklady je nutné vložit XML soubor se zadáním příkladů. Vysvětlení elementů:
* <priklady>: kořenový element sbírky příkladl na dané téma
* <nazev>: název testu, který bude generován na vrcholu dokumentu se zadáním
* <uvod>: úvodní text k testu, užitečný jako motivace nebo instrukce pro vyplnění
* <zaver>: závěrečný text k testu, užitečný jako motivace nebo instrukce pro zaslání testu
* <priklad skupina=... typ=...>: uvozuje jeden konkrétní příklad, skupina je skupina pro znesnadněné opisování pro vytisknuté zadání na offline hodinu (např. ze školy skupina A, B vedle sebe), typ je typ příkladu (každý student má pak například 2 příklady 1. typu a 3 příklady 2. typu ve svém testu).
* <zadani>: obsahuje zadání příkladu, které je v místech s dynamickým obsahem označen složenými závorkami s názvem proměnné
* <promenne>: obsahuje seznam elementů proměnná, místo kterých se mají dynamicky vygenerovat náhodná čísla
* <znacka>: značka proměnné, která když se shoduje s proměnnou v textu v závorkách, tak se využijí informace této proměnné (jednotka, min, max, desetiny) pro generování náhodného čísla
* <nazev>: název, který se napíše před hodnotu (nemusí být využit, pokud je název již v textu zadání napevno)
* <jednotka>: jednotka, která se zapíše za náhodné číslo
* <min>: nejmenší možná hodnota vygenerované náhodné hodnoty proměnné
* <max>: největší možná hodnota vygenerované náhodné hodnoty proměnné
* <desetiny>: na kolik desetinných míst má být náhodná hodnota zaokrouhlena
* <vysledky>: seznam výsledků, které se mají spočítat a vygenerovat v učitelské verzi
* <vysledek>: jeden z výsledků, který se spočítá
* <nazev>: název nebo značka před rovnítkem s výsledkem
* <vzorec>: vzorec v jazyce Python, který se vyhodnotí a výsledek se napíše za rovnítko

Většina nastavení probíhá hned pod vstupním bodem aplikace v souboru *main.py*.

```
def main():

    xmlPath = "priklady/termika.xml"
    studenti_soubor = "studenti/septima.txt"
    test_cesta = "testy/"
    reseni_cesta = "reseni/"
    styl_cesta = "stylytestu/styl.css"
    nprikladu_typu = [2, 2, 1]
```

Do proměnné ```xmlPath``` se nastaví cesta k vybrané sbírce příkladů v xml souboru. 

Dále je nutné v adresáři studenti nahrát zvlášť na řádky jména studentů. Pro každého ze studentů se vytvoří test. Soubor se studenty se nastaví v souboru *main.py* do proměnné ```studenti_soubor```.

Do adresáře uvedeném v proměnné ```test_cesta``` se vygenerují neřešené testy ve formátu PDF pro studenty. Do adresáře uvedeném v proměnné ```reseni_cesta``` se vygenerují řešení testy ve formátu PDF pro učitele.

Důležité je nastavení v proměnné ```nprikladu_typu```. V této proměnné se zapíše na daný index, kolik příkladů daného typu se má vygenerovat. Například nastavení ```[2, 2, 1]``` znamená, že každý student bude mít 2 příklady typu 1, 2 příklady typu 2 a 1 příklad typu 3.

Aplikaci spustíme příkazem v terminálu: ```python main.py``` nebo dvojklikem na soubor ```main.py```.

## 4. Rozbor kódové báze

bude...

## 5. Poděkování

Zatím nikomu :)

