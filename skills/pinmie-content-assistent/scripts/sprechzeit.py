#!/usr/bin/env python3
"""sprechzeit.py - misst, wie lange ein deutscher Sprechtext dauert, und prüft den Takt.

Teil des PINMIE Content-Assistenten (pinmie.de).

Annahme: etwa 150 Wörter pro Minute, das ist ruhiges, natürliches Sprechen vor der Kamera.
Jede Zeile im Text ist ein Abschnitt (eine Einstellung). Leerzeilen werden ignoriert.

Geprüft wird:
  - erster Abschnitt länger als 3 Sekunden (der Einstieg muss schnell sitzen)
  - ein Abschnitt länger als 6 Sekunden (dort wird es zäh, Schnitt oder Bildwechsel einplanen)
  - Satz mit mehr als 20 Wörtern (beim Sprechen schwer, lieber teilen)
  - Gesamtlänge im Vergleich zum Ziel (--ziel), Abweichung über 20 Prozent

Aufruf
  python3 sprechzeit.py skript.txt
  python3 sprechzeit.py skript.txt --ziel 30
  python3 sprechzeit.py skript.txt --wpm 165     # wer schneller spricht
"""
import argparse
import re
import sys

WORT = re.compile(r"[A-Za-zÄÖÜäöüß0-9€%]+")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--ziel", type=float, help="Ziellänge in Sekunden")
    ap.add_argument("--wpm", type=float, default=150.0, help="Wörter pro Minute (Standard 150)")
    a = ap.parse_args()
    zeilen = [z.strip() for z in open(a.datei, encoding="utf-8") if z.strip()]
    if not zeilen:
        sys.exit("Der Text ist leer.")
    proSek = a.wpm / 60
    t = 0.0
    warn = []
    print(f"\nSPRECHZEIT ({a.wpm:.0f} Wörter pro Minute)\n")
    for i, z in enumerate(zeilen, 1):
        n = len(WORT.findall(z))
        d = n / proSek + 0.3 * len(re.findall(r"[.!?]", z))  # kurze Pause je Satzende
        print(f"{t:5.1f} s  +{d:4.1f} s  {z[:80]}")
        if i == 1 and d > 3:
            warn.append(f"Abschnitt 1 dauert {d:.1f} s. Der Einstieg sollte in höchstens 3 Sekunden gesagt sein.")
        if d > 6:
            warn.append(f"Abschnitt {i} dauert {d:.1f} s. Teilen oder einen Bildwechsel einplanen.")
        for s in re.split(r"(?<=[.!?])\s+", z):
            if len(WORT.findall(s)) > 20:
                warn.append(f"Abschnitt {i}: Satz mit {len(WORT.findall(s))} Wörtern. Beim Sprechen lieber teilen.")
        t += d
    print(f"\nGesamt: {t:.1f} Sekunden, {len(zeilen)} Abschnitte")
    if a.ziel:
        abw = (t - a.ziel) / a.ziel
        if abs(abw) > 0.2:
            richtung = "zu lang" if abw > 0 else "zu kurz"
            warn.append(f"Gesamt {t:.0f} s statt {a.ziel:.0f} s, {abs(abw) * 100:.0f} Prozent {richtung}.")
    if warn:
        print("\nWARNUNGEN")
        for w in warn:
            print(f"  · {w}")
        sys.exit(1)
    print("Keine Warnungen.")


if __name__ == "__main__":
    main()
