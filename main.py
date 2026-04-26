import json
import os
from abc import ABC, abstractmethod
from datetime import date, datetime

# --- 1. ABSTRAKCIJA (OOP REIKALAVIMAS) --- [cite: 76]
class BirthdayBase(ABC):
    def __init__(self, name: str, birth_date: date):
        self.name = name
        self.birth_date = birth_date

    @abstractmethod
    def get_details(self) -> str:
        pass

# --- 2. PAVELDĖJIMAS IR ENKAPSULIACIJA --- [cite: 76]
class StandardBirthday(BirthdayBase):
    def get_details(self) -> str:
        age = self.calculate_age()
        return f"👤 {self.name:<15} | {self.birth_date} | {age} m."

    def calculate_age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

# --- 3. SINGLETON ŠABLONAS IR KOMPOZICIJA --- [cite: 76]
class BirthdayManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BirthdayManager, cls).__new__(cls)
            cls._instance.__birthdays = {}  # Enkapsuliacija (privatus)
            cls._instance.file_path = "birthdays.json"
            cls._instance.load_from_file()
        return cls._instance

    def add_birthday(self, name: str, b_date: date):
        self.__birthdays[name] = StandardBirthday(name, b_date)
        self.save_to_file()

    def remove_birthday(self, name: str) -> bool:
        if name in self.__birthdays:
            del self.__birthdays[name]
            self.save_to_file()
            return True
        return False

    def get_all(self):
        return self.__birthdays.values()

    # --- 4. DARBAS SU FAILU (REIKALAVIMAS) --- [cite: 76]
    def save_to_file(self):
        data = {name: b.birth_date.isoformat() for name, b in self.__birthdays.items()}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for name, date_str in data.items():
                        self.__birthdays[name] = StandardBirthday(
                            name, date.fromisoformat(date_str)
                        )
            except Exception:
                self.__birthdays = {}

# --- VIZUALIZACIJA (GRĄŽINTAS DIZAINAS) ---
def print_menu():
    print("\n" + "═" * 38)
    print("      🎂 GIMTADIENIŲ PRIMINIMAS")
    print("═" * 38)
    print("  1. Pridėti gimtadienį")
    print("  2. Gimtadienių sąrašas (su amžiumi)")
    print("  3. Pašalinti gimtadienį")
    print("  4. Artimiausi gimtadieniai")
    print("  5. Išeiti")
    print("═" * 38)

def get_days_until(b_date: date) -> int:
    today = date.today()
    next_b = b_date.replace(year=today.year)
    if next_b < today:
        next_b = next_b.replace(year=today.year + 1)
    return (next_b - today).days

def main():
    manager = BirthdayManager()
    
    while True:
        print_menu()
        choice = input("Pasirinkite parinktį: ").strip()

        if choice == "5":
            print("Viso gero! 👋")
            break

        elif choice == "1":
            name = input("Įveskite vardą: ").strip()
            d_str = input("Gimimo data (YYYY-MM-DD): ").strip()
            try:
                manager.add_birthday(name, date.fromisoformat(d_str))
                print(f"✅ {name} sėkmingai pridėtas!")
            except ValueError:
                print("❌ Klaida: Neteisingas formatas. Naudokite YYYY-MM-DD.")

        elif choice == "2":
            birthdays = list(manager.get_all())
            if not birthdays:
                print("📭 Sąrašas tuščias.")
            else:
                print("\n" + "-" * 40)
                print(f"{'VARDAS':<15} | {'DATA':<10} | {'AMŽIUS'}")
                print("-" * 40)
                for b in birthdays:
                    print(b.get_details())

        elif choice == "3":
            name = input("Įveskite vardą, kurį norite pašalinti: ").strip()
            if manager.remove_birthday(name):
                print(f"🗑️ {name} pašalintas.")
            else:
                print("❌ Klaida: Toks vardas nerastas.")

        elif choice == "4":
            birthdays = list(manager.get_all())
            if not birthdays:
                print("📭 Nėra įvestų gimtadienių.")
            else:
                print("\n--- KAS ŠVĘS ARTIMIAUSIU METU ---")
                sorted_list = sorted(birthdays, key=lambda x: get_days_until(x.birth_date))
                for b in sorted_list:
                    days = get_days_until(b.birth_date)
                    status = "ŠIANDIEN! 🥳" if days == 0 else f"po {days} d."
                    # Skaičiuojame kiek sueis
                    age_next = b.calculate_age() + (1 if days > 0 else 0)
                    print(f"🎂 {b.name}: {status} (Sueis {age_next} m.)")

        else:
            print("⚠️ Neteisingas pasirinkimas.")

        input("\nSpustelėkite ENTER, kad tęstumėte...")

if __name__ == "__main__":
    main()