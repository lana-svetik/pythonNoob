#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# schere_stein_papier.py
# Ein einfaches Spiel – Schere, Stein, Papier
# Updated 2025-04-18

"""
Ein einfaches Spiel – Schere, Stein, Papier.

Dieses Programm ermöglicht dem Benutzer, Schere, Stein, Papier gegen 
den Computer zu spielen und den Spielstand zu verfolgen.
"""

import random
import sys
import time
from typing import Tuple, Dict, List, Optional


class SchereSteinPapier:
    """Klasse zur Verwaltung eines Schere-Stein-Papier-Spiels."""
    
    # Mögliche Züge
    ZUEGE = ["schere", "stein", "papier"]
    
    # Alternativen Eingaben für die Züge
    ZUG_ALTERNATIVEN = {
        "schere": ["s", "sc", "sch", "scissors"],
        "stein": ["st", "rock", "r"],
        "papier": ["p", "pa", "paper"]
    }
    
    # ASCII-Art für die Züge
    ZUEGE_ASCII = {
        "schere": """
    _       ,/'
   (_).  ,/'
   __  ::
  (__)'  `\.
            `\.
        """,
        "stein": """
      _______
  ---'   ____)
        (_____)
        (_____)
        (____)
  ---.__(___)
        """,
        "papier": """
      _______
  ---'   ____)____
            ______)
            _______)
           _______)
  ---.__________)
        """
    }
    
    def __init__(self):
        """Initialisiert ein neues Schere-Stein-Papier-Spiel."""
        self.spieler_punkte = 0
        self.computer_punkte = 0
        self.unentschieden = 0
        self.runden = 0
        self.letzter_spieler_zug = None
        self.letzter_computer_zug = None
        
    def ist_zulaessiger_zug(self, zug: str) -> bool:
        """
        Überprüft, ob ein Zug zulässig ist.
        
        Args:
            zug: Der zu überprüfende Zug
            
        Returns:
            True, wenn der Zug zulässig ist, sonst False
        """
        zug = zug.lower()
        
        # Direkter Zug
        if zug in self.ZUEGE:
            return True
            
        # Alternative Eingabe
        for echte_zuege, alternativen in self.ZUG_ALTERNATIVEN.items():
            if zug in alternativen:
                return True
                
        return False
        
    def normalisiere_zug(self, zug: str) -> str:
        """
        Normalisiert einen Zug auf einen der Standardzüge.
        
        Args:
            zug: Der zu normalisierende Zug
            
        Returns:
            Der normalisierte Zug
        """
        zug = zug.lower()
        
        # Direkter Zug
        if zug in self.ZUEGE:
            return zug
            
        # Alternative Eingabe
        for echter_zug, alternativen in self.ZUG_ALTERNATIVEN.items():
            if zug in alternativen:
                return echter_zug
                
        # Sollte nicht vorkommen, wenn ist_zulaessiger_zug vorher aufgerufen wurde
        return zug
        
    def computer_zug(self) -> str:
        """
        Generiert einen zufälligen Zug für den Computer.
        
        Returns:
            Der Zug des Computers
        """
        return random.choice(self.ZUEGE)
        
    def bestimme_gewinner(self, spieler_zug: str, computer_zug: str) -> int:
        """
        Bestimmt den Gewinner einer Runde.
        
        Args:
            spieler_zug: Der Zug des Spielers
            computer_zug: Der Zug des Computers
            
        Returns:
            1 für Spielersieg, -1 für Computersieg, 0 für Unentschieden
        """
        # Unentschieden
        if spieler_zug == computer_zug:
            return 0
            
        # Spieler gewinnt
        if ((spieler_zug == "schere" and computer_zug == "papier") or
            (spieler_zug == "stein" and computer_zug == "schere") or
            (spieler_zug == "papier" and computer_zug == "stein")):
            return 1
            
        # Computer gewinnt
        return -1
        
    def aktualisiere_punktestand(self, ergebnis: int) -> None:
        """
        Aktualisiert den Punktestand basierend auf dem Ergebnis.
        
        Args:
            ergebnis: Das Ergebnis der Runde (1, -1 oder 0)
        """
        self.runden += 1
        
        if ergebnis == 1:
            self.spieler_punkte += 1
        elif ergebnis == -1:
            self.computer_punkte += 1
        else:
            self.unentschieden += 1
            
    def spielrunde(self, spieler_zug: str) -> Tuple[int, str]:
        """
        Führt eine Spielrunde durch.
        
        Args:
            spieler_zug: Der Zug des Spielers
            
        Returns:
            Tuple mit (Ergebnis, Nachricht)
        """
        # Spielerzug normalisieren
        spieler_zug = self.normalisiere_zug(spieler_zug)
        
        # Computerzug generieren
        computer_zug = self.computer_zug()
        
        # Züge speichern
        self.letzter_spieler_zug = spieler_zug
        self.letzter_computer_zug = computer_zug
        
        # Gewinner bestimmen
        ergebnis = self.bestimme_gewinner(spieler_zug, computer_zug)
        
        # Punktestand aktualisieren
        self.aktualisiere_punktestand(ergebnis)
        
        # Nachricht generieren
        if ergebnis == 1:
            nachricht = f"Du gewinnst! {spieler_zug.capitalize()} schlägt {computer_zug}."
        elif ergebnis == -1:
            nachricht = f"Du verlierst! {computer_zug.capitalize()} schlägt {spieler_zug}."
        else:
            nachricht = f"Unentschieden! Beide wählen {spieler_zug}."
            
        return ergebnis, nachricht
        
    def get_statistik(self) -> Dict[str, int]:
        """
        Gibt die Spielstatistik zurück.
        
        Returns:
            Dictionary mit Spielstatistiken
        """
        return {
            "spieler_punkte": self.spieler_punkte,
            "computer_punkte": self.computer_punkte,
            "unentschieden": self.unentschieden,
            "runden": self.runden
        }
        
    def zeige_ascii_art(self, spieler_zug: str, computer_zug: str) -> None:
        """
        Zeigt ASCII-Art für die Züge an.
        
        Args:
            spieler_zug: Der Zug des Spielers
            computer_zug: Der Zug des Computers
        """
        spieler_ascii = self.ZUEGE_ASCII.get(spieler_zug, "")
        computer_ascii = self.ZUEGE_ASCII.get(computer_zug, "")
        
        # Splitten und Zeilen für Nebeneinanderstellung vorbereiten
        spieler_linien = spieler_ascii.split("\n")
        computer_linien = computer_ascii.split("\n")
        
        # Maximale Anzahl an Zeilen bestimmen
        max_zeilen = max(len(spieler_linien), len(computer_linien))
        
        # Ausgabe formatieren
        print("\n" + "=" * 50)
        print("Spieler" + " " * 16 + "vs." + " " * 17 + "Computer")
        print("=" * 50)
        
        for i in range(max_zeilen):
            spieler_linie = spieler_linien[i] if i < len(spieler_linien) else ""
            computer_linie = computer_linien[i] if i < len(computer_linien) else ""
            
            # Gepolsterte Ausgabe
            print(f"{spieler_linie:<25}{computer_linie}")
            
        print("=" * 50)
        
    def zeige_punktestand(self) -> None:
        """Zeigt den aktuellen Punktestand an."""
        print("\nPunktestand:")
        print(f"Spieler: {self.spieler_punkte}  |  Computer: {self.computer_punkte}  |  Unentschieden: {self.unentschieden}")
        print(f"Gespielte Runden: {self.runden}")


