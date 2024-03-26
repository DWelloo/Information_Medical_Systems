import tkinter as tk
from tkinter import ttk

from patient import Patient
from measurement import Measurement,graph_measurements
from display_data import Display_data,date_to_SQL
from input_backend import *
from input_frontend import *

import random

win=tk.Tk()
win.geometry("500x100")
win.resizable(False,False)
try:
    mydb,cur=establish_connection()
except Exception:
    frame=tk.Frame(win,width=500,height=100)
    frame.place(x=0,y=0)
    lconfirm=tk.Label(frame,
        text="Wystąpił błąd w trakcie łączenia z bazą danych. Program nie będzie funkcjonował\n poprawnie, dlatego zostanie zamknięty.")
    lconfirm.place(x=10,y=10)

    butconfirm=tk.Button(frame,text="Ok",command=exit)
    butconfirm.place(x=180,y=50)
    win.mainloop()

try:
    win.geometry("800x600")
except Exception:
    exit()

establish_database(cur,mydb)

global AuxMes
AuxMes=Measurement()

def create_test_data():
    pesels=[]
    for i in range(49):
        random_name=random.choice(["Adam","Jacek","Dominik","Patryk"])
        random_lname=random.choice(["D","C","W","K","S"])
        while True:
            random_pes=str(random.randint(1000,2221))
            if random_pes not in pesels:
                pesels.append(random_pes)
                break
        p=Patient(random_name,random_lname,random_pes)
        cur.execute("INSERT INTO patients (name,last_name,PESEL) VALUES (%s,%s,%s);",params=(p.get_name(),p.get_lname(),p.get_PESEL(),))
        mydb.commit()
        pesels.append(random_pes)

    p=Patient("X","D","2222")
    pesels.append(2222)
    cur.execute(f"INSERT INTO patients (name,last_name,PESEL) VALUES ('{p.get_name()}','{p.get_lname()}','{p.get_PESEL()}');")
    mydb.commit()

    for i in range(20):
        m=Measurement((2023,12,random.randint(3,31)),"2222",f"{random.randint(1,13)}:{random.randint(0,59)}",random.randint(50,150))
        cur.execute(f"INSERT INTO measurements (PESEL,date,time,result) VALUES ('{m.get_patient()}','{m.get_date_SQL()}','{m.get_time()}',{m.get_result()});")
        mydb.commit()

    for i in range(20):
        m=Measurement((2023,12,random.randint(3,31)),random.choice(pesels),f"{random.randint(1,13)}:{random.randint(0,59)}",random.randint(50,150))
        cur.execute(f"INSERT INTO measurements (PESEL,date,time,result) VALUES ('{m.get_patient()}','{m.get_date_SQL()}','{m.get_time()}',{m.get_result()});")
        mydb.commit()

def main():
    """
    Główna funkcja inicjująca interfejs graficzny aplikacji i ustawiająca przyciski dla różnych funkcji.
    """
    frame=tk.Frame(win,width=800,height=600,bg="grey")
    frame.place(x=0,y=0)

    butaddpatient=tk.Button(frame,text="Dodaj pacjenta",command=patient_add_screen)
    butaddpatient.place(x=10,y=20)

    butdelpatient=tk.Button(frame,text="Usuń pacjenta",command=patient_drop_screen)
    butdelpatient.place(x=10,y=50)

    butshowpatient=tk.Button(frame,text="Wyświetl pacjentów",command=patient_print_screen)
    butshowpatient.place(x=10,y=80)

    butaddmeas=tk.Button(frame,text="Dodaj pomiar",command=meas_add_screen)
    butaddmeas.place(x=10,y=110)

    butprintchosen=tk.Button(frame,text="Usuń pomiar",command=meas_delete_screen)
    butprintchosen.place(x=10,y=140)

    butshowmeas=tk.Button(frame,text="Wyświetl pomiary dla danego pacjenta",command=meas_choose_patient_print_screen)
    butshowmeas.place(x=10,y=170)                                            


####################################
#   funkcje związane z pomiarami   #
####################################

