import math

from flask import Flask, flash, redirect, render_template, request, url_for

from varasto import Varasto


app = Flask(__name__)
app.config["SECRET_KEY"] = "ohtuvarasto-kehityssalaisuus"

varastot = {}
SEURAAVA_ID = {"arvo": 1}


def lue_positiivinen_luku(
    teksti, puuttuu_viesti, virhe_viesti, positiivinen_viesti
):
    if not teksti:
        flash(puuttuu_viesti)
        return None

    luku = parsi_luku(teksti, virhe_viesti)
    if luku is None:
        return None

    if luku <= 0:
        flash(positiivinen_viesti)
        return None
    return luku


def parsi_luku(teksti, virhe_viesti):
    try:
        luku = float(teksti)
    except ValueError:
        flash(virhe_viesti)
        return None

    if not math.isfinite(luku):
        flash(virhe_viesti)
        return None
    return luku


def lisaa_varasto(nimi, tilavuus_teksti):
    if not nimi:
        flash("Anna varastolle nimi.")
        return False

    tilavuus = lue_positiivinen_luku(
        tilavuus_teksti,
        "Anna varaston tilavuus.",
        "Tilavuuden on oltava numero.",
        "Tilavuuden on oltava suurempi kuin nolla.",
    )
    if tilavuus is None:
        return False

    varasto_id = SEURAAVA_ID["arvo"]
    varastot[varasto_id] = {
        "nimi": nimi,
        "varasto": Varasto(tilavuus),
    }
    SEURAAVA_ID["arvo"] += 1
    return True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nimi = request.form.get("nimi", "").strip()
        tilavuus_teksti = request.form.get("tilavuus", "").strip()
        if lisaa_varasto(nimi, tilavuus_teksti):
            return redirect(url_for("index"))

    return render_template("index.html", varastot=varastot)


@app.route("/varastot/<int:varasto_id>/<toiminto>", methods=["POST"])
def muuta_saldoa(varasto_id, toiminto):
    if varasto_id not in varastot:
        flash("Varastoa ei löytynyt.")
        return redirect(url_for("index"))

    maara = lue_maara()
    if maara is not None:
        suorita_muutos(varasto_id, toiminto, maara)
    return redirect(url_for("index"))


def lue_maara():
    return lue_positiivinen_luku(
        request.form.get("maara", "").strip(),
        "Anna lisättävä tai otettava määrä.",
        "Määrän on oltava numero.",
        "Määrän on oltava suurempi kuin nolla.",
    )


def suorita_muutos(varasto_id, toiminto, maara):
    varasto = varastot[varasto_id]["varasto"]
    if toiminto == "lisaa":
        varasto.lisaa_varastoon(maara)
    elif toiminto == "ota":
        varasto.ota_varastosta(maara)
    else:
        flash("Tuntematon toiminto.")


if __name__ == "__main__":
    app.run()
