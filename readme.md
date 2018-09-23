Zur Installation
Registrieren des Bots bei Telegram

    Schreib @BotFather bei Telegram per PN an
    Mit dem Kommando /newbot legt ihr einen neuen Bot an
    Auf die Frage: „Alright, a new bot. How are we going to call it? Please choose a name for your bot.“ gebt ihr den Namen für euren Bot an.
    Danach einen Usernamen, mit dem ihr euren Bot später bei Telegram anschreiben könnt.
    Darauf hin erhaltet ihr einen HTTP API Key. Den brauchen wir später in den Konfigurationsdateien unseres telebots

Installation des Bots auf dem PI

    Clonen des gits ins Homeverzeichnis von pi:
    git clone https://github.com/electrigga/telebot
    Die python-dev muss noch installiert werden:
    sudo apt-get install -t jessie python-dev
    
    Mit einem Editor eurer Wahl die Konfigurationen bearbeiten. Zum Besipiel:

    nano config.py
    Bei grant und botowner trag ihr am besten eure Telegram-ID ein. Das ist nicht der Alias (@dl2ajb), sondern eine mehrstellige Nummer. Diese findet ihr heraus, indem ihr eine PN per Telegram an @FalconGate_Bot schreibt und dort /get_my_id eingebt.
    Die Datei botlog.txt uns users.csv noch anlegen (die kommen später zum Einsatz und werden später auch automatisch angelegt).
    Im Arbeitsprozess stecken noch einige Konfigurationen in der eigentlichen Bot-Datei (telebot.py). Diese werden im Laufe der Zeit in die Config umziehen. Kontrolliert also die Datei telebot.py auf eventuelle Einstellungen.
    Die Datei ausführbar machen mit:

    chmod +x telebot.py

    Notwendige Python-Module noch laden:

    sudo pip install psutil telepot requests

Kleine Verfeinerungen

Man kann den Bot auch automatisch nach dem Start starten. Ich habe ihn dazu in die Crontab eingetragen und in Screen gestartet, damit ich mir zur Laufzeit eventuelle Ausgaben zu Debug-Zwecken ansehen kann.

crontab -e

Dort dann

@reboot sleep 20 && cd /home/pi/telebot && screen -m -d -S telebot /home/pi/telebot/telebot.py

Fragen, Anregungen, Wünsche und Hilfe bekommt ihr standesgemäß über Telegram. Dort einfach an in die Gruppe telebot schreiben: https://t.me/joinchat/E9aKOhLeY_fCgjCT8Txn_g

