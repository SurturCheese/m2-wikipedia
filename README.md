# m2-wikipedia

On utilise les dumps suivants (lien de téléchargement direct) : 

https://dumps.wikimedia.org/enwiki/20231101/enwiki-20231101-pages-articles-multistream.xml.bz2

https://dumps.wikimedia.org/enwiki/20231101/enwiki-20231101-pages-articles-multistream-index.txt.bz2

Lien de la présentation sur Google Slides : 

https://docs.google.com/presentation/d/1w3oenm_fEwmVxAVO64WVFI0U7ezsdlDVOIkO2tqmeK0/edit?usp=sharing

## Sujet : 

Le jeu de données Wikipedia (Anglais, texte, 20Go) est intéressant et utile pour sa variété, son utilité sociale-intellectuelle
et sa structure XML. Ce projet vise à définir, implémenter, documenter et mesurer la performance d’opérations de
requêtes et analyse de données sur Wikipedia. Il faut:

• ❌ Définir un ensemble, ou mieux un langage, de requêtes sur ces données. Définir aussi des analyses (optionnel :
de l’apprentissage machine) avec des résultats signifiants pour leur domaine d’application.

• ❌ Implanter une ou plusieurs versions Spark ou autres de ces opérations.

• ❌ Proposer des exemples signifiants pour des domaines d’application connus : analyse de sentiment (statique ),
jointures limitées, sélection de sous-ensembles sur un sujet, analyse de la langue naturelle etc.

• ❌ Mesurer les vitesses de traitement en fonction de : nb de cœurs, taille des données, type d’opération,
(optionnel : multi-nœud et/ou GPU). Comparer les 2+ implantations. Extrapoler sur de très grandes tailles.

• ❌ Optionnel : définir, implanter et tester une version avec chiffrement homomorphe où le serveur stocke le XML
Wikipedia chiffré par morceaux et exécute les recherches (limitées en variété) sur ce contenu chiffré pour
rendre un résultat chiffré que seul l’utilisateur peut déchiffrer.

• ❌ Livrables: un document latex/Word en format IEEE à deux colonnes (guide utilisateur, documentation
développeur, exemples de requêtes, analyse des performances), fichiers de test, données sur la performance
(tableaux csv avec explication des champs), code source.


## Install :
    • installez python
    • installez pip
    • recuperez le projet sur git : https://github.com/SurturCheese/m2-wikipedia/tree/WikiSearch
    • placez vous dans le dossier m2-wikipedia
    • checkout la branche Wikisearch : git checkout WikiSearch
    • créez un virtual env : python -m venv /*nomVirtualEnv*/
    • activez le virtual env : /*nomVirtualEnv*/ +\Scripts\activate
    • executez le fichier requirements.txt : pip install -r requirements.txt

## exécution :
    • python wikiSearch\manage.py runserver
    
## stop :
    • Ctrl + c
    • deactivate

    