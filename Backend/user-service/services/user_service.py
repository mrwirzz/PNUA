from models.user_model import User

def find_user_by_email(email):
    """Найти пользователя по email"""
    return User.objects(email=email).first()

def add_preference_to_user(user_id, preference):
    """Добавить предпочтение пользователю"""
    user = User.objects(id=user_id).first()
    if not user:
        raise ValueError("User not found")
    user.preferences.append(preference)
    user.save()
    return user