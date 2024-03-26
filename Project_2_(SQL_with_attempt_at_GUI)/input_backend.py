import mysql.connector

def establish_connection() -> tuple[object, object]:
    """
    Nawiązuje połączenie z bazą danych MySQL.

    Argumenty:
    win: tk.Tk - Opcjonalny argument, okno tkinter, jeśli wymagane w kontekście GUI.

    Zwraca:
    tuple[object, object]: Krotka zawierająca obiekty reprezentujące połączenie (mydb) i kursor (cur).
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="=7T?4he",
    )
    cur = mydb.cursor()
    return mydb, cur


def establish_database(cur: object = None, mydb: object = None):
    """
    Ustala strukturę bazy danych, tworząc tabelę 'patients' i 'measurements', oraz zeruje dane w tabelach.

    Argumenty:
    cur: object - Kursor bazy danych.
    mydb: object - Połączenie z bazą danych.
    """
    cur.execute("CREATE DATABASE IF NOT EXISTS ismedprojekt;")
    cur.execute("USE ismedprojekt;")

    # Tworzenie tabeli patients
    cur.execute("""
                CREATE TABLE IF NOT EXISTS patients(
                `idpatients` INT NOT NULL AUTO_INCREMENT, 
                `name` VARCHAR(45) NULL, 
                `last_name` VARCHAR(45) NULL, 
                `PESEL` VARCHAR(45) NULL UNIQUE,
                PRIMARY KEY (`idpatients`)
                );
                """)

    # Tworzenie tabeli measurements z kluczem obcym do tabeli patients
    cur.execute("""
                CREATE TABLE IF NOT EXISTS measurements(
                `idmeasurements` INT NOT NULL AUTO_INCREMENT,
                `PESEL` VARCHAR(45) NULL,
                `date` DATE NULL,
                `time` TIME NULL,
                `result` FLOAT NULL,
                PRIMARY KEY (`idmeasurements`),
                FOREIGN KEY (`PESEL`) REFERENCES patients(`PESEL`) ON DELETE CASCADE
                );
                """)

    # Czyszczenie tabel
    cur.execute("DELETE from measurements")
    cur.execute("DELETE from patients")

    # Resetowanie auto inkrementacji
    cur.execute("ALTER TABLE measurements AUTO_INCREMENT = 1;")
    cur.execute("ALTER TABLE patients AUTO_INCREMENT = 1;")

    mydb.commit()