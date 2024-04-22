import os
import numpy as np
import pandas as pd
import skimage
from skimage import color
from skimage.util import img_as_ubyte

def wyznacz_cechy_probki(sciezka_probki):
    probka = skimage.io.imread(sciezka_probki)
    probka_w_skali_szrosci = img_as_ubyte(color.rgb2gray(probka)) // 16
    #print(probka_w_skali_szrosci)
    cechy_wyznaczone = []

    odleglosc_pikseli = [1, 3, 5]
    kierunki = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

    for i_dyst in odleglosc_pikseli:
        for j_kier in kierunki:
            g = skimage.feature.graycomatrix(probka_w_skali_szrosci, distances=[i_dyst], angles=[np.degrees(j_kier)], levels=256, symmetric=True, normed=True)

            dissimilarity = skimage.feature.graycoprops(g, 'dissimilarity')[0, 0]
            correlation = skimage.feature.graycoprops(g, 'correlation')[0, 0]
            contrast = skimage.feature.graycoprops(g, 'contrast')[0, 0]
            energy = skimage.feature.graycoprops(g, 'energy')[0, 0]
            homogeneity = skimage.feature.graycoprops(g, 'homogeneity')[0, 0]
            asm = skimage.feature.graycoprops(g, 'ASM')[0, 0]

            cecha_dla_probki = pd.DataFrame({
                'Category': [os.path.basename(os.path.dirname(sciezka_probki))],
                'Distance': [i_dyst],
                'Angle': [np.degrees(j_kier)],
                'Dissimilarity': [dissimilarity],
                'Correlation': [correlation],
                'Contrast': [contrast],
                'Energy': [energy],
                'Homogeneity': [homogeneity],
                'ASM': [asm]
            })

            cechy_wyznaczone.append(cecha_dla_probki)
            #print(cechy_wyznaczone)

    polaczone_wyznaczone_cechy = pd.concat(cechy_wyznaczone, ignore_index=True)

    return polaczone_wyznaczone_cechy


def przygotuj_probke(sciezki_z_probkami, ileprobek):
    for i in sciezki_z_probkami:
        ktory_folder = os.path.basename(os.path.normpath(i))
        dataframe_temp = pd.DataFrame()
        nr_probki = 1

        while True:
            if nr_probki > ileprobek:
                break
            nazwa_probki = f'probka_nr_{nr_probki}.jpeg'
            sciezka_probki = os.path.join(i, nazwa_probki)
            print("sciezka probki:", sciezka_probki)

            if not os.path.exists(sciezka_probki):
                print("nie odnaleziono probki, break")
                break
            cecha_probki = wyznacz_cechy_probki(sciezka_probki)
            dataframe_temp = pd.concat([dataframe_temp, cecha_probki], ignore_index=True)
            nr_probki += 1

        nazwa_csv = f'{ktory_folder}.csv'
        dataframe_temp.to_csv(nazwa_csv, index=False)


sciezki_z_probkami = [r'C:\Users\aleks\pythony\pygit\poi3\podzieloneProbki\blat', r'C:\Users\aleks\pythony\pygit\poi3\podzieloneProbki\plytka', r'C:\Users\aleks\pythony\pygit\poi3\podzieloneProbki\tynk']
ileprobek = 450
przygotuj_probke(sciezki_z_probkami, ileprobek)