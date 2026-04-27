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


# ---------------------------------------------------------------------------
# CAS 2 — Valeur modérée (>= seuil modéré, < seuil critique)
# ---------------------------------------------------------------------------

def test_moderate_co2_between_thresholds():
    """Une valeur CO2 entre seuil modéré et critique doit retourner level=moderate et valid=True."""
    result = post_validate("co2", 850.0)

    assert result["level"] == "moderate"
    assert result["valid"] is True


def test_moderate_temperature_between_thresholds():
    """Une valeur température entre seuil modéré et critique doit retourner level=moderate."""
    result = post_validate("temperature", 37.0)

    assert result["level"] == "moderate"
    assert result["valid"] is True


# ---------------------------------------------------------------------------
# CAS 3 — Valeur critique (>= seuil critique)
# ---------------------------------------------------------------------------

def test_critical_noise_above_critical_threshold():
    """Une valeur bruit >= seuil critique doit retourner level=critical et valid=False."""
    result = post_validate("noise", 90.0)

    assert result["level"] == "critical"
    assert result["valid"] is False


def test_critical_pm25_at_exact_critical_threshold():
    """Une valeur pm25 exactement égale au seuil critique doit retourner level=critical."""
    result = post_validate("pm25", 50.0)

    assert result["level"] == "critical"
    assert result["valid"] is False


# ---------------------------------------------------------------------------
# CAS 4 — Capteur inconnu
# ---------------------------------------------------------------------------

def test_unknown_sensor_returns_unknown_level():
    """Un capteur non répertorié doit retourner level=unknown et valid=False."""
    result = post_validate("radioactivity", 999.0)

    assert result["level"] == "unknown"
    assert result["valid"] is False


# ---------------------------------------------------------------------------
# Capteur supplémentaire — humidity
# ---------------------------------------------------------------------------

def test_normal_humidity_below_moderate():
    result = post_validate("humidity", 50.0)
    assert result["level"] == "normal"
    assert result["valid"] is True


def test_critical_humidity_above_critical():
    result = post_validate("humidity", 95.0)
    assert result["level"] == "critical"
    assert result["valid"] is False


# ---------------------------------------------------------------------------
# Horodatage et structure de l'événement
# ---------------------------------------------------------------------------

def test_response_contains_timestamp():
    """Chaque réponse doit inclure un horodatage ISO 8601."""
    result = post_validate("co2", 500.0)

    assert "timestamp" in result
    assert result["timestamp"] is not None
    # Pydantic sérialise datetime en ISO 8601 — le 'T' sépare date et heure
    assert "T" in result["timestamp"]


def test_response_contains_unit_for_known_sensor():
    """La réponse d'un capteur connu doit inclure son unité de mesure."""
    result = post_validate("temperature", 20.0)

    assert "unit" in result
    assert result["unit"] == "°C"


# ---------------------------------------------------------------------------
# Validation Pydantic des entrées
# ---------------------------------------------------------------------------

def test_empty_sensor_name_is_rejected():
    """Un nom de capteur vide doit être rejeté par la validation Pydantic (422)."""
    response = client.post("/validate", json={"sensor": "  ", "value": 100.0})
    assert response.status_code == 422


def test_negative_value_is_rejected():
    """Une valeur négative doit être rejetée par la validation Pydantic (422)."""
    response = client.post("/validate", json={"sensor": "co2", "value": -10.0})
    assert response.status_code == 422



def test_classify_value_normal():
    threshold = SENSOR_THRESHOLDS["co2"]
    assert classify_value(300.0, threshold) == "normal"


def test_classify_value_moderate():
    threshold = SENSOR_THRESHOLDS["co2"]
    assert classify_value(850.0, threshold) == "moderate"


def test_classify_value_critical():
    threshold = SENSOR_THRESHOLDS["co2"]
    assert classify_value(1200.0, threshold) == "critical"


def test_validate_sensor_reading_unknown():
    result = validate_sensor_reading("unknown_sensor", 42.0)
    assert result.level == "unknown"
    assert result.valid is False
    