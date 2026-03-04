#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tarfile
import os
import shutil
import datetime
import subprocess

def archiver_logs(source_dir, dest_dir):
    # Créer le dossier destination s'il n'existe pas
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Vérification espace disque (via commande système)
    try:
        subprocess.run(["df", "-h"], check=True)
    except:
        pass # Ignore si la commande échoue (ex: sur Windows)

    nom_archive = f"backup_{datetime.date.today()}.tar.gz"
    chemin_archive = os.path.join(dest_dir, nom_archive)
    
    with tarfile.open(chemin_archive, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    
    return chemin_archive