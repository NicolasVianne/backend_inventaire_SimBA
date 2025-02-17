# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:25:17 2025

@author: Collège Santé
"""

import requests
from config import SUPABASE_URL, HEADERS_ANON, HEADERS_SECRET

def get_all_items():
    """
    Récupère tous les items depuis la table `items` via l'API REST de Supabase.
    """
    url = f"{SUPABASE_URL}/rest/v1/items"
    response = requests.get(url, headers=HEADERS_ANON)
    return response.json() if response.status_code == 200 else response.text

def get_item_by_id(item_id):
    """Récupère un item par son ID."""
    url = f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}"
    response = requests.get(url, headers=HEADERS_ANON)
    item_data = response.json()
    return item_data[0] if item_data else None

def update_item(item_id, updated_data):
    """
    Met à jour un item existant dans la table `items`.
    Expects a dictionary `updated_data` with the updated item's fields and the id of the corresponding item.
    """
    url = f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}"
    response = requests.patch(url, headers=HEADERS_SECRET, json=updated_data)  # Supabase retourne une liste contenant l'objet modifié
    return response.status_code == 200
