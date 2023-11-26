import os

SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://alice:Admin!23@localhost:3306/auth")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
