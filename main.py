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
det_etats_nouvaux = []
nom_fichier = "automates/C8_"
saisi = input("Entrez le numero de l'automate: ")
nom_fichier = nom_fichier + saisi + ".txt" 

def process_input_string(input_string): # Convertir les lignes du fichier en chaine de caractère
    input_string = input_string.rstrip("\n")
    input_list = input_string.split(",")
    return input_list

with open(nom_fichier, "r") as f: # extraction des informations 
    liste = f.readlines()
    alphabet = liste[0]
    nbr_etats = liste[1]
    etats_init = liste[2]
    etats_term = liste[3]
    nbr_transi = liste[4]
    transi = [liste[5]]

    # Reformatages des données

    alphabet = process_input_string(alphabet)
    nbr_etats = process_input_string(nbr_etats)
    etats_init = process_input_string(etats_init)
    etats_term = process_input_string(etats_term)
    nbr_transi = nbr_transi.split(",")

    trans = [] 

    for i in transi:
        i = i.rstrip("\n")
        trans.append(i.split(","))
    f.close()

liste_etats = []
for i in range(int(nbr_etats[0])):
    liste_etats.append(i)

def transition_list(a):
    # Transformation de transition en string vers une liste (ex : '2a3' -> [2,0,3])
    l = [int(a[0])]
    b = str(a[1])
    l.append(alphabet.index(b))
    l.append(a[2])
    return l

# intialisation de la matrice automate sous la forme de matrice carrée remplie de mot vide (noté "-")
Automate = []
nbr_transi = len(alphabet)
nbr_etats = int(nbr_etats[-1])
for i in range(nbr_etats):
    temp = []
    for j in range(nbr_transi):
        temp.append('-')
    Automate.append(temp)

# remplissage d'Automate avec les transitions de la variable trans
for i in trans:
    for j in i:
        l = transition_list(j)
        if Automate[l[0]][l[1]] == '-':
            Automate[l[0]][l[1]] = l[2]
        else:
            Automate[l[0]][l[1]] += ',' + l[2]


def affichage_defaut(alphabet, Automate):
    # AFFICHAGE D'UN AUTOMATE COMPLET SOUS LA FORME DE TABLEAU
    print(" ", alphabet)
    n = 0
    for i in Automate[0:-1]:
        print(n, i)
        n += 1
    print('P', Automate[-1])

# remarque l'algo ne marche que pour des transition litterales de (a à v) et des etats allant de 0 a 9

def est_un_automate_deterministe(Automate):
    # VERIFIE SI L'AUTOMATE EST DETERMINISTE OU NON, RENVOIE True/False
    for i in Automate:
        for j in i:
            if len(j) >= 3:
                return False
    if len(etats_init) != 1:
        return False

    return True

def est_complet(Automate):
    # Parcourt chaque ligne de l'automate
    for ligne in Automate:
        # Parcourt chaque élément de la ligne
        for element in ligne:
            # Si un élément est égal à '-', l'automate n'est pas complet
            if element == '-':
                return False
    # Si aucun élément n'est égal à '-', l'automate est complet
    return True


def completion(Automate):
    c1 = 0
    c2 = 0
    for i in Automate:
        c2 = 0
        for j in i:
            if '-' == j:
                Automate[c1][c2] = 'P'

            c2 += 1
        c1 += 1
    ltemp = []
    for i in range(len(Automate[0])):
        ltemp.append('P')
    Automate.append(ltemp)
    return Automate

def donne_etat(etat, etat_term, etat_init):
    # 1 = initial, 2 = final, 3 = quelconque
    for i in etat_term:
        if int(i) == etat:
            return 2
    for i in etat_init:
        if int(i) == etat:
            return 1
    return 0


def determinisation(Automate):
    nouveaux_etats = [] # Initialise une liste pour stocker les nouveaux états
    etats_non_parcourus = [] # Initialise une liste pour stocker les états non encore parcourus
    temp = ""
    for i in etats_init:
        temp = temp + i
    etat_initial = temp # Concatène les états initiaux
    etats_non_parcourus.append(etat_initial) # Ajoute les états initiaux à la liste des états non parcourus
    stockage = ""
    supprimer_doublon = ""
    transitions_determinisees = [] # Initialise une liste pour stocker les transitions déterminisées
    while len(etats_non_parcourus) != 0: # Boucle jusqu'à ce que tous les états soient parcourus
        for j in range(len(alphabet)):
            for i in range(len(etats_non_parcourus[0])):
                if not Automate[int(etats_non_parcourus[0][i])][j].replace(",", "") == "-":
                    stockage = stockage + Automate[int(etats_non_parcourus[0][i])][j].replace(",", "")

            for caractere in stockage:
                if caractere not in supprimer_doublon:
                    supprimer_doublon += caractere # Supprime les doublons dans les transitions
            if not supprimer_doublon == "":
                transitions_determinisees.append(supprimer_doublon) # Ajoute les transitions déterminisées à la liste
            else:
                transitions_determinisees.append("-")
            if not supprimer_doublon in nouveaux_etats:
                if supprimer_doublon != etat_initial:
                    if supprimer_doublon != "":
                        nouveaux_etats.append(supprimer_doublon) # Ajoute les nouveaux états à la liste s'ils n'ont pas été déjà explorés
                        etats_non_parcourus.append(supprimer_doublon) # Supprime l'état exploré de la liste des états non parcourus

            stockage = ""
            supprimer_doublon = ""

        etats_non_parcourus.remove(etats_non_parcourus[0])

    nouveaux_etats.insert(0, etat_initial) # Insère l'état initial dans la liste des nouveaux états
    seen = set()
    result = []
    for s in nouveaux_etats:
        sorted_s = ''.join(sorted(s))
        if sorted_s not in seen:
            seen.add(sorted_s)
            result.append(s) # Trie les nouveaux états et élimine les doublons

    print("Nouveaux états après déterminisation: ", result, "\n")
    automate_determinise = [] # Initialise une liste pour stocker les transitions déterminisées
    liste_temp = []
    n = 0
    for i in range(len(result)):
        for j in range(len(alphabet)):
            liste_temp.append(transitions_determinisees[n])
            n = n + 1
        automate_determinise.append(liste_temp)
        liste_temp = []
    return automate_determinise, result # Ajoute les transitions déterminisées



