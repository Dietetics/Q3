# CE FICHIER NE SERT QU'A APPELER ET TESTER VOTRE CODE.
# VOUS NE DEVRIEZ PAS AVOIR BESOIN DE LE MODIFIER, SAUF POUR
# AJOUTER VOUS-MÊME D'AUTRES TESTS SI VOUS LE VOULEZ.
# NE PAS REMETTRE SUR STUDIUM. REMETTEZ SEULEMENT frites.py

# THIS FILE IS ONLY USED TO CALL AND TEST YOUR CODE.
# YOU SHOULD NOT HAVE TO MODIFY IT, EXCEPT FOR ADDING
# NEW CUSTOM TESTS IF YOU WISH TO DO SO.
# DO NOT SUBMIT ON STUDIUM. ONLY SUBMIT frites.py

import frites
import time
import traceback


def read(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    file.close()
    return lines


def verifyAns(studentOutputFile, inputFile, expectedAnswer):
    studentOutput = read(studentOutputFile)

    if (len(studentOutput) != 1):
        raise Exception("Output file doesn't have only 1 line")
    if (studentOutput[0].rstrip('\r\n') != expectedAnswer):
        raise Exception("Wrong answer, got " + studentOutput[0].rstrip('\r\n') + ", expected " + expectedAnswer)




if __name__ == '__main__':
    # Choisis les tests que tu veux exécuter
    test_ids = [1,2,3,4,5,6,7,8,9]  # Modifie cette liste selon les tests à lancer
    answers = ["infini", "4", "0", "6", "18", "infini", "11", "1", "0", "105",
               "0", "320", "319", "2071", "13", "16", "27367", "105179", "infini", "720060"]

    for i in test_ids:
        start = time.time()
        try:
            input_file = f"input{i}.txt"
            output_file = f"output{i}.txt"

            frites.main([input_file, output_file])

            verifyAns(output_file, input_file, answers[i - 1])
            print(f"Test {i} OK, took {time.time() - start:.3f} seconds\n")
        except Exception as e:
            print(f"Test {i} Fail, took {time.time() - start:.3f} seconds")
            print(e)
            print()