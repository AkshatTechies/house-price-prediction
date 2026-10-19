# database/crud.py
import bcrypt, json
from database.models import (
    User, PredictionHistory, FavoriteProperty)

def create_user(db, username, email, password):
    hashed = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt())
    user = User(
        username=username, email=email,
        password_hash=hashed.decode())
    db.add(user); db.commit()
    return user

def verify_user(db, email, password):
    user = db.query(User).filter(
        User.email==email).first()
    if user and bcrypt.checkpw(
        password.encode(),
        user.password_hash.encode()
    ):
        return user
    return None

def save_prediction(db, user_id, features, price):
    record = PredictionHistory(
        user_id=user_id,
        features=json.dumps(features),
        predicted_price=price)
    db.add(record); db.commit()
    return record

def get_user_predictions(db, user_id):
    return db.query(PredictionHistory).filter(
        PredictionHistory.user_id==user_id
    ).order_by(
        PredictionHistory.timestamp.desc()
    ).all()

def save_favorite(db, user_id, property_data):
    fav = FavoriteProperty(
        user_id=user_id,
        property_data=json.dumps(property_data))
    db.add(fav); db.commit()
    return fav