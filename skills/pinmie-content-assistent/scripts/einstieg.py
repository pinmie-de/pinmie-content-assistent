#!/usr/bin/env python3
"""einstieg.py - bewertet den ersten Satz eines Firmen-Reels (Text im Bild oder gesprochen).

Teil des PINMIE Content-Assistenten (pinmie.de).

Grundlage ist die PINMIE-Auswertung deutscher Firmenkonten (Oktober 2026, 44 Konten, rund 560 Reels).
Die Ausreißer dort hatten fast immer einen ersten Satz, der
  1. in etwa zwei Sekunden lesbar ist,
  2. nach Alltag klingt: eine Situation, eine Person, gesprochene Sprache („POV“, „wir kennen alle“, „klar, hab ich“),
  3. die Zuschauer einbezieht (du/ihr, eine Frage, „jeder“, „keiner“),
  4. etwas offen lässt (eine Frage, ein Widerspruch, „ganz sicher?“),
  5. nicht nach Bericht, Ankündigung oder Werbung klingt (Messe, Jubiläum, Projekt, Jahreszahl, Begrüßung).
Das Programm misst diese fünf Punkte am Text. Es sagt NICHT voraus, wie oft ein Reel aufgerufen wird.

Wie gut es ist: Die Regeln wurden an 33 echten Einstiegen deutscher Firmenreels abgestimmt (15 Ausreißer,
18 schwache). Dort trennt es stark und schwach sehr gut (AUC 0,94). An 18 Einstiegen, die beim Abstimmen nicht
benutzt wurden, nur mäßig (AUC 0,66 bis 0,72, 0,5 wäre Zufall). Es erkennt zuverlässig Berichte, Ankündigungen,
Werbeton und Vorreden. Zwischen zwei ordentlichen Einstiegen entscheidet es kaum.
Das entscheiden Situation, Person, Schnitt und wer das Video zu sehen bekommt. Nutze es, um schwache
Einstiege auszusortieren und drei Kandidaten zu vergleichen.

Aufruf
  python3 einstieg.py einstiege.txt        # ein Einstieg pro Zeile, Rangliste
  python3 einstieg.py --text "POV: ..."    # einzelner Einstieg mit Details
  python3 einstieg.py einstiege.txt --json
"""
import argparse
import json
import re
import statistics
import sys

WORT = re.compile(r"[A-Za-zÄÖÜäöüß0-9€%]+")

