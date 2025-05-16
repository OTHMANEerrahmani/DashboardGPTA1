import reflex as rx
from app.states.organe_state import OrganeState
from app.app import State


def sidebar_link(
    text: str, href: str, is_active: rx.Var[bool]
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            text,
            class_name=rx.cond(
                is_active,
                "px-4 py-3 bg-indigo-700 text-white rounded-lg font-semibold shadow-md",
                "px-4 py-3 text-indigo-100 hover:bg-indigo-500 hover:text-white rounded-lg transition-colors duration-150 font-medium",
            ),
        ),
        href=href,
        class_name="w-full block",
    )


def sidebar() -> rx.Component:
    current_path = State.router.page.path
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Navigation",
                class_name="text-xs text-indigo-300 uppercase font-semibold tracking-wider mb-3 px-4",
            ),
            sidebar_link(
                "Accueil", "/", current_path == "/"
            ),
            sidebar_link(
                "Dashboard GPTA",
                "/dashboard",
                current_path == "/dashboard",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Organes du GPTA",
                class_name="text-xs text-indigo-300 uppercase font-semibold tracking-wider mb-3 px-4",
            ),
            rx.foreach(
                OrganeState.organes,
                lambda organe: sidebar_link(
                    organe["name"],
                    "/dashboard",
                    (
                        OrganeState.selected_organe_id
                        == organe["id"]
                    )
                    & (current_path == "/dashboard"),
                ),
            ),
            rx.foreach(
                OrganeState.organes,
                lambda organe: rx.el.div(
                    sidebar_link(
                        organe["name"],
                        "/dashboard",
                        (
                            OrganeState.selected_organe_id
                            == organe["id"]
                        )
                        & (current_path == "/dashboard"),
                    ),
                    on_click=OrganeState.select_organe(
                        organe["id"]
                    ),
                ),
            ),
            class_name="space-y-1",
        ),
        class_name="h-screen w-72 bg-indigo-600 text-white p-6 fixed shadow-2xl overflow-y-auto",
    )