"""
PROJET AUTOMATE GROUPE C8

VONG LUCAS
ZHANG NICOLAS
JIN JOHN
TCHING ANGELA

/!\ ETAPE NON FAITES : 5, 6 ET 7
"""

from prettytable import PrettyTable # Module permettant de créer des tableaux dédiée à l'affichage

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "h,", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t","u","v", "w", "x", "y", "z"]
det_etats_nouveaux = []
nom_fichier = "automates/C8_"
saisi = input("Entrez le numero de l'automate: ")
nom_fichier = nom_fichier + saisi + ".txt"

def process_input_string(input_string): # Convertir les lignes du fichier en chaine de caractère
    input_string = input_string.rstrip("\n")
    input_list = input_string.split(",")
    return input_list

with open(nom_fichier, "r") as f: # On lit le fichier tout en affectant les données à diverses variables
    donnee = f.readlines()
    alphabet = donnee[0]
    nbr_etats = donnee[1]
    etats_init = donnee[2]
    etats_term = donnee[3]
    nbr_transi = donnee[4]
    transi = [donnee[5]]


    alphabet = process_input_string(alphabet)
    nbr_etats = process_input_string(nbr_etats)
    etats_init = process_input_string(etats_init)
    etats_term = process_input_string(etats_term)
    nbr_transi = nbr_transi.split(",")

    trans = list()

    for i in transi:
        i = i.rstrip("\n") #Retirer les sauts de lignes
        trans.append(i.split(","))

    f.close()

def transition_list(a):
    # Transformation de transition en string vers une liste (ex : '2a3' -> [2,a,3])
    l = [int(a[0])]
    b = str(a[1])
    l.append(alphabet.index(b))
    l.append(a[2])
    return l

# intialisation d'un automate composé de mot vide (noté "-")
Automate = []
nbr_transi = len(alphabet)
nbr_etats = int(nbr_etats[-1])
for i in range(nbr_etats):
    temp = []
    for j in range(nbr_transi):
        temp.append("-")
    Automate.append(temp)

# remplissage de l'automate initialisé précédemment avec les transitions de la variable trans
for i in trans:
    for j in i:
        l = transition_list(j)
        if Automate[l[0]][l[1]] == "-":
            Automate[l[0]][l[1]] = l[2]
        else:
            Automate[l[0]][l[1]] += "," + l[2]


def est_un_automate_deterministe(Automate):
    for i in Automate:
        for j in i:
            if len(j) >= 3:
                return False
    if len(etats_init) != 1:
        return False

    return True

def est_complet(Automate):
    for ligne in Automate:
        for element in ligne:
            if element == "-":
                return False
    return True


def completion(Automate):
    A = Automate
    compteur1 = 0
    compteur2 = 0
    for i in A:
        compteur2 = 0
        for j in i:
            if "-" == j:
                A[compteur1][compteur2] = 'P'

            compteur2 += 1
        compteur1 += 1
    temp = []
    for i in range(len(A[0])):
        temp.append('P')
    A.append(temp)
    return A

def determinisation(Automate):
    nouveaux_etats = []
    etats_non_parcourus = []
    temp = ""
    for i in etats_init:
        temp = temp + i
    etat_initial = temp
    etats_non_parcourus.append(etat_initial)
    stockage = ""
    supprimer_doublon = ""
    transitions_determinisees = []
    while len(etats_non_parcourus) != 0:
        for j in range(len(alphabet)):
            for i in range(len(etats_non_parcourus[0])):
                if not Automate[int(etats_non_parcourus[0][i])][j].replace(",", "") == "-":
                    stockage = stockage + Automate[int(etats_non_parcourus[0][i])][j].replace(",", "")

            for caractere in stockage:
                if caractere not in supprimer_doublon:
                    supprimer_doublon += caractere
            if not supprimer_doublon == "":
                transitions_determinisees.append(supprimer_doublon)
            else:
                transitions_determinisees.append("-")
            if not supprimer_doublon in nouveaux_etats:
                if supprimer_doublon != etat_initial:
                    if supprimer_doublon != "":
                        nouveaux_etats.append(supprimer_doublon)
                        etats_non_parcourus.append(supprimer_doublon)

            stockage = ""
            supprimer_doublon = ""

        etats_non_parcourus.remove(etats_non_parcourus[0])

    nouveaux_etats.insert(0, etat_initial) # Insère l'état initial dans la liste des nouveaux états
    seen = set()
    result = []
    for s in nouveaux_etats:
        sorted_s = ''.join(sorted(s))
        if sorted_s not in seen: # supprime les doublons
            seen.add(sorted_s) # Trie les nouveaux états 
            result.append(s) 

    automate_determinise = [] # stockage transition determinisé
    liste_temp = []
    n = 0
    for i in range(len(result)):
        for j in range(len(alphabet)):
            liste_temp.append(transitions_determinisees[n])
            n = n + 1
        automate_determinise.append(liste_temp)
        liste_temp = []
    return automate_determinise, result # retourne l'automate déterminisée


