import reflex as rx
from app.components.sidebar import sidebar
from app.components.organe_detail_view import (
    organe_detail_view,
)
from app.states.organe_state import OrganeState


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            organe_detail_view(),
            class_name="ml-72 p-8 bg-gray-50 min-h-screen",
        ),
        class_name="flex",
    )