def affichage_automate(Automate):
    tableau = PrettyTable() # Initialisation d'une variable "tableau" pouvoir afficher les tableaux à l'aide du module prettytable

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
    # Initialisation d'une liste "fusion" pour stocker les données de chaque ligne du tableau.
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

        # Boucle sur chaque symbole de l'alphabet pour remplir les données de chaque colonne.
        for j in range(len(alphabet)):
            fusion.append(Automate[i][j])

        # Ajout de la liste "fusion" comme une nouvelle ligne dans la variable "tableau".
        tableau.add_row(fusion)

        # Réinitialisation de la liste "fusion" pour remplir la prochaine ligne.
        fusion = []
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


# Définition de la fonction standardiser qui prend en entrée un automate et l'état initial.
def standardiser(Automate,etat_init):
    stand_table = [] # Initialisation d'une liste "stand_table" qui va stocker les transitions de l'état initial.
    # Initialisation d'une liste "etats" avec l'état initial "i".
    etats = ["i"]
    tempo = ""
    for i in range(nbr_etats):
        etats.append(i)
    # Boucle sur chaque état de l'automate.
    for i in range(len(alphabet)):
        for j in range(nbr_etats):
            if not Automate[j][i] == "-":
                if str(j) in etat_init:
                    for z in Automate[j][i]:
                        if z not in tempo:
                            tempo = tempo + Automate[j][i]


        stand_table.append(tempo)
        tempo = ""
    # Initialisation d'une liste "temp" pour stocker les transitions standardisées.
    temp = []
    for i in range(len(stand_table)):
        temp.append(stand_table[i].replace(",",""))
    etat_init.clear()
    etat_init.append("i")
    Automate.insert(0,temp)
    # Retourne les listes "etats" et "temp".
    return etats,temp

Automate_std = []


Automate_std = []
def affichage_automate_standard(etats,auto):
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
            fusion.append(auto[i][j])
        tableau.add_row(fusion)
        fusion.pop(0)
        fusion.pop(0)
        Automate_std.append(fusion)
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
    
Automate2 = []

for i in Automate:
    Automate2.append(i)
verif = 0


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
    print("1.standardiser ?")
    print("2.determinisiser ?")
    print("3.completer ?")


    while True:
        choix = input("Votre choix  : ")
        if choix == '1':

            if not est_un_automate_standard(Automate):
                print("\n STANDARDISATION: ")
                std = standardiser(Automate, etats_init)
                affichage_automate_standard(std[0], Automate)
                if not est_complet(Automate):
                    choix = input("Il n'est pas complet. Rendre complet ?? y ou n : ")

                    if choix == "y":
                        completion(Automate_std)
                        affichage_automate_standard(std[0], Automate_std)
                        continue
                    elif choix == "n":
                        break
                    else:
                        print("Choix incorrect")
            else:
                print("L'automate est déjà standard !")

        if choix == '2':
            if not est_un_automate_deterministe(Automate):
                print("DETERMINISATION")
            print("\nTable de transition après determinisation\n")
            if est_complet(Automate):
                for i in range(len(Automate)):
                    for j in range(len(alphabet)):
                        if Automate[i][j] == "P":
                            Automate[i][j] = "-"

                determini = determinisation(Automate)
                completion(determini[0])
                affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
            else:
                determini = determinisation(Automate)
                affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                if not est_complet(Automate):
                    print("Cependant il n'est pas complet. Rendre complet ? : y ou n")
                    choix = input("")
                    if choix == 'y':
                        completion(determini[0])
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                        if choix == 'n':
                            break
                    if choix == 'n':
                        break

        elif choix == '3':
            if not est_complet(Automate):
                completion(Automate)
                affichage_automate(Automate)
            else:
                print("Deja complet !")



menu()

