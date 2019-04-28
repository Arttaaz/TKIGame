"""
Permet l'affichage d'un menu.
La fonction principale renvoie un nombre correspondant
au bouton sur lequel l'utilisateur a appuyé.
"""

import pygame

from dimensions import *
from afficher_arbre import centrer_objet
from gerer_arbre import has_clicked_on_rect


JOUER = 1
CREDITS = 2
QUITTER = 3

IDLE = 1
SURVOL = 2
ENFONCE = 3

nom_images = ["jouer", "credits", "quitter"]
etats = ["idle", "survol", "enfonce"]

def menu(screen):
    """
    Fonction initialisant les variables
    du menu et lance la boucle principale.
    """
    dict_images = {}
    for nom_i in nom_images:
        for nom_e in etats:
            dict_images["{}_{}".format(nom_i, nom_e)] = pygame.image.load('assets/menu/{}_{}.png'.format(nom_i, nom_e)).convert()

    etat_boutons = [IDLE for _ in range(len(nom_images))]
    return boucle_principale(screen, dict_images, etat_boutons)

def update_screen(screen, etat_boutons, images):
    """
    Update le menu, affichant en surbrillance
    les boutons que l'on survole, et affichant
    les boutons sur lesquels on clic en mode enfoncé.
    
    - tab_boutons : liste contenant tout les boutons sur l'écran
    - etat_boutons : liste qui donne l'état de tout les boutons sur l'écran
    - images : dictionnaire contenant toutes les images chargées des boutons dans
    tout les etats possibles
    """
    coord_courant = (0, 0)
    dict_rect = {}

    screen.blit(images["background_menu"], coord_courant)
    pas_bouton = HAUTEUR_FENETRE // len(etat_boutons)
    for num_bouton range(len(etat_boutons)):
        img = images["{}_{}".format(nom_images[num_bouton], etats[etat_boutons[num_bouton]])]
        coords_image = centrer_objet(coord_courant, (img.get_rect().width, img.get_rect().height), (LONGUEUR_FENETRE, pas_bouton))
        screen.blit(img, coords_image)

        coord_courant = (coord_courant[0], coord_courant[1] + pas_bouton)
        dict_rect[coords_image + (img.get_rect().width, img.get_rect().height)] = num_bouton

    return dict_rect # retourne le dictionnaire contenant la position des boutons (pour détecter le clic)


def handle_event(etat_boutons, dico_rect):
    """
    Actualise l'état des boutons et retourne si un bouton
    a été clické (numéro du bouton en question).
    Retourne -1 par défaut, lorsqu'aucun bouton n'a été clické.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # on relache le clic sur un bouton ?
            for i in range(len(etat_boutons)):
                etat_boutons[i] = IDLE # réinitialise tout les états

            obj_click = has_clicked_on_rect(dico_rect, event)
            if obj_click is not None:
                return obj_click[0] # retourne le numero du bouton clické
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # on enfonce le clic sur un bouton ?
            obj_click = has_clicked_on_rect(dico_rect, event)
            if obj_click is not None:
                etat_boutons[obj_click[0]] = ENFONCE
        elif event.type == pygame.MOUSEMOTION: # on passe par dessus un bouton ?
            for i in range(len(etat_boutons)):
                if etat_boutons[i] == SURVOL:
                    etat_boutons[i] = IDLE # réinitialise l'état des boutons

            obj_click = has_clicked_on_rect(dico_rect, event)
            if obj_click is not None:
                etat_boutons[obj_click[0]] = SURVOL

    return -1


def boucle_principale(screen, nom_images, etat_boutons):
    """
    Boucle d'affichage.
    Retourne le numéro du bouton sur lequel on a clické.
    """
    valeur_retour = -1
    while valeur_retour == -1:
       dict_rect = update_screen(screen, etat_boutons)
       valeur_retour = handle_event(etat_boutons, dico_rect)
       pygame.display.update()
       pygame.time.delay(100)

    return valeur_retour
