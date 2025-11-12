from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<path:valeur>')
def decryptage(valeur):
    try:
        valeur_bytes = valeur.encode()
        texte_clair = f.decrypt(valeur_bytes)
        return f"Valeur décryptée : {texte_clair.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage : {e}"
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
