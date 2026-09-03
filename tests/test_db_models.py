"""Database tests for games and profiles"""
from database.db import init_db, SessionLocal
from database.models import Game, Profile


def test_game_profile_crud():
    init_db()
    db = SessionLocal()
    try:
        g = Game(name='TestGame', exe_path='C:/fake/game.exe')
        db.add(g)
        db.commit()
        db.refresh(g)
        assert g.id is not None

        p = Profile(game_id=g.id, name='Default', data='{}')
        db.add(p)
        db.commit()
        db.refresh(p)
        assert p.id is not None

        # cleanup
        db.delete(p)
        db.delete(g)
        db.commit()
    finally:
        db.close()
