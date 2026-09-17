from app.services.auth_service import AuthService
from app.repositories.auth_repository import AuthError

service = AuthService()

try:
    user = service.register(
        "Eijkim", "eijkim@example.com", "password123", "password123"
    )
    print("Created:", user.label, "|", user.id)
except AuthError as e:
    print("Error:", e)