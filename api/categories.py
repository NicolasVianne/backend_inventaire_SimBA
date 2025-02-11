# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:55:26 2025

@author: Collège Santé
"""

import requests
from config import SUPABASE_URL, HEADERS

def get_all_categories():
    """
    Récupère toutes les catégories depuis la table `categories` via l'API REST de Supabase.
    """
    url = f"{SUPABASE_URL}/rest/v1/categories"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else response.text
