# 📰 Positive News Web Application

Deze applicatie haalt nieuwsartikelen op via de Event Registry API, voert sentimentanalyse uit met een BERT-model en slaat alleen positieve artikelen op in de database.

---

## 📋 **Inhoudsopgave**
* [Over het project](#over-het-project)
* [Functies](#Functies)  
* [Installatie](#installatie)
* [Configuratie](#configuratie)
* [Command-line Scripts](#command-line-scripts)  
* [API Eindpunten](#api-eindpunten)  
* [Requirements](#Requirements)  
* [Licentie](#licentie) 

---

## 🌍 **Over het project**
Positive News App verzamelt alleen positief nieuws van verschillende bronnen en categoriseert dit automatisch met behulp van Vader voor sentimentanalyse. Gebruikers kunnen zich registreren, artikelen opslaan als favoriet en gepersonaliseerde nieuwsfeeds ontvangen.

---

## 🚀 **Functies**
✅ Alleen positief nieuws tonen  
✅ Inloggen, registreren en gebruikersprofiel beheren  
✅ Artikelen opslaan als favoriet  
✅ Artikelen filteren op categorie en bron  
✅ Zoekfunctie op titel  
✅ Gepersonaliseerde categorie- en broninstellingen  
✅ Automatisch ophalen van nieuwsartikelen via externe API's  
✅ Automatisch categoriseren van nieuwsartikelen met sentimentanalyse  

---

## 🛠️ **Installatie**

Volg deze stappen om het project lokaal op te zetten.

1. **Project klonen vanaf GitHub**  

```bash
git clone https://github.com/AventusCT/3-alleen-maar-goed-nieuws-sld-vuurstormers
cd 3-alleen-maar-goed-nieuws-sld-vuurstormers
```

2. **Virtuele omgeving maken en activeren** 

```bash 
python -m venv venv
# Windows:
.\venv\Scripts\activate
# MacOS/Linux:
source venv/bin/activate
```
3. **Packages installeren**

Installeer de vereiste pakketten met pip:
```bash
pip install django
pip install transformers
pip install torch
pip install requests
```
⚠️ Let op: torch moet correct worden geïnstalleerd afhankelijk van je systeemconfiguratie. Gebruik deze link om de juiste versie te vinden:
👉 https://pytorch.org/get-started/locally/

4. **Database migreren**

Het project gebruikt een SQLite-database. U kunt de database maken door de volgende opdracht uit te voeren:

```bash
python manage.py migrate
```

5. **Fetch positive news articles**  
Dit script haalt automatisch artikelen op uit externe bronnen op bepaalde tijden:
Bestand: management/commands/fetch_articles.py
```Python
python manage.py fetch_articles
```

6. **Start de ontwikkelserver**

```bash
python manage.py runserver
```

7. **Bezoek de applicatie**

http://127.0.0.1:8000

---

## ⚙️ **Configuratie**

1. **Database configureren**  

Pas DATABASES aan in settings.py als u andere database wilt gebruiken:

```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'positive_news_db',
        'USER': 'root',
        'PASSWORD': 'jouw-wachtwoord',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

2. **API Sleutel configureren** 

Voeg je nieuws-API-sleutel toe in services.py bestand

## 📝 **Command-line Scripts**

**Re-categorize existing articles**

Dit script controleert en werkt automatisch categorieën van artikelen bij:
Bestand: management/commands/recategorize_articles.py
```Python
python manage.py recategorize_articles
```

## 🌐 **API Eindpunten**
**Homepagina**
URL: /
Methode: GET
Beschrijving: Geeft een overzicht van de laatste artikelen weer.
**Categorie artikelen**
URL: /category/<category>/
Methode: GET
Beschrijving: Geeft artikelen van een specifieke categorie weer.
**Zoekfunctie**
URL: /search/
Methode: GET
Parameters: q (zoekterm)
Beschrijving: Zoekt naar artikelen op basis van de titel.
**Artikeldetails**
URL: /article/<article_id>/
Methode: GET
Beschrijving: Toont details van het geselecteerde artikel.
**Favorieten beheren**
URL: /favorites/
Methode: GET
Beschrijving: Toont opgeslagen favorieten van de gebruiker.
**Inloggen**
URL: /login/
Methode: POST
Beschrijving: Logt de gebruiker in.
**Uitloggen**
URL: /logout/
Methode: POST
Beschrijving: Logt de gebruiker uit.
**Gebruikersprofiel (Buiten gebruik)**
URL: /profile/
Methode: GET, POST
Beschrijving: Toont en wijzigt het profiel van de gebruiker.


## ✅ **Requirements**
Python 3.10+
Django 4.2+
MySQL
requests

## 📝 **Licentie**
Dit project is gelicentieerd onder de MIT-licentie. Zie het bestand LICENSE voor details.

## 🎯 **Toekomstige verbeteringen**
✅ Thema-ondersteuning
✅ Donkere modus
✅ Meer nieuwsbronnen integreren
✅ Pushmeldingen voor nieuw positief nieuws
✅ Notificaties


