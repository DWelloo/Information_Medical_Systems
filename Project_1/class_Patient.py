class Patient:
    """
    Klasa służąca przechowywaniu i zarządzaniu informacjami 
    dotyczącymi bezpośrednio Pacjentów w systemie 

    Pola
    ----
    __name:str
        string przechowujący informacje o imieniu pacjenta

    __last_name:str
        string przechowujący informacje o nazwisku pacjenta

    __PESEL:str
        string przechowujący informacje o PESELu pacjenta

    static __patients:set
        set przechowujący wszystkich pacjentów

    Metody
    ------
    set_name(name:str)->None
        metoda przypisująca polu __name wartość argumentu przekazanego

    set_last_name(last_name:str)->None
        metoda przypisująca polu __last_name wartość argumentu przekazanego

    set_PESEL(pesel:str)->None
        metoda przypisująca polu __PESEL wartość argumentu przekazanego

    is_match_patient(arg:[str])->bool
        metoda sprawdzająca, czy dla podanych fraz wyszukiwania 
        znajdujących się w argumencie przekazanym odpowiadają jakiekolwiek 
        wartości pól obiektu

    print()->None
        metoda wyświetlająca informacje o obiekcie

    set_name_from_keyboard()->None
        metoda pozwalająca na przypisanie polu name wpisanej przez użytkownika 
        z poziomu klawiatury wartości

    set_last_name_from_keyboard()->None
        metoda pozwalająca na przypisanie polu last_name wpisanej przez użytkownika 
        z poziomu klawiatury wartości

    set_PESEL_from_keyboard()->None
        metoda pozwalająca na przypisanie polu PESEL wpisanej przez użytkownika 
        z poziomu klawiatury wartości

    set_patient_from_keyboard()->None
        metoda pozwalająca na przypisanie wszystkim polom obiektu wpisanych przez użytkownika 
        z poziomu klawiatury wartości

    validate_PESEL(pesel:str)->bool
        metoda weryfikująca poprawność przekazanego nr PESEL

    get_name()->str
        metoda zwracająca wartość pola __name obiektu

    get_last_name()->str
        metoda zwracająca wartość pola __last_name obiektu

    get_PESEL()->str
        metoda zwracająca wartość pola __PESEL obiektu

    wipe_all_patients()->None
        metoda usuwająca wszystkich zapisanych pacjentów w polu __patients

    get_all_patients()->[Patient]
        metoda zwracająca wartość pola __patients

    set_all_patients(new_patients:[Patient])->None
        metoda przypisująca polu __patients wartość argumentu przekazanego

    find_patient(pesel:str)->Patient
        metoda przeszukująca zawartość pola __patients w poszukiwaniu
        obiektu o polu __PESEL odpowiadającym wartości argumentu przekazanego
    """

    __patients=[]

    def __init__(self,name:str="",last_name:str="",PESEL:str="11111111111",ancilla:bool=False) -> None:
        """
        Konstruktor klasy Patient, umożliwiający inicjalizację obiektu bez 
        żadnych danych lub części danych

        Parametry
        ----------
        name : str, opcjonalny
            Imię pacjenta (domyślnie puste).
        last_name : str, opcjonalny
            Nazwisko pacjenta (domyślnie puste).
        PESEL : str, opcjonalny
            Numer PESEL pacjenta (domyślnie "11111111111").
        ancilla : bool, opcjonalny
            Flaga, która jeśli ustawiona na True, pozwala na inicjalizację 
            obiektu bez przypisywania ID (domyślnie False)
        """

        self.set_name(name)
        self.set_lastname(last_name)
        self.set_PESEL(PESEL)
        if ancilla==True:
            return
        Patient.__patients.append(self)

    def set_name(self,name:str) -> None:
        """
        Metoda przypisująca polu name klasy Patient wartość przekazaną

        Parametry
        ----------
        name : str
            Imię pacjenta
        """

        #ze względu na np. dzieci Elona Muska zakładana jest możliwość wystąpienia 
        # w czyjeś godności znaków innych niż alfabetyczne (stąd brak kontroli argumentu typu .isalpha())
        self.__name=name

    def set_lastname(self,lastname:str) -> None:
        """ 
        Metoda przypisująca polu last_name klasy Patient wartość przekazaną 
        
        Parametry
        ----------
        lastname : str
            Nazwisko pacjenta.
        """

        #ze względu na np. dzieci Elona Muska zakładana jest możliwość wystąpienia 
        # w czyjeś godności znaków innych niż alfabetyczne (stąd brak kontroli argumentu typu .isalpha())
        self.__last_name=lastname

    def set_PESEL(self,pesel:str) -> None:
        """ 
        Metoda przypisująca polu PESEL klasy Patient wartość przekazaną

        Parametry
        ----------
        pesel : str
            Numer PESEL pacjenta
        """

        if self.validate_PESEL(pesel)==True:
            self.__PESEL=pesel
        else:
            print("Z powodu błędów w PESELU nie został on ustawiony")
    
    def is_match_patient(self,arg:[str]) -> bool:
        """ 
        Metoda sprawdzająca, czy dla podanych fraz wyszukiwania (arg) 
        odpowiadają jakiekolwiek pola obiektów klasy Patient 
        
        Parametry
        ----------
        arg : List[str]
            Lista fraz wyszukiwania.

        Zwraca
        -------
        bool
            True, jeśli dla przynajmniej jednej frazy odpowiada pole obiektu Patient; 
            False w przeciwnym razie.
        """

        attributes=[self.__name,self.__last_name,self.__PESEL]
        for el in arg:
            if el in attributes:
                return True
        return False
    
    def print(self) -> None:
        """ 
        Metoda wypisująca wszystkie informacje o Pacjencie 
        """

        print("Informacje o pacjencie:")
        print(f"Imię i nazwisko: {self.__name} {self.__last_name}")
        print(f"nr PESEL: {self.__PESEL}")

    def set_name_from_keyboard(self) -> None:
        """ 
        Metoda pozwalająca na wprowadzenie wartości 
        pola name z poziomu klawiatury 
        """

        print("Podaj imię: ")
        name=input()
        self.set_name(name)

    def set_last_name_from_keyboard(self) -> None:
        """ 
        Metoda pozwalająca na wprowadzenie wartości 
        pola last_name z poziomu klawiatury 
        """

        print("Podaj nazwisko: ")
        lname=input()
        self.set_lastname(lname)

    def set_PESEL_from_keyboard(self) -> None:
        """ 
        Metoda pozwalająca na wprowadzenie wartości 
        pola PESEL z poziomu klawiatury 
        """

        inputing=True
        while inputing:
            print("Podaj PESEL")
            pesel=input()
            if self.validate_PESEL(pesel)==True:
                if self.find_patient(pesel)!=None:
                    print("W systemie istnieje już pacjent z takim nr PESEL")
                else:
                    self.__PESEL=pesel
                    inputing=False
        
    def set_patient_from_keyboard(self) -> None:
        """ 
        Metoda pozwalająca na wprowadzenie wartości wszystkich pól klasy z poziomu klawiatury 
        """

        self.set_name_from_keyboard()
        self.set_last_name_from_keyboard()
        self.set_PESEL_from_keyboard()
        Patient.__patients.append(self)
    
    def validate_PESEL(self,pesel:str) -> bool:
        """ 
        Metoda weryfikująca poprawność podanego nr PESEL 
        
        Parametry
        ---------
        pesel : str
            PESEL do weryfikacji

        Zwraca
        ------
        bool
            True, jeżeli podany pesel spełnia wymogi nr PESEL, w przeciwnym razie False
        """

        if pesel.isdigit()==False:
            print("PESEL nie może zawierać znaków innych niż cyfry")
            return False
        return True
    
    def get_name(self) -> str:
        """ 
        Metoda zwracająca wartość pola name obiektu 
        
        Zwraca
        ------
        str
            wartość pola name obiektu
        """

        return self.__name
    
    def get_last_name(self) -> str:
        """ 
        Metoda zwracająca wartość pola last_name obiektu 
        
        Zwraca
        ------
        str
            wartość pola last_name obiektu
        """

        return self.__last_name
    
    def get_PESEL(self) -> str:
        """ 
        Metoda zwracająca wartość pola PESEL obiektu 
        
        Zwraca
        ------
        str
            wartość pola PESEL obiektu        
        """

        return self.__PESEL

    def wipe_all_patients(self) -> None:
        """
        Metoda usuwająca zawartość pola statycznego __patients
        """

        Patient.__patients=[]

    def get_all_patients(self) -> list:
        """
        Metoda zwracająca wartość pola statycznego __patients

        Zwraca
        ------
        [Patient]
            lista wszystkich pacjentów
        """

        return Patient.__patients
    
    def set_all_patients(self,new_patients:list) -> None:
        """
        Metoda przypisująca polu statycznemu __patients
        wartość argumentu przekazanego

        Parametry
        ---------
        new_patients : [Patient]
            lista pacjentów, którzy mają znaleźć się w systemie
        """

        Patient.__patients=new_patients

    def find_patient(self,pesel:str,disp_info:bool=True) -> object:
        """
        Metoda wyszukujaca pacjenta po nr PESEL

        Parametry
        ---------
        pesel : str
            nr PESEL szukanego pacjenta

        Zwraca
        ------
        Patient
            znaleziony pacjent (w przypadku nie znalezienia nikogo metoda zwraca None)
        """

        for el in Patient.__patients:
            if el.get_PESEL()==pesel:
                return el
        if disp_info==True:
            print("Nie znaleziono pacjenta")
        return None

def test_class_patient():
    p1=Patient()
    p2=Patient(name='Dominik',PESEL='1234')
    p3=Patient('Adam','Poziomka','324215029')
    p1.print()
    print()
    p2.print()
    print()
    p3.print()
    p_control=Patient()
    print()
    for el in p_control.get_all_patients():
        el.print()
        print()

if __name__=="__main__":
    test_class_patient()