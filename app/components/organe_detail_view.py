import reflex as rx
from app.states.organe_state import OrganeState
from app.components.kpi_card import kpi_card
from app.components.maintenance_table import (
    maintenance_table,
)


def organe_detail_view() -> rx.Component:
    return rx.cond(
        OrganeState.selected_organe,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        tag="settings",
                        class_name="text-3xl text-indigo-600 mr-3",
                    ),
                    rx.el.h2(
                        "Fiche : ",
                        OrganeState.selected_organe["name"],
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.p(
                    OrganeState.selected_organe["function"],
                    class_name="text-gray-600 mt-1 mb-6 text-lg",
                ),
                class_name="mb-6 pb-6 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            OrganeState.selected_organe[
                                "name"
                            ],
                            class_name="text-xl font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.image(
                            src=rx.cond(
                                OrganeState.selected_organe["image_url"].is_none(),
                                "/favicon.ico",
                                OrganeState.selected_organe["image_url"]
                            ),
                            alt=OrganeState.selected_organe["name"],
                            class_name="w-full h-64 object-contain rounded-lg border border-gray-200 p-4 bg-white shadow-sm mb-8",
                        ),
                        class_name="bg-gray-50 p-6 rounded-xl shadow-lg border border-gray-200 mb-8",
                    ),
                    maintenance_table(),
                    class_name="w-full lg:w-2/3 lg:pr-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "📊 Indicateurs de Performance",
                            class_name="text-xl font-semibold text-gray-700 mb-6",
                        ),
                        rx.el.div(
                            kpi_card(
                                "MTBF",
                                OrganeState.mtbf.to_string(),
                                "h",
                                "⏱️",
                                "bg-blue-50 text-blue-700 border-blue-200",
                            ),
                            kpi_card(
                                "MTTR",
                                OrganeState.mttr.to_string(),
                                "h",
                                "🛠️",
                                "bg-orange-50 text-orange-700 border-orange-200",
                            ),
                            kpi_card(
                                "λ (Lambda)",
                                OrganeState.lambda_val.to_string(),
                                "h⁻¹",
                                "📉",
                                "bg-purple-50 text-purple-700 border-purple-200",
                            ),
                            kpi_card(
                                "Disponibilité",
                                OrganeState.availability.to_string(),
                                "%",
                                "✅",
                                "bg-green-50 text-green-700 border-green-200",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-xl border border-gray-200 mb-8",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "🔧 Fiabilité et Maintenance préventive",
                            class_name="text-xl font-semibold text-gray-700 mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Durée de fonctionnement (t): ",
                                rx.el.span(
                                    OrganeState.slider_t_value.to_string()
                                    + " h",
                                    class_name="font-bold text-indigo-600",
                                ),
                                class_name="block text-sm font-medium text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                type="range",
                                min="0",
                                max="5000",
                                default_value=OrganeState.slider_t_value.to_string(),
                                on_change=OrganeState.set_slider_t_value,
                                class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600 mb-4",
                            ),
                            kpi_card(
                                "R(t)",
                                OrganeState.reliability_rt.to_string(),
                                "",
                                "📈",
                                "bg-teal-50 text-teal-700 border-teal-200",
                            ),
                            class_name="mb-8",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Fiabilité minimale (R₀): ",
                                rx.el.span(
                                    (
                                        OrganeState.slider_r0_value
                                        * 100
                                    ).to_string()
                                    + " %",
                                    class_name="font-bold text-indigo-600",
                                ),
                                class_name="block text-sm font-medium text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                type="range",
                                min="1",
                                max="99",
                                default_value=(
                                    OrganeState.slider_r0_value
                                    * 100
                                ).to_string(),
                                on_change=OrganeState.set_slider_r0_value,
                                class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600 mb-4",
                            ),
                            kpi_card(
                                "Périodicité Préventive",
                                OrganeState.preventive_periodicity.to_string(),
                                "h",
                                "🔄",
                                "bg-pink-50 text-pink-700 border-pink-200",
                            ),
                        ),
                        class_name="bg-white p-6 rounded-xl shadow-xl border border-gray-200",
                    ),
                    class_name="w-full lg:w-1/3",
                ),
                class_name="flex flex-col lg:flex-row",
            ),
            class_name="p-8 bg-gray-100 rounded-xl shadow-inner",
        ),
        rx.el.div(
            rx.el.p(
                "Veuillez sélectionner un organe dans la barre latérale.",
                class_name="text-xl text-gray-500 text-center py-20",
            ),
            class_name="flex items-center justify-center h-full",
        ),
    )