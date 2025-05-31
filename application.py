from flask import Flask, render_template, redirect, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Email
from flask_wtf import FlaskForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


application = Flask(__name__)
application.secret_key = 'master_code'


# Configure the database URI
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(application)

# Initialize Bcrypt
bcrypt = Bcrypt(application)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

# Initialize CSRF Protection
csrf = CSRFProtect(application)

# Flask-Admin para interface administrativa
admin = Admin(application)

# Define User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Formulários
class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            InputRequired(message='O campo nome de usuário é obrigatório.'),
            Length(min=3, max=20, message='O nome de usuário deve ter entre 3 e 20 caracteres.')
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            InputRequired(message='O campo email é obrigatório.'),
            Email(message='Email inválido.'),
            Length(max=120, message='O email deve ter no máximo 120 caracteres.')
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            InputRequired(message='O campo senha é obrigatório.'),
            Length(min=5, max=80, message='A senha deve ter entre 5 e 80 caracteres.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            InputRequired(message='O campo confirmação de senha é obrigatório.'),
            EqualTo('password', message='As senhas devem coincidir.')
        ]
    )
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
    submit = SubmitField('Login')


# Routes

@application.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', username=current_user.username)
    return render_template('index.html', username=None)

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login realizado com sucesso.', 'success')
            return redirect('/')
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
    return render_template('login.html', form=form)

# Configuração do LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.route('/minha_conta')
@login_required
def minha_conta():
    return render_template('minha_conta.html', username=current_user.username)

@application.route('/user_info/<username>')
@login_required
def user_info(username):
    # Verifica se o usuário existe no banco de dados
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)  # Retorna erro 404 se o usuário não existir

    return render_template('user_info.html', username=username)

@application.route('/consumo')
def consumo():
    return render_template('consumo.html', username=current_user.username if current_user.is_authenticated else None)

@application.route('/energia_solar')
def energia_solar():
    return render_template('energia_solar.html', username=current_user.username if current_user.is_authenticated else None)

@application.route('/energia_eolica')
def energia_eolica():
    return render_template('energia_eolica.html', username=current_user.username if current_user.is_authenticated else None)

@application.route('/energia_hidreletrica')
def energia_hidreletrica():
    return render_template('energia_hidreletrica.html', username=current_user.username if current_user.is_authenticated else None)

@application.route('/energia_biomassa')
def energia_biomassa():
    return render_template('energia_biomassa.html', username=current_user.username if current_user.is_authenticated else None)

@application.route('/energia_residencial')
def energia_residencial():
    return render_template('energia_residencial.html', username=current_user.username if current_user.is_authenticated else None)

@application.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@application.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_username:
            flash('Esse username já existe. Por favor escolha outro.', 'error')
        elif existing_user_email:
            flash('Esse e-mail já está em uso. Por favor escolha outro.', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registrado com sucesso. Por favor, faça o login.', 'success')
            return redirect('/login')
    return render_template('registro.html', form=form)

# Flask-Admin para administração de usuários
class UserView(ModelView):
    column_list = ['id', 'username', 'email', 'is_admin']
    form_columns = ['username', 'email', 'password', 'is_admin']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            model.password = bcrypt.generate_password_hash(model.password).decode('utf-8')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(UserView(User, db.session))

@application.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        # Verificar se o e-mail existe no banco de dados
        user = User.query.filter_by(email=email).first()
        if user:
            # Aqui geraríamos um token de redefinição de senha e enviaria um e-mail com um link contendo o token
            # O link levaria o usuário para outra rota onde ele pode redefinir a senha
            # Por enquanto, vamos apenas exibir uma mensagem de sucesso
            flash('Um e-mail com instruções para redefinir sua senha foi enviado para o seu endereço de e-mail.', 'success')
            return redirect('/login')
        else:
            flash('Este e-mail não está associado a uma conta. Por favor, verifique e tente novamente.', 'error')
    return render_template('reset_password_request.html')

if __name__ == '__main__':
    application.run(debug=True)
