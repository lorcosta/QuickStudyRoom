from app import pswManager


def hash_psw(psw):
	return pswManager.generate_password_hash(psw).decode('utf-8')
