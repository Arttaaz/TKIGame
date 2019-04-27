"""
Contient de quoi créer des comportement d'unités (des arbres).
"""


from arbre import *
from target import Target
def creer_unite_attaque(unit):
    """
    Créé une unité d'attaque classique.
    """
    ### Code de l'état Idle
    changer_etat1 = Action('Changer état', unit.set_tree_state, ["Attaquer cible"], None)
    selectionner_cible1 = Action('Sélectionner cible', unit.select_target, [Target.NEAREST_ENEMY], changer_etat1)
    idle = Etat(selectionner_cible1, 'Idle')

    ### Code de l'état Attaquer cible
    marcher_vers1 = Action('Marcher vers', unit.move, ["Cible courante"], None)
    changer_etat2 = Action('Changer état', unit.set_tree_state, ["Attaquer cible"], None)

    est_mort1 = Action('Est mort', unit.is_dead, ["Cible courante"], {"Oui" : changer_etat2})
    attaquer1 = Action('Attaquer', unit.shoot, ["Cible courante"], est_mort1)
    est_a_portee1 = Action('Est à portée', unit.est_a_portee, ["Cible courante"], {"Oui" : attaquer1, "Non" : marcher_vers1})
    attaquer_cible = Etat(est_a_portee1, 'Attaquer cible')

    ### Code de l'état Soigner cible
    soigner1 = Action('Soigner', action_inutile, ["Cible courante"], None)
    marcher_vers2 = Action('Marcher vers', unit.move, ["Cible courante"], None)
    est_a_portee2 = Action('Est à portée', unit.est_a_portee, ["Cible courante"], {"Oui" : soigner1, "Non" : marcher_vers2})
    soigner_cible = Etat(est_a_portee2, 'Soigner cible')

    return Arbre([idle, attaquer_cible, soigner_cible], idle, "Unité basique")
