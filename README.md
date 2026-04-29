# House Price Predictor : Pipeline End-to-End Snowflake & ML

Ce projet présente une solution complète de prédiction immobilière utilisant l'architecture Medallion sur Snowflake. Il intègre l'ingestion de données brutes, leur transformation via Snowpark, l'entraînement d'un modèle RandomForest optimisé et le déploiement d'une application interactive via Streamlit.

---

## 1. Analyse des Performances du Modèle

Le modèle final repose sur l'algorithme **RandomForestRegressor**, choisi pour sa robustesse face aux données tabulaires et sa capacité à capturer des relations non-linéaires.

### Métriques de Validation
Après une phase d'optimisation par recherche de grille (**Grid Search**), le modèle a été évalué sur les métriques suivantes :

* **MAE (Mean Absolute Error)** : Calcule l'erreur moyenne en dollars. Le modèle affiche une précision accrue sur les biens de gamme moyenne.
* **RMSE (Root Mean Squared Error)** : Indique la stabilité du modèle face aux valeurs aberrantes (prix très élevés).
* **R² Score** : Confirme que le modèle explique une part significative de la variance des prix immobiliers du dataset.

[image-tag: code-generated-image-0-1777495387724411692]
*Figure 1 : Corrélation entre les prix réels et les prix prédits par le modèle.*

---

## 2. Analyse des Propriétés et Influence sur le Prix

L'étude des caractéristiques (features) via le modèle montre que certains facteurs sont prédominants dans l'estimation financière.

### Hiérarchie de l'Importance
1.  **Surface (AREA)** : C'est le moteur principal du prix.
2.  **Climatisation (AIRCONDITIONING)** : Variable de confort majeure ayant un impact significatif sur la valorisation.
3.  **Localisation (PREFAREA)** : Le fait d'être situé dans une zone privilégiée agit comme un multiplicateur de valeur.
4.  **Commodités** : Le nombre de salles de bain et de places de parking complètent l'ajustement du prix.

[image-tag: code-generated-image-1-1777495387724417542]
*Figure 2 : Importance relative des variables dans la décision du modèle.*

---

## 3. Architecture Technique et Pipeline

Le projet suit une structure de données organisée en couches au sein de Snowflake :

### Architecture Medallion
* **Bronze (Raw)** : Données brutes importées depuis un stage S3 au format JSON.
* **Silver (Structured)** : Transformation via Snowpark. Conversion des types (chaînes "yes/no" en Boolean), nettoyage des valeurs manquantes et calcul de la variable `PRICE_PER_M2`.
* **Gold (Inference)** : Modèle stocké dans le **Snowflake Model Registry** (version v2) et utilisé pour générer des prédictions en temps réel.

### Pile Technologique
* **Environnement** : Python 3.11
* **Framework ML** : Scikit-Learn (RandomForest)
* **Interface** : Streamlit (Intégré à Snowflake)
* **Gestion de données** : Snowflake Snowpark & Snowflake ML Library

---

## 4. Utilisation de l'Application

L'interface Streamlit permet une estimation immédiate en saisissant :
* Les dimensions de la maison (Surface, Étages).
* La configuration (Chambres, Salles de bain).
* Les options de confort (Climatisation, Chauffage, Parking).

Le modèle est chargé via `st.cache_resource` pour garantir une réponse instantanée sans rechargement du registre à chaque prédiction.

---

## 5. Perspectives d'Amélioration
* Intégration de modèles de Gradient Boosting (XGBoost) pour réduire davantage la MAE.
* Ajout de données externes (proximité des écoles, commerces).
* Analyse temporelle pour intégrer les fluctuations du marché immobilier.