#############################################
#   funkcje związane z dodawaniem pomiaru   #
#############################################
def meas_add_screen():
    """
    Funkcja do tworzenia interfejsu graficznego dodawania pomiarów medycznych.
    """
    m=Measurement()

    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    butmenu=tk.Button(frame,text="Wróć do menu",command=main)
    butmenu.place(x=10,y=30)

    lpatientdata=tk.Label(frame,text="Wyszukaj pacjenta",foreground="white",background="black")
    lpatientdata.place(x=200,y=10)
    entpatientdata=tk.Entry(frame,background="grey",width=20)
    entpatientdata.place(x=200,y=30)
    butentpatientdata=tk.Button(frame,text="OK",command=lambda: find_patient(entpatientdata))
    butentpatientdata.place(x=200,y=50,width=30,height=20)

    lpatientinput=tk.Label(frame,text="Podaj PESEL pacjenta",foreground="white",background="black")
    lpatientinput.place(x=200,y=80)
    entpatientinput=tk.Entry(frame,background="grey",width=20)
    entpatientinput.place(x=200,y=110)
    laccpatientinput=tk.Label(frame,text="",foreground="white",background="black")
    butentpatientinput=tk.Button(frame,text="OK",
        command=lambda: accept_patient_input(m,entpatientinput,laccpatientinput))
    butentpatientinput.place(x=200,y=140,width=30,height=20)

    lcalendar=tk.Label(frame,text="",foreground="white",background="black")
    butent2=tk.Button(frame,text="Wybierz datę",command=lambda: calendar_screen(frame,m))#dodać label
    butent2.place(x=200,y=170,width=200,height=20)

    lclock=tk.Label(frame,text="",foreground="white",background="black")
    butent3=tk.Button(frame,text="Wybierz godzinę",command=lambda: time_screen(frame,m,lclock))
    butent3.place(x=200,y=200,width=200,height=20)

    lresult=tk.Label(frame,text="Podaj wynik pomiaru",foreground="white",background="black")
    lresult.place(x=200,y=230)
    entresult=tk.Entry(frame,background="grey",width=20)
    entresult.place(x=200,y=260)
    laccresultinput=tk.Label(frame,text="",foreground="white",background="black")
    butentresultinput=tk.Button(frame,text="OK",
        command=lambda: accept_result_input(m,entresult,laccresultinput))
    butentresultinput.place(x=200,y=290,width=30,height=20)

    laddpatient=tk.Label(frame,text="Dodaj pomiar",foreground="white",background="black")
    laddpatient.place(x=200,y=320)
    laccaddpatient=tk.Label(frame,text="",foreground="white",background="black")
    butent4=tk.Button(frame,text="OK",command=lambda: add_meas(m,laccaddpatient))
    butent4.place(x=200,y=350,width=30,height=20)

def accept_patient_input(meas:Measurement=None,ent:tk.Entry=None,label:tk.Label=None):
    """
    Akceptuje dane wejściowe od pacjenta i sprawdza poprawność podanego numeru PESEL.

    Parametry:
    - meas (Measurement): Obiekt pomiaru.
    - ent (tk.Entry): Widget Entry dla danych wejściowych pacjenta.
    - label (tk.Label): Etykieta do wyświetlania komunikatów walidacyjnych.
    """
    pesel=ent.get()
    flag=pesel.isnumeric()
    if flag==False:
        label.config(text="PESEL powinien składać się wyłącznie z cyfr",foreground="white")
    else:
        cur.execute("SELECT * FROM patients WHERE PESEL=%s;",params=(pesel,))
        candidates=cur.fetchall()
        if candidates==[]:
            label.config(text=f"Nie znaleziono pacjenta o PESELu:{pesel}",foreground="white")
        else:
            meas.set_patient(pesel)
            label.config(text="Pomyślnie wybrano pacjenta",foreground="white")
    label.place(x=330,y=80)

