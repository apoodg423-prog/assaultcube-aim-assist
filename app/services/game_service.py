"""Game service helpers to CRUD games and profiles in DB"""
from database.db import SessionLocal
from database.models import Game, Profile
import json

class GameService:
    @staticmethod
    def list_games():
        db = SessionLocal()
        try:
            return db.query(Game).order_by(Game.name).all()
        finally:
            db.close()

    @staticmethod
    def add_game(name: str, exe_path: str = None, metadata: dict = None):
        db = SessionLocal()
        try:
            g = Game(name=name, exe_path=exe_path, metadata=json.dumps(metadata or {}))
            db.add(g)
            db.commit()
            db.refresh(g)
            return g
        finally:
            db.close()

    @staticmethod
    def delete_game(game_id: int):
        db = SessionLocal()
        try:
            g = db.query(Game).filter(Game.id == game_id).first()
            if g:
                db.delete(g)
                db.commit()
                return True
            return False
        finally:
            db.close()

class ProfileService:
    @staticmethod
    def list_profiles(game_id: int = None):
        db = SessionLocal()
        try:
            q = db.query(Profile)
            if game_id:
                q = q.filter(Profile.game_id == game_id)
            return q.order_by(Profile.name).all()
        finally:
            db.close()

    @staticmethod
    def add_profile(game_id: int, name: str, data: dict = None, is_default: bool = False):
        db = SessionLocal()
        try:
            p = Profile(game_id=game_id, name=name, data=json.dumps(data or {}), is_default=is_default)
            db.add(p)
            db.commit()
            db.refresh(p)
            return p
        finally:
            db.close()

    @staticmethod
    def delete_profile(profile_id: int):
        db = SessionLocal()
        try:
            p = db.query(Profile).filter(Profile.id == profile_id).first()
            if p:
                db.delete(p)
                db.commit()
                return True
            return False
        finally:
            db.close()
