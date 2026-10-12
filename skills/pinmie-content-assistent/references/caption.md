# Modul: Caption

Die Caption ist der Text unter dem Reel. Sie hat bei Firmen drei Aufgaben, und jede Caption erfüllt
hauptsächlich eine davon. Frag dich zuerst, welche.

| Aufgabe | Woran man sie erkennt | Länge |
|---|---|---|
| **Mitreden lassen** | Das Reel endet mit einer Frage oder Situation, die jeder kennt | 1 bis 2 Sätze |
| **Erklären** | Fehler zeigen, Härtetest, Meinung. Wer mehr wissen will, liest weiter | 3 bis 6 Sätze |
| **Zum nächsten Schritt führen** | Stelle, Angebot, Termin, Liste zum Herunterladen | 2 bis 4 Sätze |

## Aufbau

1. **Erste Zeile:** Sie steht neben dem Video, bevor jemand auf „mehr“ tippt. Sie setzt den Einstieg fort
   oder stellt die Frage. Sie wiederholt nicht den Text im Bild.
2. **Mittelteil** (nur bei „Erklären“ und „Nächster Schritt“): ein konkretes Detail aus dem Betrieb, ein Grund,
   eine kurze Erklärung. Kurze Absätze, damit es auf dem Handy lesbar bleibt.
3. **Eine Bitte:** entweder eine Frage zum Kommentieren, oder „Schick das dem Kollegen, der …“, oder ein
   nächster Schritt (Nachricht schreiben, Link im Profil). Nie mehrere Bitten in einer Caption.
4. **Suchbegriffe:** Seit Juli 2025 können öffentliche Beiträge von Unternehmenskonten auch bei Google
   auftauchen, und Instagram selbst durchsucht Captions. Deshalb gehören zwei bis drei Wörter in den Text,
   nach denen jemand suchen würde: Beruf, Leistung, Ort. Natürlich eingebaut, etwa „Wir suchen einen
   Elektroniker in Hanau“.
5. **Hashtags:** Instagram begrenzt seit Dezember 2025 die Zahl auf fünf pro Beitrag. Drei bis fünf passende
   reichen: Beruf, Branche, Ort. Allgemeine Riesen-Hashtags wie #viral oder #fyp bringen nichts.

## Regeln

- Stil nach `stil.md`, Anrede und Absender nach Firmenprofil.
- Keine Versprechen, keine Superlative, die man nicht belegen kann.
- Bei Kooperation mit einem Hersteller oder Partner: als Werbung kennzeichnen (Instagram-Funktion
  „Bezahlte Partnerschaft“ oder deutlich „Werbung“ am Anfang).
- Personen nur mit Namen markieren, wenn sie zugestimmt haben.
- Telefonnummern und E-Mail-Adressen gehören ins Profil, nicht in jede Caption.
- Prüfe die fertige Caption mit `scripts/stilcheck.py`.

## Ausgabe

```
CAPTION · Aufgabe: {Mitreden | Erklären | Nächster Schritt}

{Text}

{Hashtags}

Suchbegriffe darin: {…}  ·  Stil: {Ergebnis}
```

Biete zwei Varianten an, wenn die Aufgabe nicht eindeutig ist. Nächster Schritt: Rechts-Check vor dem Posten.
