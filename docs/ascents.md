# Ascents

- Wilder Kaiser, Fleischbank, Fleischbank-Ostwand, Tourname
- Mallorca, Alaro, Sector Chorreras, Tour
    
| Kontinent | Land       | Areal              | Region            | Gebiet    | Summit/Massif/Sector | Route       |
| --------- | ---------- | ------------------ | ----------------- | --------- | -------------------- | ----------- |
| Europe    | Österreich | Wilder Kaiser      | Fleischbank       |           | Südostwand           | Südostkante |
| Europe    | Österreich | Dolomiten          | Sextener          |           | Große Zinne          | Comici      |
| Europe    | D          | Sächsische Schweiz | Schrammsteine     |           | Teufelsturm          | Talseite    |
| Europe    | D          | Frankenjura        | Süd West - Herbrc | Hiltpol   | Hexenküche           | Athos       |
| Europe    | D          | Sachsen            | Liebethaler Grund |           | Sektor Eckwand       | Lot         |
| Europe    | D          | Sachsen            | Liebethaler Grund |           | Sektor Dach          | Weg für F.  |
| Europe    | D          | Sachsen            | Kälbersteine      |           | Kleiner Kälberstein  | Per Tramp   |
| Europe    | CZ         | Böhmische Schweiz  | Elbtal Links      | Dolni     | Kleiner Teufel       | Tvrdolin    |
| Europe    | CZ         | Adrsbach           | Königreich        |           | Karlchen             | Problem     |
| Europe    | Malta      | Ghar Lapsi Qrendi  | Three Caves Area  |           | Learning to Fly Cave | Flypie      |
| Europe    | Spain      | Costa Blanca       | Benidorm          | Sella     | Espolon Pertemba     | Tesores     |
| Europe    | Mallorca   | Baleares           | Castell d Alaro   |           | Choreras             | Buf         |
| Europe    | F          | Bleau              | Ouest             | Buthier   | buthier nord         | Matrix      |
| Europe    | F          | Bleau              | West              | Trois-Pig | 95.2                 | Triplette   |
    
# Route Charackter

| ID  | Name     |
| --- | -------- |
| 1   | Handriß  |
| 2   | Faustriß |
| 3   | Schulter |
| 4   | Überhang |
| 5   | Reibung  |
    
# Route Characters

| FK_Route | FK_Character |
| -------- | ------------ |
| 1        | 1            |
| 1        | 2            |
| 1        | 3            |
  
    
# Diary

Description of the day and people (climbing partners and not climbing related persons). With this we can write not only about a route but rather about the day.

| ID  | Date       | Description      |
| --- | ---------- | ---------------- |
| 1   | 01.01.2016 | Super Toller Tag |

# People

| ID  | Name   | LastName | Nickname       |
| --- | ------ | -------- | -------------- |
| 1   | Stefan | W...     | Muscle         |
| 2   | Stefan | E...     | Reibungsrainer |

# Diary-People

| FK_Diary | FK_Buddies |
| -------- | ---------- |
| 1        | 1          |
| 1        | 2          |
| 1        | 3          |

# Ascent

| ID  | FK_Route | FK_Ascent_Style | Ascent_Number | Rope Party | Description | Date       |
| --- | -------- | --------------- | ------------- | ---------- | ----------- | ---------- |
| 1   | 1        | 1               | 73            |            | Ultra Geil  | 01.01.2016 |

# Ascent Style

| ID  | Name |
| --- | ---- |
| 1   | AF   |
| 2   | RP   |
| 3   | OS   |
| 4   | o.U  |
| 5   | m.U  |

# Rope Party

| FK_Begehung | FK_Buddy |
| ----------- | -------- |
| 1           | 1        |
| 1           | 2        |