"""
Tests du microservice de validation capteur.
Couvre les 4 cas contractuels + cas limites.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.domain.validator import validate_sensor_reading
from src.domain.classifier import classify_value
from src.config.thresholds import SENSOR_THRESHOLDS

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def post_validate(sensor: str, value: float) -> dict:
    """Appelle POST /validate et retourne le JSON de réponse."""
    response = client.post("/validate", json={"sensor": sensor, "value": value})
    assert response.status_code == 200
    return response.json()

# ---------------------------------------------------------------------------
# CAS 1 — Valeur normale (< seuil modéré)
# ---------------------------------------------------------------------------
 
def test_normal_co2_below_moderate_threshold():
    """Une valeur CO2 inférieure au seuil modéré doit retourner level=normal et valid=True."""
    result = post_validate("co2", 300.0)
 
    assert result["level"] == "normal"
    assert result["valid"] is True
    assert result["sensor"] == "co2"