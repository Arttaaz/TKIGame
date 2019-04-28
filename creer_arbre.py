"""
Contient de quoi créer des comportement d'unités (des arbres).
"""


from arbre import *
from target import Target

def bronzer(param):
    pass
def creer_unite(unit, id):
    if id == 1:
        ### Code de l'état Idle
        bronzer1 = Action('Bronzer', bronzer, ['Crème'], None)
        selectionner_cible1 = Action('Sélectionner cible', unit.select_target, [Target.NEAREST_ENEMY], bronzer1)
        
        idle = Etat(selectionner_cible1, 'Idle')

        ### Code de l'état Attaquer cible
        attaquer1 = Action('Attaquer', unit.shoot, ["Ma Cible"], None)
        
        attaquer_cible = Etat(attaquer1, 'Attaquer')

        return Arbre([idle, attaquer_cible], idle, "Unité basique")
    return creer_unite_attaque(unit)
def creer_unite_attaque(unit):
    """
    Créé une unité d'attaque classique.
    """
    ### Code de l'état Idle
    changer_etat1 = Action('Changer état', unit.set_tree_state,['Attaquer'], None)
    selectionner_cible1 = Action('Sélectionner cible', unit.select_target, [Target.NEAREST_ENEMY], changer_etat1)
    idle = Etat(selectionner_cible1, 'Idle')

    ### Code de l'état Attaquer cible
    marcher_vers1 = Action('Marcher vers', unit.move, ["Ma Cible"], None)
    changer_etat2 = Action('Changer état', unit.set_tree_state, ['Idle'], None)

    est_mort1 = Action('Est mort', unit.is_dead, ["Ma Cible"], {"Oui" : changer_etat2})
    attaquer1 = Action('Attaquer', unit.shoot, ["Ma Cible"], est_mort1)
    est_a_portee1 = Action('Est à portée', unit.est_a_portee, ["Ma Cible"], {"Oui" : attaquer1, "Non" : marcher_vers1})
    attaquer_cible = Etat(est_a_portee1, 'Attaquer')

    ### Code de l'état Soigner cible
    soigner1 = Action('Soigner', unit.heal, ["Ma Cible"], None)
    marcher_vers2 = Action('Marcher vers', unit.move, ["Ma Cible"], None)
    est_a_portee2 = Action('Est à portée', unit.est_a_portee, ["Ma Cible"], {"Oui" : soigner1, "Non" : marcher_vers2})
    soigner_cible = Etat(est_a_portee2, 'Soigner')

    return Arbre([idle, attaquer_cible, soigner_cible], idle, "Unité basique")
