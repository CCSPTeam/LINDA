# Lightweight Individual Network Detector And Anihilator

Ce projet met en place un système de tourelle bi-axes connectée exploitant un serveur Web pour l'acquisition des cibles à pointer. La tourelle est équipée d'un laser, ainsi que d'un dispositif de propulsion motorisé permettant de cibler un individu. Ce système est couplé à un algorithme de detectiion des visages et d'approximation des distances décentralisé par le concours d'un serveur Web.

## Serveur Web

Un client se connecte au serveur qui accepte les requêtes GET pour l'affichage de l'interface Web. Le client capture une image sur son navigateur qui est envoyé au serveur par une requête POST. 

## Module IA

La détection d'un visage dans l'image se fait par la méthode des Cascades de Haar pré-implémentées dans OpenCV. Cet algorithme renvoit la position ansi que les dimensions en pixels du visage dans l'image. A l'aide de règles trigonométriques élémentaires, les mesures extraites du module sont converties en dimensions réelles qui pourront être traitées par l'Arduino.

## Arduino

Le serveur communique avec la carte Arduino à l'aide d'une liaison série par l'intermédiaire d'un câble USB. Le programme Arduino reçoit par ce biais les coordonnées cartésiennes à cibler grâce à la tourelle. Les consignes en position sont converties en consignes angulaires pour les servomoteurs. Une fois la position atteinte, une commande en échelon est envoyée au moteur à courant continu par l'intermédiaire d'un pont en H pour propulser la fléchette. 

## Environnement

* [OpenCV](https://opencv.org) - Framework de traitement de l'image
* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - Framework pour serveur Web en Python
* [Pyserial](https://pythonhosted.org/pyserial/) - Liaison série vers l'Arduino

## Auteurs

* **Pierre Cabanis** - [Github Page](https://github.com/PierreCabanis)

* **Steeven Janny** - [Github Page](https://github.com/SteevenJ7)

* **Claire Pillet** - [Github Page](https://github.com/ClairePillet)

* **Cyril Reymond** - [Github Page](https://github.com/creymond)
