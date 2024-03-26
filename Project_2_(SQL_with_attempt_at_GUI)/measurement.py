from patient import Patient
from matplotlib import pyplot as plt

class Measurement:
    """
    Klasa reprezentująca pomiar związany z pacjentem, zawierająca informacje takie jak data, godzina, wynik i pacjent.

    Atrybuty:
    __patient (str): PESEL pacjenta, którego dotyczy pomiar.
    __date (tuple): Data pomiaru w formacie (rok, miesiąc, dzień).
    __time (str): Godzina pomiaru w formacie HH:MM.
    __result (float): Wynik pomiaru.
    
    Metody:
    __init__(self, datex: tuple = None, patient: str = None, time: str = None, result: float = None, aux: bool = False) -> None:
        Inicjalizuje nowy obiekt Measurement z określoną datą, pacjentem, godziną i wynikiem.

    get_patient(self) -> str:
        Zwraca nazwę pacjenta, którego dotyczy pomiar.

    get_date(self) -> tuple:
        Zwraca datę pomiaru w formacie (rok, miesiąc, dzień).

    get_date_SQL(self) -> str:
        Zwraca datę pomiaru w formacie do zapisu w bazie danych SQL.

    get_time(self) -> str:
        Zwraca godzinę pomiaru w formacie HH:MM.

    get_result(self) -> float:
        Zwraca wynik pomiaru.

    set_patient(self, patient: str = None) -> None:
        Ustawia nowego pacjenta dla pomiaru.

    set_date(self, datex: tuple = None) -> None:
        Ustawia nową datę pomiaru.

    set_time(self, time: str = None) -> None:
        Ustawia nową godzinę pomiaru.

    set_result(self, result: float = None) -> None:
        Ustawia nowy wynik pomiaru.

    compare_dates(self, dat1: tuple = None, dat2: tuple = None) -> bool:
        Metoda porównująca daty dwóch pomiarów.

    """

    def __init__(self, datex: tuple = None, patient: str = None, time: str = None, result: float = None, aux: bool = False) -> None:
        """
        Inicjalizuje nowy obiekt Measurement z określoną datą, pacjentem, godziną i wynikiem.

        Argumenty:
        datex: tuple - Data pomiaru w formacie (rok, miesiąc, dzień).
        patient: str - PESEL pacjenta, którego dotyczy pomiar.
        time: str - Godzina pomiaru w formacie HH:MM.
        result: float - Wynik pomiaru.
        aux: bool - Opcjonalny parametr, kontroluje specjalny przypadek.
        """
        if aux:
            return
        self.__patient = patient
        self.__date = datex
        self.__time = time
        self.__result = result

    def get_patient(self) -> str:
        """
        Zwraca nazwę pacjenta, którego dotyczy pomiar.

        Zwraca:
        str: Nazwa pacjenta.
        """
        return self.__patient
    
    def get_date(self) -> tuple:
        """
        Zwraca datę pomiaru w formacie (rok, miesiąc, dzień).

        Zwraca:
        tuple: Data pomiaru.
        """
        return self.__date
    
    def get_date_SQL(self) -> str:
        """
        Zwraca datę pomiaru w formacie do zapisu w bazie danych SQL.

        Zwraca:
        str: Data pomiaru w formacie SQL.
        """
        return f"{self.get_date()[0]}-{self.get_date()[1]}-{self.get_date()[2]}"
    
    def get_time(self) -> str:
        """
        Zwraca godzinę pomiaru w formacie HH:MM.

        Zwraca:
        str: Godzina pomiaru.
        """
        return self.__time
    
    def get_result(self) -> float:
        """
        Zwraca wynik pomiaru.

        Zwraca:
        float: Wynik pomiaru.
        """
        return self.__result
    
    def set_patient(self, patient: str = None) -> None:
        """
        Ustawia nowego pacjenta dla pomiaru.

        Argumenty:
        patient: str - Nowa nazwa pacjenta.
        """
        self.__patient = patient

    def set_date(self, datex: tuple = None) -> None:
        """
        Ustawia nową datę pomiaru.

        Argumenty:
        datex: tuple - Nowa data pomiaru.
        """
        self.__date = datex

    def set_time(self, time: str = None) -> None:
        """
        Ustawia nową godzinę pomiaru.

        Argumenty:
        time: str - Nowa godzina pomiaru w formacie HH:MM.
        """
        self.__time = time

    def set_result(self, result: float = None) -> None:
        """
        Ustawia nowy wynik pomiaru.

        Argumenty:
        result: float - Nowy wynik pomiaru.
        """
        self.__result = result 

    def compare_dates(self, dat1: tuple = None, dat2: tuple = None) -> bool:
        """
        Metoda porównująca daty dwóch pomiarów.

        Argumenty:
        dat1: tuple - Pierwsza data do porównania.
        dat2: tuple - Druga data do porównania.

        Zwraca:
        bool: Wartość logiczna stwierdzająca, czy dat1 jest wcześniejsza niż dat2.
        """
        if dat1[0] > dat2[0]:
            return False
        if dat1[0] == dat2[0] and dat1[1] > dat2[1]:
            return False
        if dat1[0] == dat2[0] and dat1[1] == dat2[1] and dat1[2] > dat2[2]:
            return False
        return True

def graph_measurements(arr: list = None, max_val: float = 140.0, min_val: float = 80.0):
    """
    Funkcja rysująca wykres pomiarów glukozy we krwi.

    Argumenty:
    arr: list - Lista pomiarów do przedstawienia na wykresie.
    max_val: float - Górna granica zakresu normy na wykresie (domyślnie 140.0).
    min_val: float - Dolna granica zakresu normy na wykresie (domyślnie 80.0).
    """
    colors = [bool(el[4] <= max_val and el[4] >= min_val) * 'g' + bool(el[4] > max_val) * 'r' + bool(el[4] < min_val) * 'b' for el in arr]
    x_vals = [f"{el[2]},{el[3]}" for el in arr]
    y_vals = [el[4] for el in arr]

    plt.scatter(x_vals, y_vals, s=50, c=colors)
    plt.xlabel("Data pomiaru")
    plt.ylabel("Ilość glukozy we krwi [mg/dl]")
    plt.tick_params(axis='x', labelrotation=90)
    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    m=Measurement()
    print(m.compare_dates(dat1=(2014,13,13),dat2=(2014,10,30)))
    print(m.compare_dates((2005,5,28),(2013,5,10)))