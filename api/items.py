# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:25:17 2025

@author: Collège Santé
"""

import requests
from config import SUPABASE_URL, HEADERS
import utils.qrcode

def get_all_items():
    """
    Récupère tous les items depuis la table `items` via l'API REST de Supabase.
    """
    url = f"{SUPABASE_URL}/rest/v1/items"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else response.text

def get_item_by_id(item_id):
    """Récupère un item par son ID."""
    url = f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}"
    response = requests.get(url, headers=HEADERS)
    item_data = response.json()
    return item_data[0] if item_data else None
    
def create_item(data):
    """
    Crée un nouvel item dans la table `items`.
    Expects a dictionary `data` with the item's fields.
    """
    url = f"{SUPABASE_URL}/rest/v1/items"
    response = requests.post(url, headers=HEADERS, json=data)
    item = response.json()[0]  # Supabase retourne une liste contenant l'objet inséré
    return item

def update_item(item_id, updated_data):
    """
    Met à jour un item existant dans la table `items`.
    Expects a dictionary `updated_data` with the updated item's fields and the id of the corresponding item.
    """
    url = f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}"
    response = requests.patch(url, headers=HEADERS, json=updated_data)  # Supabase retourne une liste contenant l'objet modifié
    return response.status_code == 200

def delete_item(item_id):
    """
    Supprime un item dans la table `items`.
    Expects a number `id` to delete the corresponding item.
    """
    url = f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}"
    response = requests.delete(url, headers=HEADERS)
    return response.text

def create_item_with_qr(data):
    response = create_item(data)  # Crée l'item via l'API REST
    if "id" in response:  # Vérifie que l'item a bien été créé
        qr_path, qr_data = utils.qrcode.generate_qr_code(response["id"], response["name"])
        print(f"QR code généré : {qr_path}, {qr_data}")
        data = {"qr_code": qr_data}
        update_item(response["id"], data)
    return qr_path

def get_item_from_qr(image_path):
    qr_data = utils.qrcode.read_qr_code(image_path)
    if qr_data.startswith("https://"):
        item_id = qr_data.split("/")[-1]  # Extraire l'ID depuis l'URL
        return get_item_by_id(item_id)
    return "QR code invalide"
