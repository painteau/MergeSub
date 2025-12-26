# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [2.0.0] - 2025-12-26

### Ajouté
- Architecture orientée objet avec classe `SubtitleMerger`
- Configuration externalisée dans `config.json`
- Fichier `requirements.txt` pour la gestion des dépendances
- Documentation complète avec README.md
- Type hints complets pour toutes les méthodes
- Docstrings détaillées pour toutes les fonctions
- Validation du répertoire média au démarrage
- Statistiques d'exécution (processed, merged, skipped, errors)
- Résumé détaillé en fin d'exécution
- Gestion des interruptions clavier (Ctrl+C)
- Support des variantes majuscules/minuscules pour les extensions
- Méthode `_find_primary_subtitle()` dédiée
- Méthode `_find_video_files()` optimisée
- Méthode `_validate_media_directory()` pour la validation
- Méthode `_print_summary()` pour les statistiques
- .gitignore amélioré pour Python et IDE
- Fichier LICENSE (MIT)
- Ce fichier CHANGELOG.md

### Modifié
- Migration complète de `os.path` vers `pathlib`
- Recherche de fichiers optimisée : 1 glob au lieu de 4 boucles imbriquées
- Logging structuré avec niveaux appropriés (DEBUG/INFO/WARNING/ERROR)
- Gestion d'erreurs améliorée avec continuation en cas d'échec
- Messages de log plus informatifs et structurés
- Séparation des responsabilités en méthodes privées

### Supprimé
- Fonction `clear_console()` inutilisée
- Magic strings hardcodées (déplacées vers config.json)
- Double appel à `os.path.splitext` redondant
- Boucles imbriquées inefficaces pour la recherche de fichiers
- Mélange incohérent de `os.path` et `pathlib`

### Corrigé
- Condition complexe ligne 52 simplifiée
- Gestion des fichiers .srt génériques vs spécifiques aux langues
- Accès réseau non optimisé avec gestion d'erreurs appropriée
- Logging incohérent (uniformisation)

## [1.0.0] - Date inconnue

### Ajouté
- Version initiale du script
- Recherche récursive de fichiers vidéo
- Fusion de sous-titres coréens et primaires
- Logging basique avec rotation
- Support des extensions .mp4, .mkv, .avi, .mov
- Priorité de sélection des sous-titres : .srt > .en.srt > .fr.srt

---

## Types de modifications

- **Ajouté** : pour les nouvelles fonctionnalités
- **Modifié** : pour les changements aux fonctionnalités existantes
- **Déprécié** : pour les fonctionnalités bientôt supprimées
- **Supprimé** : pour les fonctionnalités supprimées
- **Corrigé** : pour les corrections de bugs
- **Sécurité** : en cas de vulnérabilités