def affichage_automate(Automate):
    tableau = PrettyTable()

    if len(alphabet) == 2:
        colonne = ["Type E ou S", "Etat", "a", "b"]
    elif len(alphabet) == 4:
        colonne = ["Type E ou S", "Etat", "a", "b", "c", "d"]
    elif len(alphabet) == 1:
        colonne = ["Type E ou S", "Etat", "a"]
    else:
        colonne = ["Type E ou S", "Etat", "a", "b", "c"]
    # Attribution des en-têtes de colonnes à la variable "tableau".
    tableau.field_names = colonne
    # stockage des données de chaque ligne du tableau.
    fusion = []

    # Remplissage les données de chaque ligne du tableau.
    for i in range(nbr_etats):
        if str(i) in etats_init:
            if str(i) in etats_term:
                fusion.append("ES") # État initial et final
            else:
                fusion.append("E") # État initial seulement

        elif str(i) in etats_term:
            fusion.append("S") # État final seulement
        else:
            fusion.append("-") # Ni état initial ni état final

        # Ajout de l'indice de l'état courant dans la liste "fusion".
        fusion.append(i)

        # Remplissage de chaque en tête de colonne avec la lettre de l'alphabet de l'automate choisi.
        for j in range(len(alphabet)):
            fusion.append(Automate[i][j])

        # Ajout de la liste "fusion" comme une nouvelle ligne dans la variable "tableau".
        tableau.add_row(fusion)

        # Réinitialisation de la liste "fusion" pour remplir la prochaine ligne.
        fusion.clear()
    # Affichage du tableau de transition.
    print(tableau)

def est_un_automate_standard(etats_init):
    if len(etats_init) == 1:
        for i in trans:
            for j in i:
                if j[2] != etats_init[0]:
                    return False
        return True
    return False

def standardiser(Automate, etat_init):
    transitions_standardisees = []  # Initialise une liste pour stocker les transitions standardisées
    nouveaux_etats_initiaux = ["i"]  # Initialise une liste pour les nouveaux états initiaux avec "i"

    for i in range(nbr_etats):
        nouveaux_etats_initiaux.append(i)

    # Boucle sur chaque caractère de l'alphabet
    for char_index in range(len(alphabet)):
        transition_temporaire = ""  # Initialise une chaîne temporaire pour stocker la transition

        # Parcourt chaque état de l'automate
        for etat_index in range(nbr_etats):
            transition = Automate[etat_index][char_index]

            # Vérifie si la transition n'est pas vide et si l'état est initial
            if transition != "-" and str(etat_index) in etat_init:
                # Concatène la transition à la chaîne temporaire en éliminant les virgules
                transition_temporaire += "".join(transition.split(","))

        # Ajoute la transition normalisée à la liste des transitions standardisées
        transitions_standardisees.append(transition_temporaire)

    # Supprime les états initiaux multiples et remplace par "i"
    etat_init.clear()
    etat_init.extend(nouveaux_etats_initiaux)

    # Insère les transitions standardisées au début de l'automate
    Automate.insert(0, transitions_standardisees)

    # Retourne les nouveaux états initiaux et les transitions standardisées
    return nouveaux_etats_initiaux, transitions_standardisees


