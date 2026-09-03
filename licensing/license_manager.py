"""License management for Ipro71 Nexus

Provides License, LicenseManager, LicenseGenerator, LicenseValidator, AdminLicenseManager
"""
import hmac
import hashlib
import secrets
import datetime
from typing import Optional, List
from database.db import SessionLocal
from database.models import License as LicenseModel

# Admin secret - in production this should be stored securely
_ADMIN_SECRET = b"ipro71-admin-secret"

class License:
    def __init__(self, key: str, license_type: str, created_at: datetime.datetime, activated_at: Optional[datetime.datetime], expires_at: Optional[datetime.datetime], status: str):
        self.key = key
        self.license_type = license_type
        self.created_at = created_at
        self.activated_at = activated_at
        self.expires_at = expires_at
        self.status = status

class LicenseGenerator:
    @staticmethod
    def generate_key() -> str:
        # Simple HMAC-based key generation with randomness
        rand = secrets.token_hex(8)
        mac = hmac.new(_ADMIN_SECRET, rand.encode('utf-8'), hashlib.sha256).hexdigest()[:24]
        key = f"{rand[:4]}-{rand[4:8]}-{mac[:4]}-{mac[4:8]}-{mac[8:12]}"
        return key.upper()

class LicenseValidator:
    @staticmethod
    def validate(key: str) -> dict:
        # Basic validation: check DB for key and compute status
        db = SessionLocal()
        lic = db.query(LicenseModel).filter(LicenseModel.key == key).first()
        if not lic:
            return {"status": "INVALID"}
        now = datetime.datetime.utcnow()
        if lic.expires_at and lic.expires_at < now:
            return {"status": "EXPIRED", "expires_at": lic.expires_at}
        return {"status": lic.status, "expires_at": lic.expires_at}

class LicenseManager:
    @staticmethod
    def activate(key: str) -> dict:
        db = SessionLocal()
        lic = db.query(LicenseModel).filter(LicenseModel.key == key).first()
        if not lic:
            return {"status": "INVALID"}
        lic.activated_at = datetime.datetime.utcnow()
        lic.status = 'ACTIVE'
        db.add(lic)
        db.commit()
        return {"status": "ACTIVE", "expires_at": lic.expires_at}

class AdminLicenseManager:
    @staticmethod
    def create_license(license_type: str = '1 Month') -> LicenseModel:
        db = SessionLocal()
        key = LicenseGenerator.generate_key()
        now = datetime.datetime.utcnow()
        if license_type == '1 Month':
            expires = now + datetime.timedelta(days=30)
        elif license_type == '6 Months':
            expires = now + datetime.timedelta(days=182)
        elif license_type == 'Lifetime':
            expires = None
        else:
            expires = now + datetime.timedelta(days=30)

        lic = LicenseModel(key=key, license_type=license_type, created_at=now, expires_at=expires, status='INACTIVE')
        db.add(lic)
        db.commit()
        return lic

    @staticmethod
    def list_licenses() -> List[LicenseModel]:
        db = SessionLocal()
        return db.query(LicenseModel).order_by(LicenseModel.created_at.desc()).all()
