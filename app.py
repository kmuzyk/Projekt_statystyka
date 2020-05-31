# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:25:50 2020

@author: kmuzy
"""


import numpy as np
import pandas as pd

df = pd.read_csv("https://sebkaz.github.io/teaching/PrzetwarzanieDanych/data/polish_names.csv")

from sklearn.ensemble import RandomForestClassifier

index = df.index
col = df.columns
val = df.values
a = df["gender"]

def string_into_number(string):
    return int(string == 'm')


df['target'] = df['gender'].map( lambda x: int(x == 'm') )
df['len_name'] = df['name'].map( lambda y: len(y) )
df['last_letter'] = df['name'].map( lambda z: int(z[-1] == 'a') )

X = df[ ['len_name', 'last_letter'] ].values
y = df['target'].values

model2 = RandomForestClassifier()
model2.fit(X,y)
y_pred_lr = model2.predict(X)


from flask import Flask
from flask import render_template
from flask import request
import sqlite3
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    conn = sqlite3.connect("bazaimion.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS osoby (imie TEXT NOT NULL, plec TEXT NOT NULL)''')
    c.execute('''SELECT imie, plec FROM osoby''')
    items = c.fetchall()
    if request.method == 'POST':
        input_name = request.form['fname']
        if(input_name == ''):
            return render_template('index.html', gender='Nie wpisano imienia', items=items)
        if(not input_name.isalpha()):
            return render_template('index.html', gender='Wpisano niedozwolone znaki', items=items)
        input_name = input_name.lower()
        sprawdzenie = model2.predict(np.array([[(lambda x : len(x))(input_name), (lambda x: int(x[-1] == 'a'))(input_name) ]]))
        if(sprawdzenie == 1):
            c.execute("INSERT INTO osoby VALUES (?, ?)", (input_name, 'mezczyzna'))
            conn.commit()
            conn.close()
            return render_template('index.html', gender='Mężczyzna', items=items)
        if(sprawdzenie == 0):
            c.execute("INSERT INTO osoby VALUES (?, ?)", (input_name, 'kobieta'))
            conn.commit()
            conn.close()
            return render_template('index.html', gender='Kobieta', items=items)
   
    if request.method == 'GET':
        return render_template('index.html', items=items)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')

