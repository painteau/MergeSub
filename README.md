# MergeSub - Automatic Subtitle Merger

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](CHANGELOG.md)

Outil Python pour fusionner automatiquement des sous-titres coréens avec des sous-titres primaires afin de créer des fichiers de sous-titres bilingues.

## 📑 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Utilisation](#-utilisation)
- [Exemple de sortie](#-exemple-de-sortie)
- [Structure du projet](#-structure-du-projet)
- [Optimisations](#-optimisations-implémentées)
- [Dépannage](#-dépannage)
- [Changelog](#-changelog)
- [Licence](#-licence)
- [Contribution](#-contribution)

## 🚀 Fonctionnalités

- **Recherche récursive** de fichiers vidéo dans un répertoire
- **Détection intelligente** des sous-titres avec priorités configurables
- **Fusion automatique** de sous-titres coréens et primaires
- **Configuration externalisée** via fichier JSON
- **Logging détaillé** avec rotation de fichiers
- **Statistiques d'exécution** en fin de traitement
- **Gestion d'erreurs robuste** pour les accès réseau

## 📋 Prérequis

- Python 3.7+
- Module `srtmerge`

## 📦 Installation

1. **Cloner le dépôt** (ou télécharger les fichiers)
   ```bash
   git clone https://github.com/painteau/MergeSub.git
   cd MergeSub
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer le script**
   ```bash
   # Modifier config.json selon vos besoins
   nano config.json
   ```

4. **Lancer le script**
   ```bash
   python MergeSub.py
   ```

## ⚙️ Configuration

Créez ou modifiez le fichier `config.json` :

```json
{
  "media_directory": "\\\\192.168.1.100\\media\\TV",
  "video_extensions": [".mp4", ".mkv", ".avi", ".mov"],
  "subtitle_priorities": [".srt", ".en.srt", ".fr.srt"],
  "korean_subtitle_extension": ".ko.srt",
  "output_subtitle_extension": ".yo.srt",
  "excluded_subtitle_patterns": [".en.srt", ".fr.srt", ".ko.srt", ".yo.srt"],
  "log_file": "activity.log",
  "log_max_size": 1000000,
  "log_backup_count": 1
}
```

### Paramètres de configuration

| Paramètre | Description |
|-----------|-------------|
| `media_directory` | Répertoire racine contenant les vidéos |
| `video_extensions` | Extensions de fichiers vidéo à traiter |
| `subtitle_priorities` | Ordre de priorité pour les sous-titres primaires |
| `korean_subtitle_extension` | Extension des sous-titres coréens |
| `output_subtitle_extension` | Extension des sous-titres fusionnés |
| `excluded_subtitle_patterns` | Patterns de sous-titres à exclure |
| `log_file` | Nom du fichier de log |
| `log_max_size` | Taille max du log avant rotation (bytes) |
| `log_backup_count` | Nombre de fichiers de log à conserver |

## 🎯 Utilisation

```bash
python MergeSub.py
```

Le script va :
1. Valider le répertoire média configuré
2. Rechercher tous les fichiers vidéo
3. Pour chaque vidéo :
   - Chercher les sous-titres primaires (priorité : .srt > .en.srt > .fr.srt)
   - Chercher les sous-titres coréens (.ko.srt)
   - Fusionner les deux si les sous-titres de sortie (.yo.srt) n'existent pas
4. Afficher un résumé des opérations

## 📊 Exemple de sortie

```
2025-12-26 10:00:00 :: INFO :: 🚀 MergeSub - Starting subtitle merger
2025-12-26 10:00:01 :: INFO :: Searching for video files in: \\192.168.1.100\media\TV
2025-12-26 10:00:05 :: INFO :: Total video files found: 150
==========================================================================================
2025-12-26 10:00:05 :: INFO :: Processing: Movie.Name.S01E01.mkv
2025-12-26 10:00:05 :: INFO :: Primary subtitle: Movie.Name.S01E01.en.srt
2025-12-26 10:00:05 :: INFO :: Korean subtitle: Movie.Name.S01E01.ko.srt
2025-12-26 10:00:05 :: INFO :: Merging: Movie.Name.S01E01.en.srt + Movie.Name.S01E01.ko.srt → Movie.Name.S01E01.yo.srt
2025-12-26 10:00:06 :: INFO :: ✓ Successfully created: Movie.Name.S01E01.yo.srt
==========================================================================================
2025-12-26 10:15:30 :: INFO :: 📊 SUMMARY
2025-12-26 10:15:30 :: INFO ::   Videos processed: 150
2025-12-26 10:15:30 :: INFO ::   Subtitles merged: 42
2025-12-26 10:15:30 :: INFO ::   Files skipped: 105
2025-12-26 10:15:30 :: INFO ::   Errors: 3
==========================================================================================
2025-12-26 10:15:30 :: INFO :: ✓ MergeSub completed
```

## 📁 Structure du projet

```
MergeSub/
├── MergeSub.py           # Script principal (classe SubtitleMerger)
├── config.json           # Configuration externalisée
├── requirements.txt      # Dépendances Python
├── README.md             # Documentation (ce fichier)
├── CHANGELOG.md          # Historique des versions
├── LICENSE               # Licence MIT
├── .gitignore            # Fichiers à ignorer par Git
└── activity.log          # Logs d'exécution (généré automatiquement)
```

### Fichiers principaux

| Fichier | Description |
|---------|-------------|
| `MergeSub.py` | Script principal avec architecture OOP |
| `config.json` | Configuration : chemins, extensions, priorités |
| `requirements.txt` | Dépendances : `srtmerge>=0.1.0` |
| `activity.log` | Logs d'exécution avec rotation (1 MB max) |

## 🔧 Optimisations implémentées

### Performance
- ✅ Utilisation exclusive de `pathlib` (au lieu de `os.path`)
- ✅ Recherche optimisée : glob unique au lieu de boucles imbriquées
- ✅ Gestion intelligente des variantes majuscules/minuscules

### Architecture
- ✅ Architecture orientée objet avec classe `SubtitleMerger`
- ✅ Séparation des responsabilités (méthodes privées dédiées)
- ✅ Configuration externalisée (JSON)
- ✅ Type hints pour meilleure maintenabilité

### Robustesse
- ✅ Validation du répertoire média
- ✅ Gestion d'erreurs par fichier (continue si erreur)
- ✅ Gestion des interruptions clavier (Ctrl+C)
- ✅ Messages d'erreur détaillés

### Code Quality
- ✅ Docstrings complètes
- ✅ Suppression des magic strings (tout en config)
- ✅ Logging structuré avec niveaux appropriés
- ✅ Statistiques d'exécution

## 📝 Logs

Les logs sont enregistrés dans `activity.log` avec rotation automatique :
- Taille maximale : 1 MB (configurable)
- Fichiers conservés : 1 backup (configurable)
- Niveaux : DEBUG (fichier), INFO (console)

## 🆘 Dépannage

### "Configuration file not found"
Créez le fichier `config.json` dans le même répertoire que le script.

### "Media directory does not exist"
Vérifiez que le chemin réseau est accessible et correctement formaté dans `config.json`.

### Pas de sous-titres fusionnés
Vérifiez que :
- Les sous-titres primaires existent (.srt, .en.srt, ou .fr.srt)
- Les sous-titres coréens existent (.ko.srt)
- Les sous-titres de sortie n'existent pas déjà (.yo.srt)

## 📋 Changelog

Toutes les modifications notables sont documentées dans [CHANGELOG.md](CHANGELOG.md).

### Version actuelle : 2.0.0

Refonte majeure avec :
- Architecture orientée objet
- Configuration externalisée
- Optimisations de performance
- Gestion d'erreurs robuste
- Documentation complète

Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique complet.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

**En résumé** : Vous êtes libre d'utiliser, modifier et distribuer ce logiciel, tant que vous conservez la notice de copyright.

## 🤝 Contribution

Les contributions sont les bienvenues !

### Comment contribuer

1. **Fork** le projet
2. **Créer** une branche (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Rapporter un bug

Ouvrez une [issue](https://github.com/painteau/MergeSub/issues) avec :
- Description du problème
- Étapes pour reproduire
- Comportement attendu vs comportement actuel
- Logs pertinents (extraits de `activity.log`)

---

**Développé avec ❤️ pour la communauté des sous-titres bilingues**
