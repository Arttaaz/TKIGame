"""
Permet l'affichage d'un menu.
La fonction principale renvoie un nombre correspondant
au bouton sur lequel l'utilisateur a appuyé.
"""

import pygame

from dimensions import *
from afficher_arbre import centrer_objet
from gerer_arbre import has_clicked_on_rect


JOUER = 0
CREDITS = 1
QUITTER = 2

IDLE = 0
SURVOL = 1
ENFONCE = 2


class Menu:
    def __init__(self):
        """
        Fonction initialisant les variables
        du menu et lance la boucle principale.
        """
        self.nom_images = ["jouer", "credits", "quitter"]
        self.etats = ["idle", "survol", "enfonce"]
        self.dict_images = {}
        self.dict_rect = {}

        for nom_i in self.nom_images:
            for nom_e in self.etats:
                self.dict_images["{}_{}".format(nom_i, nom_e)] = pygame.image.load('assets/menu/{}_{}.png'.format(nom_i, nom_e))
        self.dict_images["background_menu1"] = pygame.image.load('assets/menu/background1.png').convert()
        self.dict_images["background_menu2"] = pygame.image.load('assets/menu/background2.png').convert()
        self.dict_images["titre"] = pygame.image.load('assets/menu/titre.png')

        self.timer = 0
        self.etat_boutons = [IDLE for _ in range(len(self.nom_images))]

    def update_screen(self, screen):
        """
        Update le menu, affichant en surbrillance
        les boutons que l'on survole, et affichant
        les boutons sur lesquels on clic en mode enfoncé.

        - tab_boutons : liste contenant tout les boutons sur l'écran
        - etat_boutons : liste qui donne l'état de tout les boutons sur l'écran
        - immages : dictionnaire contenant toutes les images chargées des boutons dans
        tout les etats possibles
        """
        img = self.dict_images["titre"]
        
       
        coord_courant = (0, 280)
        self.timer += 0.01
        if self.timer > 1 :
            self.timer = 0
        if self.timer > 0.5:
            screen.blit(self.dict_images["background_menu1"], (0, 0))
        else:
            screen.blit(self.dict_images["background_menu2"], (0, 0))

        screen.blit(img,(255, 40))

        pas_bouton = HAUTEUR_FENETRE // (len(self.etat_boutons) + 3)
        for num_bouton in range(len(self.etat_boutons)):
            img = self.dict_images["{}_{}".format(self.nom_images[num_bouton], self.etats[self.etat_boutons[num_bouton]])]
            coords_image = centrer_objet(coord_courant, (img.get_rect().width, img.get_rect().height), (LONGUEUR_FENETRE, pas_bouton))
            screen.blit(img, coords_image)

            coord_courant = (coord_courant[0], coord_courant[1] + pas_bouton)
            self.dict_rect[coords_image + (img.get_rect().width, img.get_rect().height)] = num_bouton



    def handle_event(self, event):
        """
        Actualise l'état des boutons et retourne si un bouton
        a été clické (numéro du bouton en question).
        Retourne -1 par défaut, lorsqu'aucun bouton n'a été clické.
        """
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # on relache le clic sur un bouton ?
            for i in range(len(self.etat_boutons)):
                self.etat_boutons[i] = IDLE # réinitialise tout les états

                obj_click = has_clicked_on_rect(self.dict_rect, event)
                if obj_click is not None:
                    return obj_click[0] # retourne le numero du bouton clické
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # on enfonce le clic sur un bouton ?
                    obj_click = has_clicked_on_rect(self.dict_rect, event)
                    if obj_click is not None:
                        self.etat_boutons[obj_click[0]] = ENFONCE
        elif event.type == pygame.MOUSEMOTION: # on passe par dessus un bouton ?
            for i in range(len(self.etat_boutons)):
                if self.etat_boutons[i] == SURVOL:
                    self.etat_boutons[i] = IDLE # réinitialise l'état des boutons

            obj_click = has_clicked_on_rect(self.dict_rect, event)
            if obj_click is not None:
                self.etat_boutons[obj_click[0]] = SURVOL

        return -1


    def boucle_principale(screen, nom_images, etat_boutons):
        """
        Boucle d'affichage.
        Retourne le numéro du bouton sur lequel on a clické.
        """
        valeur_retour = -1
        while valeur_retour == -1:
            pygame.display.update()
            pygame.time.delay(100)

        return valeur_retour