def add_meas(meas:Measurement=None,label:tk.Label=None):
    """
    Dodaje pomiar medyczny do bazy danych.

    Parametry:
    - meas (Measurement): Obiekt pomiaru.
    - label (tk.Label): Etykieta do wyświetlania komunikatów sukcesu lub błędu.
    """
    if meas.get_date()==None or meas.get_patient()==None or meas.get_time()==None or meas.get_result()==None:
        label.config(text="Przynajmniej jedno z pól jest nieuzupełnione, bądź\n uzupełnione niepoprawnie. Pomiar nie zostanie dodany",
                     foreground="white")
    else:
        try:
            cur.execute("SELECT * FROM measurements WHERE date=%s AND time=%s AND PESEL=%s ;",params=(meas.get_date_SQL(),meas.get_time(),meas.get_patient(),))
            collisions=cur.fetchall()
        except Exception:
            label.config(text="Wystąpił błąd związany z funkcjonowaniem bazy danych.\n Operacja zakończona niepowodzeniem")
            label.place(x=450,y=30)
            return
        if collisions!=[]:
            label.config(text="Pomyślnie nadpisano pomiar",foreground="white")
        else:
            label.config(text="Pomyślnie dodano pomiar",foreground="white")
        try:
            cur.execute("INSERT INTO measurements (PESEL,date,time,result) VALUES (%s,%s,%s,%s);",params=(meas.get_patient(),meas.get_date_SQL(),meas.get_time(),meas.get_result(),))
            mydb.commit()
        except Exception:
            label.config(text="Wystąpił błąd związany z funkcjonowaniem bazy danych.\n Operacja zakończona niepowodzeniem")
            label.place(x=450,y=30)
            return            
    label.place(x=500,y=30)

##################################
#####   usuwanie pomiarów    #####
##################################
    
def meas_delete_screen():
    """
    Funkcja do tworzenia interfejsu graficznego usuwania pomiarów medycznych.
    """
    m=Measurement()

    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    butmenu=tk.Button(frame,text="Wróć do menu",command=main)
    butmenu.place(x=10,y=30)

    lpatientdata=tk.Label(frame,text="Wyszukaj pacjenta",foreground="white",background="black")
    lpatientdata.place(x=200,y=10)
    entpatientdata=tk.Entry(frame,background="grey",width=20)
    entpatientdata.place(x=200,y=30)
    butentpatientdata=tk.Button(frame,text="OK",command=lambda: find_patient(entpatientdata))
    butentpatientdata.place(x=200,y=50,width=30,height=20)

    lpatientinput=tk.Label(frame,text="Podaj PESEL pacjenta",foreground="white",background="black")
    lpatientinput.place(x=250,y=80)
    entpatientinput=tk.Entry(frame,background="grey",width=20)
    entpatientinput.place(x=200,y=110)
    laccpatientinput=tk.Label(frame,text="",foreground="white",background="black")
    butentpatientinput=tk.Button(frame,text="OK",
        command=lambda: accept_patient_input(m,entpatientinput,laccpatientinput))
    butentpatientinput.place(x=200,y=140,width=30,height=20)

    lcalendar=tk.Label(frame,text="",foreground="white",background="black")
    butent2=tk.Button(frame,text="Wybierz datę",command=lambda: calendar_screen(frame,m))#dodać label
    butent2.place(x=200,y=170,width=200,height=20)

    lclock=tk.Label(frame,text="",foreground="white",background="black")
    butent3=tk.Button(frame,text="Wybierz godzinę",command=lambda: time_screen(frame,m,lclock))
    butent3.place(x=200,y=200,width=200,height=20)

    ldelpatient=tk.Label(frame,text="Usuń pomiar",foreground="white",background="black")
    ldelpatient.place(x=200,y=240)
    laccdelpatient=tk.Label(frame,text="",foreground="white",background="black")
    butent4=tk.Button(frame,text="OK",command=lambda: delete_meas(m,laccdelpatient))
    butent4.place(x=200,y=270,width=30,height=20)

