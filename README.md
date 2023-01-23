# SMA TP "Vivarium"

Projet réalisé à Polytech dans le cadre d'un TP de Système Multi-Agents.  
Voici le sujet : [Systèmes-Multi-Agents-et-Self-TP-2Bis.pdf](https://github.com/remi-martinez/sma-tp/files/10482898/Systemes-Multi-Agents-et-Self-TP-2Bis.pdf)

![image](https://user-images.githubusercontent.com/64494563/214128998-4d4da657-8035-4ce0-88f1-a3b3cacbb4a6.png)


## Installation

Configurer un nouveau projet avec les dépendances se trouvant dans requirements.txt (créer un venv si nécessaire) :

```bash
python -m venv venv 
venv\Scripts\activate
pip install -r requirements.txt
```
Lancer la simulation avec `py main.py` dans un terminal

:warning: Prévoir de côté le gestionnaire des tâches pour kill les processus, au cas où Python plante à cause du deuxième thread (qui peut crash en fermant une fenêtre).  
## Utilisation

La simulation se lance dans une fenêtre et le graphique dans une autre.
Quelques fonctionnalités :
* **Touche R** : remet à zéro la simulation
* **Clic gauche** sur un agent : afficher ses jauges de faim, fatigue, reproduction
* **Clic droit** n'importe où : déselectionner tous les agents



## Informations supplémentaires

* Lorsque l'agent dort, il y a écrit 'Zzz...' au dessus de sa tête
* Lorsque l'agent est à 80% de sa faim, il y a écrit 'AFFAMÉ' au dessus de sa tête
* Un agent qui se reproduit (jauge au max) émet un petit coeur et un deuxième agent du même type apparaît
* Les décomposeurs "grignotent" les cadavres, qui à la fin de la décomposition deviennent des végétaux
* La mort d'un décomposeur entraîne l'apparition d'un végétal
* Légende :  
![image](https://user-images.githubusercontent.com/64494563/214129891-56814f4a-becd-48d3-837d-81bc8f5bca34.png)

