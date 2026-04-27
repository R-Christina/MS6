"""
Routes de l'API REST.
Responsabilité unique : définir les endpoints et déléguer
la logique métier au domaine.
"""

from fastapi import APIRouter

from src.schemas import SensorEvent, SensorReading
from src.domain.validator import validate_sensor_reading

router = APIRouter()


@router.post("/validate")
def validate(reading: SensorReading) -> SensorEvent:
    """
    Reçoit une mesure capteur et retourne sa classification.

    - **sensor**: identifiant du capteur (ex: "co2", "temperature")
    - **value**: valeur mesurée (doit être >= 0)
    """
    return validate_sensor_reading(reading.sensor, reading.value)