def delete_meas(meas:Measurement=None,label:tk.Label=None):
    """
    Usuwa pomiar medyczny z bazy danych.

    Parametry:
    - meas (Measurement): Obiekt pomiaru.
    - label (tk.Label): Etykieta do wyświetlania komunikatów sukcesu lub błędu.
    """
    if meas.get_date()==None or meas.get_patient()==None or meas.get_time()==None:
        label.config(text="Przynajmniej jedno z pól jest nieuzupełnione, bądź\n uzupełnione niepoprawnie. Pomiar nie zostanie usunięty")
    else:
        try:
            cur.execute("SELECT * FROM measurements WHERE date=%s AND time=%s AND PESEL=%s ;",params=(meas.get_date_SQL(),meas.get_time(),meas.get_patient(),))
            collisions=cur.fetchall()
        except Exception:
            label.config(text="Wystąpił błąd związany z funkcjonowaniem bazy danych.\n Operacja zakończona niepowodzeniem")
            label.place(x=450,y=30)
            return
        if collisions==[]:
            label.config(text="Nie znaleziono pomiaru")
        else:
            label.config(text="Pomyślnie usunięto pomiar")
        try:
            cur.execute("DELETE FROM measurements WHERE date=%s AND time=%s AND PESEL=%s ;",params=(meas.get_date_SQL(),meas.get_time(),meas.get_patient(),))
            mydb.commit()
        except Exception:
            label.config(text="Wystąpił błąd związany z funkcjonowaniem bazy danych.\n Operacja zakończona niepowodzeniem")
            label.place(x=450,y=30)
            return
    label.place(x=450,y=30)


##################################
##### wyświetlenie pomiarów ######
##################################

def meas_choose_patient_print_screen():
    """
    Funkcja do tworzenia interfejsu graficznego wyświetlania pomiarów dla wybranego pacjenta.
    """
    chosendata=Display_data()

    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    l1=tk.Label(frame,text="Wybierz pacjenta, dla którego mają zostać wyświetlone dane",
             foreground="white",background="black")
    l1.place(x=400,y=10)

    lreturn=tk.Button(frame,text="Powrót do menu",command=main)
    lreturn.place(x=10,y=50)

    lfind=tk.Label(frame,text="Wyszukiwarka pacjentów",foreground="white",background="black")
    lfind.place(x=400,y=50)
    entfind=tk.Entry(frame,background="grey",width=20)
    entfind.place(x=400,y=80)
    butfind=tk.Button(frame,text="Szukaj",command=lambda: find_patient(entfind))
    butfind.place(x=400,y=100)

    lpick=tk.Label(frame,text="Wprowadź PESEL pacjenta",foreground="white",background="black")
    lpick.place(x=400,y=160)
    laccpick=tk.Label(frame,text="",foreground="white",background="black")
    laccpick.place(x=400,y=240)
    entpick=tk.Entry(frame,background="grey",width=20)
    entpick.place(x=400,y=190)
    butpick=tk.Button(frame,text="Wybierz",
        command=lambda: acc_patient_choose_screen(entpick,chosendata,laccpick))
    butpick.place(x=400,y=210)                                              

def acc_patient_choose_screen(ent:tk.Entry=None,chosendata:Display_data=None,label:tk.Label=None):
    """
    Funkcja wybierająca ekran dla pacjenta i potwierdzająca wybór.

    Parametry:
    - ent (tk.Entry): Widget Entry dla danych wejściowych pacjenta.
    - chosendata (Display_data): Obiekt zawierający dane wybranego pacjenta.
    - label (tk.Label): Etykieta do wyświetlania komunikatów.

    Efekt:
    - Przejście do ekranu potwierdzającego wybór pacjenta lub wyświetlenie komunikatu o braku pacjenta.
    """
    try:
        cur.execute("SELECT * FROM patients WHERE PESEL=%s;",params=(ent.get(),))
    except Exception:
        label.config(text="Wystąpił błąd związany z funkcjonowaniem bazy danych.\n Operacja zakończona niepowodzeniem")
        return
    candidates=cur.fetchall()
    if candidates!=[]:
        meas_choose_period_print_screen(ent,chosendata)
    else:
        label.config(text="Nie znaleziono pacjenta o takim PESELu")

