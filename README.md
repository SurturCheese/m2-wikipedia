# m2-wikipedia

Les micros datasets sont à télécharger et à extraire dans `wikiSearch/search/data`

https://www.dropbox.com/scl/fo/ui38w0l8iy4wy3pz0jini/h?rlkey=pwc9tgtgxxz1am7natkmrz9yh&dl=0

## Lancement rapide:
    git clone https://github.com/SurturCheese/m2-wikipedia
    docker compose up

## Lancement via virtualenv:
- Installer Python

- Récuperer le projet sur git : `git clone https://github.com/SurturCheese/m2-wikipedia`

- Créer un virtual env : `python -m venv <nomVirtualEnv>`

- Activer le virtual env : 
    - Pour Windows : `<nomVirtualEnv>\Scripts\activate.ps1`
    - Pour Linux/Mac : `source <nomVirtualEnv>/Scripts/activate`

- Installer les bibliothèques nécessaire : `pip install -r requirements.txt`

- Lancer avec : `python wikiSearch/manage.py runserver`

## Interface :

    http://localhost:8000

## Arrêt :
- Arrêter le serveur : `CTRL + C`
    
- Sortir du virtual env : `deactivate`

## Résultat :

Le temps des résultats sont dans result.json.
Le format est : 

`{"time": <temps d'exécution en secondes>, "query": <Requête lancée>}`

Les résultats sont enregistrés dans `output_result.txt`.

## Source des datasets :

https://dumps.wikimedia.org/enwiki/20231101/enwiki-20231101-pages-articles-multistream.xml.bz2
