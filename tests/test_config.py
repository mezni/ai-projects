from config import settings


def test_settings_initialization():
    assert isinstance(settings.CHUNK_SIZE, int)
    assert settings.CHUNK_SIZE > 0
    assert isinstance(settings.CHUNK_OVERLAP, int)
    assert settings.MODEL_NAME != ""