def meas_choose_period_print_screen(ent:tk.Entry=None,chosendata:Display_data=None):
    """
    Funkcja tworząca interfejs graficzny wybierania przedziału czasowego dla pomiarów.

    Parametry:
    - ent (tk.Entry): Widget Entry dla danych wejściowych pacjenta.
    - chosendata (Display_data): Obiekt zawierający dane wybranego pacjenta.

    Efekt:
    - Ustawienie ekranu do wyboru przedziału czasowego dla pomiarów danego pacjenta.
    """
    chosendata.set_patient(ent.get())

    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    l1=tk.Label(frame,text="Wybierz przedział czasu, z którego mają zostać odczytane dane",
             foreground="white",background="black")
    l1.place(x=400,y=10)

    lpesel=tk.Label(frame,text=f"Wybrano pacjenta o peselu:\n{ent.get()}",
             foreground="white",background="black")
    lpesel.place(x=200,y=10)

    butmain=tk.Button(frame,text="Wróć do menu głównego",command=main)
    butmain.place(x=10,y=20)

    butback=tk.Button(frame,text="Wróć do wyboru pacjenta",command=meas_choose_patient_print_screen)
    butback.place(x=10,y=50)

    butstartdate=tk.Button(frame,text="Wybierz datę początkową",command=lambda: calendar_screen(win=frame,datapack=chosendata,endflag=False))
    butstartdate.place(x=400,y=50)

    butenddate=tk.Button(frame,text="Wybierz datę końcową",command=lambda: calendar_screen(win=frame,datapack=chosendata,endflag=True))
    butenddate.place(x=400,y=80)

    laccfinal=tk.Label(frame,text="",foreground="white",background="black")
    butfinal=tk.Button(frame,text="Zatwierdź dane",command=lambda: meas_confirm_screen(chosendata,laccfinal))
    butfinal.place(x=400,y=110)

def meas_confirm_screen(datapack:Display_data=None,label:tk.Label=None):
    """
    Funkcja potwierdzająca dane wybrane do wyświetlenia pomiarów.

    Parametry:
    - datapack (Display_data): Obiekt zawierający dane wybranego pacjenta i przedziału czasowego.
    - label (tk.Label): Etykieta do wyświetlania komunikatów.

    Efekt:
    - Przejście do ekranu potwierdzającego wybór danych lub wyświetlenie komunikatu o błędzie.
    """
    if datapack.get_patient()==None or datapack.get_startdate()==None or datapack.get_enddate()==None:
        label.config(text="Brakuje potrzebnych danych")
        label.place(x=400,y=140)
    elif AuxMes.compare_dates(datapack.get_startdate(),datapack.get_enddate())==False:
        label.config(text="Błąd:data końcowa nie może być wcześniejsza niż data początkowa")
        label.place(x=400,y=140)
    else:
        frame=tk.Toplevel(win)
        frame.geometry("300x200")
        lconfirm=tk.Label(frame,
            text=f"Wybrane dane:\nPESEL:{datapack.get_patient()}\n data początkowa:{datapack.get_startdate()}\n data końcowa:{datapack.get_enddate()}.\nCzy potwierdzasz?")
        lconfirm.place(x=0,y=0)

        butconfirm=tk.Button(frame,text="Tak",command=lambda: meas_table_or_graph(datapack,frame))
        butconfirm.place(x=30,y=150)

        butdeny=tk.Button(frame,text="Nie",command=lambda: [meas_choose_patient_print_screen,frame.destroy(),frame.update()])
        butdeny.place(x=230,y=150)

