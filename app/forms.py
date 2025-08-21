from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from app import db,  app
from app.models import Contato,User,Post, PostComentarios
import os
from werkzeug.utils import secure_filename

bcrypt = Bcrypt()

class Userform(FlaskForm):
    nome= StringField('Nome',validators=[DataRequired()])
    sobrenome=StringField('Sobrenome',validators=[DataRequired()])
    email=StringField('E-mail',validators=[DataRequired(),Email()])
    senha= PasswordField('Senha',validators=[DataRequired()])
    confirmacao_senha=PasswordField('Senha',validators=[DataRequired(),EqualTo('senha')])
    btnSubmit=SubmitField('Cadastrar')

    def validate_email(self,email):
        if User.query.filter(email==email.data).first():
            return ValidationError('Usuario ja cadastrado com esse E-mail :(')
    def save(self):
        senha=bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user=User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha.decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        #Recuperar o usuário do email
        user = User.query.filter_by(email=self.email.data).first()
        #Verificar se a senha é valida
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                #retorna o usuário
                return user
            else:
                raise Exception('Senha incorreta.')
        else: 
            raise Exception('Usuário não encontrado.')

class contatoForm(FlaskForm):
    nome= StringField('Nome',validators=[DataRequired()])
    email=StringField('E-mail',validators=[DataRequired(),Email()])
    assunto= StringField('Assunto',validators=[DataRequired()])
    mensagem=StringField('Mensagem',validators=[DataRequired()])
    btnSubmit=SubmitField('Enviar')
    
    def save(self):
        contato=Contato(
            nome=self.nome.data,
            email=self.email.data,
            assunto=self.assunto.data,
            mensagem=self.mensagem.data
            )
        db.session.add(contato)
        db.session.commit()

class PostForm(FlaskForm):
    mensagem=StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('imagem', validators=[DataRequired()])
    btnSubmit=SubmitField('Enviar')
    def save(self, user_id):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)
        post = Post(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem=nome_seguro
        )
        caminho = os.path.join(
            #pegar a pasta que esta no projeto
            os.path.abspath(os.path.dirname(__file__)),
            #Definir a pasta que configuramos para UPLOAD
            app.config['UPLOAD_FILES'],
            #A pasta que está os POST
            'post',
            nome_seguro
        )

        imagem.save(caminho)
        db.session.add(post)
        db.session.commit()

class PostComentarioForm(FlaskForm):
    comentario=StringField('Comentario',validators=[DataRequired()])
    btnSubmit=SubmitField('Enviar')

    def save(self,user_id,post_id):
        comentario=PostComentarios(
            comentario=self.comentario.data,
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(comentario)
        db.session.commit()