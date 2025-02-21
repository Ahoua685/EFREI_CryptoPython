from cryptography.fernet import Fernet 
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/generate_key')
def generate_key():
    key = Fernet.generate_key()
    return f"Votre clé personnelle : {key.decode}"


@app.route('/encrypt/<string:custuom_key>/<string:valeur>')
def encryptage(custom_key,valeur):
    f = Fernet(custom_key.encode())
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:custom_key>/<string:token>')
def decryptage(custom_key,token):
    f = Fernet(custom_key.encode())
    token_bytes = token.encode()
    valeur_dechiffree = f.decrypt(token_bytes)
    return f"Valeur décryptée : {valeur_dechiffree.decode()}"
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
