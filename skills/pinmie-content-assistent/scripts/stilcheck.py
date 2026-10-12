#!/usr/bin/env python3
"""stilcheck.py - prüft deutsche Social-Media-Texte auf typische KI- und Agentur-Muster.
Teil des PINMIE Content-Assistenten (pinmie.de). Regeln: references/stil.md

Regeln:
  1. keine Gedankenstriche
  2. keine KI-Floskeln (ploetzlich, in der heutigen Zeit, und genau das, nicht weil/sondern weil ...)
  3. keine "nicht X, sondern Y"-Konstruktion
  4. kein negativer Satz, dem ein kurzer positiver "Antwortsatz" folgt
  5. keine Zwei-/Drei-Wort-Saetze (Fragmente)
  6. keine "Kein X. Kein Y."-Aufzaehlungen
  7. keine Fachbegriffe / Agentursprache (Warnung, Suchbegriffe ausgenommen)

Aufruf:  python3 stilcheck.py datei.txt        (eine Einheit pro Zeile, Leerzeilen trennen nicht)
         python3 stilcheck.py --text "..."
Ausgabe: je Zeile die Treffer, am Ende Summe. Exit 1 wenn ein FEHLER gefunden wurde.
"""
import argparse, re, sys, json

FLOSKELN = [
    r"pl[öo]tzlich", r"in der heutigen zeit", r"und genau das", r"genau das ist",
    r"nicht weil", r"sondern weil", r"game ?changer", r"spannend", r"lass(?:t)? uns",
    r"kurz gesagt", r"spoiler", r"das beste daran", r"hier kommt der clou",
    r"die wahrheit ist", r"fakt ist", r"am ende des tages", r"next level",
    r"in diesem video", r"herzlich willkommen", r"wir freuen uns sehr",
]
FACHBEGRIFFE = [
    "content", "hook", "hooks", "engagement", "call-to-action", "cta", "funnel", "leads",
    "branding", "storytelling", "community", "insights", "performance", "kpi", "kpis",
    "conversion", "awareness", "touchpoint", "usp", "employer branding", "b-roll",
    "payoff", "outlier", "retention", "reach", "brand awareness",
]
# Suchbegriffe, die bewusst so in Captions stehen sollen
ERLAUBT = ["content ideen für unternehmen", "content plan", "hook video",
           "instagram insights", "community management", "employer branding"]

NEG = re.compile(r"\b(nicht|kein\w*|nie|niemand|nichts|ohne)\b", re.I)
SATZ = re.compile(r"[^.!?]+[.!?]+|[^.!?]+$")
WORT = re.compile(r"[A-Za-zÄÖÜäöüß0-9€%]+")


def saetze(text):
    t = re.sub(r"[„“\"»«]", "", text)
    out = [s.strip() for s in SATZ.findall(t) if s.strip()]
    return out


def pruefe(text):
    funde = []
    low = text.lower()
    if re.search(r"[–—]| - ", text):
        funde.append(("FEHLER", "Gedankenstrich"))
    for f in FLOSKELN:
        if re.search(f, low):
            funde.append(("FEHLER", f"Floskel: {re.search(f, low).group(0)}"))
    if re.search(r"\b(nicht|kein\w*)\b[^.!?]{0,80}\bsondern\b", low):
        funde.append(("FEHLER", "\"nicht X, sondern Y\""))
    ss = saetze(text)
    for i, s in enumerate(ss):
        n = len(WORT.findall(s))
        if 0 < n <= 3:
            funde.append(("FEHLER", f"Fragment ({n} Wörter): \"{s}\""))
        if i + 1 < len(ss):
            nxt = ss[i + 1]
            if NEG.search(s) and not NEG.search(nxt) and len(WORT.findall(nxt)) <= 9:
                funde.append(("FEHLER", f"Negativ, dann Antwortsatz: \"{s}\" → \"{nxt}\""))
            a = WORT.findall(s)[:1]
            b = WORT.findall(nxt)[:1]
            if a and b and a[0].lower() == b[0].lower() and a[0].lower() in (
                    "kein", "keine", "keinen", "ohne", "nicht", "nie", "weniger", "mehr"):
                funde.append(("FEHLER", f"Aufzählung \"{a[0]} X. {b[0]} Y.\""))
        if re.search(r"(?i)\bstimmt nicht\b|\bkein problem\b", s):
            funde.append(("FEHLER", f"Antwort-Floskel: \"{s}\""))
    low2 = low
    for e in ERLAUBT:
        low2 = re.sub(r"(?<![a-zäöüß])" + re.escape(e) + r"(?![a-zäöüß])", "", low2)
    for w in FACHBEGRIFFE:
        if re.search(r"(?<![a-zäöüß])" + re.escape(w) + r"(?![a-zäöüß])", low2):
            funde.append(("WARNUNG", f"Fachbegriff: {w}"))
    return funde


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?")
    ap.add_argument("--text")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    lines = [a.text] if a.text else [l.rstrip("\n") for l in open(a.input, encoding="utf-8") if l.strip()]
    res, fehler, warn = [], 0, 0
    for l in lines:
        f = pruefe(l)
        fehler += sum(1 for x in f if x[0] == "FEHLER")
        warn += sum(1 for x in f if x[0] == "WARNUNG")
        res.append({"text": l, "funde": f})
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for r in res:
            if r["funde"]:
                print(r["text"][:110])
                for k, m in r["funde"]:
                    print(f"   {k:8} {m}")
        print(f"\n{len(lines)} Zeilen geprüft · {fehler} Fehler · {warn} Warnungen")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