def meas_table_or_graph(datapack:Display_data=None,top:tk.Toplevel=None):
    """
    Funkcja wybierająca tryb wyświetlania pomiarów jako tabeli lub wykresu.

    Parametry:
    - datapack (Display_data): Obiekt zawierający dane wybranego pacjenta i przedziału czasowego.
    - top (tk.Toplevel): Okno toplevel.

    Efekt:
    - Przejście do ekranu wyboru trybu wyświetlania pomiarów.
    """
    top.destroy()
    top.update()

    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    butmain=tk.Button(frame,text="Wróć do menu głównego",command=main)
    butmain.place(x=10,y=20)

    topframe=tk.Toplevel(frame)
    topframe.geometry("200x100")
    lchoose=tk.Label(topframe,text="Wybierz format wizualizacji danych")
    lchoose.place(x=0,y=0)

    buttable=tk.Button(topframe,text="Tabela",command=lambda: show_data_table(datapack,topframe))
    buttable.place(x=10,y=60)

    butgraph=tk.Button(topframe,text="Wykres",command= lambda: show_data_graph(datapack,topframe))
    butgraph.place(x=130,y=60)

def show_data_table(data:Display_data=None,top:tk.Toplevel=None):
    """
    Funkcja wyświetlająca dane pomiarów w formie tabeli.

    Parametry:
    - data (Display_data): Obiekt zawierający dane wybranego pacjenta i przedziału czasowego.
    - top (tk.Toplevel): Okno toplevel.

    Efekt:
    - Wyświetlenie danych pomiarów w formie tabeli.
    """
    top.destroy()
    top.update()
    cur.execute("SELECT * FROM measurements WHERE date>=%s AND date<=%s AND PESEL=%s ORDER BY date,time;",
                params=(date_to_SQL(data.get_startdate()),date_to_SQL(data.get_enddate()),data.get_patient(),))
    dataset=cur.fetchall()
    meas_print_screen(win,dataset)

def show_data_graph(data:Display_data=None,top:tk.Toplevel=None):
    """
    Funkcja wyświetlająca dane pomiarów w formie wykresu.

    Parametry:
    - data (Display_data): Obiekt zawierający dane wybranego pacjenta i przedziału czasowego.
    - top (tk.Toplevel): Okno toplevel.

    Efekt:
    - Wyświetlenie danych pomiarów w formie wykresu.
    """
    top.destroy()
    top.update()
    cur.execute("SELECT * FROM measurements WHERE date>=%s AND date<=%s AND %s ORDER BY date,time;",params=(date_to_SQL(data.get_startdate()),date_to_SQL(data.get_enddate()),data.get_patient(),))
    dataset=cur.fetchall()
    graph_measurements(dataset)

####################################
#   funkcje związane z pacjentami   #
####################################

##############################################
#   funkcje związane z dodawaniem pacjenta   #
##############################################

def patient_add_screen():
    """
    Funkcja tworząca interfejs graficzny dla dodawania nowego pacjenta.

    Efekt:
    - Ustawienie interfejsu graficznego do wprowadzania danych nowego pacjenta.
    """
    new_patient=Patient()

    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    but1=tk.Button(frame,text="Wróć do menu",command=main)
    but1.place(x=10,y=30)

    l1=tk.Label(frame,text="Podaj imię",foreground="white",background="black")
    l1.place(x=200,y=10)
    ent1=tk.Entry(frame,background="grey",width=20)
    ent1.place(x=200,y=30)
    lacc1=tk.Label(frame,text="",foreground="white",background="black")
    butent1=tk.Button(frame,text="OK",command=lambda: accept_name_input(new_patient,ent1,lacc1))
    butent1.place(x=200,y=50,width=30,height=20)

    l2=tk.Label(frame,text="Podaj nazwisko",foreground="white",background="black")
    l2.place(x=200,y=80)
    ent2=tk.Entry(frame,background="grey",width=20)
    ent2.place(x=200,y=100)
    lacc2=tk.Label(frame,text="",foreground="white",background="black")
    butent2=tk.Button(frame,text="OK",command=lambda: accept_lname_input(new_patient,ent2,lacc2))
    butent2.place(x=200,y=120,width=30,height=20)

    l3=tk.Label(frame,text="Podaj PESEL",foreground="white",background="black")
    l3.place(x=200,y=150)
    ent3=tk.Entry(frame,background="grey",width=20)
    ent3.place(x=200,y=170)
    lacc3=tk.Label(frame,text="",foreground="white",background="black")
    butent3=tk.Button(frame,text="OK",command=lambda: accept_pesel_input(new_patient,ent3,lacc3))
    butent3.place(x=200,y=190,width=30,height=20)

    l4=tk.Label(frame,text="Dodaj pacjenta",foreground="white",background="black")
    l4.place(x=200,y=220)
    lacc4=tk.Label(frame,text="",foreground="white",background="black")
    butent4=tk.Button(frame,text="OK",command=lambda: add_patient(lacc4,new_patient))
    butent4.place(x=200,y=240,width=30,height=20)

