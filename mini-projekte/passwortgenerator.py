#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# passwortgenerator.py
# Generator für sichere Passwörter nach spezifischem Muster
# Updated 2025-03-02

"""
Generator für sichere Passwörter nach spezifischem Muster.

Dieses Programm erzeugt Passwörter im Format: xxxxxx-xxxxxx-xxxxxx
Jede Gruppe besteht aus kleinen Buchstaben, mit beschränkter Anzahl 
von Großbuchstaben (max. 2) und Zahlen (max. 1) pro Gruppe.
"""

import random
import string
import sys
from typing import List, Tuple


def generate_group(length: int = 6, max_uppercase: int = 2, max_digits: int = 1) -> str:
    """
    Erzeugt eine Gruppe von Zeichen für das Passwort.
    
    Args:
        length: Länge der zu erstellenden Gruppe
        max_uppercase: Maximale Anzahl von Großbuchstaben in der Gruppe
        max_digits: Maximale Anzahl von Ziffern in der Gruppe
        
    Returns:
        Eine Zeichenkette mit zufälligen Zeichen
    """
    # Sicherstellen, dass die Einschränkungen sinnvoll sind
    if max_uppercase + max_digits > length:
        raise ValueError("Die Summe aus max_uppercase und max_digits darf length nicht überschreiten")
    
    # Entscheiden, wie viele von jedem Zeichentyp verwendet werden
    num_uppercase = random.randint(0, max_uppercase)
    num_digits = random.randint(0, max_digits)
    num_lowercase = length - num_uppercase - num_digits
    
    # Zeichen für jede Kategorie generieren
    uppercase_chars = random.choices(string.ascii_uppercase, k=num_uppercase)
    digit_chars = random.choices(string.digits, k=num_digits)
    lowercase_chars = random.choices(string.ascii_lowercase, k=num_lowercase)
    
    # Alle Zeichen kombinieren und mischen
    all_chars = uppercase_chars + digit_chars + lowercase_chars
    random.shuffle(all_chars)
    
    # Als String zurückgeben
    return ''.join(all_chars)


def generate_password(
    num_groups: int = 3, 
    group_length: int = 6, 
    separator: str = "-",
    max_uppercase: int = 2,
    max_digits: int = 1
) -> str:
    """
    Erzeugt ein Passwort aus mehreren Zeichengruppen.
    
    Args:
        num_groups: Anzahl der zu erzeugenden Gruppen
        group_length: Länge jeder Gruppe
        separator: Trennzeichen zwischen den Gruppen
        max_uppercase: Maximale Anzahl von Großbuchstaben pro Gruppe
        max_digits: Maximale Anzahl von Ziffern pro Gruppe
        
    Returns:
        Ein Passwort bestehend aus mehreren Zeichengruppen
    """
    groups = [
        generate_group(group_length, max_uppercase, max_digits)
        for _ in range(num_groups)
    ]
    
    return separator.join(groups)


def main() -> int:
    """
    Haupteinstiegspunkt für den Passwortgenerator.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    print("Passwortgenerator")
    print("Format: xxxxxx-xxxxxx-xxxxxx")
    print("'exit' zum Beenden, 'neu' für ein neues Passwort")
    
    while True:
        # Benutzereingabe
        user_input = input("\nBefehl: ").strip().lower()
        
        # Überprüfen auf Befehle
        if user_input in ['exit', 'quit', 'beenden']:
            print("Programm wird beendet.")
            return 0
        elif user_input in ['neu', 'pw', 'generate']:
            try:
                password = generate_password()
                print(f"Generiertes Passwort: {password}")
            except Exception as e:
                print(f"Fehler bei der Passworterzeugung: {e}")
        else:
            print("Unbekannter Befehl. Gib 'neu' für ein neues Passwort ein oder 'exit' zum Beenden.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
