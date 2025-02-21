from cryptography.fernet import Fernet 
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  

def generate_key():
    key = Fernet.generate_key()
    return key.decode()

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt', methods=['POST'])
def encryptage():
    data = request.get_json()  
    custom_key = data.get('key')
    valeur = data.get('valeur')

    
    if not custom_key:
        custom_key = generate_key()

    f = Fernet(custom_key.encode())
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Chiffrement de la valeur

    return jsonify({'key': custom_key, 'valeur_encryptee': token.decode()})


@app.route('/decrypt', methods=['POST'])
def decryptage():
    data = request.get_json() 
    custom_key = data.get('key')
    token = data.get('token')

    f = Fernet(custom_key.encode())  
    token_bytes = token.encode()  
    valeur_dechiffree = f.decrypt(token_bytes)  

    return jsonify({'valeur_decryptee': valeur_dechiffree.decode()})
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
