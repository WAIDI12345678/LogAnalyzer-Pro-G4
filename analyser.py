#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
from collections import Counter

def analyser_logs(chemin_source, niveau_filtre="ALL"):
    stats = {"total": 0, "ERROR": 0, "WARN": 0, "INFO": 0}
    erreurs = []
    fichiers_lus = []

    # Chercher les fichiers .log en chemin absolu
    chemin_abs = os.path.abspath(chemin_source)
    fichiers = glob.glob(os.path.join(chemin_abs, "*.log"))
    
    for f_path in fichiers:
        fichiers_lus.append(os.path.basename(f_path))
        with open(f_path, 'r', encoding='utf-8') as f:
            for ligne in f:
                stats["total"] += 1
                parts = ligne.split()
                if len(parts) >= 3:
                    lvl = parts[2]  # Récupère le niveau (INFO, ERROR...)
                    if lvl in stats:
                        stats[lvl] += 1
                    
                    # Filtrage pour le Top 5 des erreurs
                    if lvl == "ERROR":
                        erreurs.append(" ".join(parts[3:]))

    # Calcul du Top 5
    top5 = Counter(erreurs).most_common(5)
    
    # Filtrer les stats selon le niveau demandé pour le rapport final
    if niveau_filtre != "ALL":
        print(f"Filtrage activé : {niveau_filtre} uniquement.")
        
    return stats, top5, fichiers_lus