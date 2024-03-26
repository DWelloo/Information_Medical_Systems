import tkinter as tk
from tkinter import ttk
import tkcalendar as tcal
from tktimepicker import AnalogPicker

from patient import Patient
from measurement import Measurement
from display_data import Display_data,isfloat


################################
########### pomiar #############    
################################

def accept_result_input(meas: Measurement = None, ent: tk.Entry = None, label: tk.Label = None) -> None:
    """
    Sprawdza poprawność wprowadzonego wyniku pomiaru i aktualizuje obiekt pomiaru.

    Argumenty:
    meas: Measurement - Obiekt Measurement, do którego wprowadzane są dane.
    ent: tk.Entry - Widget Entry z GUI, zawierający wprowadzoną wartość wyniku pomiaru.
    label: tk.Label - Widget Label z GUI, na którym wyświetlane są komunikaty.

    Zwraca:
    None
    """

    val = ent.get()
    if not isfloat(val):
        label.config(text="Wynik pomiaru powinien być liczbą", foreground="white")
    else:
        flag = float(val)
        if flag < 0:
            label.config(text="Wynik pomiaru nie może być ujemny", foreground="white")
        else:
            meas.set_result(flag)
            label.config(text="Pomyślnie ustawiono wynik pomiaru", foreground="white")
    label.place(x=300, y=260)

def meas_print_screen(win: tk.Tk = None, measurements: list = None) -> None:
    """
    Tworzy okno z interfejsem do wyświetlania pomiarów glukozy we krwi w formie tabeli.

    Argumenty:
    win: tk.Tk - Okno główne aplikacji.
    measurements: list - Lista pomiarów do wyświetlenia w tabeli.

    Zwraca:
    None
    """

    frame = tk.Toplevel(win)
    frame.geometry("800x400")
    table = ttk.Treeview(frame, columns=("date", "time", "result", "pesel"), show="headings", selectmode="browse")
    table.heading("date", text="Data pomiaru")
    table.heading("time", text="Godzina pomiaru")
    table.heading("result", text="Wynik")
    table.heading("pesel", text="PESEL")
    table.pack(fill="both", expand=True)
    max_val_glucose = 140
    min_val_glucose = 80
    table.tag_configure('g', background="white")
    table.tag_configure('r', background="red")
    table.tag_configure('b', background="blue", foreground='white')
    cur_tag = 'g'
    for i in range(len(measurements)):
        tab_name = i + 1
        pesel = measurements[i][1]
        date_ = measurements[i][2]
        time = measurements[i][3]
        result = measurements[i][4]
        data = (date_, time, result, pesel)
        too_high = result > max_val_glucose
        too_low = result < min_val_glucose
        cur_tag = 'r' * too_high + 'b' * too_low + 'g' * (not too_high and not too_low)
        table.insert(parent="", index=tab_name, values=data, tags=(cur_tag))

##############################
##########   data   ##########
##############################
    
def calendar_screen(win: tk.Tk = None, meas: Measurement = None, 
                    datapack: None = None, endflag: bool = None) -> None:
    """
    Tworzy okno z kalendarzem umożliwiającym wybór daty dla pomiaru.

    Argumenty:
    win: tk.Tk - Okno główne aplikacji.
    meas: Measurement - Obiekt Measurement, do którego wprowadzane są dane.
    datapack: None - Obiekt Display_data, nie jest używany w tej funkcji.
    endflag: bool - Flaga informująca, czy wybierana jest data początkowa czy końcowa.

    Zwraca:
    None
    """

    frame = tk.Toplevel(win)
    frame.minsize(800, 400)
    cal = tcal.Calendar(frame, setmode="day", date_pattern="dd/mm/yyyy")
    cal.pack(pady=10, fill="both")

    opencal = tk.Button(frame, text="Zatwierdź datę", command=lambda: select_date(cal, meas, datapack, endflag, frame))
    opencal.pack(pady=50)

