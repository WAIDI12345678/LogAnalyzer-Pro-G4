
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os

# Import des modules locaux
import analyser
import rapport
import archiver

def main():
    parser = argparse.ArgumentParser(description="LogAnalyzer Pro - Pipeline")
    parser.add_argument("--source", required=True, help="Dossier des logs")
    parser.add_argument("--niveau", default="ALL", help="Niveau (INFO, WARN, ERROR, ALL)")
    parser.add_argument("--dest", default="./backups", help="Dossier archivage")
    
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"ERREUR : Le dossier '{args.source}' est introuvable.")
        sys.exit(1)

    try:
        print("1. Analyse des logs...")
        stats, top5, fichiers = analyser.analyser_logs(args.source, args.niveau)
        
        print("2. Génération du rapport...")
        chemin_rep = rapport.generer_json(stats, top5, fichiers, args.source)
        print(f"   -> Rapport créé : {chemin_rep}")
        
        print("3. Archivage...")
        archive = archiver.archiver_logs(args.source, args.dest)
        print(f"   -> Archive créée : {archive}")
        
        print("\n--- Succès ! Tout a été traité ---")

    except Exception as e:
        print(f"\nERREUR FATALE : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
   
