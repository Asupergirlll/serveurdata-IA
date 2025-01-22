from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'dataia'

jwt = JWTManager(app)

# Liste des livres
books = [
    {"id": 1, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "year": 1997},
    {"id": 2, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 4, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 5, "title": "A Promised Land", "author": "Barack Obama", "year": 2020}
]

# Dictionnaire des utilisateurs (pour la démonstration)
users = {
    "lydie": "congo",  # Exemple de nom d'utilisateur et mot de passe
    "mathieu": "rwanda"
}

# Route de connexion
@app.route('/secure-page', methods=['GET'])
@jwt_required()
def secure_page():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Bienvenue {current_user}, vous avez accès à cette page sécurisée."})

@app.route("/login", methods=['POST'])
@jwt_required()
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Vérification des identifiants
    if users.get(username) == password:
        return jsonify({"message": f"Bienvenue {username}!"})
    else:
        return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect."}), 401


# Route principale pour afficher le formulaire
@app.route("/", methods=['GET'])
@jwt_required()
def index():
    return render_template("index.html")


# API pour rechercher des livres par auteur
@app.route("/search", methods=['GET'])
@jwt_required()
def search():
    author_query = request.args.get('author', '').strip().lower()
    if not author_query:
        return jsonify({"error": "Veuillez entrer un nom d'auteur."}), 400

    # Filtrer les livres par auteur
    results = [book for book in books if author_query in book["author"].lower()]

    if results:
        return jsonify(results)
    else:
        return jsonify({"message": "Aucun livre trouvé pour cet auteur."})


# API pour ajouter un livre
@app.route("/add_book", methods=['POST'])
@jwt_required()
def add_book():
    # Récupérer les données envoyées dans la requête
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')

    # Ajouter un nouveau livre à la liste
    new_book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "year": int(year)
    }
    books.append(new_book)

    # Retourner une réponse avec le livre ajouté
    return jsonify({"message": "Livre ajouté avec succès!", "book": new_book})


if __name__ == "__main__":
    app.run(debug=True, port=80)
