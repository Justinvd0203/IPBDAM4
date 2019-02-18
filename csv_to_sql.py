import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from pandas.io import sql
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def csv_naar_sql(gebruiker, wachtwoord, host, database):
    root = tk.Tk()
    root.withdraw()
    naam = filedialog.askopenfilename(initialdir='/', title='Kies een csv bestand',
                                      filetypes=(('csv files', '*.csv'), ('alle files', '*.*')))
    df = pd.read_csv(str(naam), sep=',')

    # creeren naam uit path location
    naam = naam.split('.')
    naam = str(naam[0])
    naam = naam.split('/')
    naam = str(naam[-1])

    # verbinden met de database en dit vervolgens met df.to_sql het df in de database zetten
    connector = 'mysql+mysqlconnector://' + gebruiker + ':' + wachtwoord + '@' + host + '/' + database
    engine = create_engine(str(connector))
    con = engine.connect()
    print('test1')
    df.to_sql(con=con, name=naam, if_exists='replace')
    print('test2')
    # kijken of de tabel nu bestaat_tabel
    gelukt = bestaat_tabel(engine, naam)
    if gelukt == True:
        tk.messagebox.showinfo('Succes', 'De data is met succes overgezet in de database')
    elif gelukt == False:
        tk.messagebox.showinfo('Niet gelukt', 'De data is niet succesvol overgezet in de database')


def bestaat_tabel(engine, naam):
    # nogmaals verbinden met een raw connection om te kijken of het overzetten gelukt is
    raw_connection = engine.raw_connection()
    cursor = raw_connection.cursor()

    # select statement om te kijken of de database bestaat_tabel, bij een error bestaat_tabel hij niet en returned False.
    try:
        cursor.execute('SELECT 1 FROM ' + naam + ' LIMIT 1;')
        result = cursor.fetchone()
        if result[0] == 1:
            return True
    except mysql.connector.errors.ProgrammingError as e:
        return False


if __name__ == '__main__':
    gebruiker = 'KLl3FHYNbF'
    wachtwoord = 'EUaYYrl13J'
    host = 'remotemysql.com'
    database = 'KLl3FHYNbF'
    csv_naar_sql(gebruiker, wachtwoord, host, database)
