class Patient:
    """
    Klasa reprezentująca pacjenta z podstawowymi informacjami, takimi jak imię, nazwisko i PESEL.

    Atrybuty:
    __name (str): Imię pacjenta.
    __lname (str): Nazwisko pacjenta.
    __PESEL (str): Numer PESEL pacjenta.

    Metody:
    __init__(self, name: str = "", lname: str = "", PESEL: str = "") -> None:
        Inicjalizuje nowy obiekt pacjenta z określonym imieniem, nazwiskiem i numerem PESEL.

    get_name(self) -> str:
        Zwraca imię pacjenta.

    get_lname(self) -> str:
        Zwraca nazwisko pacjenta.

    get_PESEL(self) -> str:
        Zwraca numer PESEL pacjenta.

    set_name(self, name: str) -> None:
        Ustawia nowe imię pacjenta.

    set_lname(self, lname: str) -> None:
        Ustawia nowe nazwisko pacjenta.

    set_PESEL(self, pesel: str) -> None:
        Ustawia nowy numer PESEL pacjenta.

    """
    
    def __init__(self, name: str = "", lname: str = "", PESEL: str = "") -> None:
        """
        Inicjalizuje obiekt Patient z podanymi wartościami lub pustymi stringami.

        Argumenty:
        name: str - Imię pacjenta.
        lname: str - Nazwisko pacjenta.
        PESEL: str - Numer PESEL pacjenta.

        Zwraca:
        None
        """
        
        self.__name = name
        self.__lname = lname
        self.__PESEL = str(PESEL)

    def get_name(self) -> str:
        """
        Zwraca imię pacjenta.

        Zwraca:
        str - Imię pacjenta.
        """

        return self.__name

    def get_lname(self) -> str:
        """
        Zwraca nazwisko pacjenta.

        Zwraca:
        str - Nazwisko pacjenta.
        """

        return self.__lname

    def get_PESEL(self) -> str:
        """
        Zwraca numer PESEL pacjenta.

        Zwraca:
        str - Numer PESEL pacjenta.
        """

        return self.__PESEL

    def set_name(self, name: str) -> None:
        """
        Ustawia imię pacjenta na podstawie przekazanego argumentu.

        Argumenty:
        name: str - Nowe imię pacjenta.

        Zwraca:
        None
        """

        self.__name = name

    def set_lname(self, lname: str) -> None:
        """
        Ustawia nazwisko pacjenta na podstawie przekazanego argumentu.

        Argumenty:
        lname: str - Nowe nazwisko pacjenta.

        Zwraca:
        None
        """

        self.__lname = lname

    def set_PESEL(self, pesel: str) -> None:
        """
        Ustawia numer PESEL pacjenta na podstawie przekazanego argumentu.

        Argumenty:
        pesel: str - Nowy numer PESEL pacjenta.

        Zwraca:
        None
        """

        self.__PESEL = pesel