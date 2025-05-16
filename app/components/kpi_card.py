import reflex as rx
from typing import Union


def kpi_card(
    title: str,
    value: rx.Var[Union[str, int, float]],
    unit: str = "",
    icon: str = "📊",
    color_class: str = "bg-blue-100 text-blue-700",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(icon, class_name="text-2xl mr-3"),
            rx.el.p(
                title,
                class_name="text-sm font-medium text-gray-600",
            ),
            class_name="flex items-center mb-1",
        ),
        rx.el.div(
            rx.el.p(value, class_name="text-3xl font-bold"),
            rx.el.p(
                unit,
                class_name="text-lg font-semibold ml-1 self-end pb-1",
            ),
            class_name="flex items-baseline",
        ),
        class_name=f"p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 {color_class} border border-gray-200",
    )