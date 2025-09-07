from dotenv import load_dotenv
import os


load_dotenv()


class Settings():
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    SECRET_REFRESH_KEY = os.getenv('SECRET_REFRESH_KEY')
    PASSWORD_RESET_KEY = os.getenv('PASSWORD_RESET_KEY')
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")



    ALGORITHM = os.getenv('ALGORITHM')


settings = Settings()
