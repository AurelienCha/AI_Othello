# Reversi

REversi est un Jeu qui se joue à deux dont le but est de capturer le plus de pion possible.

Le jeu est présenté avec trois AI différentes, l'une avec une recherche aléatoire, l'une avec l'agorithm MinMax et l'une implemente par JOSEGALARZE.


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
Le jeu en mode recherche se lance comme ceci:
```bash
poetry run python main.py 
```

Une fois lancé, vous pouvez jouer vous même en encodant la position du pion dans le terminal; ou selectionner le type d'IA à utiliser.




