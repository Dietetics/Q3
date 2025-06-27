# Nom, Matricule
# Nom, Matricule

import sys

def read(input_file):
    """Fonctions pour lire dans les fichier. Vous pouvez les modifier,
    faire du parsing, rajouter une valeur de retour, mais n'utilisez pas
    d'autres librairies.
    Functions to read in files. you can modify them, do some parsing,
    add a return value, but don't use other librairies"""

    file = open(input_file, "r")
    lines = file.readlines()
    file.close()

    # TODO: Compléter ici/Complete here
    # traiter les lignes du fichier pour le problème
    # process the file lines for the problem


def write(str_content, output_file):
    """Fonctions pour écrire dans un fichier. Vous pouvez la modifier,
    faire du parsing, rajouter une valeur de retour, mais n'utilisez pas
    d'autres librairies.
    Functions to read in files. you can modify them, do some parsing,
    add a return value, but don't use other librairies"""

    file = open(output_file, "w")
    file.write(str_content)
    file.close()


    

#Ceci est la fonction que nous appelerons pour tester
#Assurez-vous qu'elle retourne la réponse!
#
#This is the function we will call to test, make sure it
#returns the answer!
def main(args):
    """Fonction main/Main function"""
    input_file = args[0]
    output_file = args[1]
    data = read(input_file)

    #TODO : Completer ici/Complete here
    #Vous pouvez créer de nouvelles fonctions
    #You may create new functions
    
    

# NE PAS TOUCHER
# DO NOT TOUCH
if __name__ == "__main__":
    main(sys.argv[1:])
