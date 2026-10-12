# Modul: Reel

Aus einer Idee wird ein Reel, das die Firma mit dem Handy an einem Vormittag drehen kann.
Ergebnis: Text im Bild, Sprechtext (falls gesprochen wird), Ablauf mit Sekunden und eine Drehliste.

## 1. Situation klären

Ein Reel braucht eine echte Situation aus dem Betrieb. Wenn die Idee dünn ist („irgendwas mit Azubis“),
frag einmal gebündelt:
- Was genau passiert dabei? Wo, mit wem?
- Was ist daran typisch, lustig, ärgerlich oder überraschend?
- Wer würde mitspielen?

Wenn die Firma gar keine Idee hat, schlag drei Situationen aus `einstiege.json` für ihre Branche vor und lass
sie wählen. Formuliere sie so um, dass sie zu dem passen, was laut Firmenprofil im Alltag zu filmen ist.

## 2. Format wählen

Lies `formate.md` und nimm das Format, das zur Situation und zum Ziel aus dem Firmenprofil passt:

| Ziel | Formate zuerst |
|---|---|
| Neue Leute erreichen | 1 POV, 2 „Wir kennen alle …“, 5 Trend mit Belegschaft |
| Kommentare bekommen | 3 Mitredefrage, 4 Fehler zeigen |
| Bewerber gewinnen | 7 fester Kollege, 5 Trend mit Belegschaft, 6 Meinung |
| Kunden überzeugen | 4 Fehler zeigen, 8 Härtetest, 6 Meinung |

Prüf auch die Liste „Was regelmäßig schwach läuft“. Wenn die Idee dazu gehört (Messe, Projekt-Update,
Weihnachtsgruß), sag es offen und zeig, wie man sie in eines der acht Formate packt.

## 3. Drei Einstiege schreiben

Schreib drei Einstiege aus mindestens zwei verschiedenen Formaten. Jeder Einstieg hat:
- **Text im Bild:** der Satz, der in der ersten Sekunde groß im Bild steht. Höchstens etwa 12 Wörter.
  Er muss die Situation ohne Ton erklären.
- **Gesprochen** (nur wenn jemand spricht): der erste Satz, den die Person sagt.
- **Erstes Bild:** was man in der ersten Sekunde sieht. Bewegung schlägt ein stehendes Gesicht.

Bewerte die drei mit `scripts/einstieg.py` und zeig die Rangliste. Liegt der beste Einstieg unter 60 Punkten,
überarbeite ihn, bevor du weitermachst. Das Programm prüft Textmerkmale. Ob ein Reel läuft, entscheidet am Ende
die Situation selbst, deshalb gewinnt im Zweifel der Einstieg mit der echteren Situation.

## 4. Ablauf schreiben

Nimm den besten Einstieg und schreib den Ablauf in Abschnitten mit Sekunden:

```
0 bis 2 s    Einstieg       Text im Bild steht, erstes Bild mit Bewegung
2 bis …      Situation      was passiert, in kurzen Einstellungen, jede höchstens 3 bis 4 Sekunden
…            Wendung        die Pointe, die Auflösung oder der überraschende Moment
letzte 2 s   Ende           eine Frage an die Zuschauer, ein Blick in die Kamera, oder nichts.
                            Höchstens eine Bitte (kommentieren ODER folgen ODER schicken, nie alles).
```

Längen aus der Recherche: POV und Szenen 7 bis 15 Sekunden, Mitredefrage und Härtetest 10 bis 25 Sekunden,
Fehler zeigen 15 bis 45 Sekunden, Meinung und fester Kollege bis 2 Minuten.

Wenn gesprochen wird, schreib den Sprechtext in die Datei `skript.txt` und miss ihn mit
`scripts/sprechzeit.py skript.txt --ziel {Sekunden}`. Behebe jede Warnung.

## 5. Drehliste

Für jede Einstellung eine Zeile: was ist zu sehen, wer, wo, wie lang. Dazu immer diese Punkte:
- Handy hochkant, Kamera auf Augenhöhe oder knapp darunter, Linse vorher abwischen.
- Ton: Wenn gesprochen wird, ein Ansteckmikrofon oder nah ans Handy. Ton ist wichtiger als Licht.
- Jede Einstellung zwei- bis dreimal drehen.
- Keine Kunden, Adressen, Kennzeichen, Bildschirme mit Daten oder fremden Firmenlogos im Bild, außer es ist
  abgesprochen.
- Wer im Bild ist, braucht eine schriftliche Einwilligung (siehe `rechts-check.md`).

## 6. Prüfen

Lass alle Texte (Text im Bild, Sprechtext) durch `scripts/stilcheck.py` laufen und behebe jeden Fehler.

## Ausgabe

```
REEL: {Arbeitstitel}
Format: {Name}  ·  Ziel: {aus Firmenprofil}  ·  Länge: ca. {x} s

EINSTIEGE (bewertet)
1. {Punkte}  {Text im Bild}
2. …
3. …

TEXT IM BILD
0 s   {Satz}
…

SPRECHTEXT (falls gesprochen)
{Text}

ABLAUF
{Abschnitte mit Sekunden}

DREHLISTE
1. {Einstellung} · {wer} · {wo} · {Sekunden}
…

MUSIK
Nur aus der Musikbibliothek, die Instagram für Unternehmenskonten freigibt, oder ohne Musik.

PRÜFUNG
Stil: {Ergebnis}  ·  Sprechzeit: {Ergebnis}

Nächster Schritt: Caption schreiben.
```

Biete danach an, die Caption zu schreiben. Veröffentliche nichts.
