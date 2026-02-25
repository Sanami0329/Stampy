from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[DataRequired(), Length(min=1, max=50)]
    )
    email = StringField(
        "メールアドレス",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(), Length(min=8, message="8文字以上で入力してください")]
    )
    password_confirm = PasswordField(
        "確認用パスワード",
        validators=[DataRequired(), EqualTo("password", message="パスワードが一致しません")]
    )
    

class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired()]
    )