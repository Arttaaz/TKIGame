"""
Fonctions permettant d'afficher sur
l'écran principal un écran affichant
un arbre d'actions, et permettant la
modification en directe de l'arbre.
"""

import pygame
import sys

from dimensions import *
from arbre import Etat, Action

PADDING_ARBRE_HAUT = 8
PADDING_ARBRE_COTES = 15
TAILLE_FONT_NOM = 40
TAILLE_FONT_ATTRIBUTS = 20
TAILLE_FONT_PARAMS = 15
TAILLE_FONT_CONDITIONS = 20
TAILLE_FONT_MINIMUM = 10
DECALAGE_ATTRIBUTS_HAUTEUR = 100 # distance entre deux attributs alignés
WIDTH_LIGNES = 3
WIDTH_LIGNES_BLOQUEES = 5
LARGEUR_HIT_BOX_LIGNES_MINIMALE = 30
COULEUR_FLECHE = (255, 0, 0)
COULEUR_FLECHE_BLOQUEE = (128, 128, 128)


class AfficherArbre:
    """
    Regroupe toutes les fonctions et
    les variables utiles pour afficher
    un arbre et le modifier.
    """
    def __init__(self, arbre, screen):
        self.arbre = arbre
        self.screen = screen

        self.background_arbre = pygame.image.load('assets/arbre/background_arbre.png').convert()
        self.background_etat = pygame.image.load('assets/arbre/background_etat.png').convert()
        self.background_action = pygame.image.load('assets/arbre/background_action.png').convert()
        self.background_params = pygame.image.load('assets/arbre/background_parametre.png').convert()
        self.background_etat_defaut = pygame.image.load('assets/arbre/background_etat_defaut.png').convert()

        pygame.font.init() # initialise le module font
        self.font_etat = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_ATTRIBUTS, bold=True)
        self.font_action = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_ATTRIBUTS)
        self.font_nom = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_NOM, bold=True, italic=True)
        self.font_params = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_PARAMS, italic=True)
        self.font_conditions = pygame.font.SysFont(pygame.font.get_default_font(), TAILLE_FONT_CONDITIONS)

        self.coord_background_arbre = (PADDING_COTES, PADDING_HAUT)
        self.couleur_fleche = (255, 0, 0)

    def afficher_arbre(self):
        """
        Affiche sur l'écran l'arbre donné en paramètre.
        Retourne un dictionnaire permettant de passer d'un 'Rect'
        à son attribut associé dans l'arbre (le 'Rect' en question représentant
        la place de l'attribut associé sur l'écran).

        Le 'Rect' dans le dico est représenté par un tuple (x, y, width, height).
        Si l'attribut du 'Rect' est une 'Action' ou un 'Etat', ajoute tel quel l'attribut au dico.
        Si le 'Rect' représente une ligne, alors associe au 'Rect' un tableau [Attribut départ, Attribut arrivée, condition entre les deux, pos_debut_fleche, pos_fin_fleche].
        """
        ### Initialisations
        rect = self.background_etat.get_rect()
        dico_rect = {} # Dictionnaire associant un rect à sont attribut
        self.screen.blit(self.background_arbre, self.coord_background_arbre)

        ### Affiche le nom de l'arbre
        longueur_ecran = self.background_arbre.get_rect().width - 2*PADDING_ARBRE_COTES # fois 2 car padding des deux côtés
        pas_etat = longueur_ecran // len(self.arbre.list_etats)
        text_nom = self.font_nom.render(self.arbre.nom_arbre, True, (0, 0, 0))
        coord_nom_arbre = centrer_coords_longueur((PADDING_COTES+PADDING_ARBRE_COTES, PADDING_ARBRE_HAUT + PADDING_HAUT), LONGUEUR_MAX_NOM, text_nom.get_rect().width)
        coord_etat = (self.coord_background_arbre[0], coord_nom_arbre[1]+DECALAGE_ATTRIBUTS_HAUTEUR)
        coords_debut_etat = [] # tableau contenant les coords haut de chacun des états (pour tracer des lignes)

        ### Début de l'affichage des états et de leurs actions associées
        for etat in self.arbre.list_etats:
            coords = centrer_coords_longueur(coord_etat, pas_etat, rect.width)
            fin_coords_etat = (coords[0]+rect.width//2, coords[1]+rect.height)

            new_key = coords + (rect.width, rect.height)
            dico_rect[new_key] = etat

            self.screen.blit(self.background_etat, coords)
            blit_text_properly(self.screen, etat.nom_etat, pygame.Rect(coords[0], coords[1], rect.width, rect.height), self.font_etat, TAILLE_FONT_ATTRIBUTS)
            milieu_action = self.afficher_action(etat.action_associee, (coord_etat[0], coord_etat[1]+DECALAGE_ATTRIBUTS_HAUTEUR), pas_etat, dico_rect)

            rect_line = dessiner_ligne(self.screen, fin_coords_etat, milieu_action, etat.liaison_modifiable)
            if etat.liaison_modifiable:
                rect_line = adapt_rect_line(rect_line)
                dico_rect[(rect_line.left, rect_line.top, rect_line.width, rect_line.height)] = [etat, etat.action_associee, None, fin_coords_etat, milieu_action]

            coord_etat = (coord_etat[0]+pas_etat, coord_etat[1])
            coords_debut_etat.append((fin_coords_etat[0], coords[1]))

        ### Fini par dessiner le nom de l'arbre et les liens vers les etats
        self.screen.blit(text_nom, coord_nom_arbre)
        fin_coords_nom_arbre = (coord_nom_arbre[0]+text_nom.get_rect().width//2, coord_nom_arbre[1]+text_nom.get_rect().height)
        for coords in coords_debut_etat:
            pygame.draw.line(self.screen, COULEUR_FLECHE_BLOQUEE, fin_coords_nom_arbre, coords, WIDTH_LIGNES_BLOQUEES)

        ### Dessine l'état par défaut de l'arbre
        coords_etat_defaut = (fin_coords_nom_arbre[0]+text_nom.get_rect().width//2-self.background_etat_defaut.get_rect().width, fin_coords_nom_arbre[1])
        rect_text = pygame.Rect(coords_etat_defaut, (self.background_etat_defaut.get_rect().width, self.background_etat_defaut.get_rect().height))
        self.screen.blit(self.background_etat_defaut, coords_etat_defaut)
        blit_text_properly(self.screen, self.arbre.etat_courant.nom_etat, rect_text, self.font_etat, TAILLE_FONT_ATTRIBUTS)

        return dico_rect

    def afficher_action(self, action, coord_action, place_dispo_largeur, dico_rect):
        """
        Fonction récursive affichant
        l'action donnée en paramètres,
        et les actions suivantes récursivement.
        Retourne la coordonnée milieu_haut de l'action (pour
        tracer une ligne qui relie l'action à la précédente).

        Actualise aussi le dico_rect.
        """
        ### Affiche l'action de manière normale
        background_action_rect = self.background_action.get_rect()
        ### Affiche l'action
        text = self.font_action.render(action.nom, True, (0, 0, 0))
        coords = centrer_coords_longueur(coord_action, place_dispo_largeur, background_action_rect.width)
        coords_fin_action = (coord_action[0] + place_dispo_largeur//2, coord_action[1]+background_action_rect.height)

        self.screen.blit(self.background_action, coords)
        blit_text_properly(self.screen, action.nom, pygame.Rect(coords, (background_action_rect.width, background_action_rect.height)), self.font_action, TAILLE_FONT_ATTRIBUTS)

        ### Affiche les paramètres
        coords_params = (coords[0]+background_action_rect.width//2, coords[1]+background_action_rect.height)
        params = action.params_action_associee
        if params is not None:
            for p in params:
                self.screen.blit(self.background_params, coords_params)
                blit_text_properly(self.screen, p, pygame.Rect(coords_params, (self.background_params.get_rect().width, self.background_params.get_rect().height)), self.font_params, TAILLE_FONT_PARAMS)
                coords_params = (coords_params[0], coords_params[1]+self.background_params.get_rect().height)

        ### Actualise le dico
        new_key = coords + (background_action_rect.width, background_action_rect.height)
        dico_rect[new_key] = action # actualise le dico avec une nouvelle entrée correspondant à l'action en cours de traitement

        if action.list_actions_suivantes is None:
            return (coords[0]+background_action_rect.width//2, coords[1])# il n'y a aucunes actions qui découlent de l'action courante

        ### Affiche les actions suivantes et trace des flèches verte entre cette action et les actions suivantes ainsi que les conditions potentielles
        if type(action.list_actions_suivantes) is not type({}):
            action.list_actions_suivantes = {None : action.list_actions_suivantes} # le passe en mode dico pour simplifier le traitement

        # Regarde le nombre d'actions à afficher réellement
        actions_a_afficher = []
        for val_action in action.list_actions_suivantes:
            rect = is_action_already_blitten(action.list_actions_suivantes[val_action], dico_rect) # est-ce que l'action existe ?
            if rect is None:
                actions_a_afficher.append(val_action) # il faut tracer cette action
                continue

            milieu_coords = (rect.left+rect.width//2, rect.top) # il faut quand même tracer la ligne qui va vers l'action
            rect_line = dessiner_ligne(self.screen, coords_fin_action, milieu_coords, action.liaison_modifiable[val_action])
            if action.liaison_modifiable[val_action]:
                rect_line = adapt_rect_line(rect_line)
                dico_rect[(rect_line.left, rect_line.top, rect_line.width, rect_line.height)] = [action, action.list_actions_suivantes[val_action], val_action, coords_fin_action, milieu_coords]

            if val_action is not None: # cas où il y a de condition
                text = self.font_conditions.render(str(val_action), True, (0, 0, 0))
                coords_text = centrer_objet((rect_line.left, rect_line.top), (text.get_rect().width, text.get_rect().height), (rect_line.width, rect_line.height))
                self.screen.blit(text, coords_text)


        if actions_a_afficher == []: # aucunes actions à afficher
            return (coords[0]+background_action_rect.width//2, coords[1])# il n'y a aucunes actions qui découlent de l'action courante


        pas_action = place_dispo_largeur // len(actions_a_afficher)
        for val_action in actions_a_afficher: # contient les clefs des actions à afficher
            milieu_coords = self.afficher_action(action.list_actions_suivantes[val_action], (coord_action[0], coord_action[1]+DECALAGE_ATTRIBUTS_HAUTEUR), pas_action, dico_rect)
            rect_line = dessiner_ligne(self.screen, coords_fin_action, milieu_coords, action.liaison_modifiable[val_action])
            if action.liaison_modifiable[val_action]:
                rect_line = adapt_rect_line(rect_line)
                dico_rect[(rect_line.left, rect_line.top, rect_line.width, rect_line.height)] = [action, action.list_actions_suivantes[val_action], val_action, coords_fin_action, milieu_coords]

            if val_action is not None: # cas où il y a de condition
                text = self.font_conditions.render(str(val_action), True, (0, 0, 0))
                coords_text = centrer_objet((rect_line.left, rect_line.top), (text.get_rect().width, text.get_rect().height), (rect_line.width, rect_line.height))
                self.screen.blit(text, coords_text)


            coord_action = (pas_action + coord_action[0], coord_action[1])

        return (coords[0]+background_action_rect.width//2, coords[1])


def centrer_coords_longueur(debut_coord, longueur_dispo, longueur_objet):
    """
    Retourne les coordonnées où il faut
    placer l'objet de sorte à ce qu'il soit centré en longueur seulement.
    """
    return (debut_coord[0] + (longueur_dispo-longueur_objet)//2, debut_coord[1])


def centrer_objet(coord_initial, taille_objet, place_reservee):
    """
    Retourne les coordonnées qui centrent l'objet dans la place réservée.
    """
    return (coord_initial[0] + (place_reservee[0]-taille_objet[0])//2, coord_initial[1] + (place_reservee[1]-taille_objet[1])//2)


def adapter_taille_font(font, msg, longueur_limite, taille_initiale):
    """
    Retourne la bonne taille pour que le msg à
    écrire ne soit pas plus long que la longueur limite
    donnée.
    """
    taille_font = taille_initiale
    bonne_font = False
    while taille_font >= TAILLE_FONT_MINIMUM:
        if font.size(str(msg))[0] < longueur_limite:
            return taille_font
        taille_font -= 1
        font = changer_width_font(font, taille_font)
    return TAILLE_FONT_MINIMUM


def changer_width_font(font, nv_width):
    """
    Retourne une nouvelle font qui a les mêmes
    propriétés que la font initiale mais change la width.
    """
    return pygame.font.SysFont(pygame.font.get_default_font(), nv_width, italic=font.get_italic(), bold=font.get_bold())


def blit_text_properly(screen, msg, rect, font, taille_font_initial):
    """
    Ecrit le message dans le rectangle donné de manière à centrer
    le message et à faire en sorte qu'il rentre en entier.
    """
    taille_font = adapter_taille_font(font, msg, rect.width, taille_font_initial)
    font = changer_width_font(font, taille_font)
    text = font.render(str(msg), True, (0, 0, 0))
    coords = centrer_objet((rect.left, rect.top), (text.get_rect().width, text.get_rect().height), (rect.width, rect.height))
    screen.blit(text, coords)

def adapt_rect_line(rect):
    """
    Fais en sorte que la hit box de la ligne
    soit au moins de la largeur minimale imposée.
    Retourne un nouveau rect_line valide.
    """
    width = max(rect.width, LARGEUR_HIT_BOX_LIGNES_MINIMALE)
    return pygame.Rect(rect.left+rect.width//2-width//2, rect.top, width, rect.height)

def is_action_already_blitten(action, dict_rect):
    """
    Permet de savoir si une action a déjà été dessinée
    sur l'écran ou non.
    Si c'est le cas, elle retourne le
    rect où est placer l'action en question.
    """
    for rect in dict_rect:
        if dict_rect[rect] is action:
            return pygame.Rect(rect)

def dessiner_ligne(screen, coord_debut_fleche, coord_fin_fleche, is_modifiable):
    """
    Dessine la ligne en vérifiant
    si on trace une ligne
    que l'on peut modifier ou alors
    une ligne que l'on n'a pas le droit
    de modifier.

    Retourne le rect de la ligne.
    """
    if is_modifiable:
        taille_line = WIDTH_LIGNES
        couleur_fleche = COULEUR_FLECHE
    else:
        taille_line = WIDTH_LIGNES_BLOQUEES
        couleur_fleche = COULEUR_FLECHE_BLOQUEE
    rect_line = adapt_rect_line(pygame.draw.line(screen, couleur_fleche, coord_debut_fleche, coord_fin_fleche, taille_line))

    return rect_line


if __name__ == "__main__":
    from arbre import *

    marcher_vers = Action('marcher_vers', action_inutile, ["Coucou"], None)
    attaquer = Action('attaquer', action_inutile, [9], None)
    decider_quelque_chose = Action('decider_quelque_chose', action_inutile, None, {"Oui" : marcher_vers, "Non" : attaquer})
    idle = Etat(marcher_vers, False, 'Idle')
    faire_quelque_chose = Etat(decider_quelque_chose, 'Faire quelque chose')
    arbre = Arbre([idle, faire_quelque_chose], idle)

    screen = pygame.display.set_mode((1152, 640))
    background = pygame.image.load('assets/background.jpg').convert()
    screen.blit(background, (0, 0))

    dico_rect = AfficherArbre(arbre, screen).afficher_arbre()

    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.time.delay(100)
