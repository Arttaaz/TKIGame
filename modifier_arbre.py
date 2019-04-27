"""
Permet de modifier un arbre en deux temps :
    - enregistre d'abord la modification en enregistrant l'attribut
    à modifier et l'attribut vers lequel on souhaite qu'il pointe
    - effectue ensuite cette modification

Tout ceci est géré par un objet 'Modification'.
"""

import pygame

from afficher_arbre import centrer_coords

class Modification:
    """
    Enregistre une modification et les effectue.
    """
    def __init__(self, attribut_a_modifier, rect_depart, attribut_souhaite, rect_fin):
        self.attribut_depart = attribut_a_modifier
        self.attribut_fin = attribut_souhaite
        self.rect_depart = rect_depart
        self.rect_fin = rect_fin
        self.couleur_fleche = (0, 255, 0)

    def dessiner_modification(self, screen):
        """
        Dessine une flèche verte sur l'écran donné entre les deux attributs
        à modifier.
        """
        coord_fin_attr = (self.rect_depart.left+self.rect_depart.width//2, self.rect_depart.top+self.rect_depart.height)
        coord_debut_attr = (self.rect_fin.left+self.rect_fin.width//2, self.rect_fin.top)

        pygame.draw.aaline(screen, self.couleur_fleche, coord_fin_attr, coord_debut_attr)


    def effectuer_modification(self):
        """
        Enregistre la modification sur l'arbre.
        """
        self.attribut_depart.action_associee = self.attribut_fin
