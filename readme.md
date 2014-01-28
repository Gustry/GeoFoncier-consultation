# Consultation des dossiers GéoFoncier

Plugin QGIS pour la consultation des dossiers GéoFoncier.

English version follows.

# Installation

* Installation manuel : https://github.com/Gustry/GeoFoncier-consultation/archive/master.zip
 * Décompressez l'archive et déplacer le dossier dans votre répertoire des plugins python de QGIS.
 * Démarrer QGIS puis Menu Extension -> Gestionnaire d'extension -> Activez le plugin "Mes dossiers GéoFoncier"

# Utilisation
* Il est nécessaire d'avoir un couple nom d'utilisateur / mot de passe de client GéoFoncier.
 * Pour les tests : clientge / clientge comme nom d'utilisateur et mot de passe.
* Il possible d'ajouter une couche cartographique et une couche aérienne.

# Le projet :
* Code source :
 * https://github.com/Gustry/GeoFoncier-consultation
* Rapport de bugs :
 * https://github.com/Gustry/GeoFoncier-consultation/issues
* Documentation du code :
 * https://qgis.trimaille.eu/geofoncier/

 English short description
==========================
This plugin helps French users to get informations about works made by french licensed surveyors : boundaries for ownership, locations ... A login/password is required.
It is only useful in France for people having access to GéoFoncier with a login and password. For testing, we can use the login/password "clientge". The English's translation is partial because only French people will use this plugin.

This plugins has 3 steps :
* connect with a login/password to GéoFoncier's API
* get all records from the user
* get all details about a record (documents and maps related to this record)

You can add two cartographic layers : OSM and Google