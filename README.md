# LALko
LaserAblationLogger

TO DO FRONTEND
-tabulka širší a scrollovatelná do stran a vidět pořád ne až dole
-nereaguje "margin-left: 10px !important;", kdysi to šlo
-jsou tam dvě, úplně dolní lze vypnout v base.html "overflow-x: hidden;"
-vidět lištu s popisky sloupců pořád a ne aby se mi schovala
-šířka sloupců pro výsledky filtrování podle All OPerations
-upravit pořadí sloupců, aby to sedělo všude včetně Djanga
-označit co jsou povinná pole

TO DO Course requirements
-Dokumentace: Každá třída a funkce by měla mít alespoň jednořádkovou dokumentaci ("""...""" nebo #). Je třeba projít celý kód a přidat chybějící popisy.
-Testy (pytest): Toto je klíčový a nedokončený požadavek. Musíte vytvořit minimálně 3 testy pomocí frameworku pytest, které pokryjí klíčové funkcionality. Pro každý pohled by měly být alespoň dva testy.

IMPORT Z EXCELU
-Začistit data, aby to nedělalo nepořádek v roletkách
-Upravit co bylo dělané Káťou, co Spiralem/LongPlates(mana s2 neco bylo taky longplaty)
-Udělat zálohu dat
# Pro spuštění: python manage.py import_runlog /home/tomas/Programming/CodersLab/LALko/LALko/fixtures/excel_import/runlog2.xlsm

POSTUPY        
# návrat k poslednímu commitu "git reset --hard HEAD"

#POSTGRES ZAČÁTEK NA NOVÉM PC
# sudo -u postgres psql
# CREATE USER lalko_user WITH PASSWORD 'lalko_pass';
# CREATE DATABASE lalko_db OWNER lalko_user;
# GRANT ALL PRIVILEGES ON DATABASE lalko_db TO lalko_user;
# \l (zjištění, že databáze existuje, vyjedu z toho kliknutím na "q")
# připojení se k databázi pomocí \c lalko_db

#RESET DATABÁZE
# DROP DATABASE lalko_db;
# CREATE DATABASE lalko_db;
# python manage.py makemigrations; python manage.py migrate;
# python manage.py createsuperuser (tomashambalek@eu.aacoptics.com a uživatel a heslo "admin" pro superuser Django)
# python manage.py load_input_data
# python manage.py runserver
        
#EXPORT PROJECT
# pro requirements "pip freeze > requirements.txt"
# pro export databáze "python manage.py dumpdata runlog.Operation > fixtures/operation_data.json"
# git add .
# git commit -m "První commit"
# git push -u origin main

#IMPORT PROJECT
# jedno LALko: source venv/bin/activate
# jedno LALko: git status; git pull origin main
# dve LALka: pip install -r requirements.txt

#POSTGRES IMPORT
# sudo -u postgres psql
# v Djangu - python manage.py migrate
# v Djangu - python manage.py loaddata fixtures/initial_data.json
# python manage.py runserver
# python manage.py createsuperuser (tomashambalek@eu.aacoptics.com a uživatel a heslo "admin" pro superuser Django)
