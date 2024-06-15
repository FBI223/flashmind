import subprocess

# Lista plików testowych do uruchomienia
test_files = ["TestDragDropMenu.py", "TestEditFlashCardMenu.py", "TestEditSetMenu.py",
              "TestProfileMenu.py", "TestSettingMenu.py", "TestShowHideMenu.py",
              "TestStudyFlashcardMenu.py", "TestTimerApp.py", "TestTypeCheckMenu.py"]

# Pętla do uruchomienia testów
for test_file in test_files:
    print(f"Uruchamianie pliku testowego: {test_file}")
    try:
        subprocess.run(["python", test_file], check=True)
        print(f"Plik testowy {test_file} został pomyślnie wykonany.")
    except subprocess.CalledProcessError:
        print(f"Wystąpił błąd podczas wykonania pliku testowego: {test_file}")
