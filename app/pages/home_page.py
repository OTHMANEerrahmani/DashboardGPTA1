import reflex as rx
from app.components.sidebar import sidebar
from app.components.home_page_content import (
    home_page_content,
)


def home_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            home_page_content(),
            class_name="ml-72 p-0 bg-gray-50 min-h-screen",
        ),
        class_name="flex",
    )