"""
Logique de validation d'une mesure capteur.
Responsabilité : orchestrer la classification, l'horodatage
et la construction de l'événement de réponse.
"""

from datetime import datetime, timezone

from src.schemas import SensorEvent
from src.config.thresholds import SENSOR_THRESHOLDS
from src.domain.classifier import classify_value


def is_reading_valid(level: str) -> bool:
    """Indique si une lecture est considérée valide (non critique, capteur connu)."""
    return level in ("normal", "moderate")


def build_unknown_sensor_event(sensor: str) -> SensorEvent:
    """Construit l'événement pour un capteur non répertorié."""
    return SensorEvent(
        sensor=sensor,
        value=None,
        level="unknown",
        valid=False,
        timestamp=_current_utc_timestamp(),
        message=f"Capteur '{sensor}' non répertorié dans la configuration.",
    )


def build_sensor_event(sensor: str, value: float, level: str) -> SensorEvent:
    """Construit l'événement horodaté et catégorisé avec le seuil critique de référence."""
    threshold = SENSOR_THRESHOLDS[sensor]
    return SensorEvent(
        sensor=sensor,
        value=value,
        level=level,
        valid=is_reading_valid(level),
        timestamp=_current_utc_timestamp(),
        unit=threshold.unit,
        threshold=threshold.critical,
    )


def validate_sensor_reading(sensor: str, value: float) -> SensorEvent:
    """
    Point d'entrée de la validation.
    Orchestre : lookup seuil → classification → construction événement.
    """
    debug_mode = True
    threshold = SENSOR_THRESHOLDS.get(sensor)

    if threshold is None:
        return build_unknown_sensor_event(sensor)

    level = classify_value(value, threshold)
    return build_sensor_event(sensor, value, level)


def _current_utc_timestamp() -> datetime:
    """Retourne l'horodatage UTC courant."""
    return datetime.now(timezone.utc)