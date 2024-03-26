Opis repo
Program pozwala na rejestrację pacjentów oraz wizyt lekarskich

Pacjent posiada w systemie następujące dane:
imię;nazwisko;PESEL;unikalne ID

Menu wygląda następująco:
[1] Dodaj pacjenta -> funkcja prosi o podanie danych pacjenta: imię, nazwisko i PESEL
[2] Usuń pacjenta -> funkcja wyświetla wszystkich zapisanych pacjentów z przydzieloną numeracją; usunięcie pacjenta
wymaga wpisanie odpowiedniego numeru
[3] Wyświetl pacjentów -> funkcja wyświetla wszystkich zapisanych pacjentów
[4] Zapisz dane do plików -> funkcja nadpisuje dane w plikach Patient_data.csv oraz Visit_data.csv danymi
zapisanymi w systemie
[5] Dopisz dane do plików -> funkcja dopisuje dane zapisane w systemie do plików Patient_data.csv oraz Visit_data.csv
[6] Wczytaj dane z plików -> funkcja nadpisuje dane w systemie danymi pobranymi z plików Patient_data.csv oraz
Visit_data.csv
[7] Dodaj wizytę -> funkcja pobiera datę i godzinę wizyty oraz pacjenta, któremu ma być przypisana
[8] Usuń wizytę -> funkcja pobiera datę i godzinę wizyty, w przypadku istnienia wizyty w danym terminie jest ona usuwana
oraz podawane są informacje o niej
[9] Wypisz wizyty dla danego dnia -> funkcja pobiera datę, wypisuje wszystkie zapisane w systemie wizyty tego
dnia
[10] Wypisz wszystkie wizyty -> funkcja wypisuje wszystkie zapisane w systemie wizyty
[11] Wypisz wizyty dla danego pacjenta -> funkcja pobiera dane o pacjencie, wypisuje wszystkie 
zapisane w systemie wizyty przypisane jemu
[12] Zakończ -> funkcja powodująca przerwanie działania programu

Wizyty są możliwe w godzinach 8-17:30, tylko i wyłącznie o godzinach pełnych lub 'wpół do', tj. albo XX:00 albo XX:30

Dane o pacjentach są zapisywane/wczytywane z pliku Patient_data.csv
Dane o wizytach są zapisywane/wczytywane z pliku Visit_data.csv
UWAGA! Wczytanie danych spowoduje utratę wszelkich manualnie wprowadzonych danych, przy czym tymi 
można albo nadpisać dane w pliku albo dopisać je do pliku

Aby skorzystać z programu należy uruchomić program main_loop.py, uruchomienie wszelkich innych skryptów .py 
spowoduje wywołanie funkcji testujących funkcjonalności zawarte w skryptach