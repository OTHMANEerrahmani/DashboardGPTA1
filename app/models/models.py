import reflex as rx
from typing import TypedDict, List, Optional


class MaintenanceEntry(TypedDict):
    date: str
    type: str
    duration_h: float
    action: str
    remarks: str
    is_failure: bool


class Organe(TypedDict):
    id: str
    name: str
    function: str
    image_url: str | None
    maintenance_history: List[MaintenanceEntry]
    total_operational_time_h: float


INITIAL_ORGANES_DATA: List[Organe] = [
    {
        "id": "GPA1",
        "name": "GPA1 - Groupe à vis",
        "function": "Compresse l'air du système.",
        "image_url": "/favicon.ico",
        "maintenance_history": [
            {
                "date": "2024-02-10",
                "type": "Corrective",
                "duration_h": 2.5,
                "action": "Remplacement roulements",
                "remarks": "Bruit",
                "is_failure": True,
            },
            {
                "date": "2024-03-15",
                "type": "Changement",
                "duration_h": 1.0,
                "action": "Alumine",
                "remarks": "RAS",
                "is_failure": False,
            },
            {
                "date": "2024-03-25",
                "type": "Graissage +",
                "duration_h": 2.5,
                "action": "Graissage + realignement",
                "remarks": "Fuite",
                "is_failure": True,
            },
            {
                "date": "2024-04-12",
                "type": "Graissage +",
                "duration_h": 1.0,
                "action": "Graissage",
                "remarks": "",
                "is_failure": False,
            },
            {
                "date": "2024-04-12",
                "type": "Fuite",
                "duration_h": 1.5,
                "action": "Réparation fuite",
                "remarks": "",
                "is_failure": True,
            },
        ],
        "total_operational_time_h": 50000.0,
    },
    {
        "id": "GPA2",
        "name": "GPA2 - Dessiccateur",
        "function": "Assèche l'air comprimé.",
        "image_url": "/favicon.ico",
        "maintenance_history": [],
        "total_operational_time_h": 50000.0,
    },
    {
        "id": "GPA3",
        "name": "GPA3 - ADCU",
        "function": "Unité de contrôle et de commande.",
        "image_url": "/favicon.ico",
        "maintenance_history": [],
        "total_operational_time_h": 50000.0,
    },
    {
        "id": "GPA4",
        "name": "GPA4 - Ventilateur",
        "function": "Refroidissement du système.",
        "image_url": "/favicon.ico",
        "maintenance_history": [],
        "total_operational_time_h": 50000.0,
    },
    {
        "id": "GPA5",
        "name": "GPA5 - Capteurs / Pressostats",
        "function": "Mesure et contrôle des paramètres.",
        "image_url": "/favicon.ico",
        "maintenance_history": [],
        "total_operational_time_h": 50000.0,
    },
    {
        "id": "GPA6",
        "name": "GPA6 - Soupape de sécurité",
        "function": "Protection contre la surpression.",
        "image_url": "/favicon.ico",
        "maintenance_history": [],
        "total_operational_time_h": 50000.0,
    },
    {
        "id": "GPA7",
        "name": "GPA7 - Système de graissage",
        "function": "Lubrification des composants mobiles.",
        "image_url": "/favicon.ico",
        "maintenance_history": [],
        "total_operational_time_h": 50000.0,
    },
]