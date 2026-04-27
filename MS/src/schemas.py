"""
Modèles Pydantic définissant le contrat d'interface de l'API.
Responsabilité : validation des entrées et typage fort des sorties.
"""

from datetime import datetime

from pydantic import BaseModel, field_validator


class SensorReading(BaseModel):
    """Schéma d'entrée du endpoint POST /validate."""
    sensor: str
    value: float

    @field_validator("sensor")
    @classmethod
    def sensor_must_not_be_empty(cls, sensor: str) -> str:
        if not sensor.strip():
            raise ValueError("L'identifiant du capteur ne peut pas être vide.")
        return sensor.strip().lower()

    @field_validator("value")
    @classmethod
    def value_must_be_non_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("La valeur du capteur ne peut pas être négative.")
        return value


class SensorEvent(BaseModel):
    """Schéma de sortie du endpoint POST /validate — événement horodaté et catégorisé."""
    sensor: str
    value: float | None
    level: str
    valid: bool
    timestamp: datetime
    unit: str | None = None
    threshold: float | None = None  # seuil critique de référence
    message: str | None = None
    