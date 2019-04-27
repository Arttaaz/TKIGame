"""
Fonctions permettant d'afficher sur
l'écran principal un écran affichant
un arbre d'actions, et permettant la
modification en directe de l'arbre.
"""

import pygame
import sys

from dimensions import *

PADDING_ARBRE_HAUT = 8
PADDING_ARBRE_COTES = 20
TAILLE_FONT_NOM = 40
TAILLE_FONT_ATTRIBUTS = 20
DECALAGE_ATTRIBUTS_HAUTEUR = 100 # distance entre deux attributs alignés

class AfficherArbre:
    """
    Regroupe toutes les fonctions et
    les variables utiles pour afficher
    un arbre et le modifier.
    """
    def __init__(self, arbre, screen):
        self.arbre = arbre
        self.screen = screen

        self.background_arbre = pygame.image.load('assets/arbre/background_arbre.jpeg').convert()
        self.background_etat = pygame.image.load('assets/arbre/background_etat.jpeg').convert()
        self.background_action = pygame.image.load('assets/arbre/background_action.jpeg').convert()

        self.coord_background_arbre = (PADDING_COTES, PADDING_HAUT)
        self.couleur_fleche = (255, 0, 0)

    def afficher_arbre(self):
        """
        Affiche sur l'écran l'arbre donné en paramètre.
        Retourne un dictionnaire permettant de passer d'un 'Rect'
        à son attribut associé dans l'arbre (le 'Rect' en question représentant
        la place de l'attribut associé sur l'écran).
        """
        ### Initialisations
        dico_rect = {} # Dictionnaire associant un rect à sont attribut
        pygame.font.init() # initialise le module font
        font_etat = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_ATTRIBUTS, bold=True)
        font_nom = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_NOM, bold=True, italic=True)
        self.screen.blit(self.background_arbre, self.coord_background_arbre)
        
        longueur_ecran = self.background_arbre.get_rect().width - 2*PADDING_ARBRE_COTES # fois 2 car padding des deux côtés
        pas_etat = longueur_ecran // len(self.arbre.list_etats)
        text_nom = font_nom.render(self.arbre.nom_arbre, True, (0, 0, 0))
        coord_nom_arbre = centrer_coords((PADDING_COTES+PADDING_ARBRE_COTES, PADDING_ARBRE_HAUT + PADDING_HAUT), LONGUEUR_ARBRE, text_nom.get_rect().width)
        coord_etat = (self.coord_background_arbre[0], coord_nom_arbre[1]+DECALAGE_ATTRIBUTS_HAUTEUR)
        coords_debut_etat = [] # tableau contenant les coords haut de chacun des états (pour tracer des lignes)

        ### Début de l'affichage des états et de leurs actions associées
        for etat in self.arbre.list_etats:
            rect = self.background_etat.get_rect()
            text = font_etat.render(etat.nom_etat, True, (0, 0, 0))
            coords = centrer_coords(coord_etat, pas_etat, rect.width)
            coords_text = centrer_coords(coord_etat, pas_etat, text.get_rect().width)
            coords_text = (coords_text[0], coords_text[1]+rect.height//2)
            fin_coords_etat = (coords[0]+rect.width//2, coords[1]+rect.height)
            
            new_key = coords + (rect.width, rect.height)
            dico_rect[new_key] = etat

            self.screen.blit(self.background_etat, coords)
            self.screen.blit(text, coords_text)
            milieu_action = self.afficher_action(etat.action_associee, (coord_etat[0], coord_etat[1]+DECALAGE_ATTRIBUTS_HAUTEUR), pas_etat, font_etat, dico_rect)

            pygame.draw.aaline(self.screen, self.couleur_fleche, fin_coords_etat, milieu_action)
            coord_etat = (coord_etat[0]+pas_etat, coord_etat[1])
            coords_debut_etat.append((fin_coords_etat[0], coords[1]))

        ### Fini par dessiner le nom de l'arbre et les liens vers etats
        self.screen.blit(text_nom, coord_nom_arbre)
        fin_coords_nom_arbre = (coord_nom_arbre[0]+text_nom.get_rect().width//2, coord_nom_arbre[1]+text_nom.get_rect().height)
        for coords in coords_debut_etat:
            pygame.draw.aaline(self.screen, self.couleur_fleche, fin_coords_nom_arbre, coords)

        pygame.font.quit() # termine le module font
        return dico_rect
        
    def afficher_action(self, action, coord_action, place_dispo_largeur, font_action, dico_rect):
        """
        Fonction récursive affichant
        l'action donnée en paramètres,
        et les actions suivantes récursivement.
        Retourne la coordonnée milieu_haut de l'action (pour
        tracer une ligne qui relie l'action à la précédente).

        Actualise aussi le dico_rect.
        """
        text = font_action.render(action.nom, True, (0, 0, 0))
        coords = centrer_coords(coord_action, place_dispo_largeur, self.background_action.get_rect().width)
        coords_text = centrer_coords(coords, self.background_action.get_rect().width, text.get_rect().width)
        coords_text = (coords_text[0], coords_text[1]+self.background_action.get_rect().height//2)
        self.screen.blit(self.background_action, coords)
        self.screen.blit(text, coords_text)

        new_key = coords + (self.background_action.get_rect().width, self.background_action.get_rect().height)
        dico_rect[new_key] = action # actualise le dico avec une nouvelle entrée correspondant à l'action en cours de traitement

        if action.list_actions_suivantes is None:
            return (coords[0]+self.background_action.get_rect().width//2, coords[1])# il n'y a aucunes actions qui découlent de l'action courante

        coords_fin_action = (coord_action[0] + place_dispo_largeur//2, coord_action[1]+self.background_action.get_rect().height)
        pas_action = place_dispo_largeur // len(action.list_actions_suivantes)
        for a in action.list_actions_suivantes:
            milieu_coords = self.afficher_action(a, (coord_action[0], coord_action[1]+DECALAGE_ATTRIBUTS_HAUTEUR), pas_action, font_action, dico_rect)
            pygame.draw.aaline(self.screen, self.couleur_fleche, coords_fin_action, milieu_coords)
            coord_action = (pas_action + coord_action[0], coord_action[1])

        return (coords[0]+self.background_action.get_rect().width//2, coords[1])


def centrer_coords(debut_coord, longueur_dispo, longueur_objet):
    """
    Retourne les coordonnées où il faut
    placer l'objet de sorte à ce qu'il soit centré.
    """
    return (debut_coord[0] + (longueur_dispo-longueur_objet)//2, debut_coord[1])


def has_clicked_on_attribut(dico_rect, event):
    """
    Retourne l'attribut sur lequel a clické l'utilisateur,
    s'il a clické sur un attribut !
    """
    for key in dico_rect:
        rect = pygame.Rect(key)
        if rect.collidepoint(event.pos):
            return dico_rect[key], rect


if __name__ == "__main__":
    from arbre import *

    marcher_vers = Action('marcher_vers', action_inutile, None, None)
    attaquer = Action('attaquer', action_inutile, None, None)
    decider_quelque_chose = Action('decider_quelque_chose', action_inutile, None, [marcher_vers, attaquer])
    idle = Etat(marcher_vers, 'Idle')
    faire_quelque_chose = Etat(decider_quelque_chose, 'Faire quelque chose')
    arbre = Arbre([idle, faire_quelque_chose], idle)

    screen = pygame.display.set_mode((1152, 640))
    background = pygame.image.load('assets/background.jpg').convert()
    screen.blit(background, (0, 0))

    dico_rect = AfficherArbre(arbre, screen).afficher_arbre()
    obj_valide = None

    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                obj_click = has_clicked_on_attribut(dico_rect, event)
                print(obj_click)

        pygame.time.delay(100)
