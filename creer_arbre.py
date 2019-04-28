"""
Contient de quoi créer des comportement d'unités (des arbres).
"""


from arbre import *
from target import Target

def bronzer(param):
    pass

def est_mort(unit,oui, non):
    return Action('Est mort', unit.is_dead, ["Ma Cible"], {"Oui" : oui, "Non" : non})
def attaquer(unit, suivant, mod = True):
    return Action('Attaquer', unit.shoot, ["Ma Cible"], suivant, mod)
def soigner(unit, suivant):
    return Action('Soigner', unit.heal, ["Ma Cible"], suivant)
def marcher(unit, suivant):
    return Action('Marcher vers', unit.move, ["Ma Cible"], suivant)
def bronzer_act(suiv):
    return Action('Bronzer', bronzer, ['Crème'], suiv)
def select_cible(unit, cible, suiv, mod = True):
    return Action('Sélectionner cible', unit.select_target, [cible], suiv, mod)
def changer_etat(unit, etat, suiv):
    return Action('Changer état', unit.set_tree_state, [etat], suiv)
def subit(unit, oui, non):
    return Action('Menacé ?', unit.subit_attaque, None, {"Oui" : oui, "Non" : non})
def est_a_portee(unit, oui, non):
    return Action('Est à portée', unit.est_a_portee, ["Ma Cible"], {"Oui" : oui, "Non" : non})
def creer_unite(unit, id):
    if id == 1:
        ### Code de l'état Idle
        bronzer1 = Action('Bronzer', bronzer, ['Crème'], None)
        selectionner_cible1 = Action('Sélectionner cible', unit.select_target, [Target.NEAREST_ENEMY], bronzer1)
        
        idle = Etat(selectionner_cible1, 'Idle')

        ### Code de l'état Attaquer cible
        attaquer1 = Action('Attaquer', unit.shoot, ["Ma Cible"], bronzer1)
        
        attaquer_cible = Etat(attaquer1, 'Attaquer')

        return Arbre([idle, attaquer_cible], idle, "Crabe vacancier")
    if id == 2:
        ### Code de l'état Idle
        changer_eta = changer_etat(unit, "Attaquer", None)
        selectionner_cible1 = Action('Sélectionner cible', unit.select_target, [Target.NEAREST_ENEMY], changer_eta)
        
        idle = Etat(selectionner_cible1, 'Idle')

        ### Code de l'état Attaquer
        changer_et = changer_etat(unit, "Idle", None)
        march = marcher(unit, None)
        attaq = attaquer(unit, None)
        est_a_portee1 = est_a_portee(unit, attaq, march)
        est_m = est_mort(unit, changer_et, est_a_portee1)
        sel_cible = select_cible(unit, Target.THREAT, est_a_portee1)
        subit_attaque = subit(unit, sel_cible, est_m)
        attaquer_cible = Etat(subit_attaque, 'Attaquer')

        return Arbre([idle, attaquer_cible], idle, "BerserKrabe")
    if id == 3:

        ### Code de l'état Attaquer
        attaq = attaquer(unit, None)
        sel_cible = select_cible(unit, Target.NEAREST_ENEMY, attaq, False)
        attaquer_cible = Etat(sel_cible, 'Attaquer', False)

        return Arbre([attaquer_cible], attaquer_cible, "Crabe sniper")
    if id == 4:

        soigner1 = soigner(unit, None)
        marcher1 = marcher(unit, None) 
        est_a_portee1 = est_a_portee(unit, soigner1, marcher1)
        sel_cible = select_cible(unit, Target.NEAREST_ALLY, est_a_portee1)
        soin = Etat(sel_cible, 'Soigner')
        
        ### Code de l'état Attaquer
        attaq = attaquer(unit, None)
        sel_cible = select_cible(unit, Target.NEAREST_ENEMY, attaq)
        attaquer_cible = Etat(sel_cible, 'Attaquer')

        return Arbre([attaquer_cible, soin], soin, "Homaropathe")
    if id == 5:
        marcher1 = marcher(unit, None) 
        
        ### Code de l'état Attaquer
        attaq = attaquer(unit, None)
        est_a_portee1 = est_a_portee(unit, attaq, marcher1)
        sel_cible1 = select_cible(unit, Target.THREAT, est_a_portee1)
        sel_cible2 = select_cible(unit, Target.NEAREST_ENEMY, est_a_portee1)
        subit1 = subit(unit, sel_cible1, sel_cible2)
        attaquer_cible = Etat(subit1, 'Attaquer')

        return Arbre([attaquer_cible], attaquer_cible, "Soldat crabe")
        
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
