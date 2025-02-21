from cryptography.fernet import Fernet 
from flask import Flask, render_template_string, render_template, jsonify, request, json
from flask import render_template
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

# Fonction pour générer une clé
def generate_key():
    key = Fernet.generate_key()
    return key.decode()

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Route pour chiffrer une valeur
@app.route('/encrypt', methods=['POST'])
def encryptage():
    data = request.get_json()  # Récupérer les données JSON envoyées
    valeur = data.get('valeur')

    # Si aucune clé n'est fournie, on génère une nouvelle clé
    custom_key = data.get('key') if data.get('key') else generate_key()

    f = Fernet(custom_key.encode())  # Créer l'objet Fernet avec la clé
    valeur_bytes = valeur.encode()  # Conversion du texte en bytes
    token = f.encrypt(valeur_bytes)  # Chiffrement de la valeur

    return jsonify({'key': custom_key, 'valeur_encryptee': token.decode()})

# Route pour déchiffrer une valeur
@app.route('/decrypt', methods=['POST'])
def decryptage():
    data = request.get_json()  # Récupérer les données JSON envoyées
    custom_key = data.get('key')  # La clé fournie pour le déchiffrement
    token = data.get('token')  # Le token chiffré à déchiffrer

    if not custom_key or not token:
        return jsonify({'message': 'Clé ou token manquants. Veuillez fournir une clé et un token valides.'})

    f = Fernet(custom_key.encode())  # Créer l'objet Fernet avec la clé
    token_bytes = token.encode()  # Conversion du token en bytes
    valeur_dechiffree = f.decrypt(token_bytes)  # Déchiffrement du token

    return jsonify({'valeur_decryptee': valeur_dechiffree.decode()})

if __name__ == "__main__":
    app.run(debug=True)
