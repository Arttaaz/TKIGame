"""
Contient de quoi créer des comportement d'unités (des arbres).
"""


from arbre import *


def creer_unite_attaque():
    """
    Créé une unité d'attaque classique.
    """
    ### Code de l'état Idle
    changer_etat1 = Action('Changer état', action_inutile, ["Attaquer cible"], None)
    selectionner_cible1 = Action('Sélectionner cible', action_inutile, ["Plus proche ennemi"], changer_etat1)
    idle = Etat(selectionner_cible1, 'Idle')

    ### Code de l'état Attaquer cible
    marcher_vers1 = Action('Marcher vers', action_inutile, ["Cible courante"], None)
    changer_etat2 = Action('Changer état', action_inutile, ["Idle"], None)
    rien_faire1 = Action('Rien changer', action_inutile, None, None)
    est_mort1 = Action('Est mort', action_inutile, ["Cible courante"], {"Oui" : changer_etat2})
    attaquer1 = Action('Attaquer', action_inutile, ["Cible courante"], est_mort1)
    est_a_portee1 = Action('Est à portée', action_inutile, ["Cible courante"], {"Oui" : attaquer1, "Non" : marcher_vers1})
    attaquer_cible = Etat(est_a_portee1, 'Attaquer cible')

    ### Code de l'état Soigner cible
    soigner1 = Action('Soigner', action_inutile, ["Cible courante"], None)
    marcher_vers2 = Action('Marcher vers', action_inutile, ["Cible courante"], None)
    est_a_portee2 = Action('Est à portée', action_inutile, ["Cible courante"], {"Oui" : soigner1, "Non" : marcher_vers2})
    soigner_cible = Etat(est_a_portee2, 'Soigner cible')

    return Arbre([idle, attaquer_cible, soigner_cible], idle, "Unité basique")
