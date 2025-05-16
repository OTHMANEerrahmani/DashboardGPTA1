import reflex as rx
from app.states.organe_state import OrganeState


def organe_preview_card(
    organe: rx.Var[dict],
) -> rx.Component:
    return rx.el.div(
        rx.el.image(
            src=organe["image_url"].else_("/favicon.ico"),
            alt=organe["name"],
            class_name="w-full h-40 object-contain rounded-t-lg bg-gray-200 p-2",
        ),
        rx.el.div(
            rx.el.h3(
                organe["name"],
                class_name="text-lg font-semibold text-gray-800 mb-1 truncate",
            ),
            rx.el.p(
                organe["function"],
                class_name="text-sm text-gray-600 h-10 overflow-hidden text-ellipsis",
            ),
            class_name="p-4",
        ),
        on_click=[
            OrganeState.select_organe(organe["id"]),
            rx.redirect("/dashboard"),
        ],
        class_name="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 cursor-pointer border border-gray-200 flex flex-col justify-between overflow-hidden",
    )


def add_organe_dialog() -> rx.Component:
    return rx.el.dialog(
        rx.el.form(
            rx.el.div(
                rx.el.h2(
                    "Ajouter un Nouvel Organe",
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "ID Organe",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="id",
                        placeholder="Ex: GPA8",
                        default_value=OrganeState.new_organe_id,
                        class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Nom de l'Organe",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="name",
                        placeholder="Ex: Nouveau Compresseur",
                        default_value=OrganeState.new_organe_name,
                        class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Fonction",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="function",
                        placeholder="Ex: Description de la fonction",
                        default_value=OrganeState.new_organe_function,
                        class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "URL de l'Image (Optionnel)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="image_url",
                        placeholder="Ex: /image.png ou https://example.com/image.png",
                        default_value=OrganeState.new_organe_image_url,
                        class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Temps Opérationnel Total (h)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="total_operational_time_h",
                        type="number",
                        placeholder="Ex: 50000",
                        default_value=OrganeState.new_organe_total_op_time,
                        class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Annuler",
                        on_click=OrganeState.toggle_add_organe_dialog,
                        type="button",
                        class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors mr-2",
                    ),
                    rx.el.button(
                        "Ajouter Organe",
                        type="submit",
                        class_name="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="p-6 bg-white rounded-lg shadow-xl w-full max-w-lg",
            ),
            on_submit=OrganeState.add_new_organe_from_form,
            reset_on_submit=True,
        ),
        open=OrganeState.show_add_organe_dialog,
        on_open_change=OrganeState.toggle_add_organe_dialog,
        class_name="fixed inset-0 open:flex items-center justify-center bg-black bg-opacity-50 p-4 z-50",
    )


def home_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Dashboard Technique Interactif – GPTA",
            class_name="text-4xl font-extrabold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.h2(
                "Introduction au Projet",
                class_name="text-2xl font-semibold text-gray-700 mb-3",
            ),
            rx.el.p(
                "Ce dashboard a pour but de fournir une interface moderne et claire pour le suivi des organes du système GPTA. Il s'inspire des outils de maintenance industrielle pour offrir une expérience utilisateur professionnelle. Les indicateurs clés de performance (KPIs) tels que MTBF, MTTR, Lambda (λ), Disponibilité (A), Fiabilité R(t) et Périodicité Préventive sont calculés automatiquement pour chaque organe.",
                class_name="text-gray-600 mb-4 leading-relaxed",
            ),
            rx.el.p(
                "Technologie utilisée : Reflex (Python).",
                class_name="text-gray-600 mb-8",
            ),
            class_name="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Gestion des Organes",
                class_name="text-2xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        "➕ Ajouter un Organe Manuellement",
                        on_click=OrganeState.toggle_add_organe_dialog,
                        class_name="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-md font-semibold",
                    ),
                    add_organe_dialog(),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Importer des Organes depuis JSON",
                        class_name="text-lg font-medium text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        default_value=OrganeState.json_input,
                        on_change=OrganeState.set_json_input,
                        placeholder='[{"id": "GPA_JSON", "name": "Organe JSON", "function": "Fonction test", "image_url": null, "maintenance_history": [], "total_operational_time_h": 60000}]',
                        class_name="w-full h-32 p-3 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mb-3 text-sm",
                    ),
                    rx.el.button(
                        "Charger JSON",
                        on_click=OrganeState.load_organes_from_json,
                        class_name="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md font-semibold",
                    ),
                    class_name="p-4 bg-gray-50 rounded-lg border border-gray-200",
                ),
                class_name="mb-8",
            ),
            class_name="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Liste des Organes",
                class_name="text-2xl font-semibold text-gray-700 mb-6",
            ),
            rx.cond(
                OrganeState.organes.length() > 0,
                rx.el.div(
                    rx.foreach(
                        OrganeState.organes,
                        organe_preview_card,
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "Aucun organe n'est actuellement chargé. Veuillez en ajouter manuellement ou via JSON.",
                        class_name="text-center text-gray-500 italic py-10 text-lg",
                    ),
                    class_name="bg-gray-50 p-6 rounded-lg border border-dashed border-gray-300",
                ),
            ),
        ),
        class_name="container mx-auto px-4 py-8",
    )