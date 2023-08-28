from app import db
from app.models import User

def add_user(email, password):
    #db.create_all()
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

# Usage example:
# email = 'user@example.com'
# password = 'password123'
# add_user(email, password)
