from flask import Flask, flash, redirect, render_template, request, url_for

from varasto import Varasto


app = Flask(__name__)
app.config["SECRET_KEY"] = "ohtuvarasto-kehityssalaisuus"

varastot = {}
seuraava_id = 1


@app.route("/", methods=["GET", "POST"])
def index():
    global seuraava_id

    if request.method == "POST":
        nimi = request.form.get("nimi", "").strip()
        tilavuus_teksti = request.form.get("tilavuus", "").strip()

        if not nimi:
            flash("Anna varastolle nimi.")
        elif not tilavuus_teksti:
            flash("Anna varaston tilavuus.")
        else:
            try:
                tilavuus = float(tilavuus_teksti)
            except ValueError:
                flash("Tilavuuden on oltava numero.")
            else:
                if tilavuus <= 0:
                    flash("Tilavuuden on oltava suurempi kuin nolla.")
                else:
                    varastot[seuraava_id] = {
                        "nimi": nimi,
                        "varasto": Varasto(tilavuus),
                    }
                    seuraava_id += 1
                    return redirect(url_for("index"))

    return render_template("index.html", varastot=varastot)


@app.route("/varastot/<int:varasto_id>/<toiminto>", methods=["POST"])
def muuta_saldoa(varasto_id, toiminto):
    if varasto_id not in varastot:
        flash("Varastoa ei löytynyt.")
        return redirect(url_for("index"))

    maara_teksti = request.form.get("maara", "").strip()
    if not maara_teksti:
        flash("Anna lisättävä tai otettava määrä.")
        return redirect(url_for("index"))

    try:
        maara = float(maara_teksti)
    except ValueError:
        flash("Määrän on oltava numero.")
        return redirect(url_for("index"))

    if maara <= 0:
        flash("Määrän on oltava suurempi kuin nolla.")
        return redirect(url_for("index"))

    varasto = varastot[varasto_id]["varasto"]
    if toiminto == "lisaa":
        varasto.lisaa_varastoon(maara)
    elif toiminto == "ota":
        varasto.ota_varastosta(maara)
    else:
        flash("Tuntematon toiminto.")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
