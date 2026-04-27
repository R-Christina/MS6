"""
Logique de classification d'une valeur capteur.
Responsabilité unique : déterminer le niveau de pollution
à partir d'une valeur et d'un seuil.
"""

from src.config.thresholds import SensorThreshold


def classify_value(value: float, threshold: SensorThreshold) -> str:
    """
    Classifie une valeur selon les seuils du capteur.

    Returns:
        "critical"  si value >= seuil critique
        "moderate"  si value >= seuil modéré
        "normal"    sinon
    """
    if value >= threshold.critical:
        return "critical"
    if value >= threshold.moderate:
        return "moderate"
    return "normal"