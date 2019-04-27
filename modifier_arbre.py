"""
Permet de modifier un arbre en deux temps :
    - enregistre d'abord la modification en enregistrant l'attribut
    à modifier et l'attribut vers lequel on souhaite qu'il pointe
    - effectue ensuite cette modification

Tout ceci est géré par un objet 'Modification'.
"""

import pygame

from arbre import Etat
from afficher_arbre import centrer_coords_longueur, centrer_objet, TAILLE_FONT_CONDITIONS, WIDTH_LIGNES

class Modification:
    """
    Enregistre une modification et les effectue.
    """
    def __init__(self, attribut_a_modifier, ancien_attribut, attribut_souhaite, debut_ligne, ancien_fin_ligne, fin_ligne_souhaite, font_params=None, condition=None):
        """
        Objets attributs sont soit des 'Action' soit des 'Etat'.
        Les lignes sont des coordonnees (debut_ligne = (x_debut_ligne, y_debut_ligne)).
        Il est possible de mettre None à ancien_attribut et ancien_fin_ligne (dans le cas par exemple où ils n'existent pas).
        """
        self.attribut_depart = attribut_a_modifier
        self.attribut_fin = attribut_souhaite
        self.ancien_attribut = ancien_attribut
        self.debut_ligne = debut_ligne
        self.ancien_fin_ligne = ancien_fin_ligne
        self.fin_ligne_souhaite = fin_ligne_souhaite
        self.condition = condition
        self.font = font_params

        self.couleur_fleche_ajoutee = (0, 255, 0)
        self.couleur_fleche_enlevee = (0, 0, 255)

    def dessiner_modification(self, screen):
        """
        Dessine une flèche verte sur l'écran donné entre les deux attributs
        à modifier.
        """
        pygame.draw.line(screen, self.couleur_fleche_ajoutee, self.debut_ligne, self.fin_ligne_souhaite, WIDTH_LIGNES)
        if self.ancien_fin_ligne is not None: # dans le cas où il y a un ancien ligne
            pygame.draw.line(screen, self.couleur_fleche_enlevee, self.debut_ligne, self.ancien_fin_ligne, WIDTH_LIGNES)

        if self.condition is not None: # on recopie la condition
            text = self.font.render(str(self.condition), True, (0, 0, 0))
            coords = centrer_objet(self.debut_ligne, (text.get_rect().width, text.get_rect().height), (self.fin_ligne_souhaite[0]-self.debut_ligne[0], self.fin_ligne_souhaite[1]-self.debut_ligne[1]))
            screen.blit(text, coords)

    def effectuer_modification(self):
        """
        Enregistre la modification sur l'arbre.
        """
        if type(self.attribut_depart) is type(Etat): # Cas où on modifie le cablâge d'un état
            self.attribut_depart.action_associee = self.attribut_fin
            return

        if self.condition is None:
            self.attribut_depart.list_actions_suivantes = self.attribut_fin
        else:
            self.attribut_depart.list_actions_suivantes[self.condition] = self.attribut_fin
