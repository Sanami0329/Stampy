from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = StringField(
        "メールアドレス",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(), Length(min=8)]
    )
    password_confirm = PasswordField(
        "パスワード（確認）",
        validators=[DataRequired(), EqualTo("password", message="パスワードが一致しません")]
    )