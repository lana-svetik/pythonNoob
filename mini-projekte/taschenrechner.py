#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# taschenrechner.py
# Ein einfacher Taschenrechner mit Kommandozeilenschnittstelle
# Updated 2025-02-19

"""
Ein einfacher Taschenrechner mit Kommandozeilenschnittstelle.

Dieses Programm bietet grundlegende arithmetische Operationen mit Klammerunterstützung
und fungiert als Einstiegsprojekt für Python-Anfänger.
"""

import sys
import re
from typing import Dict, List, Tuple, Union, Optional


def add(a: float, b: float) -> float:
    """Addiert zwei Zahlen."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtrahiert b von a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multipliziert zwei Zahlen."""
    return a * b


def divide(a: float, b: float) -> Optional[float]:
    """
    Dividiert a durch b.
    
    Returns:
        Das Ergebnis der Division oder None, wenn durch 0 geteilt wird
    """
    if b == 0:
        print("Fehler: Division durch Null ist nicht erlaubt.")
        return None
    return a / b


def tokenize(expression: str) -> List[str]:
    """
    Zerlegt einen mathematischen Ausdruck in Tokens.
    
    Args:
        expression: Der zu zerlegende mathematische Ausdruck
        
    Returns:
        Liste der erkannten Tokens (Zahlen, Operatoren, Klammern)
    """
    # Alle Leerzeichen entfernen
    expression = expression.replace(" ", "")
    
    # Regex-Muster für Zahlen und Operatoren
    pattern = r'(\d*\.\d+|\d+|[\+\-\*/\(\)])'
    tokens = re.findall(pattern, expression)
    
    return tokens


def evaluate_expression(expression: str) -> Optional[float]:
    """
    Wertet einen mathematischen Ausdruck aus, der Klammern enthalten kann.
    
    Args:
        expression: Der auszuwertende mathematische Ausdruck
        
    Returns:
        Das Ergebnis der Berechnung oder None bei Fehlern
    """
    tokens = tokenize(expression)
    
    def parse():
        """
        Rekursive Funktion zum Analysieren und Auswerten des Ausdrucks.
        """
        def parse_expression():
            left = parse_term()
            while tokens and tokens[0] in ['+', '-']:
                op = tokens.pop(0)
                right = parse_term()
                if op == '+':
                    left = left + right
                else:  # op == '-'
                    left = left - right
            return left
            
        def parse_term():
            left = parse_factor()
            while tokens and tokens[0] in ['*', '/']:
                op = tokens.pop(0)
                right = parse_factor()
                if op == '*':
                    left = left * right
                else:  # op == '/'
                    if right == 0:
                        raise ValueError("Division durch Null ist nicht erlaubt.")
                    left = left / right
            return left
            
        def parse_factor():
            if not tokens:
                raise ValueError("Unerwartetes Ende des Ausdrucks")
                
            token = tokens.pop(0)
            
            # Klammer auf
            if token == '(':
                value = parse_expression()
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Fehlende schließende Klammer")
                return value
                
            # Negative Zahl
            elif token == '-':
                return -parse_factor()
                
            # Zahl
            else:
                try:
                    return float(token)
                except ValueError:
                    raise ValueError(f"Ungültiges Token: {token}")
                    
        return parse_expression()
    
    try:
        result = parse()
        return result
    except ValueError as e:
        print(f"Fehler: {e}")
        return None
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        return None


def print_help() -> None:
    """Zeigt die Hilfeübersicht für den Taschenrechner an."""
    print("\nEinfacher Taschenrechner")
    print("------------------------")
    print("Unterstützte Operationen:")
    print("  + : Addition (z. B. 5 + 3)")
    print("  - : Subtraktion (z. B. 5 - 3)")
    print("  * : Multiplikation (z. B. 5 * 3)")
    print("  / : Division (z. B. 5 / 3)")
    print("  ( ) : Klammern für Vorrang (z. B. 2 * (3 + 4))")
    print("\nBefehle:")
    print("  help : Hilfeübersicht anzeigen")
    print("  exit/quit : Programm beenden")
    print("\nFormat: Mathematischer Ausdruck (z. B. 5 + 3 * 2 oder (2 + 3) * 4)")


def main() -> int:
    """
    Haupteinstiegspunkt für den Taschenrechner.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    print("Einfacher Taschenrechner")
    print("'help' für Hilfeübersicht, 'exit' zum Beenden")
    
    while True:
        # Benutzereingabe
        user_input = input("\nBerechnung: ").strip()
        
        # Überprüfen auf Befehle
        if user_input.lower() in ['exit', 'quit']:
            print("Programm wird beendet.")
            return 0
        elif user_input.lower() == 'help':
            print_help()
            continue
        
        # Rechenoperation ausführen
        try:
            result = evaluate_expression(user_input)
            
            if result is not None:
                # Ausgabe ohne Nachkommastellen, wenn das Ergebnis ganzzahlig ist
                if result == int(result):
                    print(f"Ergebnis: {int(result)}")
                else:
                    print(f"Ergebnis: {result}")
                    
        except ValueError as e:
            print(f"Fehler: {e}")
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