def accept_pesel_input(p:Patient=None,entry:tk.Entry=None,label:tk.Label=None):
    """
    Funkcja akceptująca wprowadzony PESEL dla nowego pacjenta.

    Parametry:
    - p (Patient): Obiekt reprezentujący pacjenta.
    - entry (tk.Entry): Widget Entry dla danych wejściowych PESEL.
    - label (tk.Label): Etykieta do wyświetlania komunikatów.

    Efekt:
    - Sprawdzenie poprawności PESEL-u, ustawienie PESEL-u dla pacjenta i wyświetlenie komunikatu.
    """
    pesel=entry.get()
    flag=pesel.isnumeric()
    if flag==False:
        label.config(text="Podany PESEL jest niepoprawny")
    else:
        cur.execute("SELECT * FROM patients WHERE PESEL=%s;",params=(pesel,))
        collisions=cur.fetchall()
        if collisions!=[]:
            label.config(text="Taki PESEL już istnieje w systemie")
        else:
            p.set_PESEL(pesel)
            label.config(text="Pomyślnie ustawiono PESEL")
    label.place(x=350,y=190,width=200,height=20)

def add_patient(label:tk.Label=None,p:Patient=None):
    """
    Funkcja dodająca nowego pacjenta do bazy danych.

    Parametry:
    - label (tk.Label): Etykieta do wyświetlania komunikatów.
    - p (Patient): Obiekt reprezentujący pacjenta.

    Efekt:
    - Dodanie nowego pacjenta do bazy danych i wyświetlenie komunikatu.
    """
    if p.get_name()=="" or p.get_lname()=="" or p.get_PESEL()=="":
        label.config(text="Jedno lub więcej pól jest nieuzupełnionych, bądź jest niepoprawne")
    else:
        cur.execute("SELECT * FROM patients WHERE PESEL=%s;",params=(p.get_PESEL(),))
        collisions=cur.fetchall()
        if collisions!=[]:
            label.config(text="Pacjent o takim peselu już istnieje w systemie")
        else:
            cur.execute("INSERT INTO patients (name,last_name,PESEL) VALUES (%s,%s,%s);",params=(p.get_name(),p.get_lname(),p.get_PESEL()))
            mydb.commit()
            label.config(text="Pomyślnie dodano pacjenta")
    label.place(x=270,y=260,width=500,height=20)

#############################################
#   funkcje związane z usuwaniem pacjenta   #
#############################################

def patient_drop_screen():
    """
    Funkcja tworząca interfejs graficzny dla usuwania pacjenta.

    Efekt:
    - Ustawienie interfejsu graficznego do wprowadzania danych pacjenta do usunięcia.
    """
    frame=tk.Frame(win,width=800,height=600,bg="black")
    frame.place(x=0,y=0)

    l1=tk.Label(frame,text="Podaj dane pacjenta do usunięcia",background="black")
    l1.place(x=200,y=10)

    cur.execute("SELECT * FROM patients")
    candidates=cur.fetchall()
    if candidates==[]:
        l2=tk.Label(frame,text="Nie ma żadnych zapisanych pacjentów.Operacja usunięcia nie jest możliwa",
                    foreground="white",background="black")
        l2.place(x=200,y=30)
    else:
        ent1=tk.Entry(frame,background="grey",width=20)
        ent1.place(x=200,y=170)
        butfindpat=tk.Button(frame,text="Szukaj pacjenta",command=lambda: find_patient(ent1))
        butfindpat.place(x=200,y=200)

        lpesel=tk.Label(frame,text="Podaj PESEL pacjenta",foreground="white",
                background="black")
        lpesel.place(x=200,y=300)

        entpesel=tk.Entry(frame,background="grey",width=20)
        entpesel.place(x=200,y=330)

        lacc1=tk.Label(frame,text="",foreground="white",background="black")

        butdelpat=tk.Button(frame,text="Zatwierdź",command=lambda: delete_patient(entpesel,lacc1))
        butdelpat.place(x=200,y=360)


    but1=tk.Button(frame,text="Wróć do menu",command=main)
    but1.place(x=10,y=30)

