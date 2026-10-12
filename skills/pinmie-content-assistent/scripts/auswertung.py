#!/usr/bin/env python3
"""auswertung.py - findet Ausreißer unter den eigenen Reels und erkennt vermutlich bezahlte Beiträge.

Teil des PINMIE Content-Assistenten (pinmie.de).

Eingabe: CSV mit Kopfzeile, Trenner ; oder , oder Tab. Pflichtspalten: titel, aufrufe.
Optional: datum, likes, kommentare, geteilt, gespeichert, format.
Zahlen dürfen deutsche Tausenderpunkte haben (12.300) oder Kürzel (12,3 Tsd., 1,2 Mio.).

Rechnung:
  - Median der Aufrufe aller Reels
  - Vielfaches = Aufrufe geteilt durch Median
  - vermutlich bezahlt: Vielfaches mindestens 3 und Likes unter 0,3 Prozent der Aufrufe
    (in der PINMIE-Auswertung deutscher Firmenkonten lagen organische Ausreißer zwischen 0,7 und 3,5 Prozent)
  - Ausreißer: Vielfaches mindestens 5, nicht bezahlt
  - Zusammenfassung je Format, wenn die Spalte da ist (bezahlte Reels nicht mitgezählt)

Aufruf
  python3 auswertung.py reels.csv
  python3 auswertung.py reels.csv --json
"""
import argparse
import csv
import json
import re
import statistics
import sys


def zahl(s):
    if s is None:
        return None
    s = str(s).strip().lower().replace(" ", "")
    if not s:
        return None
    f = 1
    if "mio" in s:
        f = 1_000_000
    elif "tsd" in s or s.endswith("k"):
        f = 1_000
    s = re.sub(r"[^0-9,\.]", "", s)
    if f > 1:
        s = s.replace(".", "").replace(",", ".")
        return round(float(s) * f) if s else None
    s = s.replace(".", "").replace(",", "")
    return int(s) if s else None


def tsd(n):
    return f"{n:,.0f}".replace(",", ".")


def proz(x):
    return (f"{x:.2f}" if x < 1 else f"{x:.1f}").replace(".", ",") + " %"


def lies(datei):
    roh = open(datei, encoding="utf-8-sig").read()
    trenner = max([";", "\t", ","], key=roh.splitlines()[0].count)
    zeilen = list(csv.DictReader(roh.splitlines(), delimiter=trenner))
    out = []
    for z in zeilen:
        z = {k.strip().lower(): (v or "").strip() for k, v in z.items() if k}
        a = zahl(z.get("aufrufe"))
        if a is None:
            continue
        out.append({"datum": z.get("datum", ""), "titel": z.get("titel", ""), "aufrufe": a,
                    "likes": zahl(z.get("likes")), "kommentare": zahl(z.get("kommentare")),
                    "geteilt": zahl(z.get("geteilt")), "gespeichert": zahl(z.get("gespeichert")),
                    "format": z.get("format", "").lower()})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    reels = lies(a.datei)
    if len(reels) < 3:
        sys.exit("Zu wenige Reels mit Aufrufen gefunden. Spalten 'titel' und 'aufrufe' prüfen.")
    med = statistics.median(r["aufrufe"] for r in reels)
    for r in reels:
        r["vielfaches"] = round(r["aufrufe"] / med, 1) if med else 0
        r["like_quote"] = round(100 * r["likes"] / r["aufrufe"], 2) if r["likes"] is not None and r["aufrufe"] else None
        r["bezahlt"] = bool(r["vielfaches"] >= 3 and r["like_quote"] is not None and r["like_quote"] < 0.3)
        r["ausreisser"] = r["vielfaches"] >= 5 and not r["bezahlt"]
    formate = {}
    for r in reels:
        if r["format"] and not r["bezahlt"]:
            formate.setdefault(r["format"], []).append(r["vielfaches"])
    if a.json:
        print(json.dumps({"median": med, "reels": reels,
                          "formate": {k: {"anzahl": len(v), "median_vielfaches": statistics.median(v)}
                                      for k, v in formate.items()}}, ensure_ascii=False, indent=1))
        return
    print(f"\nAUSWERTUNG · {len(reels)} Reels · Median {tsd(med)} Aufrufe")
    if len(reels) < 12:
        print("Hinweis: Weniger als 12 Reels. Alles Folgende ist eine Vermutung, noch kein Muster.")
    print("\nAlle Reels, sortiert")
    for r in sorted(reels, key=lambda r: -r["vielfaches"]):
        m = "  AUSREISSER" if r["ausreisser"] else ("  vermutlich bezahlt" if r["bezahlt"] else "")
        lq = f"  Likes {proz(r['like_quote'])}" if r["like_quote"] is not None else ""
        vf = f"{r['vielfaches']:.1f}".replace(".", ",")
        print(f"{vf:>7}x  {tsd(r['aufrufe']):>10}  {r['titel'][:45]:<45}{lq}{m}")
    bez = [r for r in reels if r["bezahlt"]]
    if bez:
        print("\nVermutlich bezahlt beworben (nicht in der Format-Auswertung):")
        for r in bez:
            print(f"  · {r['titel'][:60]} ({tsd(r['aufrufe'])} Aufrufe, Likes {proz(r['like_quote'])})")
    if formate:
        print("\nNach Format (Median des Vielfachen)")
        for k, v in sorted(formate.items(), key=lambda kv: -statistics.median(kv[1])):
            hinweis = "" if len(v) >= 2 else "  (nur ein Reel)"
            mv = f"{statistics.median(v):.1f}".replace(".", ",")
            print(f"  {k:<14} {len(v):>2} Reels  {mv:>6}x{hinweis}")
    geteilt = [r for r in reels if r["geteilt"]]
    if geteilt:
        top = max(geteilt, key=lambda r: r["geteilt"] / r["aufrufe"])
        print(f"\nAm häufigsten weitergeschickt (im Verhältnis): {top['titel'][:60]}")


if __name__ == "__main__":
    main()
