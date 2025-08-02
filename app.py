from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

RADNO_VREME = {
    "pon-petak": {"start": 10, "end": 20},
    "subota": {"start": 10, "end": 13},
    "nedelja": None
}

DATA_FILE = "data.json"

# 🔑 Funkcija za konverziju latinice u ćirilicu
def latinica_u_cirilicu(tekst):
    mapa = str.maketrans(
        "abvgdđžzijklmnoprstćufhcčšABVGDĐŽZIJKLMNOPRSTĆUFHCČŠ",
        "абвгдђжзижјклмнопрстћуфхцчшАБВГДЂЖЗИЈКЛМНОПРСТЋУФХЦЧШ"
    )
    return tekst.translate(mapa)

def ucitaj_posebne_datume():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sacuvaj_posebne_datume(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    sada = datetime.now()
    dan = sada.weekday()
    sat = sada.hour

    posebni = ucitaj_posebne_datume()
    datum_str = sada.strftime("%Y-%m-%d")

    if datum_str in posebni:
        start, end = posebni[datum_str]
    else:
        if dan < 5:
            start, end = RADNO_VREME["pon-petak"].values()
        elif dan == 5:
            start, end = RADNO_VREME["subota"].values()
        else:
            start, end = None, None

    if start is None:
        poruka = "Danas je nedelja. Ordinacija ne radi."
    elif not (start <= sat < end):
        poruka = f"Radno vrijeme ordinacije je od {start} do {end} časova."
    else:
        poruka = "Ordinacija je trenutno otvorena."

    # ✅ Konverzija u ćirilicu za bolji TTS izgovor
    poruka_cir = latinica_u_cirilicu(poruka)

    return render_template("index.html", poruka=poruka_cir)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    posebni = ucitaj_posebne_datume()
    if request.method == "POST":
        datum = request.form["datum"]
        start = int(request.form["start"])
        end = int(request.form["end"])
        posebni[datum] = (start, end)
        sacuvaj_posebne_datume(posebni)
        return redirect(url_for("admin"))

    return render_template("admin.html", posebni=posebni)

@app.route("/obrisi/<datum>")
def obrisi(datum):
    posebni = ucitaj_posebne_datume()
    if datum in posebni:
        del posebni[datum]
        sacuvaj_posebne_datume(posebni)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
