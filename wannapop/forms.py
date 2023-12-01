from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DecimalField, SubmitField, SelectField, FileField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email
import decimal

class LoginForm(FlaskForm):
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        validators=[ DataRequired()]
    )
    submit = SubmitField()

class RegisterForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        validators=[ DataRequired()]
    )
    submit = SubmitField()

class ProfileForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        # no es obligatori canviar-lo
    )
    submit = SubmitField()

class ResendForm(FlaskForm):
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    submit = SubmitField()

class ProductForm(FlaskForm):
    title = StringField(
        validators = [DataRequired()]
    )
    description = StringField(
        validators = [DataRequired()]
    )
    photo_file = FileField()
    price = DecimalField(
        places = 2, 
        rounding = decimal.ROUND_HALF_UP, 
        validators = [DataRequired(), NumberRange(min = 0)]
    )
    category_id = SelectField(
        validators = [InputRequired()]
    )
    status_id = SelectField(
        validators = [InputRequired()]
    )
    submit = SubmitField()

class CategoryForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    slug = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

class StatusForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    slug = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

# Formulari generic per esborrar i aprofitar la CSRF Protection
class DeleteForm(FlaskForm):
    submit = SubmitField()

class UnbanForm(FlaskForm):
    csrf_token = HiddenField()

class ModerationForm(FlaskForm):
    user_id = SelectField('Selecciona un usuario', coerce=int, validators=[DataRequired()])
    message = TextAreaField('Mensaje', validators=[DataRequired()])
    submit_add = SubmitField('Añadir a la lista de bloqueados')
    submit_remove = SubmitField('Quitar de la lista de bloqueados')

    def set_user_choices(self, user_choices):
        self.user_id.choices = user_choices