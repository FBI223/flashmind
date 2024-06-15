
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------ENGLISH----------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


README
This README file contains all the necessary instructions to get started with the Flashmind application and information related to its documentation.

In the Documentation folder, you will find project-related documentation.
In the Code folder, you will find the .py files (run the source.py file).
In the Executable folder, you will find the .exe files.

Requirements
Windows 10 or Windows 11
pip (Python package manager)
For the Python Script
Python 3.12.3 or newer
You need to install the following Python libraries:
pip install tkinter
pip install ttkthemes
pip install pillow
pip install win10toast_click

First, run the application as follows (after selecting the appropriate path to the entire code file):
python source.py

If you want to set notifications, you need to set the time interval in the application and confirm it, and then run the notifications.py file:
python notifications.py
(This version includes system notifications that come after closing the application)

The source code version contains 4 sets of sample flashcards for testing purposes.

For the Executable File (.exe)
If the system prompts you to extract all files when running .exe files, you should do so.
The .gitignore, fiszki.db, source.exe, notifications.exe files, and the images folder should be in the same folder.

First, open the source.exe file. If you want the application to send notifications, set the time interval for the notifications, confirm, and then close the application. Then run the notifications.exe file. This application will send system notifications at the chosen interval (the next notification will come only after closing the application). To stop sending notifications, set "no reminder" or kill the process (e.g., by restarting the computer).

Unit Tests
In the Unit_Tests folder, you will find the source code for these tests. To run and check them yourself, run the ExecuteAllTests.py file:
python ExecuteAllTests.py

UML Diagrams
The UML diagrams included in the documentation were created using StarUML (it is recommended to open the diagrams with this program). PNG images are also included, allowing you to view the diagrams without opening the .mdj files.

Project Plan
In the Project_Plan folder, there is an extended Gantt chart showing the schedule and division of work. The file was created with GanttProject and has a .gan extension. There is also a .png file illustrating the Gantt chart and a .txt file (logs from GitHub).

Project Contributors
Mateusz Wołowiec
Marcin Sztukowski
Wiktor Drab
Wojciech Mikula
Jakub Paczek



--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------POLISH-----------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Ten plik README zawiera wszystkie niezbędne wskazówki, aby rozpocząć korzystanie z aplikacji Flashmind oraz informacje dotyczące dokumentacji.

W folderze Dokumentacja znajduje się dokumentacja związana z projektem.
W folderze Kod_programu znajdują się pliki .py (należy uruchomić plik source.py)
W folderze Plik_wykonywalny znajdują się pliki .exe

Wymagania
Windows 10 lub Windows 11
pip (menedżer pakietów Pythona)



Dla skryptu Python
Python 3.12.3 lub nowszy

Należy zainstalować następujące biblioteki Pythona
pip install tkinter
pip install ttkthemes
pip install pillow
pip install win10toast_click


Najpierw aplikację trzeba uruchomić w następujący sposób (po wybraniu odpowiedniej ścieżki do całego pliku z kodem)
python source.py


Jeśli chcemy ustawić powiadomienia należy najpierw ustawić interwał czasu i zatwierdzić w aplikacji, a dopiero następnie uruchomić plik notifications.py
python notifications.py
(wersja z powiadomieniami sysytemowymi przychodzącymi po zamknięciu aplikacji)

Wersja z kodem źródłowym zawiera 4 zestawy przykładowych fiszek w celach testowych.




Dla pliku wykonywalnego (.exe)
Jeśli przy uruchamianu plików .exe system poprosi o wyodrębnienie wszystkich plików to należy to uczynić.
Pliki .gitignore, fiszki.db, source.exe, notifications.exe oraz folder images powinny znajdować się w jednym folderze.
Należy koniecznie najpierw otworzyć plik source.exe. Jeśli chcemy aby aplikacja wysyłała powiadomienia należy ustawić interwał czasu co jaki mają przychodzić powiadomienia, zatwierdzić oraz zamknąć. Następnie uruchomić plik notifications.exe. Aplikacja ta będzie wysyłała powiadomienia systemowe w odstępie czasu równym wybranemu interwałowi (kolejne powiadomienie przyjdzie dopiero po zamknięciu aplikacji). Aby zakończyć wysyłanie powiadomień należy ustawić no reminder lub zabić wątek (np. poprzez restart komputera).



W folderze Testy_jednostkowe znajduje się kod źródłowy tych testów. Aby je uruchomić i sprawdzić ich działanie samemu należy uruchomić plik ExecuteAllTests
python ExecuteAllTests.py


Diagramy UML zawarte w dokumentacji zostały stworzone w programie StarUML (zaleca się otwarcie diagramów w tym programie). Dołączone zostały także zdjęcia w formacie PNG, które umożliwiają podgląd diagramów bez konieczności otwierania plików .mdj.

W folderze Plan_projektu znajduje się rozszerzony wykres Gantta z którego można odczytać harmonogram oraz podział pracy. Plik został stworzony w programie GanttProjekt i posiada rozszerzenie .gan.
Znajduje się tam również plik .png ilustrujący wykres Gantta oraz .txt (logi z Github).


Projekt wykonali

Mateusz Wołowiec
Marcin Sztukowski
Wiktor Drab
Wojciech Mikula
Jakub Paczek
