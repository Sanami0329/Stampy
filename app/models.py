from . import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import CheckConstraint

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    search_id = db.Column(db.String(10), unique=True, nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    mood_stamp_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # search_idのユニーク生成
    def generate_unique_search_id(session, length=10):
        while True:
            candidate = generate_search_id(length)
            exists = session.query(User).filter_by(search_id=candidate).first()
            if not exists:
                return candidate
    
    # passwordが8文字以上であることを確認し、ハッシュ化して保存
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password too short") #raiseで例外発生＆その後の処理を中断
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # passwordの検証
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    
    __table_args__ = (
        CheckConstraint("user_id != friend_id", name="check_user_not_friend"),
    )

class Talk_Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    talk_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Talk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    talk_id = db.Column(db.Integer, db.ForeignKey("talk.id"), nullable=False)
    stamp_id = db.Column(db.Integer, nullable=True)
    scale = db.Column(db.Integer, nullable=True)
    # image_url = db.Column(db.String(255), nullable=True)
    # video_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # __table_args__ = (
    #     CheckConstraint("scale >= 1 AND scale <= 5", name="check_scale_1_5"),
    # )
    
    # __table_args__ = (
    #     CheckConstraint(
    #         "(stamp_id IS NULL AND scale IS NULL) OR (stamp_id IS NOT NULL AND scale IS NOT NULL)",
    #         name="check_stamp_scale_set"
    #     ),
    # )
    