def delete_patient(ent:tk.Entry,label:tk.Label):
    """
    Funkcja usuwająca pacjenta z bazy danych.

    Parametry:
    - ent (tk.Entry): Widget Entry dla danych wejściowych pacjenta.
    - label (tk.Label): Etykieta do wyświetlania komunikatów.

    Efekt:
    - Sprawdzenie poprawności danych wejściowych, usunięcie pacjenta z bazy danych i wyświetlenie komunikatu.
    """
    pesel=ent.get()
    flag=pesel.isnumeric()
    if flag==False:
        label.config(text=f"Podany pesel:{pesel} nie jest liczbą całkowitą")
    else:
        cur.execute("SELECT * FROM patients WHERE PESEL=%s;",params=(pesel,))
        collisions=cur.fetchall()
        if collisions==[]:
            label.config(text=f"Nie znaleziono pacjenta o PESELu:{pesel}")
        else:
            cur.execute("DELETE FROM measurements WHERE PESEL = %s;",params=(pesel,))
            cur.execute("DELETE FROM patients WHERE PESEL = %s;",params=(pesel,))
            mydb.commit()
            label.config(text="Pomyślnie usunięto pacjenta")
    label.place(x=300,y=220)

#################################################
#   funkcje związane z wyświetlaniem pacjenta   #
#################################################

def patient_print_screen():
    """
    Funkcja wyświetlająca listę pacjentów w formie tabeli.

    Efekt:
    - Wyświetlenie danych pacjentów w formie tabeli.
    """
    frame=tk.Toplevel(win)
    frame.geometry("800x400")
    table=ttk.Treeview(frame,columns=("tab_name","name","lname","pesel"),show="headings")
    table.heading("tab_name",text="Nr pacjenta")
    table.heading("name",text="Imię")
    table.heading("lname",text="Nazwisko")
    table.heading("pesel",text="PESEL")
    table.pack(fill="both",expand=True)
    cur.execute("SELECT * FROM patients")
    dataset=cur.fetchall()
    for el in dataset:
        tab_name=el[0]
        name=el[1]
        lname=el[2]
        pesel=el[3]
        data=(tab_name,name,lname,pesel)
        table.insert(parent="",index=tab_name,values=data)

def find_patient(ent:tk.Entry):
    """
    Funkcja wyszukująca pacjenta w bazie danych.

    Parametry:
    - ent (tk.Entry): Widget Entry dla danych wejściowych wyszukiwanej frazy.

    Efekt:
    - Wyświetlenie wyników wyszukiwania w formie tabeli.
    """
    data=ent.get()
    cur.execute("SELECT * FROM patients WHERE name = %s OR last_name = %s OR PESEL = %s ;",params=(data,data,data,))
    candidates=cur.fetchall()
    frame=tk.Toplevel(win)
    frame.geometry("800x400")
    table=ttk.Treeview(frame,columns=("tab_name","name","lname","pesel"),show="headings")
    table.heading("tab_name",text="Nr pacjenta")
    table.heading("name",text="Imię")
    table.heading("lname",text="Nazwisko")
    table.heading("pesel",text="PESEL")
    table.pack(fill="both",expand=True)
    for el in candidates:
        tab_name=el[0]
        name=el[1]
        lname=el[2]
        pesel=el[3]
        data=(tab_name,name,lname,pesel)
        table.insert(parent="",index=tab_name,values=data)
    
#######################
#   wywołanie maina   #
#######################
        
if __name__=="__main__":
    create_test_data()
    main()
    win.mainloop()
    mydb.close()