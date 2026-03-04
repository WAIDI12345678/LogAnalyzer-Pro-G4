#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import platform
import os

def generer_json(stats, top5, fichiers, source):
    data = {
        "metadata": {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "utilisateur": os.environ.get('USER', os.environ.get('USERNAME', 'Inconnu')),
            "os": platform.system(),
            "source": os.path.abspath(source)
        },
        "statistiques": {
            "total_lignes": stats["total"],
            "par_niveau": {
                "ERROR": stats["ERROR"],
                "WARN": stats["WARN"],
                "INFO": stats["INFO"]
            },
            "top5_erreurs": top5
        },
        "fichiers_traites": fichiers
    }
    
    nom_fichier = f"rapport_{datetime.date.today()}.json"
    chemin_complet = os.path.join(os.getcwd(), nom_fichier)
    
    with open(chemin_complet, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    return chemin_complet