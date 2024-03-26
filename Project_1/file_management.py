from class_Patient import Patient
from class_Visit import Visit

def write_patients(patients:[Patient],typ:str) -> None:
    """ 
    Funkcja zapisująca do pliku CSV(semicolon) zapisanych w systemie pacjentów 

    Parametry
    ---------
    patients : [Patient]
        lista pacjentów do zapisania
    typ : str
        char decydujący, czy dane mają zostać dopisane do pliku, czy nadpisać dane w pliku
    """

    patient_strings=[]
    for patient in patients:
        patient_string=patient.get_name()+";"+patient.get_last_name()+";"+patient.get_PESEL()+"\n"
        patient_strings.append(patient_string)
    file=open("Patient_data.csv",typ,encoding='UTF-8')
    for el in patient_strings:
        file.writelines(el)
    file.close()
    print("Pacjenci zostali zapisani")

def read_patients() -> [Patient]:
    """ 
    Funkcja wczytująca z pliku CSV(semicolon) dane o pacjentach 

    Zwraca
    ------
    [Patient]
        lista pacjentów 'włączana' do systemu
    """

    patients_read=[]
    patients_saved=[]
    file=open("Patient_data.csv","r",encoding='UTF-8')
    patients_read=file.readlines()
    for i in range(len(patients_read)):
        patients_read[i]=patients_read[i].strip("\n").split(";")
        new_patient=Patient(patients_read[i][0],patients_read[i][1],patients_read[i][2])
        patients_saved.append(new_patient)
    print("Pacjenci zostali wczytani")
    return patients_saved

def write_visits(visits:set,typ:str) -> None:
    """ 
    Funkcja zapisująca do pliku CSV(semicolon) zapisane w systemie wizyty

    Parametry
    ---------
    visits : set
        zbiór wizyt w systemie do zapisania
    typ : str
        char decydujący, czy dane mają zostać dopisane do pliku, czy nadpisać dane w pliku
    """

    visit_strings=[]
    for visit in visits:
        #obiekt pomocniczy ancilla_Visit będzie miał niemożliwy do stworzenia przez
        #użytkownika kod "1000000000", a jako że jest to obiekt pomocniczy, nie
        #chcemy, aby był zapisywany do pliku
        if visit.get_code()=="1000000000": 
            continue
        visit_string=visit.get_code()+";"+visit.get_patient().get_PESEL()+"\n"
        visit_strings.append(visit_string)
    file=open("Visit_data.csv",typ,encoding='UTF-8')
    for el in visit_strings:
        file.writelines(el)
    file.close()
    print("Wizyty zostały zapisane")

def read_visits(patients:[Patient]) -> None:
    """ 
    Funkcja wczytująca z pliku CSV(semicolon) dane o wizytach 

    Parametry
    ---------
    patients : [Patient]
        zbiór pacjentów, którym mają odpowiadać wizyty w pliku
    """

    visits_read=[]
    file=open("Visit_data.csv","r",encoding='UTF-8')
    visits_read+=file.readlines()
    for i in range(len(visits_read)):
        visits_read[i]=visits_read[i].strip("\n").split(";")
        new_visit=Visit(visits_read[i][0])
        new_visit.set_patient(match_visit_with_patient(patients,visits_read[i][1]))
    print("Wizyty zostały wczytane")

def match_visit_with_patient(patients:[Patient],pesel:str) -> Patient:
    """
    Funkcja pomocnicza służąca do przypisywania wizyt odpowiednim pacjentom w trakcie odczytu z pliku

    Parametry
    ---------
    patients : [Patient]
        zbiór pacjentów, w której poszukiwany jest odpowiadający wizycie pacjent
    pesel : str
        PESEL pacjenta przypisanego wizycie, dla której funkcja szuka aktualnie pacjenta

    Zwraca
    ------
    Patient
        pacjent odpowiadający danej wizycie
    """
    
    for el in patients:
        if el.get_PESEL()==pesel:
            return el
    print("Nie znaleziono pacjenta")
    return None