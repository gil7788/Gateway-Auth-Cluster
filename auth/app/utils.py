import bcrypt


def get_database_url(username, password, host, port, database):
    return f"mysql://{username}:{password}@{host}:{port}/{database}"


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