SITUATION = [
    r"^\s*pov\b", r"\bwir kennen alle\b", r"\bjede[rsn]?\b", r"\bkeiner\b", r"\bwenn\b", r"\bsobald\b",
    r"\bimmer\b", r"\bmal wieder\b", r"\bzum \w+ mal\b", r"\berste[nr]? tag\b", r"\bnimmt euch\b",
    r"\bmorgens\b", r"\babends\b", r"\bnachts\b", r"\bfeierabend\b", r"\bpause\b", r"\bmontag\w*\b",
    r"\bfrühschicht\b", r"\bnachtschicht\b", r"\bum \w+ uhr\b",
    r"\bbaustelle\b", r"\bwerkstatt\b", r"\bhalle\b", r"\btheke\b", r"\bbackstube\b",
    r"\bkolleg\w*\b", r"\bazubi\w*\b", r"\bchef\w*\b", r"\bmeister\w*\b", r"\bperson\b",
    r"\bfahrer\w*\b", r"\bmandant\w*\b", r"\bpatient\w*\b", r"\bgast\b", r"\bnachbar\w*\b",
    r"\bwerkzeug\w*\b", r"\bding\b", r"\bteil\b", r"\bdieses?\b",
    # gesprochene Sprache: direkte Rede, Umgangssprache
    r"\bhab\b", r"\bhats\b", r"\bgibt's\b", r"\bmal\b", r"\bklar\b", r"\bganz sicher\b", r"\bhand aufs herz\b",
    r"\bich\b", r"\ber\b", r"\bsie\b",
]
EINBEZUG = re.compile(r"\b(du|dich|dir|dein\w*|ihr|euch|euer|eure\w*|wir alle|jede[rsn]?|wer|wem|keiner)\b", re.I)
SPANNUNG = [
    r"\bnicht\b", r"\bkein\w*\b", r"\bnie\b", r"\bniemand\b", r"\bfalsch\w*\b", r"\brichtig\b",
    r"\bfehler\b", r"\bganz sicher\b", r"\bversucht\b", r"\beigentlich\b", r"\bwirklich\b",
    r"\bendlich\b", r"\bschlecht\w*\b", r"\bteuer\b", r"\bgefährlich\b", r"\bgeheim\w*\b",
    r"\bfehlt\b", r"\bnur\b", r"\bnoch\b", r"\bachtung\b", r"gefährlich", r"\bniemals\b", r"\bwer kennt\b",
    r"\bausdrücklich\b", r"\bkeine zweite\b", r"\bmuss\b", r"\bgenauso\b", r"\banders\b", r"\bschon\b",
    r"\?",
]
VORREDE = [
    (r"^\s*(hallo|hi|hey|moin|servus|guten (morgen|tag|abend))\b", "Begrüßung am Anfang"),
    (r"\bherzlich willkommen\b", "Begrüßung"),
    (r"\bin diesem (video|reel|beitrag)\b", "Vorrede über das Video"),
    (r"\bheute (zeigen|stellen|möchten|wollen|haben)\b", "Vorrede („heute … wir“)"),
    (r"\bwir (freuen uns|sind stolz|starten)\b", "Pressemitteilungs-Ton"),
    (r"^\s*(also|so|okay|ok)\b", "Füllwort am Anfang"),
    (r"(hör|scroll) (auf|nicht weiter|weiter)", "„Scroll“-Aufforderung"),
]
BERICHT = [
    "qualität", "leidenschaft", "passion", "tradition", "kompetenz", "kompetent", "zuverlässig", "innovativ",
    "innovationen", "lösung", "lösungen", "partner", "partnerschaft", "service", "premium", "exklusiv", "angebot",
    "rabatt", "unschlagbar", "beste", "bester", "top", "starkes team", "teamwork", "erfolgreich", "highlight",
    "neuheit", "jubiläum", "messe", "marathon", "lauf", "advent", "weihnachten", "projekt", "serie", "vorstellen",
    "neuen", "neue", "neuer", "funktionen", "beratung", "unternehmen", "gemeinsam", "recap", "rückblick",
    "das war", "eröffnung", "inbetriebnahme", "sanierung", "hergestellt", "verändern",
]
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def clamp(x):
    return max(0.0, min(100.0, x))


def p_laenge(t):
    n = len(WORT.findall(t))
    z = len(t.strip())
    s = 100 if n <= 12 else 100 - (n - 12) * 12
    if z > 80:
        s -= 15
    return clamp(s), f"{n} Wörter, {z} Zeichen, ca. {n / 3.3:.1f} s zum Lesen (Ziel: höchstens 12 Wörter)"


def p_situation(t):
    low = t.lower()
    treffer = sorted({re.search(m, low).group(0) for m in SITUATION if re.search(m, low)})
    n = len(treffer)
    s = {0: 25, 1: 70, 2: 90}.get(n, 100)
    return float(s), (f"{n} Hinweis(e) auf Alltag, Person oder gesprochene Sprache" + (
        f": {', '.join(treffer[:4])}" if treffer else ": klingt nach Bericht, nicht nach Situation"))


def p_einbezug(t):
    low = t.lower()
    frage = "?" in t
    an = EINBEZUG.search(low)
    if frage and an:
        return 100.0, "Frage an die Zuschauer"
    if frage:
        return 90.0, "Frage"
    if re.match(r"\s*pov\b", low):
        return 85.0, "POV: Zuschauer sieht mit den eigenen Augen"
    if an:
        return 85.0, f"bezieht Zuschauer ein („{an.group(0)}“)"
    if re.search(r"\b(ich|er|sie)\b", low):
        return 70.0, "direkte Rede oder Figur, Zuschauer nicht direkt angesprochen"
    if re.search(r"\b(wir|uns|unser\w*)\b", low):
        return 50.0, "nur „wir“, Zuschauer kommen nicht vor"
    return 40.0, "niemand wird angesprochen"