def affichage_automate_standard(etats,automate):
    tableau = PrettyTable()
    sortie = 0
    if len(alphabet) == 2:
        colonne = ["Type E ou S", "Etat", "a", "b"]
    elif len(alphabet) == 4:
        colonne = ["Type E ou S", "Etat", "a", "b", "c", "d"]
    elif len(alphabet) == 1:
        colonne = ["Type E ou S", "Etat", "a"]
    else:
        colonne = ["Type E ou S", "Etat", "a", "b", "c"]
    tableau.field_names = colonne
    fusion = []
    for i in range(len(etats)):
        if i == 0:
            type = "E"
        else:
            type = "-"
        if str(etats[i]) in etats_term:
            sortie = sortie + 1

        if sortie > 0:
            type = "S"
        sortie = 0
        fusion.append(type)
        type = ""
        fusion.append(etats[i])
        for j in range(len(alphabet)):
            fusion.append(automate[i][j])
        tableau.add_row(fusion)
        fusion.pop(0)
        fusion.pop(0)
        automate.append(fusion)
        fusion = []
    print(tableau)

def affichage_automate_deter(etats, auto, etats_init, etats_term):
    tableau = PrettyTable()
    type = ""
    sortie = 0
    if len(alphabet) == 2:
        colonne = ["Type E ou S", "Etat", "a", "b"]
    elif len(alphabet) == 4:
        colonne = ["Type E ou S", "Etat", "a", "b", "c", "d"]
    elif len(alphabet) == 1:
        colonne = ["Type E ou S", "Etat", "a"]
    else:
        colonne = ["Type E ou S", "Etat", "a", "b", "c"]
    tableau.field_names = colonne
    fusion = []
    for i in range(len(etats)):
        for j in range(len(etats[i])):
            if i != 0:
                if etats[i][j] in etats_term:
                    sortie = sortie + 1
            else:
                type = "E"
        if sortie > 0:
            type = type + "S"
        if type == "" and i != 0:
            type = "-"
        sortie = 0

        fusion.append(type)
        type = ""
        fusion.append(etats[i])
        for j in range(len(alphabet)):
            fusion.append(auto[i][j])
        tableau.add_row(fusion)
        fusion = []
    print(tableau)


def menu():

    print("Affichage du fichier selectionné :")
    print("Alphabet: ", alphabet)
    print("Etats initiaux: ", etats_init)
    print("Etats terminaux: ", etats_term)
    print("Nombre d'états: ", nbr_etats)
    print("Les differentes transitions: ", trans, "\n")

    print("===============================================")
    print("\n TABLE DE TRANSITION DE BASE DE L'AUTOMATE \n")
    affichage_automate(Automate)
    print("===============================================")

    print("Propriété :")
    if not est_un_automate_standard(Automate):
        print("Standard : NON")
    else:
        print("Standard : OUI")
    if not est_un_automate_deterministe(Automate):
        print("Déterministe : NON")
    else:
        print("Déterministe : OUI")
    if not est_complet(Automate):
        print("Complet : NON")
    else:
        print("Complet : OUI")

    print("===============================================")
    print("Que voulez-vous faire ?")
    print("Vous pouvez :")
    print("1.determinisiser ?")
    print("2.standardiser?")


    while True:
        choix = input("Votre choix  : ")
        if choix == '2':

            if not est_un_automate_standard(Automate):
                print("\n STANDARDISATION: ")
                std = standardiser(Automate, etats_init)
                affichage_automate_standard(std[0], Automate)
                """  ###### NE FONCTIONNE PAS CORRECTEMENT ######
                if not est_complet(Automate):
                    choix = input("Il n'est pas complet. Rendre complet ?? y ou n : ")

                    if choix == "y":
                        completion(std[1])
                        affichage_automate_standard(std[0], std[1])
                    elif choix == "n":
                        break
                    else:
                        print("Choix incorrect")
                """
            else:
                print("L'automate est déjà standard !")

        if choix == '1':
            if not est_un_automate_deterministe(Automate):
                print("DETERMINISATION")
                print("\nTable de transition après determinisation\n")
                determini = determinisation(Automate)
                affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                if not est_complet(determini):
                    print("Cependant il n'est pas complet. Rendre complet ? : y ou n")
                    choix = input("")
                    if choix == 'y':
                        completion(determini[0])
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                        if choix == 'n':
                            break
                    if choix == 'n':
                        break
            else:
                print("Déjà determinisé!")



menu()
