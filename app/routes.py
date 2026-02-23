from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils import encrypt_url, decrypt_url
from sqlalchemy import desc

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/", methods=['GET'])
def index():
    return render_template("auth/register.html")

@routes_bp.route("/register", methods=['GET'])
def register():
    return render_template("auth/register.html")

@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("auth/login.html")


@routes_bp.route("/home", methods=['GET'])
# @login_required
def home(user_id):
    frieds = db.session.query(User).join(Friend, User.id == Friend.friend_id).filter(Friend.user_id == current_user.id).all()
    context = {
        "user": current_user,
        "friends": frieds,
    }
    return render_template("app/home.html", **context)


@routes_bp.route("/talks", methods=['GET'])
def talks(user_id):
    # current_userが所属するtalk_idのリストを取得
    user_talk_ids = db.session.query(Talk_Member.talk_id).filter(
        Talk_Member.user_id == current_user.id
    ).subquery()

    # 各talk_idのfriendユーザーの名前を取得
    talk_users = db.session.query(
        Talk_Member.talk_id,
        User.id,
        User.name
    ).join(User, Talk_Member.user_id == User.id).filter(
        Talk_Member.talk_id.in_(user_talk_ids),
        Talk_Member.user_id != current_user.id
    ).order_by(Talk.updated_at.desc())
    
    context = {
        "user": current_user,
        "messages": messages,
        "talk_users": talk_users,
    }
    return render_template("app/talks.html", **context)


@routes_bp.route("/individual-talk/<int:talk_id>", methods=['GET'])
def individual_talk(user_id, talk_id):
    messages = Message.query.filter_by(talk_id=talk_id).order_by(Message.created_at).all()
    
    talk_user = db.session.query(
        Talk_Member.talk_id,
        User.id,
        User.name
    ).join(User, Talk_Member.user_id == User.id).filter(
        Talk_Member.talk_id == talk_id,
        Talk_Member.user_id != current_user.id
    ).first()
    
    # # 登録フォームで動画URLを受け取り暗号化
    # image_url = request.form.get("image_url")
    # encrypted_image_url = encrypt_url(image_url) if image_url else None
    # video_url = request.form.get("video_url")
    # encrypted_video_url = encrypt_url(video_url) if video_url else None
    
    # # 暗号化されたURLを渡す
    # decrypted_image_url = decrypt_url(encrypted_image_url) if encrypted_image_url else None
    # decrypted_video_url = decrypt_url(encrypted_video_url) if encrypted_video_url else None
    
    context = {
        "user": current_user,
        "messages": messages,
        "talk_user": talk_user,
        # encrypted_image_url=encrypted_image_url,
        # encrypted_video_url=encrypted_video_url,
    }
    return render_template("app/individual-talk.html", **context)


@routes_bp.route("/settings")
def settings():
    return render_template("app/settings.html", user=current_user)
