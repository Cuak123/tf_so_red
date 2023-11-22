from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://admin123:admin123@Obelisk.lkhnesk.mongodb.net/Obelisk"
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro.html')
def registro_page():
    return render_template('registro.html')

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if request.method == "POST":
        nombre = request.form['input-nombre']
        correo = request.form['input-correo']
        password = request.form['input-contrasenia']
      
        # Insert user data into MongoDB
        usuario_id = ObjectId()
        db.Usuarios.insert_one({
            '_id': usuario_id,
            'nombre': nombre,
            'email': correo,
            'password': password
        })

        # Redirect to login page
        return render_template('index.html')

@app.route("/procesar_login", methods=['POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']

        # Consultar el usuario en la base de datos
        usuario = db.Usuarios.find_one({'email': correo})

        if usuario and usuario['password'] == contrasenia:
            session['usuario_id'] = str(usuario['_id'])
            return  render_template('homepage.html')

    return render_template('homepage.html')

@app.route('/crear_post', methods=['POST'])
def crear_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']

        # Insert post data into MongoDB
        post_id = ObjectId()
        db.publicaciones.insert_one({
            '_id': post_id,
            'titulo': titulo,
            'contenido': contenido
        })
    return render_template('homepage.html')

    
@app.route('/crear_comentario', methods=['POST'])
def guardar_comentario():
    if request.method == 'POST':
        comentario = request.form['comentario']

        # Insertar datos del comentario en MongoDB
        comentario_id = ObjectId()
        db.comentarios.insert_one({
            '_id': comentario_id,
            'comentario': comentario
        })

        return render_template('mostrar_posts.html')

    return render_template('mostrar_posts.html')

@app.route('/mostrar_posts')
def mostrar_posts():
    # Retrieve the last post from the database
    last_post = db.publicaciones.find().sort('_id', -1).limit(1)

    return render_template('mostrar_posts.html', posts=last_post)

@app.route('/ver_comentarios')
def ver_comentarios():
    comentarios = db.comentarios.find()
    return render_template('ver_comentarios.html', comentarios=comentarios)
@app.route('/regresar')
def regresar():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)

