"""Basic tests for licensing"""
from licensing.license_manager import AdminLicenseManager, LicenseValidator, LicenseManager


def test_license_generation_and_activation():
    lic = AdminLicenseManager.create_license('1 Month')
    assert lic is not None
    key = lic.key
    v = LicenseValidator.validate(key)
    assert v['status'] in ['INACTIVE', 'INVALID', 'EXPIRED', 'ACTIVE']

    res = LicenseManager.activate(key)
    assert res['status'] == 'ACTIVE'

    v2 = LicenseValidator.validate(key)
    assert v2['status'] == 'ACTIVE'
