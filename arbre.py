"""
Contient l'objet Arbre qui décrit le
cablâge d'une unité.

Contient les objets secondaires, qui sont utilisés
par l'arbre.

Un arbre est composé d'un ensemble d'état désignant un comportement
général. Puis chaque état est lié à une action à exécuté, et chaque actions
pointent vers d'autres actions à exécutées après leur exécutions.
"""

class Arbre:
    """
    Objet principal permettant
    la description d'un cablâge.
    """
    def __init__(self, list_etats, etat_initial, nom_arbre="NOM ARBRE"):
        """
        Initialise l'état courant de l'arbre (état qui sera exécuté
        lors de l'évaluation de l'arbre).
        Récupère aussi la liste des états possibles de l'arbre.
        """
        self.nom_arbre = nom_arbre
        self.list_etats = list_etats
        self.etat_courant = etat_initial

    def eval(self):
        """
        Execute l'état courant.
        """
        self.etat_courant.execute()

    def __str__(self):
        """
        Description textuelle de l'objet.
        """
        desc = "Etat courant : {}\n".format(self.etat_courant.nom_etat)
        for etat in self.list_etats:
            desc += str(etat) + "\n"
        return desc


class Etat:
    """
    Représente un état.
    Un état est le premier objet
    sous la racine de l'arbre. Il
    définit un comportement général.
    A un état est associée une action
    qui sera lancée lorsque l'arbre sera
    dans cet état.
    """
    def __init__(self, action_associee, nom_etat="Idle"):
        """
        Possède un nom et une action,
        l'action sera celle exécutée lorsque l'état
        est actif.
        """
        self.nom_etat = nom_etat
        self.action_associee = action_associee

    def execute(self):
        """
        Fonction activant l'état, exécute la première action.
        """
        self.action_associee.execute()

    def __str__(self):
        """
        Description de l'objet.
        """
        return "***\n[{}]\n".format(self.nom_etat) + str(self.action_associee) + "\n***\n"


class Action:
    """
    Objet effectuant quelque chose.
    Une action possède une fonction, des parametres,
    et peut pointer vers une ou plusieurs fonctions.
    Elle se termine par l'exécution d'une fonction parmi
    les celles qu'elle connait, ou par rien si c'est la fin de l'arbre.
    """
    def __init__(self, nom, action_associee, params_action_associee, list_actions_suivantes):
        """
        Si list_actions_suivantes vaut None, alors c'est que c'est la fin de l'arbre.
        """
        self.nom = nom
        self.action_associee = action_associee
        self.params_action_associee = params_action_associee
        self.list_actions_suivantes = list_actions_suivantes

    def execute():
        """
        Lance l'action associée, et réagit en fonction.
        En fonction de ce que renvoie l'action, on execute
        la bonne action suivante.
        L'action suivante est choisie par la place qu'elle
        a dans la liste 'list_actions_suivantes'. Le numéro
        de la place est le numéro que renvoie l'action
        exécutée ici ('action_associée').
        """
        numero_action_suivante = self.action_associee(self.params)
        if list_actions_suivantes is not None:
            self.list_actions_suivantes[numero_action_suivante].execute() # exécute l'action suivante

    def __str__(self):
        """
        Description de l'objet.
        """
        desc = "{} ({}) -> (".format(self.nom, self.params_action_associee)
        if self.list_actions_suivantes is not None:
            for action in self.list_actions_suivantes:
                desc += "[ " + str(action) + "]"
        return desc + ")"



def action_inutile(params_inutiles):
    """
    Fonction action de test.
    """
    pass


if __name__ == "__main__":
    marcher_vers = Action('marcher_vers', action_inutile, None, None)
    attaquer = Action('attaquer', action_inutile, None, None)
    decider_quelque_chose = Action('decider_quelque_chose', action_inutile, None, [marcher_vers, attaquer])
    idle = Etat(marcher_vers, 'Idle')
    faire_quelque_chose = Etat(decider_quelque_chose, 'Faire quelque chose')
    arbre = Arbre([idle, faire_quelque_chose], idle)

    print(arbre)
