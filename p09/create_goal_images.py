#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
import sys


def custom_str_to_nr_func(string):
    # Funktsioon teksti konverteerimiseks unikaalseks 32-bitiseks täisarvuks.
    # Väärtus on kindlalt unikaalne vaid lühemate tekstide puhul
    prime_numbers = np.array(
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
         233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
         367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
         499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
         643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
         797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
         947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
         1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213,
         1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321])
    result_int = 0
    for letter_index, letter in enumerate(string):
        result_int += ord(letter) * prime_numbers[letter_index % prime_numbers.shape[0]]

    return result_int % (2**32)


def create_angled_component(shape, freq, angle):
    # Matemaatilis-geomeetriline maagia:
    def value_calculator(row_index, col_index):
        elem_dist = col_index * np.sin(np.deg2rad(angle)) +\
                    row_index * np.cos(np.deg2rad(angle))
        value = ((np.cos(elem_dist * 2 * np.pi / freq) + 1) / 2) * 255
        return value.astype(np.uint8)
    return np.fromfunction(value_calculator, shape, dtype=np.int16)


def create_square_componenet(shape, freq):
    def value_calculator(row_index, _):
        return np.where(row_index % freq < freq / 2, 255, 0).astype(np.uint8)
    return np.fromfunction(value_calculator, shape, dtype=np.int16)


