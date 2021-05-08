import numpy as np
from egcd import egcd

#initial alphabet
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя., ?'

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod(matrix, modul):
    det = int(np.round(np.linalg.det(matrix))) # finding the determinant
    det_inv = egcd(det, modul)[1] % modul  # the inverse of the determinant element
    #matrix modulo the key matrix
    matrix_modul_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modul
    )


    return matrix_modul_inv

# Encoding the message
def encrypt(message, K):
    encrypted = ""
    message_in_numbers = []

    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    split_P = [
        message_in_numbers[i : i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[" "])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted

# Decoding a message
def decrypt(cipher, Kinv):
    decrypted = ""
    cipher_in_numbers = []

    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    split_C = [
        cipher_in_numbers[i : i + int(Kinv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


if __name__ == '__main__':
    message = input('Enter a message:')

    K = np.matrix([[0,13,5],[16,9,14],[9,8,13]])
    Kinv = matrix_mod(K, len(alphabet))

    encrypted_message = encrypt(message, K)
    decrypted_message = decrypt(encrypted_message, Kinv)

    print("Original message: " + message)
    print("Encrypted message: " + encrypted_message)
    print("Decrypted message: " + decrypted_message)


