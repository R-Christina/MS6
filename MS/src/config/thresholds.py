"""
Configuration des seuils de pollution.
Chaque capteur définit un seuil modéré et un seuil critique.
Ce module est le seul point de configuration — modifier ici suffit
pour propager les changements dans toute l'application.
"""

from pydantic import BaseModel, field_validator


class SensorThreshold(BaseModel):
    """Représente les seuils d'alerte pour un capteur donné."""
    moderate: float
    critical: float
    unit: str

    model_config = {"frozen": True}

    @field_validator("critical")
    @classmethod
    def critical_must_exceed_moderate(cls, critical: float, info) -> float:
        """Garantit la cohérence : seuil critique > seuil modéré."""
        moderate = info.data.get("moderate")
        if moderate is not None and critical <= moderate:
            raise ValueError(
                f"Le seuil critique ({critical}) doit être "
                f"supérieur au seuil modéré ({moderate})."
            )
        return critical


# --- Registre des seuils configurables ---
# Pour ajouter un capteur : ajouter une entrée ici uniquement.
SENSOR_THRESHOLDS: dict[str, SensorThreshold] = {
    "co2": SensorThreshold(moderate=800.0, critical=1000.0, unit="ppm"),
    "temperature": SensorThreshold(moderate=35.0, critical=40.0, unit="°C"),
    "noise": SensorThreshold(moderate=70.0, critical=85.0, unit="dB"),
    "pm25": SensorThreshold(moderate=25.0, critical=50.0, unit="µg/m³"),
    # Capteur supplémentaire : humidité relative
    "humidity": SensorThreshold(moderate=70.0, critical=90.0, unit="%"),
}