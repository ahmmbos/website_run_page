# Author:       Max Diekman, Nienke Gertsen & Amber Bos
# Start date:   26-05-2021
# Latest date:  30-05-2021
"""
!!! ADD DOCSTRING
"""
from flask import Flask, render_template, request
import mysql.connector
import pandas as pd

app = Flask(__name__)


@app.route('/')
def start_pagina():
    """
    !!! ADD DOCSTRING
    """
    return render_template("try1.html")


@app.route('/home')
def home_pagina():
    """
    !!! ADD DOCSTRING
    """
    return render_template("try1.html")


@app.route('/database')
def database():
    """
    !!! ADD DOCSTRING
    """
    user_inp = request.args.get('search', '')
    # Connection to biological database
    try:
        conn = mysql.connector.connect(host='145.74.104.145',
                                       user='dsntt',
                                       password='W8woord!',
                                       database='dsntt')
        cursor = conn.cursor()

        result = search_query(user_inp, cursor)
        search_hits = find_search(result, user_inp)
        amount = len(search_hits)
        hits = add_bold(result, search_hits)
    except mysql.connector.errors.ProgrammingError:
        result = ("Connection failed")
        amount = 0
        hits = ["Connection failed", "Connection failed"]
    user_inp = str(user_inp)

    return render_template("database.html", hits=hits, amount=amount)


@app.route('/resultaten')
def vragen():
    """
    !!! ADD DOCSTRING
    """
    return render_template("vragen.html")


@app.route('/about')
def about():
    """
    !!! ADD DOCSTRING
    """
    return render_template("aboutus.html")


def search_query(user_inp, cursor):
    """
    !!! ADD DOCSTRING
    """
    # Query to database for search
    sql = ("""SELECT header, accession_number, name_organism, domain, family,
           genus, species, protein_description, reliability_score,
           identity_percentage, e_value
           FROM organisms
           JOIN taxonomy USING(accession_number)
           JOIN protein_function USING(accession_number)
           JOIN sequences USING(header)
           WHERE header LIKE %s
           OR accession_number LIKE %s
           OR name_organism LIKE %s
           OR domain LIKE %s
           OR family LIKE %s
           OR genus LIKE %s
           OR species LIKE %s
           OR protein_description LIKE %s
           OR reliability_score LIKE %s
           OR identity_percentage LIKE %s
           OR e_value LIKE %s
           ORDER BY header;""")
    val = ('%'+user_inp+'%', '%'+user_inp+'%', '%'+user_inp+'%',
           '%'+user_inp+'%', '%'+user_inp+'%', '%'+user_inp+'%',
           '%'+user_inp+'%', '%'+user_inp+'%', '%'+user_inp+'%',
           '%'+user_inp+'%', '%'+user_inp+'%')
    cursor.execute(sql, val)
    result = cursor.fetchall()

    return result


def find_search(result, user_inp):
    """
    !!! ADD DOCSTRING
    """
    search_hits = []
    for i, value in enumerate(result):
        for j in value:
            h = str(j).lower()
            k = str(user_inp).lower()
            if k in h:
                search_hits.append(j)
            else:
                pass

    return search_hits


def add_bold(result, search_hits):
    """
    !!! ADD DOCSTRING
    """
    hit = []
    for value in result:
        for i in value:
            if i in search_hits:
                text =  str(i) + '@'
                hit.append(text)

            else:
                hit.append(i)

    hits = []
    for i in range(0, len(hit), 11):
        hits.append(hit[i:i + 11])

    return hits


if __name__ == '__main__':
    app.run()
