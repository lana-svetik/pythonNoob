#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# pomodoro-timer.py
# Ein einfacher Pomodoro-Timer für produktives Arbeiten
# Updated 2025-04-17

"""
Ein einfacher Pomodoro-Timer für produktives Arbeiten.

Dieses Programm implementiert die Pomodoro-Technik mit anpassbaren
Arbeits- und Pausenzeiten, inklusive längerer Pausen nach mehreren Arbeitszyklen.
"""

import sys
import time
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class PomodoroTimer:
    """Klasse zur Verwaltung eines Pomodoro-Timers."""
    
    def __init__(
        self,
        work_duration: int = 25,
        short_break_duration: int = 5,
        long_break_duration: int = 15,
        cycles_before_long_break: int = 4
    ):
        """
        Initialisierung des Pomodoro-Timers.
        
        Args:
            work_duration: Dauer der Arbeitsphase in Minuten
            short_break_duration: Dauer der kurzen Pause in Minuten
            long_break_duration: Dauer der langen Pause in Minuten
            cycles_before_long_break: Anzahl der Arbeitszyklen vor einer langen Pause
        """
        self.work_duration = work_duration
        self.short_break_duration = short_break_duration
        self.long_break_duration = long_break_duration
        self.cycles_before_long_break = cycles_before_long_break
        
        self.current_cycle = 0
        self.total_cycles_completed = 0
        self.is_running = False
        self.current_phase = "work"  # "work", "short_break", "long_break"
        
    def start(self) -> None:
        """Startet den Pomodoro-Timer."""
        self.is_running = True
        self.current_cycle = 0
        self.total_cycles_completed = 0
        self.current_phase = "work"
        
        try:
            self._run_timer_loop()
        except KeyboardInterrupt:
            print("\nTimer unterbrochen.")
            self.is_running = False
            
    def _run_timer_loop(self) -> None:
        """Führt die Hauptschleife des Timers aus."""
        while self.is_running:
            if self.current_phase == "work":
                self._run_phase("Arbeitsphase", self.work_duration)
                self.total_cycles_completed += 1
                self.current_cycle += 1
                
                # Entscheiden, ob eine kurze oder lange Pause folgt
                if self.current_cycle >= self.cycles_before_long_break:
                    self.current_phase = "long_break"
                    self.current_cycle = 0
                else:
                    self.current_phase = "short_break"
                    
            elif self.current_phase == "short_break":
                self._run_phase("Kurze Pause", self.short_break_duration)
                self.current_phase = "work"
                
            elif self.current_phase == "long_break":
                self._run_phase("Lange Pause", self.long_break_duration)
                self.current_phase = "work"
                
    def _run_phase(self, phase_name: str, duration_minutes: int) -> None:
        """
        Führt eine einzelne Phase (Arbeit oder Pause) aus.
        
        Args:
            phase_name: Name der Phase zur Anzeige
            duration_minutes: Dauer der Phase in Minuten
        """
        duration_seconds = duration_minutes * 60
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        print(f"\n{phase_name} gestartet ({duration_minutes} Minuten)")
        print(f"Ende um: {end_time.strftime('%H:%M:%S')}")
        
        # Fortschrittsanzeige
        for remaining_seconds in range(duration_seconds, 0, -1):
            mins, secs = divmod(remaining_seconds, 60)
            timer_str = f"{mins:02d}:{secs:02d}"
            
            # Fortschrittsbalken berechnen
            progress = (duration_seconds - remaining_seconds) / duration_seconds
            bar_length = 30
            bar = "=" * int(bar_length * progress) + ">" + " " * (bar_length - int(bar_length * progress) - 1)
            
            # Status ausgeben und Cursor zurücksetzen
            sys.stdout.write(f"\r[{bar}] {timer_str}")
            sys.stdout.flush()
            time.sleep(1)
            
        # Phase abgeschlossen
        sys.stdout.write("\r" + " " * 50 + "\r")  # Zeile löschen
        print(f"{phase_name} abgeschlossen!")
        
        # Benachrichtigung ausgeben
        self._notify(f"{phase_name} abgeschlossen!")
        
    def _notify(self, message: str) -> None:
        """
        Gibt eine Benachrichtigung aus.
        
        Args:
            message: Anzuzeigender Benachrichtigungstext
        """
        # Einfache Konsolenbenachrichtigung
        print("\a")  # Einfacher Piepton (falls vom Terminal unterstützt)
        print("=" * 50)
        print(f"BENACHRICHTIGUNG: {message}")
        print("=" * 50)
        
        # Hier könnte je nach Betriebssystem eine richtige Desktopbenachrichtigung
        # implementiert werden, z.B. mit 'notify-send' unter Linux oder
        # anderen plattformspezifischen Methoden