def animiere_countdown() -> None:
    """Zeigt einen animierten Countdown an."""
    print("\nSchere, Stein, Papier...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.5)
    print("Los!")


def print_help() -> None:
    """Zeigt die Hilfeübersicht für das Spiel an."""
    print("\nSchere, Stein, Papier - Hilfe")
    print("============================")
    print("Befehle:")
    print("  schere/s       - Wähle Schere")
    print("  stein/st       - Wähle Stein")
    print("  papier/p       - Wähle Papier")
    print("  statistik      - Zeigt die Spielstatistik an")
    print("  hilfe          - Diese Hilfeübersicht anzeigen")
    print("  exit/quit      - Spiel beenden")
    print("\nSpielregeln:")
    print("  - Schere schlägt Papier")
    print("  - Stein schlägt Schere")
    print("  - Papier schlägt Stein")


def main() -> int:
    """
    Haupteinstiegspunkt für das Schere-Stein-Papier-Spiel.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    print("===== Schere, Stein, Papier =====")
    print("'hilfe' für Hilfeübersicht, 'exit' zum Beenden")
    
    spiel = SchereSteinPapier()
    
    while True:
        try:
            # Benutzereingabe
            user_input = input("\nDein Zug (schere/stein/papier): ").strip().lower()
            
            # Leere Eingabe überspringen
            if not user_input:
                continue
                
            # Spezielle Befehle verarbeiten
            if user_input in ['exit', 'quit', 'beenden']:
                print("Spiel wird beendet.")
                return 0
                
            elif user_input in ['hilfe', 'help', '?']:
                print_help()
                
            elif user_input in ['statistik', 'stats', 'punkte', 'score']:
                statistik = spiel.get_statistik()
                
                print("\nSpielstatistik")
                print("==============")
                print(f"Spieler: {statistik['spieler_punkte']} Punkte")
                print(f"Computer: {statistik['computer_punkte']} Punkte")
                print(f"Unentschieden: {statistik['unentschieden']}")
                print(f"Gespielte Runden: {statistik['runden']}")
                
                if statistik['runden'] > 0:
                    gewinnrate = (statistik['spieler_punkte'] / statistik['runden']) * 100
                    print(f"Deine Gewinnrate: {gewinnrate:.1f}%")
                    
            elif spiel.ist_zulaessiger_zug(user_input):
                # Zug normalisieren
                zug = spiel.normalisiere_zug(user_input)
                
                # Countdown Animation
                animiere_countdown()
                
                # Spielrunde durchführen
                ergebnis, nachricht = spiel.spielrunde(zug)
                
                # ASCII-Art anzeigen
                spiel.zeige_ascii_art(spiel.letzter_spieler_zug, spiel.letzter_computer_zug)
                
                # Ergebnis anzeigen
                print(f"\n{nachricht}")
                
                # Punktestand anzeigen
                spiel.zeige_punktestand()
                
            else:
                print(f"Ungültiger Zug: {user_input}")
                print("Gültige Züge: schere, stein, papier (oder s, st, p)")
                
        except KeyboardInterrupt:
            print("\nSpiel wird beendet.")
            return 0
            
        except Exception as e:
            print(f"\nEin Fehler ist aufgetreten: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
