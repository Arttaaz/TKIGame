"""
Module gérant les fonctionnalités suivantes:
    - affiche un arbre par dessus le screen
    - modifie l'arbre en respectant des conditions (nombre de modifications limitées etc ...)
    - quitte proprement ces fonctionnalités avec l'arbre bien modifié
"""

import pygame
import sys

from afficher_arbre import AfficherArbre, centrer_objet
from modifier_arbre import Modification
from dimensions import *


class GererArbre:
    """
    Objet permettant toutes les fonctionnalitées cités plus haut.
    """
    def __init__(self, screen, arbre):
        """
        N'a besoin que du screen et d'un arbre.
        On pourra donner des règles en argument plus tard ?
        """
        self.screen = screen
        self.arbre = arbre
        self.afficher_arbre = AfficherArbre(arbre, screen)

        self.background_bouton = pygame.image.load('assets/arbre/background_bouton.jpeg').convert()
        self.background_clavier = pygame.image.load('assets/arbre/background_clavier.jpg').convert()

    def lancer_affichage(self):
        """
        Affiche les éléments principaux sur le screen.
        """
        self.dico_rect_attributs = self.afficher_arbre.afficher_arbre()
        self.afficher_UI()

    def afficher_UI(self):
        """
        Affiche l'interface utilisateur:
            - bouton sauvegarder & quitter
            - bouton reset modifs
            - bouton annuler & quitter
        Sauvegarde un dico associant chaque rect à son bouton.
        """
        pygame.font.init()
        font_bouton = pygame.font.SysFont(pygame.font.get_default_font(), 20, bold=True)

        nom_boutons = ["Save & quit", "Reset", "Cancel"]
        pas_bouton = HAUTEUR_TOTAL // 3 # décalage en hauteur d'un bouton à l'autre
        rect_bouton = self.background_bouton.get_rect()
        coord_initial = (PADDING_COTES+LONGUEUR_ARBRE, PADDING_HAUT)
        self.dico_rect_boutons = {}

        rect_courant = pygame.Rect(coord_initial[0], coord_initial[1], LONGUEUR_BOUTON, pas_bouton)
        self.screen.blit(self.background_clavier, coord_initial)
        for nom in nom_boutons:
            coords = centrer_objet((rect_courant.left, rect_courant.top), (rect_bouton.width, rect_bouton.height), (rect_courant.width, rect_courant.height))
            self.screen.blit(self.background_bouton, coords)
            self.dico_rect_boutons[coords+(rect_bouton.width, rect_bouton.height)] = nom

            text = font_bouton.render(nom, True, (0, 0, 0))
            coords = centrer_objet((rect_courant.left, rect_courant.top), (text.get_rect().width, text.get_rect().height), (rect_courant.width, rect_courant.height))
            self.screen.blit(text, coords)

            rect_courant.top = rect_courant.top + pas_bouton

        pygame.font.quit()

    def boucle_principale(self):
        """
        Gère l'ensemble de la fenêtre ici. Les boutons sont gérés
        ici aussi.
        """
        self.lancer_affichage() # dessine l'affichage
        pygame.display.update() # actualise la fenêtre
        attr_selectionne = None # si vaut None, on a sélectionné aucun attribut de l'arbre

        modifs = [] # tableau des modifs à faire
        quitter = False
        sauvegarder = False

        while not quitter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: #clic gauche
                        obj_click = has_clicked_on_rect(self.dico_rect_attributs, event) # regarde d'abord si on a clické sur un attribut
                        if obj_click is not None: # on a clické sur un attribut
                            if attr_selectionne is None: # premier attribut qu'on sélectionne
                                attr_selectionne = obj_click
                            else: # dessine la modification proposée
                                modifs.append(Modification(attr_selectionne[0], attr_selectionne[1], obj_click[0], obj_click[1])) # ajoute au tab des modifs
                                modifs[-1].dessiner_modification(self.screen)
                                pygame.display.update()
                                attr_selectionne = None

                        obj_click = has_clicked_on_rect(self.dico_rect_boutons, event) # regarde si on a clické sur un bouton
                        if obj_click is not None: # on a clické sur un bouton
                            if obj_click[0] == "Save & quit":
                                quitter = True
                                sauvegarder = True
                            elif obj_click[0] == "Cancel":
                                quitter = True
                            elif obj_click[0] == "Reset":
                                modifs = []
                                self.dico_rect_attributs = self.afficher_arbre.afficher_arbre()
                                pygame.display.update()

            pygame.time.delay(100)

        # fin de la boucle while : on regarde si on sauvegarde ou pas
        if sauvegarder:
            for m in modifs:
                m.effectuer_modification()


    def gerer_click(self, obj_click):
        """
        Assume que l'objet sur lequel on a clické n'est pas None.
        Effectue les actions associé au clic.
        """
        pass


def has_clicked_on_rect(dico_rect, event):
    """
    Retourne l'attribut / le bouton sur lequel a clické l'utilisateur,
    s'il a clické sur un attribut / bouton !
    """
    for key in dico_rect:
        rect = pygame.Rect(key)
        if rect.collidepoint(event.pos):
            return dico_rect[key], rect


if __name__ == "__main__":
    from arbre import *
    from creer_arbre import *

    arbre = creer_unite_attaque()

    screen = pygame.display.set_mode((1180, 640))
    background = pygame.image.load('assets/background.jpg').convert(screen)
    screen.blit(background, (0, 0))
    screen.fill((255, 255, 255))

    g = GererArbre(screen, arbre)
    g.boucle_principale()
    pygame.quit()
