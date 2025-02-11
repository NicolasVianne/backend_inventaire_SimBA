# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:07:08 2025

@author: Collège Santé
"""

import qrcode
import os
from pyzbar.pyzbar import decode
from PIL import Image

def generate_qr_code(item_id, item_name, output_dir="qrcodes/"):
    """
    Génère un QR code pour un item spécifique.
    - item_id: ID de l'item.
    - item_name: Nom de l'item (utilisé pour nommer le fichier).
    - output_dir: Dossier où les QR codes seront stockés.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # URL à inclure dans le QR code (remplacez par votre URL réelle)
    qr_data = f"https://xhcnvuqewmvinslquafo.supabase.co/item/{item_id}"
    
    # Génération du QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Sauvegarde du QR code dans un fichier image
    img = qr.make_image(fill_color="black", back_color="white")
    file_path = os.path.join(output_dir, f"{item_name}_{item_id}_qr.png")
    img.save(file_path)

    return file_path, qr_data

def read_qr_code(image_path):
    """
    Lit un QR code depuis une image.
    - image_path: Chemin du fichier image contenant le QR code.
    """
    img = Image.open(image_path)
    decoded_data = decode(img)
    
    if decoded_data:
        return decoded_data[0].data.decode("utf-8")  # Retourne la donnée encodée
    return "Aucun QR code détecté"
