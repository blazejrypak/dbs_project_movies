# Digitálna databáza filmov

- Systém umožnuje používateľom prehľadávať základné informácie o veľkom množstve filmov ako napr. názov, rok vydania, 
herecké obsadenie, popis filmu, hodnotenie filmu a veľa iného na jednom mieste. 
- Používatelia, ktorí sa zaregistrujú budú mať možnosť hodnotiť filmy, ktoré sa nachádzajú v databáze, budú mať 
prehľad o všetkých svojich recenziách a filmoch, ktoré ich zaujímajú. 
- Hlavným cieľom systému je uľahčiť ľuďom námahu pri hľadaní konkrétnych informácií o filmoch tak,
   že ich sústredíme a sprístupníme na jednom mieste. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)

## Installation

Download to your project directory

```shell script
sudo apt install pipenv
git clone project_url
cd movie-database && pipenv install
pipenv shell
```
## Usage

You can find docs at [wiki](https://github.com/FIIT-DBS2020/project-mikulas_rypak/wiki)

```shell script
cd movie_projx
python manage.py makemigrations
python manage.py migrate
python manage.py sqlsequencereset movie_app // reset sequences in the database
python manage.py runserver
```
## Support

Please [open an issue](https://github.com/FIIT-DBS2020/project-mikulas_rypak/issues/new) for support.