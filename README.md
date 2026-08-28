# gpx-project

Génère des traces GPX suivant les sentiers réels (pas des lignes droites) à
partir d'une liste de points de passage, via l'API de routing pédestre
d'[OpenRouteService](https://openrouteservice.org/) (profil `foot-hiking`,
qui suit le réseau de sentiers OpenStreetMap).

## Installation

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

1. Créer un compte gratuit sur https://openrouteservice.org/dev/#/signup
   (2000 requêtes/jour offertes)
2. Générer une clé API dans le dashboard
3. `cp .env.example .env` puis coller la clé dans `.env`
4. Charge la variable d'environnement avant de lancer le script :
   ```bash
   export $(cat .env | xargs)   # Linux/macOS
   ```
5. `cp waypoints.example.py waypoints.py` puis renseigne tes propres
   itinéraires dans `waypoints.py`

## Usage

```bash
python generate_hiking_gpx.py
```

Le script lit la liste `TRIPS` de `waypoints.py` (un ou plusieurs itinéraires,
chacun avec un nom, une liste de points de passage et un fichier de sortie),
route entre les points dans l'ordre donné pour chaque itinéraire, et produit
un fichier `.gpx` par itinéraire avec la trace suivant les sentiers réels +
altitude.

## Limites connues

- Le profil `foot-hiking` d'ORS s'appuie sur les données OpenStreetMap :
  fiable sur les GR/GRP balisés, moins bon en haute montagne peu cartographiée
  (toujours vérifier le résultat visuellement avant de
  partir).
- Le quota gratuit ORS est de 2000 requêtes/jour et 40 requêtes/minute.
- Ne jamais committer les fichiers `.env` et `waypoints.py` (déjà dans
  `.gitignore`).
