# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:50:14 2025

@author: Collège Santé
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis un fichier .env (si utilisé)
load_dotenv()

# Supabase API Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Headers pour les requêtes à l'API REST
HEADERS = {
    "apikey": SUPABASE_PUBLIC_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}
