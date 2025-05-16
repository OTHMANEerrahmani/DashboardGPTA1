import reflex as rx
from app.states.organe_state import OrganeState


def maintenance_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "🗓️ Historique d'interventions de maintenance",
            class_name="text-xl font-semibold text-gray-700 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Date",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Durée (H)",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Action",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                        rx.el.th(
                            "Remarques",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        OrganeState.maintenance_history_for_selected_organe,
                        lambda entry: rx.el.tr(
                            rx.el.td(
                                entry["date"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700",
                            ),
                            rx.el.td(
                                entry["type"],
                                class_name=rx.cond(
                                    entry["type"].lower()
                                    == "corrective",
                                    "px-6 py-4 whitespace-nowrap text-sm text-red-600 font-semibold",
                                    "px-6 py-4 whitespace-nowrap text-sm text-gray-700",
                                ),
                            ),
                            rx.el.td(
                                entry[
                                    "duration_h"
                                ].to_string(),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700",
                            ),
                            rx.el.td(
                                entry["action"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700",
                            ),
                            rx.el.td(
                                entry["remarks"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50 transition-colors duration-150",
                        ),
                    ),
                    rx.cond(
                        OrganeState.maintenance_history_for_selected_organe.length()
                        == 0,
                        rx.el.tr(
                            rx.el.td(
                                "Aucune intervention enregistrée.",
                                col_span=5,
                                class_name="px-6 py-10 text-center text-sm text-gray-500 italic",
                            )
                        ),
                        rx.fragment(),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="shadow-md rounded-lg overflow-hidden border border-gray-200",
        ),
    )