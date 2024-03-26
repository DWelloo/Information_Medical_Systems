from class_Patient import Patient
from class_Visit import Visit, set_new_visit_from_keyboard
from class_Visit import input_date_data
from file_management import write_patients, read_patients, write_visits, read_visits

def filter_patients(patients:[Patient]) -> Patient:
    """
    Funkcja pozwalająca na znajdowanie obiektów typu Patient, których 
    przynajmniej jedno z pól: name,last_name lub PESEL ma wartość taką, jaka jest poszukiwana

    Parametry
    ---------
    patients: List[Patient]
        lista wszystkich zapisanych w systemie pacjentów
    
    Zwraca
    ------
    Patient
        obiekt typu Patient spełniający kryteria
    """

    print("Wyszukiwanie pacjenta, podaj jego informacje: imię,nazwisko,PESEL lub ID pacjenta")
    print()
    search_parameter=input().split()
    candidates=[]
    for i in range(len(patients)):
        if patients[i].is_match_patient(search_parameter)==True:
            candidates.append(patients[i])
    if len(candidates)>0:
        print()
        print("Znaleziono następujące wyniki:")
        i=1
        for el in candidates:
            print(i,end='. ')
            el.print()
            i+=1
            print()
        print("Wpisz numer pacjenta wedle powyższej numeracji:",end="")
        while True:
            numer_po_filtracji=int(input())
            if numer_po_filtracji>i or numer_po_filtracji<1:
                print("Błędny numer, spróbuj ponownie")
            else:
                return candidates[numer_po_filtracji-1]
    else:
        print("Nie znaleziono pacjentów spełniających podane słowa kluczowe")
        print()
        return    

def main():
    running=True
    ancilla_Visit=Visit(ancilla=True)
    ancilla_Patient=Patient(ancilla=True)
    while running:
        print("Wybierz:")
        print("[1] Dodaj pacjenta")
        print("[2] Usuń pacjenta")
        print("[3] Wyświetl pacjentów")
        print("[4] Zapisz dane do plików")
        print("[5] Dopisz dane do plików")
        print("[6] Wczytaj dane z plików")
        print("[7] Dodaj wizytę")
        print("[8] Usuń wizytę")
        print("[9] Wypisz wizyty dla danego dnia")
        print("[10] Wypisz wszystkie wizyty")
        print("[11] Wypisz wizyty dla danego pacjenta")
        print("[12] Zakończ")
        try:
            arg=int(input())
        except ValueError:
            print("Wpisana wartość powinna być liczbą")
            continue
        print()
        match arg:
            case 1:
                new_Patient=Patient(ancilla=True)
                new_Patient.set_patient_from_keyboard()
                print()
            case 2:
                patients=ancilla_Patient.get_all_patients()
                lp=len(patients)
                if lp==0:
                    print("W systemie nie ma zapisanych pacjentów")
                    print()
                    continue
                for i in range(lp):
                    print(f'[{i+1}] ',end="")
                    patients[i].print()
                    print()
                inputting=True
                while inputting:
                    print("Wybierz indeks pacjenta, którego chcesz usunąć")
                    indeks=int(input())
                    if indeks<1 or indeks>lp:
                        print("Wybór niepoprawny, spróbuj ponownie")
                    else:
                        inputting=False
                cur_patient_id=patients[indeks-1].get_PESEL()
                visits_to_remove=[]
                for el in ancilla_Visit.return_visits():
                    if el.get_patient().get_PESEL()==cur_patient_id:
                        visits_to_remove.append(el.get_code())
                for el in visits_to_remove:
                    ancilla_Visit.remove_visit(el)
                ancilla_Patient.get_all_patients().remove(ancilla_Patient.find_patient(cur_patient_id))
                print()
            case 3:
                if len(ancilla_Patient.get_all_patients())==0:
                    print("W systemie nie ma zapisanych pacjentów")
                    print()
                    continue
                for el in ancilla_Patient.get_all_patients():
                    el.print()
                    print()
            case 4:
                write_patients(ancilla_Patient.get_all_patients(),"w")
                write_visits(ancilla_Visit.return_visits(),"w")
                print()
            case 5:
                write_patients(ancilla_Patient.get_all_patients(),"a")
                write_visits(ancilla_Visit.return_visits(),"a")
                print()
            case 6:
                ancilla_Patient.wipe_all_patients()
                ancilla_Visit.wipe_visit_data()
                ancilla_Patient.set_all_patients(read_patients())
                read_visits(ancilla_Patient.get_all_patients())
                print()
            case 7:
                print("Wybierz pacjenta, dla którego chcesz dodać wizytę")
                chosen_patient=filter_patients(ancilla_Patient.get_all_patients())
                if chosen_patient==None:
                    continue
                print()
                set_new_visit_from_keyboard(chosen_patient)
                print()
            case 8:
                code=input_date_data()
                print()
                ancilla_Visit.remove_visit(code)
                print()
            case 9:
                code=input_date_data(True)
                print()
                ancilla_Visit.print_all_visits_given_day(code)
                print()
            case 10:
                all_visits=ancilla_Visit.sort_visit_data(ancilla_Visit.return_visits())
                if len(all_visits)==0:
                    print("W systemie nie ma zapisanych wizyt")
                    print()
                    continue
                for el in all_visits:
                    el.print()
                    print()
            case 11:
                print("Wybierz pacjenta, dla którego mają zostać wyświetlone wizyty")
                chosen_patient=filter_patients(ancilla_Patient.get_all_patients())
                if chosen_patient==None:
                    continue
                ancilla_Visit.print_all_visits_given_patient(chosen_patient)
            case 12:
                running=False                      
            case _:
                print("Wybór niepoprawny, spróbuj ponownie")

if __name__=="__main__":
    main()