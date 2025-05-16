import reflex as rx
from app.pages.home_page import home_page
from app.pages.dashboard_page import dashboard_page
from app.states.organe_state import OrganeState

app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(
    home_page, route="/", title="Accueil - GPTA Dashboard"
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    title="Dashboard - GPTA",
)