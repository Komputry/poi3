import random
from PIL import Image
import os

def probka_maker(sciezka, rozmiar_probki, gdzie_probki, ile_probek):
    for path in sciezka:
        fota = Image.open(path)
        dlugosc, wysokosc = fota.size
        podzielony_folder = os.path.join(gdzie_probki, os.path.basename(path).split('.')[0])
        os.makedirs(podzielony_folder, exist_ok=True)

        for i in range(1, ile_probek):
            x_poczatku = random.randint(0, dlugosc - rozmiar_probki)
            y_poczatku = random.randint(0, wysokosc - rozmiar_probki)
            x_konca = x_poczatku + rozmiar_probki
            y_konca = y_poczatku + rozmiar_probki
            probka = fota.crop((x_poczatku, y_poczatku, x_konca, y_konca))
            probka.save(os.path.join(podzielony_folder, f'probka_nr_{i}.jpeg'))


sciezka = ['blat.jpg', 'plytka.jpg', 'tynk.jpg']
rozmiar_probki = 128
gdzie_probki = 'podzieloneProbki'
ile_probek = 500
probka_maker(sciezka, rozmiar_probki, gdzie_probki, ile_probek)
