# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:35:35 2025

@author: Collège Santé
"""

from flask import Flask, request, jsonify
import api.items #fichier dans lequel il y a la fonction get_item_by_id(item_id)
import api.users
import api.transactions
import api.categories
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route principale (test)
@app.route("/")
def home():
    return "Hello, World!"

@app.route("/item/<item_id>", methods=['GET'])
def get_item(item_id):
    try:
        # Utilise la fonction get_item_by_id pour récupérer les informations de l'objet
        item = api.items.get_item_by_id(item_id)
        
        if not item:
            return jsonify({"success": False, "message": "Objet non trouvé."}), 404
        
        # Retourne uniquement les informations nécessaires (name et location)
        return jsonify({
            "success": True,
            "name": item.get("name"),
            "location": item.get("location")
        })
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Route pour gérer les transactions
@app.route("/transaction", methods=['POST'])
def handle_transaction():
    try:
        # Étape 1 : Récupérer les données JSON envoyées par le frontend
        data = request.get_json()
        
        item_id = data.get("id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        item_name = data.get("name")
        room = data.get("location")
        quantity = data.get("quantity")
        action = data.get("action")  # "add", "remove", "borrow", "return"

        # Vérification des données reçues
        if not all([item_id, first_name, last_name, email, item_name, quantity, action]):
            return jsonify({"success": False, "message": "Données incomplètes."}), 400

        # Étape 2 : Trouver l'utilisateur par email, prénom et nom
        user = api.users.get_user_by_email_and_name(first_name, last_name, email)
        if not user:
            return jsonify({"success": False, "message": "Utilisateur non trouvé."}), 404
        user_id = user["id"]

        # Étape 4 : Préparer les données pour la transaction
        transaction_data = {
            "user_id": user_id,
            "item_id": item_id,
            "type": action,
            "quantity": quantity,
        }

        # Étape 5 : Créer la transaction en utilisant `create_transaction`
        result = api.transactions.create_transaction(transaction_data)

        if "error" in result:
            return jsonify({"success": False, "message": result["error"]}), 400

        # Étape 6 : Retourner la transaction au frontend
        return jsonify({"success": True, "transaction": result["transaction"]})

    except Exception as e:
        # Gérer les erreurs inattendues
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)