if __name__ == "__main__":
    # Annab repositooriumi kaustanime, seda sõltumata sellest, kas koodi jooksutatakse juurkausta või
    #   praktikumikausta suhtes.
    # Tingimus on, et koodifail peab asuma õigel tasemel repositooriumi kaustas.
    # Windowsi operatsioonisüsteemis võib esineda probleeme, kui kaustanimes esinevad täpitähed
    lab_dir_path = os.path.dirname(__file__)  # xxx\repo_nimi\praktikumid\p08
    labs_dir_path = os.path.split(lab_dir_path)[0]  # xxx\repo_nimi\praktikumid
    repo_dir_path = os.path.split(labs_dir_path)[0]  # xxx\repo_nimi
    repo_dir_name = os.path.split(repo_dir_path)[1]  # repo_nimi

    # Algväärtustame numpy juhuslike numbrite generaatori nii,
    #   et samas kaustas tuleksid alati samasugused juhuslikud arvud
    np.random.seed(custom_str_to_nr_func(repo_dir_name))

    print("Alustan failide genereerimist...")

    # Kõigi loodavate piltide ühine suurus
    picture_size = (500, 500)

    # Loome mustvalge pildi, mis sisaldab ühte sageduskomponenti.
    comp_freq = np.random.randint(30, 200)
    comp_direction = np.random.randint(0, 2)
    comp1D = (np.cos(np.arange(picture_size[0]) * 2 * np.pi / comp_freq) + 1) / 2
    comp1D = (comp1D * 255).astype(np.uint8)
    bw_90deg = np.tile(comp1D, (picture_size[1], 1))
    if comp_direction:
        bw_90deg = np.transpose(bw_90deg)


    # Loome värvilise pildi, millel on üks komponent suvalisel kanalil ja suvalise 90-kordse faasinihkega.
    comp_freq = np.random.randint(30, 200)
    comp_direction = not comp_direction
    freq_shift = np.random.randint(1, 4) * np.pi / 2  # 90, 180 või 270 kraadi
    comp1D = (np.cos(np.arange(picture_size[0]) * 2 * np.pi / comp_freq + freq_shift) + 1) / 2
    comp1D = (comp1D * 255).astype(np.uint8)
    ch_90deg = np.tile(comp1D, (picture_size[1], 1))
    if comp_direction:
        ch_90deg = np.transpose(ch_90deg)
    channel = np.random.randint(0, 3)
    if channel == 0:
        color_90deg = np.dstack((ch_90deg, np.zeros(picture_size, dtype=np.uint8), np.zeros(picture_size, dtype=np.uint8)))
    elif channel == 1:
        color_90deg = np.dstack((np.zeros(picture_size, dtype=np.uint8), ch_90deg, np.zeros(picture_size, dtype=np.uint8)))
    else:
        color_90deg = np.dstack((np.zeros(picture_size, dtype=np.uint8), np.zeros(picture_size, dtype=np.uint8), ch_90deg))

    # Loome värvilise pildi, kus igal kanalil on midagi ja erinevate nurkade all.
    comp_freq1 = np.random.randint(30, 200)
    comp_freq2 = np.random.randint(30, 200)
    comp_freq3 = np.random.randint(30, 200)
    comp3_angle = np.random.randint(3, 16) * 5  # Juhuslik nurk vahemikust 15 kuni 75 kraadi, mis on 5 kordne
    comp2_freq_shift = np.random.randint(1, 4) * np.pi / 2  # 90, 180 või 270 kraadi
    comp1D1 = (np.cos(np.arange(picture_size[0]) * 2 * np.pi / comp_freq1) + 1) / 2
    comp1D1 = (comp1D1 * 255).astype(np.uint8)
    comp1 = np.tile(comp1D1, (picture_size[1], 1))
    comp1D2 = (np.cos(np.arange(picture_size[0]) * 2 * np.pi / comp_freq2 + freq_shift) + 1) / 2
    comp1D2 = (comp1D2 * 255).astype(np.uint8)
    comp2 = np.tile(comp1D2, (picture_size[1], 1))
    comp2 = np.transpose(comp2)
    comp3 = create_angled_component(picture_size, comp_freq3, comp3_angle)
    color_order = np.arange(0, 3)
    np.random.shuffle(color_order)
    color_array = np.array((comp1, comp2, comp3))
    color_3comps = np.dstack((color_array[color_order[0]], color_array[color_order[1]], color_array[color_order[2]]))

    # Ruutsignaali pildi loomine
    square_freq = np.random.randint(30, 200)
    bw_90deg_sq = create_square_componenet(picture_size, square_freq)
    comp_direction = np.random.randint(0, 2)
    if comp_direction:
        bw_90deg_sq = np.transpose(bw_90deg_sq)

    # Teine osa, müraste kassipiltide loomine.

    # Mustvalge kassipilt selle koodiga samast kaustast
    if not os.path.isfile(os.path.join(lab_dir_path, "cat.png")):
        print("Skriptifailiga samas kaustas ei ole vajalikku faili kassipildiga. Pilte ei genereeritud")
        sys.exit()

    # Salvestame kõik loodud pildid failidesse.
    cv2.imwrite("task_1_goal.png", bw_90deg)
    cv2.imwrite("task_2-1_goal.png", color_90deg)
    cv2.imwrite("task_2-2_goal.png", color_3comps)
    cv2.imwrite("task_2-3_goal.png", bw_90deg_sq)

    cat_img = cv2.imdecode(np.fromfile(os.path.join(lab_dir_path, "cat.png"), dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    # Fourier' pööre
    cat_img_freq = np.fft.fft2(cat_img)
    cat_img_freq1 = cat_img_freq.copy()  # Neljanda ülesande jaoks
    # magnituudi leidmine
    cat_img_freq_mag = np.abs(cat_img_freq)
    # Juhuslik sageduskomponent
    x_bin = np.random.randint(10, 45)
    y_bin = np.random.randint(10, 45)
    y_sign = np.random.randint(0, 2)
    if y_sign:
        y_bin = -y_bin
    # ühe sageduskomponendi lisamine
    cat_img_freq[y_bin, x_bin] = np.max(cat_img_freq_mag)

    # Tagasi ruumi.
    cat_img_back = np.fft.ifft2(cat_img_freq).real
    cat_img_back = ((cat_img_back - np.min(cat_img_back)) /
                    (np.max(cat_img_back) - np.min(cat_img_back)) * 255).astype(np.uint8)

    # Tulemus faili
    cv2.imwrite("task_4_noisy_cat.png", cat_img_back)

    # Juhuslikud sageduskomponendid
    nr_of_components = 15
    x_bins = np.random.choice(np.arange(10, 45), nr_of_components)
    y_bins = np.random.choice(np.arange(10, 45), nr_of_components)
    y_signs = np.random.randint(0, 2, nr_of_components)
    cat_img_freq[y_bins, x_bins] = np.max(cat_img_freq_mag)*0.2

    cat_img_back = np.fft.ifft2(cat_img_freq).real
    cat_img_back = ((cat_img_back - np.min(cat_img_back)) /
                    (np.max(cat_img_back) - np.min(cat_img_back)) * 255).astype(np.uint8)

    cv2.imwrite("task_5_very_noisy_cat.png", cat_img_back)

    print("Failid genereeritud!")
