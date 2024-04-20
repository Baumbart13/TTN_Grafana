TheThingsIndustries richtig einstellen
======================================

Dieser Punkt erklärt nur, wie man Applications richtig aufbauen und konfigurieren muss
und nicht, wie man einzelne Sensoren einlernt.

1. Die "Application-id" muss einzigartig gewählt werden
    - Der Wert hiervon muss dann auch (case-sensitiv!!!) in der Datei "config.json" hinterlegt werden
2. Selbiges muss bedacht werden, mit den ID's der Sensoren
    - Auch dieser Wert muss in der "config.json" hinterlegt werden
3. Es muss ein "Custom Payload formatter" für Uplinks benutzt werden. Dieser ist abgespeichert unter "payloadFormatter.js"
    - Diese Datei NIEMALS ändern, außer man weiß, was man tut!!!!!
    - Diesr Formatter muss als "Default Payload formatter" genutzt werden => Erspart das Einstellen für jeden Sensor
4. "Storage Integrations" aktivieren
    - Dieser Schritt ist essentiell, um Daten abfragen zu können
    - Aktiviert unter "Integrations" -> "Storage Integrations"
5. API-Key sichern
    - Unter "API keys" einen key mit entsprechenden Rechten erstellen
    - Der vollständige Schlüssel wird NUR BEIM ERSTELLEN angezeigt!!! SOFORT SICHER ABSPEICHERN!!!
    - Den vollständigen Schlüssel auch in der "config.json" unter entsprechendem Punkt speichern


Installation
============

1. Zuerst Python installieren und den Haken setzen für die Umgebungsvariablen
2. cmd öffnen und "python" eingeben
    - Startet Python? -> Gut, weiter
    - Python startet nicht? -> Versuchs nochmal
3. In Ordner des Auslese-Programms gehen
4. cmd öffnen und "pip install -r .\requirements.txt" ausführen
    - Installiert alle Abhängigkeiten der Auslesung


Kompilierung (EXE erstellen)
============================

1. Falls "pyinstaller" noch nicht installiert ist
    1. cmd öffnen und "pip install pyinstaller" ausführen
2. Sicherstellen, dass "Logo.png" und "ttn_api.py" im gleichen Ordner existieren
2. "build.cmd" ausführen


Backup einspielen
=================

1. Backup-Datei finden
2. Inhalt von Backup-Datei kopieren
3. Inhalt in eine PostgreSQL-Shell (pgadmin öffnen, Datenbank auswählen, Query-Tool öffnen) kopieren
4. Ausführen
5. Warten bis Ende
6. (Optional) Überprüfen, ob Import funktioniert hat
