from calendar import monthrange
from class_Patient import Patient

class Visit:
    """
    Klasa służąca przechowywaniu i zarządzaniu informacjami 
    dotyczącymi bezpośrednio wizyt lekarskich w systemie

    Pola
    ----
    code:str
        string przechowujący informacje o dacie i godzinie wizyty lekarskiej w formacie DDMMRRRRHM, 
        gdzie H odczytywane jest jako godzina 8:00+H, czyli H=2 oznacza godzinę 8+2=10
        M przyjmuje wartości 0 i 1, 1 oznacza godzina:30, 0 oznacza godzina:00

    static __visits:set
        set przechowujący wszystkie obiekty typu Visit

    patient:Patient
        obiekt klasy Patient przechowujący informacje o pacjencie przypisanym do danej wizyty

    Metody
    ------
    set_code(code:str)->None
        przypisuje polu code wartość argumentu przekazanego

    set_patient(patient:Patient)->None
        przypisuje polu patient wartość argumentu przekazanego

    print()->None
        wyświetla wszystkie informacje o obiekcie

    return_visits()->set
        zwraca wartość statycznego pola __visits

    set_visits(visits:set)->None:
        przypisuje polu __visits wartość argumentu przekazanego

    print_all_visits()->None
        wyświetla wszystkie zapisane wizyty

    print_all_visits_given_day(code:str)->None
        wyświetla wszystkie wizyty w danym dniu przechowanym w argumencie code

    print_all_visits_given_patient(patient:Patient)->None
        wyświetla wszystkie wizyty przypisane danemu pacjentowi

    remove_visit(code:str)->None
        usuwa z pola __visits wizytę odpowiadającą argumentowi przekazanemu

    get_code()->str
        zwraca wartość pola __code obiektu

    get_patient()->Patient
        zwraca wartość pola __patient obiektu

    wipe_visit_data()->None
        zeruje zawartość pola statycznego visits 

    sort_visit_data(visits:set)->[Visit]
        sortuje wizyty po dacie od najwcześniejszej
    """
    __visits=set()

    def __init__(self,code:str="1000000000",patient:Patient=None,ancilla:bool=False) -> None:
        """
        Konstrukor klasy Visit, pozwalający na inicjację bez argumentów, bądź z nimi.

        Parametry
        ---------
        code : str, opcjonalny
            Kod reprezentujący datę i godzinę wizyty w formie "DDMMYYYYHM" 
            (dodatkowe informacje o formacie w opisie klasy)
        patient : Patient, opcjonalny
            Obiekt klasy Patient reprezentujący pacjenta, który ma umówioną wizytę
        ancilla : bool, opcjonalny 
            Flaga informująca, czy tworzony jest obiekt pomocniczy (jest on wyłącznie 
            używany przy pewnych operacjach, jest niewidoczny dla użytkownika w trakcie 
            działania programu)
        """

        self.set_code(code)
        self.set_patient(patient)
        for el in Visit.__visits:
            if el.__code==self.__code:
                print("Należy wybrać inny termin. Ten już jest zajęty")
                return
        if ancilla==False:
            Visit.__visits.add(self)
        
    def set_code(self,code:str) -> None:
        """ 
        Metoda przypisująca polu code obiektowi klasy Visit przekazaną wartość

        Parametry
        ----------
        code : str
            Kod reprezentujący datę i godzinę wizyty w formacie "DDMMYYYYHM" 
            (dodatkowe informacje o formacie w opisie klasy)
        """

        self.__code=code
        
    def set_patient(self,patient:Patient) -> None:
        """ 
        Metoda przypisująca polu patient obiektowi klasy Visit przekazaną wartość

        Parametry
        ----------
        patient : Patient
            Obiekt klasy Pacjent reprezentujący pacjenta na wizycie.
        """

        self.__patient=patient

    def print(self) -> None:
        """ 
        Metoda wyświetlająca informacje o dacie wizyty oraz przypisanemu pacjentowi 
        """

        year=self.__code[4:8]
        month=self.__code[2:4]
        day=self.__code[0:2]
        hour=str(int(self.__code[8])+8)
        minutes=self.__code[9]
        print("Informacje o wizycie:")
        print(f"Data:{hour}:",end="",sep="")
        if minutes=="0":
            print("00",end=", ")
        else:
            print("30",end=", ")
        print(f"{day}.{month}.{year}",sep="")
        if self.__patient==None:
            print("Wizycie nie przypisano pacjenta")
        else:
            self.__patient.print()

    def return_visits(self) -> set:
        """ 
        Metoda zwracająca wszystkie zapisane wizyty 

        Zwraca
        ------
        set
            Zbiór wszystkich zapisanych wizyt
        """

        return Visit.__visits
    
    def set_visits(self,visits:set) -> None:
        """ 
        Metoda przypisująca polu __visits przekazaną wartość 
        
        Parametry
        ----------
        wizyty : set
            Zbiór wizyt do przypisania.
        """

        Visit.__visits=visits

    def print_all_visits(self) -> None:
        """ 
        Metoda wyświetlająca wszystkie zapisane wizyty 
        """

        for el in Visit.__visits:
            el.print()

    def print_all_visits_given_day(self,code:str) -> None:
        """ 
        Metoda wyświetlająca wszystkie wizyty w danym dniu 
        
        Parametry
        ----------
        code : str
            Kod reprezentujący datę w formacie "DDMMYYYY"
        """
        
        matched_visits=[]
        for el in Visit.__visits:
            if el.__code[0:8]==code:
                matched_visits.append(el)
        if matched_visits==[]:
            print("Nie ma wizyt w podanym dniu")
            return
        print()
        matched_visits=self.sort_visit_data(matched_visits)
        print("Znaleziono następujące wyniki:")
        for el in matched_visits:
            el.print()
            print()

    def print_all_visits_given_patient(self,patient:Patient) -> None:
        """ 
        Metoda wyświetlająca wszystkie wizyty dla danego pacjenta 
        
        Parametry
        ----------
        patient : Patient
            Obiekt klasy Patient reprezentujący pacjenta.
        """

        matched_visits=[]
        for el in Visit.__visits:
            if el.__patient==patient:
                matched_visits.append(el)
        if matched_visits==[]:
            print("Nie ma wizyt w systemie dla podanego pacjenta")
            return
        print()
        matched_visits=self.sort_visit_data(matched_visits)
        print("Znaleziono następujące wyniki:")
        for el in matched_visits:
            el.print()
            print()

    def remove_visit(self,code:str) -> None:
        """ 
        Metoda usuwająca wybrany obiekt typu Visit 
        
        Parametry
        ----------
        code : str
            Kod reprezentujący datę i godzinę wizyty w formacie "DDMMYYYYHH"
            (dodatkowe informacje o formacie w opisie klasy)
        """

        for el in Visit.__visits:
            if el.__code==code:
                print("Usunięto następującą wizytę",end="\n")
                el.print()
                Visit.__visits.remove(el)
                return
        print("Nie znaleziono wizyty w tym terminie")

    def get_code(self) -> str:
        """ 
        Metoda zwracająca wartość pola code obiektu 
        
        Zwraca
        -------
        str
            Kod reprezentujący datę i godzinę wizyty w formacie "DDMMYYYYHM"
            (dodatkowe informacje o formacie w opisie klasy)
        """

        return self.__code
    
    def get_patient(self) -> Patient:
        """ 
        Metoda zwracająca wartość pola patient obiektu 
        
        Zwraca
        -------
        Patient
            Obiekt klasy Patient reprezentujący pacjenta na wizycie
        """

        return self.__patient
    
    def wipe_visit_data(self) -> None:
        """
        Metoda zerująca zawartość pola statycznego visits 
        """
        Visit.__visits=set()

    def sort_visit_data(self,visits:set) -> list:
        """
        Metoda sortująca wszystkie zapisane wizyty po datach

        Parametry
        ---------
        visits : set
            zbiór wizyt do posortowania po dacie i godzinie

        Zwraca
        ------
        [Visit]
            posortowana lista wizyt po dacie i godzinie
        """
        ancilla_list=list(visits)
        for i in range(len(ancilla_list)):
            mini=i
            for j in range(i+1,len(ancilla_list)):
                if compare_codes(ancilla_list[j].get_code(),ancilla_list[mini].get_code()):
                    mini=j
            ancilla_list[i],ancilla_list[mini]=ancilla_list[mini],ancilla_list[i]
        return ancilla_list