def select_date(cal: tcal.Calendar = None, meas: Measurement = None, datapack: Display_data = None, 
                endflag: bool = None, frame: tk.Toplevel = None) -> None:
    """
    Zatwierdza wybraną datę z kalendarza, aktualizuje obiekt Measurement lub Display_data w zależności od kontekstu.

    Argumenty:
    cal: tcal.Calendar - Obiekt kalendarza.
    meas: Measurement - Obiekt Measurement, do którego wprowadzane są dane.
    datapack: Display_data - Obiekt Display_data, przechowujący zakres dat do wyświetlenia w wykresie.
    endflag: bool - Flaga informująca, czy wybierana jest data początkowa czy końcowa.

    Zwraca:
    None
    """

    chosendate = cal.get_date()
    chosendate = chosendate.split("/")
    day = chosendate[0]
    month = chosendate[1]
    year = chosendate[2]
    if meas is not None:
        meas.set_date((int(year), int(month), int(day)))
    if datapack is not None:
        if endflag is False:
            datapack.set_startdate((int(year), int(month), int(day)))
        else:
            datapack.set_enddate((int(year), int(month), int(day)))
    frame.destroy()
    frame.update()


#################################
########### godzina #############    
#################################

def select_time(clock: AnalogPicker = None, meas: Measurement = None, label: tk.Label = None, frame: tk.Toplevel = None) -> None:
    """
    Zatwierdza wybraną godzinę z zegara analogowego, aktualizuje obiekt Measurement i wyświetla informacje.

    Argumenty:
    clock: AnalogPicker - Obiekt zegara analogowego.
    meas: Measurement - Obiekt Measurement, do którego wprowadzane są dane.
    label: tk.Label - Widget Label z GUI, na którym wyświetlane są komunikaty.

    Zwraca:
    None
    """

    chosentime = clock.time()
    chosenhour = chosentime[0]
    chosenminute = chosentime[1]
    if len(str(chosenminute)) == 1:
        chosenminute = f"0{chosenminute}"
    if clock.period() == "PM":
        chosenhour += 12
    time = f"{chosenhour}:{chosenminute}"
    if meas is not None:
        meas.set_time(time)
        label.config(text=f"Ustawiono godzinę {time}")
    else:
        label.config(text="Wystąpił błąd. Godzina nie została ustawiona")
    label.place(x=420,y=200)
    frame.destroy()
    frame.update()

def time_screen(win: tk.Tk = None, meas: Measurement = None, label: tk.Label = None):
    """
    Tworzy okno z interfejsem do wybierania godziny z zegara analogowego.

    Argumenty:
    win: tk.Tk - Okno główne aplikacji.
    meas: Measurement - Obiekt Measurement, do którego wprowadzane są dane.

    Zwraca:
    None
    """
    frame=tk.Toplevel(win)
    frame.minsize(800,400)
    clock=AnalogPicker(frame)
    clock.pack(expand=True,fill="both")

    openclock=tk.Button(frame,text="Zatwierdź czas",command=lambda: select_time(clock,meas,label,frame))
    openclock.pack(pady=50)

#################################
########### pacjent #############    
#################################

def accept_name_input(p: Patient = None, entry: tk.Entry = None, label: tk.Label = None) -> None:
    """
    Akceptuje wprowadzone dane imienia, sprawdza ich poprawność i aktualizuje obiekt pacjenta.

    Argumenty:
    p: Patient - Obiekt Patient, do którego wprowadzane są dane.
    entry: tk.Entry - Widget Entry z GUI, zawierający wprowadzone imię.
    label: tk.Label - Widget Label z GUI, na którym wyświetlane są komunikaty.

    Zwraca:
    None
    """

    name = entry.get()
    flag = name.isalpha()
    if flag:
        p.set_name(name)
        label.config(text="Pomyślnie ustawiono imię")
    else:
        label.config(text="Podane imię jest niepoprawne")
    label.place(x=350, y=50, width=200, height=20)

def accept_lname_input(p: Patient = None, entry: tk.Entry = None, label: tk.Label = None) -> None:
    """
    Akceptuje wprowadzone dane nazwiska, sprawdza ich poprawność i aktualizuje obiekt pacjenta.

    Argumenty:
    p: Patient - Obiekt Patient, do którego wprowadzane są dane.
    entry: tk.Entry - Widget Entry z GUI, zawierający wprowadzone nazwisko.
    label: tk.Label - Widget Label z GUI, na którym wyświetlane są komunikaty.

    Zwraca:
    None
    """

    lname = entry.get()
    flag = lname.isalpha()
    if flag:
        p.set_lname(lname)
        label.config(text="Pomyślnie ustawiono nazwisko")
    else:
        label.config(text="Podane nazwisko jest niepoprawne")
    label.place(x=350, y=120, width=200, height=20)