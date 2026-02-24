from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required


@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("このメールアドレスは既に登録されています", "error")
            return render_template("auth/register.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("登録しました！", "success")
        return redirect(url_for("routes.home", user_id=user.id))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not user.check_password(form.password.data):
            flash("メールアドレスまたはパスワードが違います", "error")
            return render_template("auth/login.html", form=form)

        login_user(user)
        return redirect(url_for("routes.index"))

    return render_template("auth/login.html", form=form)