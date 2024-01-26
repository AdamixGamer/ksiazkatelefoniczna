from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

kontakty = sqlite3.connect("kontakty.db")

kontakty.execute("create table if not exists kontakt (id integer PRIMARY KEY AUTOINCREMENT, imie text, nazwisko text, numer text)")
#kontakty.execute("insert into kontakt(imie,nazwisko,numer) values ('Adam','Nowak','123456789')")
#kontakty.execute("insert into kontakt(imie,nazwisko,numer) values ('Adam','Kowalski','796506406')")
#kontakty.execute("insert into kontakt(imie,nazwisko,numer) values ('Jan','Kowalski','604605697')")
#kontakty.commit()
kontakty.close()
@app.route("/")
def index(sortby="nazwisko", komunikat=""):
    kontakty = sqlite3.connect("kontakty.db")
    print(f"select * from kontakt order by {sortby}")
    lista = kontakty.execute(f"select * from kontakt order by {sortby}").fetchall()
    kontakty.close()
    return render_template("index.html",lista=lista,komunikat=komunikat,sortby=sortby)


@app.route("/add")
def add():
    imie = request.args["imie"]
    nazwisko = request.args["nazwisko"]
    numer = request.args["numer"]
    if len(imie.strip()) > 1 and len(nazwisko.strip()) > 1 and len(numer.replace(" ","").strip())==9:
        kontakty = sqlite3.connect("kontakty.db")
        kontakty.execute(f"insert into kontakt(imie,nazwisko,numer) values ('{imie}','{nazwisko}','{numer}')")
        kontakty.commit()
        kontakty.close()
        return index()
    else:
        return index("n","Niepoprawna wartość")


@app.route("/delete")
def delete():
    id = request.args["id"]
    kontakty = sqlite3.connect("kontakty.db")
    kontakty.execute(f"delete from kontakt where id={id}")
    kontakty.commit()
    kontakty.close()
    return index()

@app.route("/edit")
def edit():
    id = request.args["id"]
    kontakty = sqlite3.connect("kontakty.db")
    kontakt = kontakty.execute(f"select * from kontakt where id={id}").fetchall()[0]
    kontakty.close()
    return render_template("edit.html",kontakt=kontakt)

@app.route("/save")
def save():
    imie = request.args["imie"]
    nazwisko = request.args["nazwisko"]
    numer = request.args["numer"]
    id = request.args["id"]
    kontakty = sqlite3.connect("kontakty.db")
    kontakty.execute(f"update kontakt set imie='{imie}', nazwisko='{nazwisko}', numer='{numer}' where id={id}")
    kontakty.commit()
    kontakty.close()
    return index()

@app.route("/sort")
def sort():
    return index(request.args["sortby"]);