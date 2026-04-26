# Gimtadienių Priminimo Programa

### Kaip paleisti:
1. `python main.py` - pagrindinė programa.
2. `python test_birthday.py` - automatiniai testai.
3. `python birthday.json` - AI generuoti gimtadieniai.

### Naudoti OOP principai:
* **Abstrakcija:** Naudojama `BirthdayBase` klasė.
* **Paveldėjimas:** `StandardBirthday` paveldi iš `BirthdayBase`.
* **Inkapsuliacija:** Duomenys saugomi privačiame kintamajame `__birthdays`.
* **Polimorfizmas:** Metodas `get_details()` perrašomas dukterinėje klasėje.

### Projektavimo šablonas:
Naudojamas **Singleton** šablonas `BirthdayManager` klasėje, užtikrinantis, kad duomenys būtų valdomi per vieną objektą.
