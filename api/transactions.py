# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:43:44 2025

@author: Collège Santé
"""

import requests
from config import SUPABASE_URL, get_auth_headers, HEADERS_ANON, PASSWORD
import datetime
import api.items
import api.users

def create_transaction(data):
    """
    Crée une transaction en utilisant l'API REST de Supabase.

    Args:
        data (dict): Les données de la transaction, incluant :
            - user_id (int): ID de l'utilisateur.
            - item_id (int): ID de l'item concerné.
            - type (str): Type de transaction ("add" ou "remove" ou "borrow" ou "return").
            - quantity (int): Quantité à ajouter ou retirer.

    Returns:
        dict: Résultat ou message d'erreur.
    """

    # Étape 1 : Vérifier si l'item existe
    item = api.items.get_item_by_id(data["item_id"])
    if not item:
        return {"error": "Item inexistant."}
    
    # Étape 2 : Créer le token jwt
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers=HEADERS_ANON,
        json={"email": data["email"], "password": PASSWORD}
    )
    jwt_token = response.json()["access_token"]
    
    if response.status_code != 200:
        return {"error": "Échec de la connexion de l'utilisateur."}

    # Étape 3 : Valider la transaction
    previous_quantity = item["quantity"]
    transaction_type = data["type"]
    quantity = data["quantity"]

    if transaction_type == "remove" and quantity > previous_quantity or transaction_type == "borrow" and quantity > previous_quantity:
        return {"error": "Quantité demandée dépasse le stock disponible."}
    if quantity <= 0:
        return {"error": "La quantité doit être supérieure à 0."}

    # Étape 4 : Calculer la nouvelle quantité
    if transaction_type == "add" or transaction_type == "return":
        new_quantity = previous_quantity + quantity
    else :
        new_quantity = previous_quantity - quantity

    # Mise à jour de la quantité
    if not api.items.update_item(data["item_id"], {"quantity": new_quantity}):
        return {"error": "Échec de la mise à jour de la quantité."}

    # Étape 6 : Créer la transaction
    transaction_data = {
        "item_id": data["item_id"],
        "user_id": data["user_id"],
        "type": transaction_type,
        "quantity": quantity,
        "previous_quantity": previous_quantity,
        "new_quantity": new_quantity,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    transaction_url = f"{SUPABASE_URL}/rest/v1/transactions"
    transaction_response = requests.post(transaction_url, headers=get_auth_headers(jwt_token), json=transaction_data)

    if transaction_response.status_code == 201:  # 201 = créé avec succès
        return {"success": True, "transaction": transaction_response.json()}
    else:
        api.items.update_item(data["item_id"], {"new_quantity": -new_quantity})
        return {"error": "Échec de l'enregistrement de la transaction."}

def get_all_transactions_of_a_user(email):
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers=HEADERS_ANON,
        json={"email": email, "password": PASSWORD}
    )
    jwt_token = response.json()["access_token"]
    
    url = f"{SUPABASE_URL}/rest/v1/transactions"
    response2 = requests.get(url, headers=get_auth_headers(jwt_token))
    return response2.json() if response2.status_code == 200 else response2.text
