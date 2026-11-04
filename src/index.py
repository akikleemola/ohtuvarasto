from varasto import Varasto

def tulosta_luonnin_jalkeen(mehua, olutta):
  print("Luonnin jälkeen:")
  print(f"Mehuvarasto: {mehua}")
  print(f"Olutvarasto: {olutta}")


def tulosta_oluen_tiedot(olutta):
    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")

def kokeile_mehun_muokkausta(mehua):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")

def kokeile_virheellisia_varastoja():
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)

def kokeile_virheellisia_lisayksia(mehua, olutta):
    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def kokeile_liian_suurta_ottoa(olutta):
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")


def kokeile_negatiivista_ottoa(mehua):
    print(f"Mehuvarasto: {mehua}")
    print("mehua.ota_varastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    tulosta_luonnin_jalkeen(mehua, olutta)
    tulosta_oluen_tiedot(olutta)
    kokeile_mehun_muokkausta(mehua)
    kokeile_virheellisia_varastoja()
    kokeile_virheellisia_lisayksia(mehua, olutta)
    kokeile_liian_suurta_ottoa(olutta)
    kokeile_negatiivista_ottoa(mehua)

if __name__ == "__main__":
    main()
