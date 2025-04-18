#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# galgenmaennchen.py
# Ein einfaches Galgenmännchen-Spiel in der Konsole
# Updated 2025-04-18

"""
Ein einfaches Hangman-Spiel in der Konsole.

Dieses Programm implementiert das klassische Wort-Rate-Spiel Galgenmännchen,
bei dem Spieler Buchstaben raten, um ein verstecktes Wort aufzudecken,
bevor das Galgenmännchen vollständig gezeichnet ist.
"""

import random
import sys
import os
import time
from typing import List, Tuple, Set, Optional


class Hangman:
    """Klasse zur Verwaltung eines Hangman-Spiels."""
    
    # ASCII-Art für das Galgenmännchen (von 0 bis 6 Fehlversuchen)
    HANGMAN_ASCII = [
        """
         -----
         |   |
             |
             |
             |
             |
        -----+-----
        """,
        """
         -----
         |   |
         O   |
             |
             |
             |
        -----+-----
        """,
        """
         -----
         |   |
         O   |
         |   |
             |
             |
        -----+-----
        """,
        """
         -----
         |   |
         O   |
        /|   |
             |
             |
        -----+-----
        """,
        """
         -----
         |   |
         O   |
        /|\\  |
             |
             |
        -----+-----
        """,
        """
         -----
         |   |
         O   |
        /|\\  |
        /    |
             |
        -----+-----
        """,
        """
         -----
         |   |
         O   |
        /|\\  |
        / \\  |
             |
        -----+-----
        """
    ]
    
    # Wortliste für das Spiel (kann erweitert werden)
    WORTLISTE = [
        "apfel", "banane", "computer", "drucker", "elefant", "fenster", "garten",
        "haus", "insel", "jacke", "kalender", "lampe", "maus", "nacht", "orange",
        "pullover", "qualle", "regen", "sonne", "telefon", "uhr", "vogel", "wasser",
        "zitrone", "auto", "buch", "dach", "eimer", "fisch", "glas", "hund", "igel",
        "kaffee", "licht", "milch", "natur", "pinsel", "rose", "schuh", "tisch",
        "vase", "wolke", "zebra", "ananas", "baum", "diamant", "erde", "familie",
        "gebirge", "himmel", "internet", "karte", "limonade", "musik", "norden",
        "papier", "radio", "saft", "treppe", "universum", "wetter", "yacht", "zug",
        "blume", "donner", "elch", "feuer", "geige", "honig", "joghurt", "kuchen",
        "leiter", "mond", "nebel", "obst", "palme", "rakete", "salat", "tanne",
        "ufer", "wind", "zaun", "adler", "birne", "dose", "eidechse", "frosch",
        "giraffe", "hai", "insekt", "kamel", "leopard", "muschel", "nilpferd",
        "pferd", "ratte", "schlange", "tiger", "wal", "ziege"
    ]
    
    # Schwierigkeitsgrade
    SCHWIERIGKEITEN = {
        "leicht": {"versuche": 8, "wortliste": None},  # Alle Wörter
        "mittel": {"versuche": 6, "wortliste": None},  # Alle Wörter
        "schwer": {"versuche": 6, "wortliste": None},  # Gefilterte Wörter (siehe __init__)
        "experte": {"versuche": 5, "wortliste": None}  # Gefilterte Wörter (siehe __init__)
    }
    
    def __init__(self, schwierigkeit: str = "mittel"):
        """
        Initialisiert ein Hangman-Spiel.
        
        Args:
            schwierigkeit: Schwierigkeitsgrad ("leicht", "mittel", "schwer", "experte")
        """
        # Schwierigkeitsgrad setzen
        if schwierigkeit not in self.SCHWIERIGKEITEN:
            schwierigkeit = "mittel"
            
        self.schwierigkeit = schwierigkeit
        
        # Wortlisten für Schwierigkeitsgrade vorbereiten (falls noch nicht geschehen)
        if self.SCHWIERIGKEITEN["schwer"]["wortliste"] is None:
            # Schwere Wörter: Länger oder mit seltenen Buchstaben
            self.SCHWIERIGKEITEN["schwer"]["wortliste"] = [
                wort for wort in self.WORTLISTE
                if len(wort) >= 7 or any(c in wort for c in "qxyvjpz")
            ]
            
        if self.SCHWIERIGKEITEN["experte"]["wortliste"] is None:
            # Experten-Wörter: Länger und mit seltenen Buchstaben
            self.SCHWIERIGKEITEN["experte"]["wortliste"] = [
                wort for wort in self.WORTLISTE
                if len(wort) >= 8 and any(c in wort for c in "qxyvjz")
            ]
            
        # Spielvariablen
        self.max_versuche = self.SCHWIERIGKEITEN[schwierigkeit]["versuche"]
        self.fehlversuche = 0
        self.geratene_buchstaben = set()
        self.wort = ""
        self.spielende = False
        self.gewonnen = False
        self.hinweise_verwendet = 0
        
        # Statistik
        self.spiele_gespielt = 0
        self.spiele_gewonnen = 0
        
    def neues_spiel(self) -> None:
        """Startet ein neues Hangman-Spiel."""
        # Wortliste für den aktuellen Schwierigkeitsgrad auswählen
        wortliste = self.SCHWIERIGKEITEN[self.schwierigkeit]["wortliste"]
        
        # Wenn keine spezifische Wortliste für den Schwierigkeitsgrad vorhanden ist,
        # die allgemeine Wortliste verwenden
        if wortliste is None:
            wortliste = self.WORTLISTE
            
        # Zufälliges Wort auswählen
        self.wort = random.choice(wortliste).lower()
        
        # Spielvariablen zurücksetzen
        self.fehlversuche = 0
        self.geratene_buchstaben = set()
        self.spielende = False
        self.gewonnen = False
        self.hinweise_verwendet = 0
        
    def zeige_spielstand(self) -> None:
        """Zeigt den aktuellen Spielstand an."""
        # Terminal leeren (plattformunabhängig)
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')
            
        print("\n=== HANGMAN ===")
        
        # Hangman-ASCII anzeigen
        print(self.HANGMAN_ASCII[min(self.fehlversuche, len(self.HANGMAN_ASCII) - 1)])
        
        # Verstecktes Wort anzeigen
        verstecktes_wort = self._get_verstecktes_wort()
        print(f"\nWort: {verstecktes_wort}")
        
        # Bereits geratene Buchstaben anzeigen
        if self.geratene_buchstaben:
            sortierte_buchstaben = sorted(self.geratene_buchstaben)
            print(f"Geratene Buchstaben: {', '.join(sortierte_buchstaben)}")
            
        # Verbleibende Versuche anzeigen
        verbleibende_versuche = self.max_versuche - self.fehlversuche
        print(f"Verbleibende Versuche: {verbleibende_versuche}")
        
        # Schwierigkeitsgrad anzeigen
        print(f"Schwierigkeitsgrad: {self.schwierigkeit}")
        
    def rate_buchstabe(self, buchstabe: str) -> Tuple[bool, str]:
        """
        Verarbeitet einen geratenen Buchstaben.
        
        Args:
            buchstabe: Der geratene Buchstabe
            
        Returns:
            Tuple mit (Erfolg, Nachricht)
        """
        # Sicherstellen, dass genau ein Buchstabe eingegeben wurde
        if len(buchstabe) != 1:
            return False, "Bitte gib genau einen Buchstaben ein."
            
        # Sicherstellen, dass es ein gültiger Buchstabe ist
        if not buchstabe.isalpha():
            return False, "Bitte gib einen gültigen Buchstaben ein."
            
        # Zu Kleinbuchstaben konvertieren
        buchstabe = buchstabe.lower()
        
        # Prüfen, ob der Buchstabe bereits geraten wurde
        if buchstabe in self.geratene_buchstaben:
            return False, f"Du hast den Buchstaben '{buchstabe}' bereits geraten."
            
        # Buchstabe zur Liste der geratenen Buchstaben hinzufügen
        self.geratene_buchstaben.add(buchstabe)
        
        # Prüfen, ob der Buchstabe im Wort vorkommt
        if buchstabe in self.wort:
            # Prüfen, ob das Wort vollständig geraten wurde
            verstecktes_wort = self._get_verstecktes_wort()
            if "_" not in verstecktes_wort:
                self.spielende = True
                self.gewonnen = True
                self.spiele_gespielt += 1
                self.spiele_gewonnen += 1
                return True, "Gratulation! Du hast das Wort erraten!"
                
            return True, f"Gut geraten! Der Buchstabe '{buchstabe}' ist im Wort."
        else:
            # Fehlversuch zählen
            self.fehlversuche += 1
            
            # Prüfen, ob das Spiel verloren ist
            if self.fehlversuche >= self.max_versuche:
                self.spielende = True
                self.spiele_gespielt += 1
                return False, f"Leider verloren! Das gesuchte Wort war: {self.wort}"
                
            return False, f"Leider falsch! Der Buchstabe '{buchstabe}' ist nicht im Wort."
            
    def gib_hinweis(self) -> Tuple[bool, str]:
        """
        Gibt einen Hinweis, indem ein zufälliger, noch nicht geratener Buchstabe verraten wird.
        
        Returns:
            Tuple mit (Erfolg, Nachricht)
        """
        # Bereits die Hälfte der Versuche verbraucht?
        if self.fehlversuche < self.max_versuche // 2:
            return False, "Hinweise sind erst verfügbar, nachdem du die Hälfte der Versuche verbraucht hast."
            
        # Maximale Anzahl an Hinweisen (je nach Wortlänge)
        max_hinweise = 1
        if len(self.wort) > 7:
            max_hinweise = 2
            
        if self.hinweise_verwendet >= max_hinweise:
            return False, f"Du hast bereits die maximale Anzahl an Hinweisen ({max_hinweise}) verwendet."
            
        # Buchstaben finden, die im Wort vorkommen, aber noch nicht geraten wurden
        nicht_geratene_buchstaben = [b for b in self.wort if b not in self.geratene_buchstaben]
        
        if not nicht_geratene_buchstaben:
            return False, "Es gibt keine weiteren Buchstaben, die als Hinweis dienen könnten."
            
        # Zufälligen Buchstaben auswählen und direkt raten
        hinweis_buchstabe = random.choice(nicht_geratene_buchstaben)
        self.hinweise_verwendet += 1
        
        # Buchstabe zur Liste der geratenen Buchstaben hinzufügen
        self.geratene_buchstaben.add(hinweis_buchstabe)
        
        # Prüfen, ob das Wort vollständig geraten wurde
        verstecktes_wort = self._get_verstecktes_wort()
        if "_" not in verstecktes_wort:
            self.spielende = True
            self.gewonnen = True
            self.spiele_gespielt += 1
            self.spiele_gewonnen += 1
            return True, f"Hinweis: Der Buchstabe '{hinweis_buchstabe}' ist im Wort.\nGratulation! Du hast das Wort erraten!"
            
        return True, f"Hinweis: Der Buchstabe '{hinweis_buchstabe}' ist im Wort."
        
    def _get_verstecktes_wort(self) -> str:
        """
        Gibt das teilweise versteckte Wort basierend auf den bereits geratenen Buchstaben zurück.
        
        Returns:
            Teilweise verstecktes Wort
        """
        verstecktes_wort = ""
        for buchstabe in self.wort:
            if buchstabe in self.geratene_buchstaben:
                verstecktes_wort += buchstabe
            else:
                verstecktes_wort += "_"
                
        # Mit Leerzeichen für bessere Lesbarkeit
        return " ".join(verstecktes_wort)
        
    def get_statistik(self) -> dict:
        """
        Gibt die Spielstatistik zurück.
        
        Returns:
            Dictionary mit Spielstatistiken
        """
        return {
            "spiele_gespielt": self.spiele_gespielt,
            "spiele_gewonnen": self.spiele_gewonnen,
            "gewinnrate": (self.spiele_gewonnen / self.spiele_gespielt) * 100 if self.spiele_gespielt > 0 else 0
        }
        
    def aendere_schwierigkeit(self, schwierigkeit: str) -> bool:
        """
        Ändert den Schwierigkeitsgrad.
        
        Args:
            schwierigkeit: Neuer Schwierigkeitsgrad
            
        Returns:
            True, wenn erfolgreich, sonst False
        """
        if schwierigkeit not in self.SCHWIERIGKEITEN:
            return False
            
        self.schwierigkeit = schwierigkeit
        self.max_versuche = self.SCHWIERIGKEITEN[schwierigkeit]["versuche"]
        return True


