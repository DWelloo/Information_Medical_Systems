class Display_data:
    """
    Klasa pomocnicza, pełniąca funkcję struktury 
    """

    def __init__(self) -> None:
        """
        Inicjalizuje obiekt Display_data z domyślnymi wartościami None.

        Zwraca:
        None
        """
        self.__patient = None
        self.__startdate = None
        self.__enddate = None

    def set_patient(self, patient: str) -> None:
        """
        Ustawia wartość atrybutu __patient na podstawie przekazanego argumentu.

        Argumenty:
        patient: str - PESEL pacjenta.

        Zwraca:
        None
        """
        self.__patient = patient

    def set_startdate(self, date: tuple) -> None:
        """
        Ustawia wartość atrybutu __startdate na podstawie przekazanego argumentu.

        Argumenty:
        date: tuple - Krotka zawierająca datę w formie (rok, miesiąc, dzień).

        Zwraca:
        None
        """
        self.__startdate = date

    def set_enddate(self, date: tuple) -> None:
        """
        Ustawia wartość atrybutu __enddate na podstawie przekazanego argumentu.

        Argumenty:
        date: tuple - Krotka zawierająca datę w formie (rok, miesiąc, dzień).

        Zwraca:
        None
        """
        self.__enddate = date

    def get_patient(self) -> str:
        """
        Zwraca wartość atrybutu __patient.

        Zwraca:
        str - PESEL pacjenta.
        """
        return self.__patient

    def get_startdate(self) -> tuple:
        """
        Zwraca wartość atrybutu __startdate.

        Zwraca:
        tuple - Krotka zawierająca datę w formie (rok, miesiąc, dzień).
        """
        return self.__startdate

    def get_enddate(self) -> tuple:
        """
        Zwraca wartość atrybutu __enddate.

        Zwraca:
        tuple - Krotka zawierająca datę w formie (rok, miesiąc, dzień).
        """
        return self.__enddate
    
def date_to_SQL(date:tuple) -> str:
    return f"{date[0]}-{date[1]}-{date[2]}"

def isfloat(x:str) -> bool:
    try:
        y=float(x)
    except ValueError:
        return False
    return True