#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# zahlen_raten.py
# Ein einfaches Zahlenratespiel
# Updated 2025-04-18

"""
Ein einfaches Zahlenratespiel.

In diesem Spiel wählt der Computer eine zufällige Zahl aus, und der Spieler
versucht, diese zu erraten. Bei jedem Versuch gibt es Hinweise.
"""

import random
import sys
import time
import math
from typing import Tuple, Optional, List


class ZahlenRaten:
    """Klasse zum Verwalten des Zahlenratespiels."""
    
    def __init__(self, min_zahl: int = 1, max_zahl: int = 100, max_versuche: int = 10):
        """
        Initialisiert das Zahlenratespiel.
        
        Args:
            min_zahl: Untere Grenze des Zahlenbereichs
            max_zahl: Obere Grenze des Zahlenbereichs
            max_versuche: Maximale Anzahl an Versuchen
        """
        self.min_zahl = min_zahl
        self.max_zahl = max_zahl
        self.max_versuche = max_versuche
        self.versuche = 0
        self.punkte = 100
        self.geheimzahl = 0
        self.verloren = False
        self.gewonnen = False
        self.rateversuche = []
        
        # Spiel initialisieren
        self._neue_zahl_waehlen()
        
    def _neue_zahl_waehlen(self) -> None:
        """Wählt eine neue geheime Zahl für das Spiel aus."""
        self.geheimzahl = random.randint(self.min_zahl, self.max_zahl)
        self.versuche = 0
        self.punkte = 100
        self.verloren = False
        self.gewonnen = False
        self.rateversuche = []
        
    def rate(self, zahl: int) -> Tuple[bool, str, int]:
        """
        Verarbeitet einen Rateversuch des Spielers.
        
        Args:
            zahl: Die geratene Zahl
            
        Returns:
            Tuple mit (Erfolg, Hinweis, Punktzahl)
        """
        # Rateversuch speichern
        self.rateversuche.append(zahl)
        self.versuche += 1
        
        # Differenz berechnen
        differenz = abs(zahl - self.geheimzahl)
        
        # Punkte reduzieren basierend auf der Differenz und Anzahl der Versuche
        punkte_abzug = min(10, max(1, int(differenz / 5))) + min(5, self.versuche)
        self.punkte = max(0, self.punkte - punkte_abzug)
        
        # Prüfen, ob die Zahl richtig ist
        if zahl == self.geheimzahl:
            self.gewonnen = True
            return True, f"Glückwunsch! Du hast die Zahl {self.geheimzahl} nach {self.versuche} Versuchen erraten!", self.punkte
        
        # Prüfen, ob maximale Versuche erreicht sind
        if self.versuche >= self.max_versuche:
            self.verloren = True
            return False, f"Leider verloren! Die gesuchte Zahl war {self.geheimzahl}.", 0
        
        # Hinweis generieren
        hinweis = self._hinweis_generieren(zahl)
        
        return False, hinweis, self.punkte
        
    def _hinweis_generieren(self, zahl: int) -> str:
        """
        Generiert einen Hinweis basierend auf der geratenen Zahl.
        
        Args:
            zahl: Die geratene Zahl
            
        Returns:
            Ein Hinweis als String
        """
        # Grundlegende Hinweise
        if zahl < self.geheimzahl:
            basis_hinweis = "Die gesuchte Zahl ist größer."
        else:
            basis_hinweis = "Die gesuchte Zahl ist kleiner."
            
        # Zusätzliche Hinweise basierend auf der Anzahl der Versuche
        zusatz_hinweise = []
        
        # Ab dem zweiten Versuch mehr Hinweise geben
        if self.versuche >= 2:
            # Hinweis zur Teilbarkeit
            teiler = [2, 3, 5]
            for t in teiler:
                if self.geheimzahl % t == 0:
                    zusatz_hinweise.append(f"Die Zahl ist durch {t} teilbar.")
                    break  # Nur einen Teilbarkeitshinweis geben
                    
        # Ab dem dritten Versuch noch detailliertere Hinweise
        if self.versuche >= 3:
            # Gerade/Ungerade Hinweis
            if self.geheimzahl % 2 == 0:
                zusatz_hinweise.append("Es ist eine gerade Zahl.")
            else:
                zusatz_hinweise.append("Es ist eine ungerade Zahl.")
                
        # Ab dem vierten Versuch einen Hinweis zur Differenz geben
        if self.versuche >= 4:
            differenz = abs(zahl - self.geheimzahl)
            
            if differenz <= 5:
                zusatz_hinweise.append("Du bist sehr nah dran!")
            elif differenz <= 10:
                zusatz_hinweise.append("Du kommst der Zahl näher.")
            elif differenz <= 20:
                zusatz_hinweise.append("Du bist noch etwas entfernt.")
            else:
                zusatz_hinweise.append("Du bist noch weit entfernt.")
                
        # Ab dem fünften Versuch Hinweis zur Ziffernsumme geben
        if self.versuche >= 5:
            ziffernsumme = sum(int(ziffer) for ziffer in str(self.geheimzahl))
            zusatz_hinweise.append(f"Die Ziffernsumme ist {ziffernsumme}.")
            
        # Ab dem sechsten Versuch Bereichshinweise geben
        if self.versuche >= 6:
            zehnerstelle = (self.geheimzahl // 10) * 10
            zusatz_hinweise.append(f"Die Zahl liegt zwischen {zehnerstelle} und {zehnerstelle + 9}.")
            
        # Nur bis zu 2 zusätzliche Hinweise hinzufügen (um nicht zu viel zu verraten)
        if zusatz_hinweise:
            return f"{basis_hinweis} {' '.join(zusatz_hinweise[:2])}"
        else:
            return basis_hinweis
        
    def neues_spiel(self, min_zahl: Optional[int] = None, max_zahl: Optional[int] = None, 
                   max_versuche: Optional[int] = None) -> None:
        """
        Startet ein neues Spiel mit optionalen neuen Parametern.
        
        Args:
            min_zahl: Neue untere Grenze (optional)
            max_zahl: Neue obere Grenze (optional)
            max_versuche: Neue maximale Anzahl an Versuchen (optional)
        """
        if min_zahl is not None:
            self.min_zahl = min_zahl
            
        if max_zahl is not None:
            self.max_zahl = max_zahl
            
        if max_versuche is not None:
            self.max_versuche = max_versuche
            
        self._neue_zahl_waehlen()
        
    def get_spielzustand(self) -> dict:
        """
        Gibt den aktuellen Spielzustand zurück.
        
        Returns:
            Dictionary mit dem aktuellen Spielzustand
        """
        return {
            "min_zahl": self.min_zahl,
            "max_zahl": self.max_zahl,
            "max_versuche": self.max_versuche,
            "versuche": self.versuche,
            "punkte": self.punkte,
            "gewonnen": self.gewonnen,
            "verloren": self.verloren,
            "rateversuche": self.rateversuche
        }
        
    def get_optimale_strategie(self) -> List[int]:
        """
        Berechnet die optimale Strategie für das Raten mit binärer Suche.
        
        Returns:
            Liste der optimalen Rateversuche
        """
        # Binäre Suche simulieren
        low = self.min_zahl
        high = self.max_zahl
        zahl = self.geheimzahl
        strategie = []
        
        while low <= high:
            mid = (low + high) // 2
            strategie.append(mid)
            
            if mid == zahl:
                break
            elif mid < zahl:
                low = mid + 1
            else:
                high = mid - 1
                
        return strategie


def print_willkommen() -> None:
    """Gibt einen Willkommenstext für das Spiel aus."""
    print("\n" + "=" * 60)
    print("               Z A H L E N   R A T E N")
    print("=" * 60)
    print("Errate die geheime Zahl, die der Computer ausgewählt hat!")
    print("Bei jedem Versuch erhältst du einen Hinweis.")
    print("Je weniger Versuche du benötigst, desto mehr Punkte erhältst du!")
    print("=" * 60)


def print_help() -> None:
    """Zeigt die Hilfeübersicht für das Zahlenratespiel an."""
    print("\nZahlenratespiel Hilfe")
    print("===================")
    print("Befehle:")
    print("  start            - Startet ein neues Spiel mit Standardeinstellungen")
    print("  start <min> <max> <versuche> - Startet ein Spiel mit eigenen Parametern")
    print("  hinweis          - Gibt einen zusätzlichen Hinweis")
    print("  hilfe            - Diese Hilfeübersicht anzeigen")
    print("  exit/quit        - Programm beenden")
    print("\nSpiel:")
    print("  - Gib eine Zahl ein, um zu raten")
    print("  - Du verlierst Punkte für jeden Versuch und basierend auf der Differenz")
    print("  - Nach jedem Versuch erhältst du einen Hinweis")
    print("  - Mit jedem weiteren Versuch werden die Hinweise detaillierter")


def spielen() -> None:
    """Hauptfunktion zum Starten und Spielen des Spiels."""
    print_willkommen()
    
    # Standard-Spielparameter
    min_zahl = 1
    max_zahl = 100
    max_versuche = 10
    
    spiel = ZahlenRaten(min_zahl, max_zahl, max_versuche)
    print(f"\nIch habe mir eine Zahl zwischen {min_zahl} und {max_zahl} ausgedacht.")
    print(f"Du hast {max_versuche} Versuche. Viel Glück!")
    
    # Hauptspielschleife
    while not (spiel.gewonnen or spiel.verloren):
        try:
            # Eingabe vom Benutzer holen
            eingabe = input("\nDein Tipp (oder 'hilfe', 'exit'): ").strip().lower()
            
            # Befehlseingaben überprüfen
            if eingabe in ['exit', 'quit', 'beenden']:
                print("Spiel wird beendet.")
                print(f"Die gesuchte Zahl war: {spiel.geheimzahl}")
                return
                
            elif eingabe in ['hilfe', 'help', '?']:
                print_help()
                continue
                
            elif eingabe in ['start', 'neu', 'restart']:
                print("Neues Spiel wird gestartet...")
                spiel.neues_spiel()
                print(f"\nIch habe mir eine neue Zahl zwischen {spiel.min_zahl} und {spiel.max_zahl} ausgedacht.")
                print(f"Du hast {spiel.max_versuche} Versuche. Viel Glück!")
                continue
                
            elif eingabe.startswith('start '):
                # Eigene Parameter für ein neues Spiel
                teile = eingabe.split()[1:]
                if len(teile) >= 3:
                    try:
                        neuer_min = int(teile[0])
                        neuer_max = int(teile[1])
                        neue_versuche = int(teile[2])
                        
                        if neuer_min >= neuer_max:
                            print("Fehler: Minimum muss kleiner als Maximum sein.")
                            continue
                            
                        if neue_versuche <= 0:
                            print("Fehler: Anzahl der Versuche muss positiv sein.")
                            continue
                            
                        spiel.neues_spiel(neuer_min, neuer_max, neue_versuche)
                        print(f"\nIch habe mir eine neue Zahl zwischen {neuer_min} und {neuer_max} ausgedacht.")
                        print(f"Du hast {neue_versuche} Versuche. Viel Glück!")
                    except ValueError:
                        print("Fehler: Ungültige Parameter. Verwende Zahlen.")
                else:
                    print("Fehler: Zu wenig Parameter.")
                    print("Verwendung: start <min> <max> <versuche>")
                continue
                
            elif eingabe in ['hinweis', 'tipp', 'hint']:
                # Zusätzlicher Hinweis, kostet Punkte
                if spiel.versuche == 0:
                    print("Rate erst eine Zahl, bevor du einen Hinweis anforderst.")
                    continue
                    
                # Punkte für Hinweis abziehen
                spiel.punkte = max(0, spiel.punkte - 5)
                
                # Spezifischen Hinweis generieren
                if spiel.geheimzahl % 2 == 0:
                    paritaet = "gerade"
                else:
                    paritaet = "ungerade"
                    
                print(f"Zusätzlicher Hinweis (kostet 5 Punkte):")
                print(f"Die Zahl ist {paritaet} und liegt zwischen {spiel.min_zahl} und {spiel.max_zahl}.")
                
                # Bei fortgeschrittenem Spiel mehr Hinweise geben
                if spiel.versuche >= 3:
                    ziffernsumme = sum(int(ziffer) for ziffer in str(spiel.geheimzahl))
                    print(f"Die Ziffernsumme beträgt {ziffernsumme}.")
                    
                if spiel.versuche >= 5:
                    erste_ziffer = str(spiel.geheimzahl)[0]
                    print(f"Die erste Ziffer ist {erste_ziffer}.")
                    
                continue
                
            # Versuch, die Eingabe als Zahl zu interpretieren
            try:
                zahl = int(eingabe)
                
                # Überprüfen, ob die Zahl im gültigen Bereich liegt
                if zahl < spiel.min_zahl or zahl > spiel.max_zahl:
                    print(f"Bitte gib eine Zahl zwischen {spiel.min_zahl} und {spiel.max_zahl} ein.")
                    continue
                    
                # Rateversuch verarbeiten
                erfolg, hinweis, punkte = spiel.rate(zahl)
                
                # Rateergebnis anzeigen
                print(f"\n{hinweis}")
                print(f"Versuche: {spiel.versuche}/{spiel.max_versuche} | Punkte: {punkte}")
                
                # Bei Sieg oder Niederlage Spielstatistik anzeigen
                if spiel.gewonnen or spiel.verloren:
                    print("\n" + "=" * 60)
                    if spiel.gewonnen:
                        print(f"Glückwunsch! Du hast die Zahl {spiel.geheimzahl} erraten!")
                        print(f"Benötigte Versuche: {spiel.versuche}/{spiel.max_versuche}")
                        print(f"Punktzahl: {spiel.punkte}/100")
                    else:
                        print(f"Schade! Du hast alle {spiel.max_versuche} Versuche aufgebraucht.")
                        print(f"Die gesuchte Zahl war: {spiel.geheimzahl}")
                        
                    # Optimale Strategie anzeigen
                    print("\nZur Info: Mit binärer Suche hättest du die Zahl so erraten können:")
                    optimale_strategie = spiel.get_optimale_strategie()
                    print(f"  {' -> '.join(map(str, optimale_strategie))}")
                    print(f"  (in {len(optimale_strategie)} Versuchen)")
                    
                    # Fragen, ob ein neues Spiel gestartet werden soll
                    print("\nMöchtest du noch einmal spielen? (j/n)")
                    nochmal = input().strip().lower()
                    
                    if nochmal in ['j', 'ja', 'y', 'yes']:
                        spiel.neues_spiel()
                        print(f"\nIch habe mir eine neue Zahl zwischen {spiel.min_zahl} und {spiel.max_zahl} ausgedacht.")
                        print(f"Du hast {spiel.max_versuche} Versuche. Viel Glück!")
                    else:
                        print("Danke fürs Spielen!")
                        return
                        
            except ValueError:
                print("Bitte gib eine gültige Zahl ein.")
                
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")


def main() -> int:
    """
    Haupteinstiegspunkt für das Zahlenratespiel.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    try:
        spielen()
        return 0
    except KeyboardInterrupt:
        print("\nSpiel wurde unterbrochen.")
        return 1
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
