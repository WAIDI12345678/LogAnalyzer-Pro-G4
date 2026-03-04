#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os         
import glob       
import platform   
from collections import Counter 

def obtenir_metadonnees():
    """Récupère l'OS et l'utilisateur actuel via les bibliothèques standard."""
    return {
        "os": platform.system(),
        "utilisateur": os.environ.get('USER') or os.environ.get('USERNAME', 'Inconnu')
    }
def analyser_logs(chemin_source, niveau_filtre="ALL"):
    """
    Scanne le dossier, filtre les messages et calcule les stats.
    """
    # 1. Lister les fichiers .log avec glob [cite: 12, 77]
    pattern = os.path.join(os.path.abspath(chemin_source), "*.log")
    fichiers = glob.glob(pattern)
    
    stats_niveaux = {"INFO": 0, "WARN": 0, "ERROR": 0}
    toutes_les_erreurs = []
    total_lignes = 0
    fichiers_traites = []

    for fichier in fichiers:
        fichiers_traites.append(os.path.abspath(fichier)) # Chemins absolus requis [cite: 24, 108]
        
        with open(fichier, 'r', encoding='utf-8') as f:
            for ligne in f:
                total_lignes += 1
                parties = ligne.strip().split(' ', 3)
                
                if len(parties) >= 4:
                    niveau = parties[2]  # INFO, WARN ou ERROR
                    message = parties[3] # Le texte du log
                    
                    # Comptage par criticité [cite: 15, 81]
                    if niveau in stats_niveaux:
                        stats_niveaux[niveau] += 1
                    
                    # On stocke les messages d'erreur pour le Top 5 [cite: 16, 82]
                    if niveau == "ERROR":
                        toutes_les_erreurs.append(message)

    # Calcul du Top 5 des erreurs les plus fréquentes [cite: 17, 82]
    top5 = [msg for msg, count in Counter(toutes_les_erreurs).most_common(5)]

    return {
        "total_lignes": total_lignes,
        "par_niveau": stats_niveaux,
        "top5_erreurs": top5,
        "fichiers": fichiers_traites
    }
if __name__ == "__main__":
    # Test du module avec le dossier logs_test
    # On utilise un chemin relatif pour le test local
    dossier_test = "logs_test" 
    
    if not os.path.exists(dossier_test):
        print(f"Erreur : Le dossier {dossier_test} n'existe pas. Crée-le d'abord !")
    else:
        print("--- TEST DU MODULE ANALYSER ---")
        
        # 1. Test des métadonnées
        meta = obtenir_metadonnees()
        print(f"Système : {meta['os']} | Utilisateur : {meta['utilisateur']}")
        
        # 2. Test de l'analyse
        resultats = analyser_logs(dossier_test)
        
        print(f"\nFichiers analysés : {len(resultats['fichiers'])}")
        print(f"Total des lignes : {resultats['total_lignes']}")
        print("\nRépartition par niveau :")
        for niv, nb in resultats['par_niveau'].items():
            print(f" - {niv}: {nb}")
            
        print("\nTop 5 des erreurs détectées :")
        for i, err in enumerate(resultats['top5_erreurs'], 1):
            print(f" {i}. {err}")