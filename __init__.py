from cryptography.fernet import Fernet
from flask import Flask, request, render_template, abort
import os

app = Flask(__name__)

# --- Gestion de la clé (persistante) ---
KEYFILE = "fernet.key"

def load_or_create_key():
    # Priorité : variable d'environnement FER_KEY, sinon fichier, sinon création et sauvegarde dans fichier
    env_key = os.environ.get("FER_KEY")
    if env_key:
        return env_key.encode()

    if os.path.exists(KEYFILE):
        with open(KEYFILE, "rb") as f:
            return f.read()

    # Générer et sauvegarder
    key = Fernet.generate_key()
    with open(KEYFILE, "wb") as f:
        f.write(key)
    return key

key = load_or_create_key()
f = Fernet(key)

# --- Routes HTML utiles ---
@app.route('/')
def index():
    return render_template("crypto.html")


# --- API simples via URL ---
@app.route('/encrypt/<path:texte>')
def encrypt_route(texte):
    try:
        token = f.encrypt(texte.encode())
        # token est bytes; on renvoie la version str
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur lors de l'encryptage : {e}", 500


# On utilise <path:token> pour capturer les / et autres caractères dans le token
@app.route('/decrypt/<path:token>')
def decrypt_route(token):
    try:
        # token arrive en str, on convertit en bytes
        decrypted = f.decrypt(token.encode())
        return f"Valeur décryptée : {decrypted.decode()}"
    except Exception as e:
        # On renvoie un message propre en cas d'erreur
        return f"Erreur lors du décryptage : {e}", 400


# --- Routes utilisées par le formulaire HTML (GET) ---
@app.route('/encrypt_result')
def encrypt_result():
    texte = request.args.get('texte', '')
    if texte == '':
        return "Pas de texte fourni", 400
    token = f.encrypt(texte.encode())
    return f"Valeur encryptée : {token.decode()}"


@app.route('/decrypt_result')
def decrypt_result():
    token = request.args.get('texte', '')
    if token == '':
        return "Pas de token fourni", 400
    try:
        decrypted = f.decrypt(token.encode())
        return f"Valeur décryptée : {decrypted.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage : {e}", 400


if __name__ == "__main__":
    # debug=True pour dev local seulement
    app.run(host="0.0.0.0", port=5000, debug=True)
