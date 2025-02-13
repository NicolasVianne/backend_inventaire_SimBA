# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:42:52 2025

@author: Collège Santé
"""

import requests
from config import SUPABASE_URL, HEADERS, ABSTRACT_KEY, MBV_KEY
import MailboxValidator

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

def validate_email_with_api(email: str) -> bool:
    """
    Valide l'email en utilisant une API tierce (exemple : Abstract API).
    Retourne True si l'email est valide et existe, sinon False.
    """
    # api_key = ABSTRACT_KEY
    # url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
    
    mbv = MailboxValidator.EmailValidation(MBV_KEY)

    try:
        # response = requests.get(url)
        # response_data = response.json()

        # # Vérifie si l'email est valide et existe
        # if response_data.get("deliverability") == "DELIVERABLE":
        #     return True
        # else:
        #     return False
        
        results  = mbv.validate_email(email)
        
        if results is None:
            print("Erreur de connexion à l'API.")
            return False
        
        if 'error_code' in results and results['error_code'] != '':
            print(f"Erreur API ({results['error_code']}): {results['error_message']}")
            return False
        
        # Vérification des critères pour un email "livrable"
        if (results['is_syntax'] and
            results['is_domain'] and
            results['is_smtp'] and
            results['is_verified'] and
            not results['is_server_down'] and 
            not results['is_disposable']):
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Erreur lors de la validation de l'email : {e}")
        return False

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
