# Reversi

Reversi est un Jeu qui se joue à deux dont le but est de capturer le plus de pion possible.

Le jeu est présenté avec deux AI différentes, l'une avec une recherche aléatoire et l'une avec l'agorithm MinMax (mais certains paramètres sont optionnel).


## Installation

Pour installer l'application, commencez par copier le dépot du jeu,
soit en recupérant l'archive zip depuis github, soit à l'aide de l'outil git:
```
git clone https://github.com/AurelienCha/AI_Othello.git
```

Après avoir installé python et poetry, installez les dépendances du projet:

```bash
poetry install
```

## Utilisation

Vous pouvez ensuite lancer le jeu dans l'environnement virtuel nouvellement créé.
Le jeu en mode ia vs humain se lance comme ceci:
```bash
poetry run python main.py 5 H
```
Le programme a besoind e 2 arguments : Joueur_1 et joueur_2 qui correspondent aux parametres des joueurs 
 - 'H' : Humain
 - 'R' : aléatoire
 - '<depth>' : AI où le "depth" représente la profondeur de l'arbre avec les paramètres optionnels : 
               - '+' pour augmenter la profondeur a la fin
 
               - 'p' pour enlever le pruning
 
               - 'h' pour enlever l'heuristic
 
               - 'min' or 'max' pour specifier la strategie de capture ( par defaut : 'hybrid' min au debut, max à la fin)

Pour lancer l'algorithm random contre une ia de profondeur 4 avec la profondeur qui augmente a la fin sans pruning ni heuristique et minimisant le nombre de pion capturer :
```bash
poetry run python main.py R 4+PHmin
```

Une fois lancé, vous pouvez jouer vous même en encodant la position du pion dans le terminal; ou selectionner le type d'IA à utiliser.