def print_help() -> None:
    """Zeigt die Hilfeübersicht für das Hangman-Spiel an."""
    print("\nHangman Hilfe")
    print("=============")
    print("Befehle:")
    print("  <Buchstabe>      - Einen Buchstaben raten")
    print("  neu              - Neues Spiel starten")
    print("  schwierigkeit <niveau> - Schwierigkeitsgrad ändern")
    print("                     (leicht, mittel, schwer, experte)")
    print("  hinweis          - Einen Hinweis erhalten (kostet einen verbleibenden Versuch)")
    print("  statistik        - Spielstatistik anzeigen")
    print("  hilfe            - Diese Hilfeübersicht anzeigen")
    print("  exit/quit        - Spiel beenden")
    print("\nSpielregeln:")
    print("  - Rate Buchstaben, um das versteckte Wort aufzudecken")
    print("  - Jeder falsche Versuch ergänzt das Galgenmännchen")
    print("  - Das Spiel ist verloren, wenn das Galgenmännchen vollständig ist")
    print("  - Das Spiel ist gewonnen, wenn das Wort vollständig erraten wurde")


def main() -> int:
    """
    Haupteinstiegspunkt für das Hangman-Spiel.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    print("=== GALGENMÄNNCHEN ===")
    print("'hilfe' für Hilfeübersicht, 'exit' zum Beenden")
    
    # Spiel initialisieren
    spiel = Hangman()
    spiel.neues_spiel()
    
    # Spielschleife
    while True:
        try:
            # Aktuellen Spielstand anzeigen
            spiel.zeige_spielstand()
            
            # Wenn das Spiel beendet ist, neues Spiel anbieten
            if spiel.spielende:
                antwort = input("\nMöchtest du noch einmal spielen? (j/n): ").strip().lower()
                
                if antwort in ['j', 'ja', 'y', 'yes']:
                    spiel.neues_spiel()
                    continue
                else:
                    print("Danke fürs Spielen!")
                    return 0
                    
            # Benutzereingabe
            user_input = input("\nDein Zug: ").strip().lower()
            
            # Leere Eingabe überspringen
            if not user_input:
                continue
                
            # Spezielle Befehle verarbeiten
            if user_input in ['exit', 'quit', 'beenden']:
                print("Spiel wird beendet.")
                return 0
                
            elif user_input in ['hilfe', 'help', '?']:
                print_help()
                input("\nDrücke ENTER, um fortzufahren...")
                continue
                
            elif user_input in ['neu', 'new', 'restart']:
                spiel.neues_spiel()
                continue
                
            elif user_input.startswith(('schwierigkeit', 'schwer', 'level', 'difficulty')):
                # Schwierigkeitsgrad ändern
                teile = user_input.split(maxsplit=1)
                
                if len(teile) > 1:
                    neuer_schwierigkeitsgrad = teile[1].lower()
                    
                    if spiel.aendere_schwierigkeit(neuer_schwierigkeitsgrad):
                        print(f"Schwierigkeitsgrad auf '{neuer_schwierigkeitsgrad}' geändert.")
                        spiel.neues_spiel()
                    else:
                        print(f"Ungültiger Schwierigkeitsgrad: {neuer_schwierigkeitsgrad}")
                        print("Verfügbare Schwierigkeitsgrade: leicht, mittel, schwer, experte")
                else:
                    print("Bitte gib einen Schwierigkeitsgrad an.")
                    print("Verfügbare Schwierigkeitsgrade: leicht, mittel, schwer, experte")
                    
                input("\nDrücke ENTER, um fortzufahren...")
                continue
                
            elif user_input in ['hinweis', 'hint', 'tipp']:
                erfolg, nachricht = spiel.gib_hinweis()
                print(nachricht)
                input("\nDrücke ENTER, um fortzufahren...")
                continue
                
            elif user_input in ['statistik', 'stats', 'stat']:
                statistik = spiel.get_statistik()
                
                print("\nSpielstatistik")
                print("==============")
                print(f"Spiele gespielt: {statistik['spiele_gespielt']}")
                print(f"Spiele gewonnen: {statistik['spiele_gewonnen']}")
                print(f"Gewinnrate: {statistik['gewinnrate']:.1f}%")
                
                input("\nDrücke ENTER, um fortzufahren...")
                continue
                
            # Buchstaben raten
            if len(user_input) == 1 and user_input.isalpha():
                erfolg, nachricht = spiel.rate_buchstabe(user_input)
                
                # Bei Spielende die Nachricht anzeigen und kurz warten
                if spiel.spielende:
                    print(nachricht)
                    time.sleep(2)
                    
            else:
                print("Ungültige Eingabe. Bitte gib einen einzelnen Buchstaben ein.")
                input("\nDrücke ENTER, um fortzufahren...")
                
        except KeyboardInterrupt:
            print("\nSpiel wird beendet.")
            return 0
            
        except Exception as e:
            print(f"\nEin Fehler ist aufgetreten: {e}")
            input("\nDrücke ENTER, um fortzufahren...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
