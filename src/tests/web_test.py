import pytest

import app


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    app.app.config["SECRET_KEY"] = "testiavain"
    app.varastot.clear()
    app.SEURAAVA_ID["arvo"] = 1
    return app.app.test_client()


def test_uuden_varaston_luominen_alasaldolla(client):
    vastaus = client.post(
        "/",
        data={"nimi": "Mehuvarasto", "tilavuus": "100"},
        follow_redirects=True,
    )

    assert vastaus.status_code == 200
    assert "Mehuvarasto" in vastaus.get_data(as_text=True)
    assert "saldo 0" in vastaus.get_data(as_text=True)


def test_varaston_listaus_nayttaa_tiedot(client):
    client.post("/", data={"nimi": "Olutvarasto", "tilavuus": "50"})

    vastaus = client.get("/")
    teksti = vastaus.get_data(as_text=True)

    assert "Olutvarasto" in teksti
    assert "tilavuus 50.0" in teksti
    assert "saldo 0" in teksti


def test_tavaran_lisays_paivittaa_saldon(client):
    client.post("/", data={"nimi": "Testivarasto", "tilavuus": "20"})

    vastaus = client.post(
        "/varastot/1/lisaa",
        data={"maara": "7"},
        follow_redirects=True,
    )

    assert "saldo 7.0" in vastaus.get_data(as_text=True)


def test_tavaran_otto_paivittaa_saldon(client):
    client.post("/", data={"nimi": "Testivarasto", "tilavuus": "20"})
    client.post("/varastot/1/lisaa", data={"maara": "10"})

    vastaus = client.post(
        "/varastot/1/ota",
        data={"maara": "4"},
        follow_redirects=True,
    )

    assert "saldo 6.0" in vastaus.get_data(as_text=True)


def test_puuttuva_nimi_nayttaa_virheilmoituksen(client):
    vastaus = client.post(
        "/",
        data={"nimi": "", "tilavuus": "ei-luku"},
        follow_redirects=True,
    )

    assert "Anna varastolle nimi." in vastaus.get_data(as_text=True)


@pytest.mark.parametrize(
    "tilavuus",
    ["ei-luku", "NaN", "inf"],
)
def test_virheellinen_tilavuus_ei_luo_varastoa(client, tilavuus):
    vastaus = client.post(
        "/",
        data={"nimi": "Testivarasto", "tilavuus": tilavuus},
        follow_redirects=True,
    )

    teksti = vastaus.get_data(as_text=True)
    assert "Tilavuuden on oltava numero." in teksti
    assert "Testivarasto" not in teksti
    assert not app.varastot


@pytest.mark.parametrize("tilavuus", ["0", "-5"])
def test_nollan_tai_negatiivisen_tilavuus_ei_luo_varastoa(client, tilavuus):
    vastaus = client.post(
        "/",
        data={"nimi": "Testivarasto", "tilavuus": tilavuus},
        follow_redirects=True,
    )

    teksti = vastaus.get_data(as_text=True)
    assert "Tilavuuden on oltava suurempi kuin nolla." in teksti
    assert "Testivarasto" not in teksti
    assert not app.varastot


@pytest.mark.parametrize(
    "maara",
    ["", "ei-luku", "NaN", "inf", "0", "-5"],
)
@pytest.mark.parametrize("toiminto", ["lisaa", "ota"])
def test_virheellinen_maara_ei_muuta_saldoa(client, toiminto, maara):
    client.post("/", data={"nimi": "Testivarasto", "tilavuus": "20"})
    client.post("/varastot/1/lisaa", data={"maara": "10"})

    vastaus = client.post(
        f"/varastot/1/{toiminto}",
        data={"maara": maara},
        follow_redirects=True,
    )

    teksti = vastaus.get_data(as_text=True)
    assert "saldo 10.0" in teksti
