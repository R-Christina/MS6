"""
Point d'entrée de l'application FastAPI.
Responsabilité : assembler l'application et y monter les routes.
"""

from fastapi import FastAPI

from src.api.route import router

app = FastAPI(
    title="Pollution Sensor Validator",
    description="Microservice de validation et classification des données capteurs de pollution.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
def health() -> dict:
    """Endpoint de healthcheck — vérifie que le service est opérationnel."""
    return {"status": "ok"}