def compare_codes(code1:str,code2:str) -> bool:
    """
    Funkcja pomocnicza, porównująca 2 daty na podstawie odpowiadającym im kodom

    Parametry
    ---------
    code1 : str
        kod do porównania
    code2 : str
        kod do porównania
    
    Zwraca
    ------
    bool
        wartość logiczna zdania: data będąca I argumentem jest 
        wcześniejsza niż data II argumentu
    """
    
    if int(code1[4:8])>int(code2[4:8]):
        return False
    flag1=int(code1[4:8])<int(code2[4:8])
    flag2=(int(code1[4:8])==int(code2[4:8]))*(int(code1[2:4])<int(code2[2:4]))
    flag3=(int(code1[2:4])==int(code2[2:4]))*(int(code1[0:2])<int(code2[0:2]))
    flag4=(int(code1[0:2])==int(code2[0:2]))*(int(code1[8])<int(code2[8]))
    flag5=(int(code1[8])==int(code2[8]))*(int(code1[9])<int(code2[9]))
    return bool(flag1+flag2+flag3+flag4+flag5)
    
def set_new_visit_from_keyboard(patient:Patient) -> None:
    """ 
    Funkcja pozwalająca na stworzenie nowej wizyty z poziomu klawiatury 
    
    Parametry
    ----------
    patient : Patient
        Obiekt klasy Patient reprezentujący pacjenta na nowej wizycie
    """

    code=input_date_data()
    new_visit=Visit(code,patient)

