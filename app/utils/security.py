from werkzeug.security import check_password_hash, generate_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hash_guardado, password_plana):
    return check_password_hash(hash_guardado, password_plana)