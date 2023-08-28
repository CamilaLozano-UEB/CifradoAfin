import math
import re

modulo = 27
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z"]


def remove_accents(text):
    # Definimos un diccionario de reemplazo para las letras acentuadas
    replacements = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}

    # Utilizamos un bucle para reemplazar las letras acentuadas
    cleaned_text = ''.join(replacements.get(char, char) for char in text)

    return cleaned_text


def clean_text(text):
    text = re.sub(r'[^a-zA-ZñÑ\s]', '', text)
    return re.sub(r'\s+', ' ', text)


def affine_encryption(mensaje, a, b):
    text = mensaje.upper().replace("\n", "")  # Convertir a mayúsculas y eliminar espacios
    text = clean_text(remove_accents(text))
    mensajeCifrado = []

    for valor_original in text:
        if valor_original.isalpha():
            indice_valor_original = alphabet.index(valor_original)
            valor_cifrado = (a * indice_valor_original + b) % modulo
            mensajeCifrado.append(alphabet[valor_cifrado])
        else:
            mensajeCifrado.append(valor_original)

    return "".join(mensajeCifrado)


def find_inverse(a):
    for i in range(modulo):
        if (a * i) % modulo == 1:
            return i
    return None


def is_coprime(a):
    mcd = math.gcd(a, 27)
    return mcd == 1


def calculate_letter_frequencies(text):
    text = text.upper().replace(" ", "").replace("\n", "")  # Convertir a mayúsculas y eliminar espacios
    total_letters = len(text)
    letter_frequencies = {}

    for letter in text:
        if letter.isalpha():
            if letter in letter_frequencies:
                letter_frequencies[letter] += 1
            else:
                letter_frequencies[letter] = 1

    # Calcular los porcentajes de frecuencia
    frequencies_with_percentage = []

    for letter, count in letter_frequencies.items():
        frequency_percentage = (count / total_letters) * 100
        frequencies_with_percentage.append((letter, frequency_percentage))

    # Ordenar la lista por porcentaje de frecuencia en orden descendente
    sorted_frequencies = sorted(frequencies_with_percentage, key=lambda item: item[1], reverse=True)

    # Tomar las primeras 5 entradas de la lista
    top_letters = sorted_frequencies[:5]

    return top_letters


def find_ab(first_letter, second_letter):
    options = ["E", "A", "O"]

    for bestLetter in options:
        best1_value = alphabet.index(bestLetter)
        first_letter = alphabet.index(first_letter)
        second_letter = alphabet.index(second_letter)

        if best1_value == 0:
            a = first_letter
        elif find_inverse(best1_value) is None:
            continue
        else:
            a = (first_letter - second_letter) * pow(best1_value, -1, modulo) % modulo

        b = (first_letter - a * best1_value) % modulo

        if is_coprime(a) and find_inverse(a) is not None:
            return a, b

    return []


def returnData(text):
    frequencies = calculate_letter_frequencies(text)
    ab = find_ab(frequencies[0][0], frequencies[1][0])
    decrypt_text = decrypt(text, ab[0], ab[1])
    return {'decrypt_text': decrypt_text, "a": ab[0], "b": ab[1], "frecuencias": frequencies}


def decrypt(text, a, b):
    text = clean_text(remove_accents(text))

    inverse_a = find_inverse(a)
    plaintext = ""
    for char in text:
        if char in alphabet:
            c = alphabet.index(char)
            m = (inverse_a * (c - b)) % modulo
            plaintext += alphabet[m]
        else:
            plaintext += char

    return plaintext
