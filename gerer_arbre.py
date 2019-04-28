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
from arbre import Action, Etat
from dimensions import *

PADDING_ENCADREMENT = 10
PADDING_BOUTON_HAUT = 10

class GererArbre:
    """
    Objet permettant toutes les fonctionnalitées cités plus haut.
    """
    def __init__(self, screen, arbre, modifs_associees=[]):
        """
        N'a besoin que du screen et d'un arbre.
        Il est possible de donner un tableau de modifications qui a été
        créé lors d'une précédente modification de l'arbre.
        On pourra donner des règles de recâblage en argument plus tard ?
        """
        self.screen = screen
        self.arbre = arbre
        self.afficher_arbre = AfficherArbre(arbre, screen)

        self.modifs_intiales = modifs_associees # modifications qu'on ne change pas (pour le cas où on sauvegarde pas)
        self.modifs = [m for m in modifs_associees] # copie les modifs dans un nouveau tableau

        self.background_bouton = pygame.image.load('assets/arbre/background_bouton.jpeg').convert()
        self.background_clavier = pygame.image.load('assets/arbre/background_clavier.jpg').convert()
        self.attr_selectionne = None # si vaut None, on a sélectionné aucun attribut de l'arbre
        self.ligne_selectionnee = None # same

        self.quitter = False
        self.sauvegarder = False
        
        self.dico_rect_attributs = self.afficher_arbre.afficher_arbre()

    def lancer_affichage(self):
        """
        Affiche les éléments principaux sur le screen.
        """
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

        nom_boutons = ["Save", "Reset", "Cancel", "Quit"]
        pas_bouton = (LONGUEUR_ARBRE-LONGUEUR_MAX_NOM) // len(nom_boutons) # décalage en largeur d'un bouton à l'autre
        rect_bouton = self.background_bouton.get_rect()
        coord_initial = (PADDING_COTES+LONGUEUR_MAX_NOM, PADDING_HAUT+PADDING_BOUTON_HAUT)
        self.dico_rect_boutons = {}

        rect_courant = pygame.Rect(coord_initial[0], coord_initial[1], LONGUEUR_ARBRE-LONGUEUR_MAX_NOM, HAUTEUR_MAX_BOUTON)
        for nom in nom_boutons:
            coords = centrer_objet((rect_courant.left, rect_courant.top), (rect_bouton.width, rect_bouton.height), (rect_courant.width, rect_courant.height))
            coords = (rect_courant.left, rect_courant.top)
            self.screen.blit(self.background_bouton, coords)
            self.dico_rect_boutons[coords+(rect_bouton.width, rect_bouton.height)] = nom

            rect_courant.left = rect_courant.left + pas_bouton

    def update_main_screen(self):
        """
        Update tous les dessins sauf les encadrements
        des rects.
        Permet surtout d'actualisé les modifs, et d'effacer
        les encadrements.
        """
        self.dico_rect_attributs = self.afficher_arbre.afficher_arbre()
        self.afficher_UI()

        for m in self.modifs:
            m.dessiner_modification(self.screen) # dessine les modifs

    def encadrer_rect(self, rect):
        """
        Encadre un objet de type 'Rect'.
        Permet de montrer ce qu'a sélectionné l'utilisateur.
        """
        point_list = ((rect.left-PADDING_ENCADREMENT, rect.top-PADDING_ENCADREMENT), (rect.left+rect.width+PADDING_ENCADREMENT, rect.top-PADDING_ENCADREMENT), (rect.left+rect.width+PADDING_ENCADREMENT, rect.top+rect.height+PADDING_ENCADREMENT), (rect.left-PADDING_ENCADREMENT, rect.top+rect.height+PADDING_ENCADREMENT))
        pygame.draw.lines(self.screen, (255, 0, 0), True, point_list, 2)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: #clic gauche
                obj_click_attr = has_clicked_on_rect(self.dico_rect_attributs, event) # regarde d'abord si on a clické sur un attribut
                if obj_click_attr is not None: # on a clické sur un attribut
                    self.gerer_click_arbre(obj_click_attr)
                obj_click_bouton = has_clicked_on_rect(self.dico_rect_boutons, event) # regarde si on a clické sur un bouton
                if obj_click_bouton is not None: # on a clické sur un bouton
                    self.gerer_click_bouton(obj_click_bouton)
                if obj_click_bouton is None and obj_click_attr is None: # on a clické dans le vide : réinit les sélections
                    self.attr_selectionne = None
                    self.ligne_selectionnee = None
        return self.quitter

    def render(self):
        self.lancer_affichage() # dessine l'affichage
        self.update_main_screen()
        if self.ligne_selectionnee is not None:
            self.encadrer_rect(self.ligne_selectionnee[1])
        elif self.attr_selectionne is not None:
            self.encadrer_rect(self.attr_selectionne[1])
        
    def update(self):
        pass

    def boucle_principale(self):
        """
        Gère l'ensemble de la fenêtre ici, permets de créé des modifs grâce à la
        gestion des clics.
        Retourne le tableau des modifs réalisées.
        """
        self.lancer_affichage() # dessine l'affichage
        pygame.display.update() # actualise la fenêtre
        self.attr_selectionne = None # si vaut None, on a sélectionné aucun attribut de l'arbre
        self.ligne_selectionnee = None # same

        self.quitter = False
        self.sauvegarder = False

        while not self.quitter:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.render()
            pygame.display.update() # actualise tout le temps l'affichage pour pas se casser le cul
            pygame.time.delay(100)

        return self.get_modifs()
        
    def get_modifs(self):
        # fin de la boucle while : on regarde si on sauvegarde ou pas
        if self.sauvegarder:
            return self.modifs + self.modifs_intiales
        return self.modifs_intiales # retourne les modifs initiales si on sauvegarde pas
    
    def gerer_click_arbre(self, obj_click):
        """
        Assume que l'objet sur lequel on a clické n'est pas None.
        Effectue les actions associées au clic.
        """
        if type(obj_click[0]) is type([]): # si on a un tableau, c'est que on a clické sur une ligne
            self.ligne_selectionnee = obj_click # selectionne la ligne
            self.attr_selectionne = None # reinit la variable
        else: # on a clické sur un attribut
            if self.ligne_selectionnee is not None and type(obj_click[0]) is not Etat: # créé la modif associée, sauf si on a clické sur un état en deuxieme (pas le droit)
                attr_a_modifier, ancien_attr, attr_souhaite = self.ligne_selectionnee[0][0], self.ligne_selectionnee[0][1], obj_click[0]
                debut_ligne = self.ligne_selectionnee[0][3]
                ancien_fin_ligne = self.ligne_selectionnee[0][4]
                fin_ligne = (obj_click[1].left+obj_click[1].width//2, obj_click[1].top)
                self.gerer_nouveau_modif(Modification(attr_a_modifier, ancien_attr, attr_souhaite, debut_ligne, ancien_fin_ligne, fin_ligne, self.afficher_arbre.font_params, self.ligne_selectionnee[0][2]))
                self.ligne_selectionnee = None
            elif self.attr_selectionne is None: # premier attribut qu'on sélectionne et on a pas sélectionner une ligne
                if (type(obj_click[0]) is Action and obj_click[0].list_actions_suivantes is None) or (obj_click[0].action_associee is None): # il est possible de sélectionner uniquement un attribut qui est en fin d'arbre
                    self.attr_selectionne = obj_click
            elif type(obj_click[0]) is not Etat: # dessine la modification proposée, sauf si on a clické sur un état en deuxième (interdit)
                attr_a_modifier, attr_souhaite = self.attr_selectionne[0], obj_click[0]
                debut_ligne = (self.attr_selectionne[1].left+self.attr_selectionne[1].width//2, self.attr_selectionne[1].top+self.attr_selectionne[1].height)
                fin_ligne = (obj_click[1].left+obj_click[1].width//2, obj_click[1].top)
                self.gerer_nouveau_modif(Modification(attr_a_modifier, None, attr_souhaite, debut_ligne, None, fin_ligne)) # ajoute au tab des modifs
                self.attr_selectionne = None
                self.ligne_selectionnee = None

    def gerer_click_bouton(self, obj_click):
        """
        Assume que l'objet sur lequel on a clické n'est pas None.
        Effectue les actions associées au clic.
        """
        if obj_click[0] == "Save":
            self.sauvegarder = True
        elif obj_click[0] == "Quit":
            self.quitter = True
        elif obj_click[0] == "Cancel":
            self.modifs.pop() # retire la dernière modif
        elif obj_click[0] == "Reset":
            self.modifs = []

    def gerer_nouveau_modif(self, modif):
        """
        Ajoute la modif si l'attribut_debut n'a pas déjà été utilisé dans une autre modification.
        Sinon efface les modifs (évite les doublons non authorisés) et ajoute à la fin la nouvelle modif.
        """
        for num, m in enumerate(self.modifs):
            if m.attribut_depart is modif.attribut_depart and m.condition is modif.condition: # doublon non authorisé !
                self.modifs.remove(num) # supprime l'entrée
                self.modifs.append(modif)
                return

        self.modifs.append(modif)


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

    marcher_vers = Action('marcher_vers', action_inutile, ["Coucou"], None)
    attaquer = Action('attaquer', action_inutile, [9], None)
    decider_quelque_chose = Action('decider_quelque_chose', action_inutile, None, {"Oui" : marcher_vers, "Non" : attaquer})
    idle = Etat(marcher_vers, 'Idle')
    faire_quelque_chose = Etat(decider_quelque_chose, 'Faire quelque chose')
    arbre = Arbre([idle, faire_quelque_chose], idle)

    screen = pygame.display.set_mode((1180, 640))
    background = pygame.image.load('assets/background.jpg').convert(screen)
    screen.blit(background, (0, 0))
    screen.fill((255, 255, 255))

    g = GererArbre(screen, arbre)
    modifs = g.boucle_principale()
    pygame.quit()