def p_spannung(t):
    low = t.lower()
    treffer = sorted({re.search(m, low).group(0) for m in SPANNUNG if re.search(m, low)})
    n = len(treffer)
    s = {0: 30, 1: 75}.get(n, 100)
    return float(s), (f"{n} Spannungsmoment(e): {', '.join(treffer[:4])}" if treffer else
                       "nichts Offenes, keine Frage, kein Widerspruch")


def p_bericht(t):
    low = t.lower()
    funde = [w for w in BERICHT if re.search(r"(?<![a-zäöüß])" + re.escape(w) + r"(?![a-zäöüß])", low)]
    funde += [m for r, m in VORREDE if re.search(r, low)]
    s = 100 - 35 * len(funde)
    if re.search(r"\b20\d\d\b", t):
        s -= 30
        funde.append("Jahreszahl")
    if t.count("!") > 1 or re.search(r"!\s*$", t) and not re.search(r"\b(du|ihr|euch)\b", low):
        s -= 15
        funde.append("Ausrufezeichen wie in einer Ankündigung")
    if EMOJI.search(t):
        s -= 15
        funde.append("Emoji")
    if "#" in t:
        s -= 25
        funde.append("Hashtag")
    return clamp(s), ("klingt nicht nach Bericht oder Werbung" if not funde else "Bericht-/Werbeton: " + ", ".join(funde))


PUNKTE = [("LÄNGE", p_laenge), ("ALLTAG", p_situation), ("ZUSCHAUER", p_einbezug),
          ("SPANNUNG", p_spannung), ("KEIN BERICHT", p_bericht)]


def bewerte(t):
    erg = {name: f(t) for name, f in PUNKTE}
    werte = [v[0] for v in erg.values()]
    gesamt = clamp(statistics.mean(werte) * 0.6 + min(werte) * 0.4)
    urteil = "STARK" if gesamt >= 75 and min(werte) >= 55 else ("BRAUCHBAR" if gesamt >= 60 else "SCHWACH")
    schwach = min(erg, key=lambda k: erg[k][0])
    return erg, round(gesamt, 1), urteil, schwach


def balken(x, b=20):
    f = round(x / 100 * b)
    return "█" * f + "·" * (b - f)


def main():
    ap = argparse.ArgumentParser(description="Bewertet Einstiege für Firmen-Reels.")
    ap.add_argument("datei", nargs="?")
    ap.add_argument("--text")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.text:
        zeilen = [a.text]
    elif a.datei:
        zeilen = [z.strip() for z in open(a.datei, encoding="utf-8") if z.strip()]
    else:
        zeilen = [z.strip() for z in sys.stdin if z.strip()]
    if not zeilen:
        sys.exit("Keine Einstiege gefunden.")
    res = []
    for z in zeilen:
        erg, g, u, s = bewerte(z)
        res.append({"einstieg": z, "punkte": g, "urteil": u, "schwächster": s,
                    "einzeln": {k: {"punkte": round(v[0]), "detail": v[1]} for k, v in erg.items()}})
    if a.json:
        print(json.dumps(res if len(res) > 1 else res[0], ensure_ascii=False, indent=1))
        return
    if len(res) == 1:
        r = res[0]
        print(f"\nEINSTIEG  „{r['einstieg']}“\n")
        for k, v in r["einzeln"].items():
            print(f"  {k:<14} {balken(v['punkte'])} {v['punkte']:>3}   {v['detail']}")
        print(f"\n  GESAMT         {balken(r['punkte'])} {r['punkte']:>5}   {r['urteil']}")
        if r["urteil"] != "STARK":
            print(f"  Am schwächsten: {r['schwächster']}. Das zuerst verbessern.")
    else:
        print("\nRANGLISTE")
        for i, r in enumerate(sorted(res, key=lambda r: -r["punkte"]), 1):
            print(f"{i:>2}. {r['punkte']:>5}  {r['urteil']:<9} {r['einstieg'][:70]}")
            print(f"            schwächster Punkt: {r['schwächster']} ({r['einzeln'][r['schwächster']]['detail']})")
        print("\nHinweis: Die Punkte bewerten den Text. Ob ein Reel läuft, entscheidet vor allem die Situation.")
    sys.exit(0 if max(r["punkte"] for r in res) >= 60 else 1)


if __name__ == "__main__":
    main()
