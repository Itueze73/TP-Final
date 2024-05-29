from flask import Flask, render_template, redirect, url_for, flash, request, session
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

#BASE DE DATOS/CLAVE
app.config['SECRET_KEY'] = 'miclavesecreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuario.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'usuarios'

# MODELO USUARIO
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

#RUTAS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/envios')
def envios():
    return render_template('envios.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/pagos')
def pagos():
    return render_template('pagos.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/registroUsuarios', methods=['GET', 'POST'])
def registro_usuarios():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            flash('La dirección de correo electrónico ya está en uso. Por favor, ingrese otra.', 'error')
            return redirect(url_for('registro_usuarios'))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso. Por favor, elija otro.', 'error')
            return redirect(url_for('registro_usuarios'))

        new_user = User(name=name, lastname=lastname, username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registro completado correctamente!', 'Aviso!')
        return redirect(url_for('index'))

    return render_template('registroUsuarios.html', form=form)

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'Aviso!')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'Advertencia!')
    return render_template('usuarios.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'Aviso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