def print_stats(timer: PomodoroTimer) -> None:
    """
    Gibt Statistiken über die abgeschlossenen Pomodoro-Zyklen aus.
    
    Args:
        timer: PomodoroTimer-Instanz zur Statistikausgabe
    """
    total_work_time = timer.total_cycles_completed * timer.work_duration
    
    print("\nPomodoro-Statistik")
    print("==================")
    print(f"Abgeschlossene Arbeitszyklen: {timer.total_cycles_completed}")
    print(f"Gesamte Arbeitszeit: {total_work_time} Minuten")
    print(f"             ({total_work_time // 60} Stunden, {total_work_time % 60} Minuten)")


def print_help() -> None:
    """Zeigt die Hilfeübersicht für den Pomodoro-Timer an."""
    print("\nPomodoro-Timer Hilfe")
    print("===================")
    print("Befehle:")
    print("  start       - Timer mit Standardeinstellungen starten")
    print("  einstellen  - Timer-Einstellungen anpassen")
    print("  hilfe       - Diese Hilfeübersicht anzeigen")
    print("  exit/quit   - Programm beenden")
    print("\nWährend der Timer läuft:")
    print("  Strg+C drücken, um den Timer zu unterbrechen")


def configure_timer() -> Tuple[int, int, int, int]:
    """
    Konfiguriert die Timer-Einstellungen über Benutzereingaben.
    
    Returns:
        Tupel mit (Arbeitszeit, Kurze Pause, Lange Pause, Zyklen vor langer Pause)
    """
    try:
        print("\nTimer einstellen:")
        work_duration = int(input("Arbeitszeit in Minuten [25]: ") or "25")
        short_break = int(input("Kurze Pause in Minuten [5]: ") or "5")
        long_break = int(input("Lange Pause in Minuten [15]: ") or "15")
        cycles = int(input("Zyklen vor langer Pause [4]: ") or "4")
        
        return work_duration, short_break, long_break, cycles
    except ValueError:
        print("Fehler: Bitte gib nur Zahlen ein.")
        return 25, 5, 15, 4


def main() -> int:
    """
    Haupteinstiegspunkt für den Pomodoro-Timer.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    print("Pomodoro-Timer")
    print("'hilfe' für Hilfeübersicht, 'exit' zum Beenden")
    
    # Standardeinstellungen
    work_duration = 25
    short_break = 5
    long_break = 15
    cycles_before_long_break = 4
    
    timer = PomodoroTimer(
        work_duration=work_duration,
        short_break_duration=short_break,
        long_break_duration=long_break,
        cycles_before_long_break=cycles_before_long_break
    )
    
    while True:
        # Benutzereingabe
        user_input = input("\nBefehl: ").strip().lower()
        
        # Überprüfen auf Befehle
        if user_input in ['exit', 'quit', 'beenden']:
            if timer.total_cycles_completed > 0:
                print_stats(timer)
            print("Programm wird beendet.")
            return 0
            
        elif user_input in ['start', 'starten', 'los']:
            timer.start()
            
        elif user_input in ['einstellen', 'konfigurieren', 'config']:
            work_duration, short_break, long_break, cycles_before_long_break = configure_timer()
            timer = PomodoroTimer(
                work_duration=work_duration,
                short_break_duration=short_break,
                long_break_duration=long_break,
                cycles_before_long_break=cycles_before_long_break
            )
            print(f"Timer konfiguriert: {work_duration} Min Arbeit, {short_break} Min kurze Pause, "
                  f"{long_break} Min lange Pause nach {cycles_before_long_break} Zyklen")
                  
        elif user_input in ['hilfe', 'help', '?']:
            print_help()
            
        elif user_input in ['stats', 'statistik']:
            print_stats(timer)
            
        else:
            print("Unbekannter Befehl. Gib 'hilfe' für eine Übersicht der Befehle ein.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