def input_date_data(onlyday:bool=False) -> str:
    """ 
    Funkcja pozwalająca wygenerować kod na podstawie 
    danych wejściowych odnośnie daty wizyty 
    
    Parametry
    ----------
    onlyday : bool, opcjonalny
        Flaga pomocnicza wskazująca, czy aktualnie wprowadzana jest data 
        co do dnia, czy do godziny i minuty

    Zwraca
    -------
    str
        Wygenerowany kod reprezentujący datę i godzinę wizyty
    """
    
    print("Podaj pożądany termin:")
    year=input_visit_data("Rok")
    month=input_visit_data("Miesiąc")
    if len(month)==1:
        month="0"+month
    day=input_visit_data("Dzień",month,year)
    if len(day)==1:
        day="0"+day
    if onlyday==False:
        hour=input_visit_data("Godzina")
        minutes=input_visit_minutes_data()
        data_tuple=(day,month,year,hour,minutes)
    else:
        data_tuple=(day,month,year)
    code="".join(data_tuple)
    return code

def input_visit_data(name:str,month:str=None,year:str=None) -> str:
    """ 
    Funkcja pomocnicza dla funkcji 'input_date_data', 
    służąca przyjęciu i weryfikacji danych wejściowych 
    
    Parametry
    ----------
    name : str
        Nazwa pola wprowadzanego (np. "Rok", "Miesiąc", "Dzień", "Godzina")
    month : str, opcjonalny
        Miesiąc, jeżeli podany
    year : str, opcjonalny
        Rok, jeżeli podan

    Zwraca
    -------
    str
        Wprowadzone dane przedstawione w postaci kodu opisanego w opisie klasy Visit
    """

    if month==None and year==None:
        dayrange=31
    else:
        dayrange=(monthrange(int(year),int(month))[1])
    low_boundaries={"Rok":1980,"Miesiąc":1,"Dzień":1,"Godzina":8}
    high_boundaries={"Rok":9999,"Miesiąc":12,"Dzień":dayrange,"Godzina":17}
    while True:
        print(f"{name}:",sep="",end="")
        data=input()
        if not(data.isdigit()):
            print(f"Wartość zmiennej {name} powinna być liczbą. Spróbuj ponownie")
        elif low_boundaries[name]>int(data):
            print(f"{name} powinien przyjmować wartość niemniejszą niż {low_boundaries[name]}. Spróbuj ponownie")
        elif high_boundaries[name]<int(data):
            print(f"{name} powinien przyjmować wartość niewiększą niż {high_boundaries[name]}. Spróbuj ponownie")
        else:
            if name=="Godzina":
                data=str(int(data)-8)
            return data

def input_visit_minutes_data() -> str:
    """ 
    Funkcja pomocnicza dla funkcji 'input_date_data', 
    służąca przyjęciu i weryfikacji danych odnośnie minuty wizyty 
    
    Zwraca
    -------
    str
        Wprowadzona wartość jako znak.
    """

    while True:
        print("Wpisz 0, jeżeli wizyta ma być o pełnej godzinie, 1 jeżeli ma być 30 po")
        data=input()
        if data not in ["0","1"]:
            print("Podana liczba powinna być z zakresu [0;1]. Spróbuj ponownie")
            continue
        else:
            return data
        
if __name__=="__main__":
    visit=Visit("2707200281")
    visit.print()
    p1=Patient("Dwelloo","Eoooo","324021")
    visit.set_patient(p1)
    visit.print()
    new_visit=Visit("3220199990",p1)
    print()
    visit.print_all_visits()
    print()
    visit.print_all_visits_given_day("27.07.2002")
    print()
    set_new_visit_from_keyboard(p1)
    print()
    visit.print_all_visits()