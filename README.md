# Grupparbete: Testa en webapp

Detta projekt syftar till att ge er praktisk erfarenhet av hela testprocessen – från planering och testdesign till manuell och automatiserad testning. Ni kommer att arbeta i grupp för att testa en befintlig webbapplikation med fokus på både teori och praktik.

## Uppgiften i korthet

Ni får en färdig webapp skriven i Flask tillsammans med tillhörande dokumentation. Er uppgift är att testa applikationen genom att:

1. Skapa en testplan
2. Identifiera testfall (använd både black-box, white-box samt ekvivalensklasser/gränsvärdesanalys)
3. Utföra manuella tester
4. Skriva automatiserade tester:
   - Enhetstester (med `pytest`) för att uppnå minst 80% testtäckning
   - Integrationstester (med `pytest`) så att alla routes har minst ett test
   - Minst ett systemtest (med `Playwright`)
5. Dokumentera hittade buggar
6. Fixa hittade buggar
7. Presentera ert arbete och era lärdomar

## Applikationen

Applikationen består av flera Python-filer för routing, databaslogik och rendering. Det finns även färdig Docker-setup för att köra allt lokalt. Era integrations- och systemtester kan köras mot databasen i docker.

Webappen innehåller följande routes:

### `/`  
Visar ett välkomstmeddelande och antalet besökare.

### `/visits`  
Visar en historik över tidigare besök. Exempel:  
```
Visit history  
- 2025-04-01 12:30: Visit #1  
- 2025-04-01 12:45: Visit #2  
```

Du kan också filtrera listan med hjälp av parametrarna `to`och `from` (en eller båda).

### `/visit/<id>`  
Visar detaljer för ett specifikt besök:
- Besöksnummer
- Tidpunkt
- IP-adress
- User-agent

### `/hello`
Ger dig ett hälsningsmeddelande som beror på parametern `name`. Du kan även ladda sidan utan parametern.

### `/hello-form`
In interaktiv sida där du kan mata in ett namn som skickas vidare till `/hello`.

## Att göra

### Planering & design
- Skapa en **testplan**: beskriv vad som ska testas, ansvarsfördelning, prioritering etc.
- Identifiera testfall och dokumentera dem i tabellform.

### Manuella tester
- Utför **utforskande tester**
- Utför manuella tester enligt era testfall

### Automatiserade tester
- Skriv **enhetstester** i `tests/unit/` för interna funktioner (t.ex. logik i `rendering.py`)
- Skriv **integrationstester** i `tests/integration/` för varje route
- Skriv **minst ett systemtest** i `tests/system/` med `Playwright`

### Buggrapportering
- Logga varje buggar ni hittar i en **testrapport** och samla ihop dem i ett dokument (tex Google Docs).

### Buggfix
För alla buggar hittade:
- Om buggen inte hittades av ett automatiserat testfall, skapa först ett testfall som hittar felet (dvs ett tesfall som fallerar).
- Fixa buggen genom att ändra koden.
- Kör automatiserade test och bekräfta att buggen är fixad genom att testet nu går igenom.

### Presentation
- Presentera teststrategi, testfall, buggar ni hittat, era automatiserade tester samt vad ni lärt er. Formatet är valfritt (whiteboard, slides etc).

## Projektstruktur

```
test-apr10-grupparbete
├── app/                          # Applikationskod
│   ├── app.py                    # Flask-app och dess routes
│   ├── db.py                     # Databaslogik
│   └── rendering.py              # Textformatering
├── tests/
│   ├── unit/                     # Enhetstester
│   ├── integration/              # Integrationstester
│   └── system/                   # Systemtester (Playwright)
├── .coveragerc
├── docker-compose.yml
├── Dockerfile
├── local-start.sh                # Startar appen med Docker
├── requirements.txt              # Moduler som appen är beroende av
├── README.md                     # Denna fil
├── pytest.ini                    # Inställningar för pytest
```

## Inlämning

Skapa en zip-fil med följande innehåll:

- `summering.md`: Sammanfattning av arbetet och speciella steg (om det finns) för att köra era test
- `testplan/testplan.md`: Teststrategi, mål, roller, verktyg
- `testplan/testcases.md/pdf/xlsx`: Testfall dokumenterade i tabellform
- `tests/`: Alla automatiserade tester (unit, integration, system)
- `testrapport.md/pdf`: Sammanställning av resultat och bugglista

## Kom igång

Installera [Docker desktop](https://www.docker.com/products/docker-desktop/) (docker endast räcker inte då vi använder docker compose).

Kör igång applikationen:
```bash
./local-start.sh
```

Om du har Windows, prova Command-scriptet (inte PowerShell):
```
local-start.bat
```


---

Lycka till – och glöm inte att ha kul medan ni testar!
