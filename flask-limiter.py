from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://redis:6379",  # Адрес Redis-сервиса в Docker Compose
    strategy="fixed-window"
)