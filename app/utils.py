from cryptography.fernet import Fernet
import os

# FERNET_KEY取得
FERNET_KEY = os.environ.get("FERNET_KEY")
# ※開発環境用にFERNET_KEYをランダム生成（本番時env設定に切り替え）
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

def encrypt_url(url: str) -> str:
    """文字列URLを暗号化して文字列で返す"""
    return cipher.encrypt(url.encode()).decode('utf-8')

def decrypt_url(encrypted_url: str) -> str:
    """暗号化文字列からURLを復号化"""
    return cipher.decrypt(encrypted_url.encode()).decode('utf-8')