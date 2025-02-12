# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:42:52 2025

@author: Collège Santé
"""

import requests
from config import SUPABASE_URL, HEADERS

def get_all_users():
    url = f"{SUPABASE_URL}/rest/v1/users"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else response.text

def get_user_by_id(user_id):
    """Récupère un utilisateur par son ID."""
    url = f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}"
    response = requests.get(url, headers=HEADERS)
    user_data = response.json()
    return user_data[0] if user_data else None

def get_user_by_email(email):
    url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
    response = requests.get(url, headers=HEADERS)
    user_data = response.json()
    return user_data[0] if user_data else None

def create_user(data):
    url = f"{SUPABASE_URL}/rest/v1/users"
    response = requests.post(url, headers=HEADERS, json=data)
    user = response.json()[0]  # Supabase retourne une liste contenant l'utilisateur inséré
    return user

def update_user(user_id, updated_data):
    url = f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}"
    response = requests.patch(url, headers=HEADERS, json=updated_data)
    user = response.json()[0]  # Supabase retourne une liste contenant l'utilisateur modifié
    return user

def delete_user(user_id):
    url = f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}"
    response = requests.delete(url, headers=HEADERS)
    return response.text
