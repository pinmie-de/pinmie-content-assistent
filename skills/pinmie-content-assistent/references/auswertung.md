# Modul: Auswertung

Einmal im Monat. Ergebnis: Welche Reels sind aus der Reihe gefallen, warum vermutlich, und was davon die Firma
wiederholen sollte.

## Eingabe

Die Firma braucht von ihren letzten 12 bis 30 Reels: Datum, Titel oder erster Satz, Aufrufe, Likes. Kommentare,
Weiterleitungen und Speicherungen sind ein Plus. Das steht in Instagram unter jedem Reel bei „Insights ansehen“
oder im Profil unter „Professional Dashboard“.

Am einfachsten als Tabelle (CSV oder einfach Zeilen) in diesem Aufbau:

```
datum;titel;aufrufe;likes;kommentare;geteilt;gespeichert;format
2026-09-02;POV Teile fehlen;48200;1210;35;210;40;pov
```

Spalten nach „likes“ dürfen fehlen. Das Format kann der Assistent auch selbst zuordnen.

## Rechnen

Lass `scripts/auswertung.py datei.csv` laufen. Das Programm:
- rechnet den Median der Aufrufe,
- zeigt jedes Reel als Vielfaches des Medians,
- markiert Reels, die vermutlich bezahlt beworben wurden (Likes unter 0,3 % der Aufrufe bei hohem Vielfachen),
- fasst nach Format zusammen, wenn eine Formatspalte da ist.

Ohne Code: dieselben Schritte von Hand, und sag dazu, dass von Hand gerechnet wurde.

## Deuten

- **Ab dem Fünffachen** ist ein Reel ein echter Ausreißer. Schau, was es von den anderen unterscheidet: Situation,
  Person, erster Satz, Länge, Format.
- **Zwischen dem Doppelten und dem Fünffachen**: gut, aber noch kein Muster. Erst wenn ein Format zweimal so läuft,
  ist es eine Richtung.
- **Unter der Hälfte des Medians**: Prüf, ob es zu den schwachen Themen aus `formate.md` gehört.
- **Bezahlte Reels** aus dem Vergleich herausnehmen. Sie sagen nichts darüber, was Zuschauern gefällt.
- **Weiterleitungen und Speicherungen** zählen mehr als Likes. Ein Reel mit wenigen Aufrufen, aber vielen
  Weiterleitungen, ist ein guter Kandidat für eine zweite Version.
- Ehrlich bleiben: Bei weniger als zwölf Reels ist jede Aussage eine Vermutung.

## Ausgabe

```
AUSWERTUNG {Zeitraum} · {Anzahl} Reels · Median {Aufrufe}

Ausreißer
{Vielfaches} · {Titel} · {Format} · vermutlicher Grund: {…}

Bezahlt (nicht mitgezählt)
…

Nach Format
{Format}: {Anzahl}, Median {x}-fach

Das wiederholen wir
1. …
2. …

Das lassen wir oder packen es anders
1. …
```

Schreib das Ergebnis in `letzte-auswertung.md`, damit der Wochenplan es lesen kann.
