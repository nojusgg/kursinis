import unittest
import os  # Ši eilutė išspręs klaidą!
from datetime import date
from main import BirthdayManager, StandardBirthday
class TestBirthdayApp(unittest.TestCase):
    def setUp(self):
        """Ši dalis paleidžiama prieš kiekvieną testą – paruošiamas švarus manageris."""
        self.manager = BirthdayManager()
        # Išvalome senus testinius duomenis, jei tokių buvo
        if os.path.exists("birthdays.json"):
            os.remove("birthdays.json")
        self.manager._BirthdayManager__birthdays = {} 

    def test_add_and_calculate_age(self):
        """Testas: ar teisingai prideda ir skaičiuoja amžių."""
        test_date = date(2000, 1, 1)
        self.manager.add_birthday("Testuotojas", test_date)
        
        birthdays = list(self.manager.get_all())
        self.assertEqual(len(birthdays), 1)
        self.assertEqual(birthdays[0].name, "Testuotojas")
        
        # Patikriname amžių (2026 m. turėtų būti 26 metai)
        expected_age = 2026 - 2000
        self.assertEqual(birthdays[0].calculate_age(), expected_age)

    def test_remove_birthday(self):
        """Testas: ar veikia trynimas."""
        self.manager.add_birthday("Trinimui", date(1990, 5, 5))
        result = self.manager.remove_birthday("Trinimui")
        self.assertTrue(result)
        self.assertEqual(len(list(self.manager.get_all())), 0)

    def test_singleton(self):
        """Testas: ar tikrai veikia Singleton šablonas (reikalavimas nr. 4)."""
        manager2 = BirthdayManager()
        self.assertIs(self.manager, manager2)

if __name__ == "__main__":
    unittest.main()