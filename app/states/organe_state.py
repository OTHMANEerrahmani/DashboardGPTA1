import reflex as rx
import math
import json
from typing import List, Dict, Optional, Union
from app.models.models import (
    Organe,
    MaintenanceEntry,
    INITIAL_ORGANES_DATA,
)


class OrganeState(rx.State):
    organes: List[Organe] = INITIAL_ORGANES_DATA
    new_organe_id: str = ""
    new_organe_name: str = ""
    new_organe_function: str = ""
    new_organe_image_url: str = ""
    new_organe_total_op_time: str = "50000"
    json_input: str = ""
    selected_organe_id: Optional[str] = (
        INITIAL_ORGANES_DATA[0]["id"]
        if INITIAL_ORGANES_DATA
        else None
    )
    slider_t_value: float = 100.0
    slider_r0_value: float = 0.88
    show_add_organe_dialog: bool = False

    @rx.var
    def selected_organe(self) -> Optional[Organe]:
        if self.selected_organe_id is None:
            return None
        for organe in self.organes:
            if organe["id"] == self.selected_organe_id:
                return organe
        return None

    @rx.var
    def maintenance_history_for_selected_organe(
        self,
    ) -> List[MaintenanceEntry]:
        if self.selected_organe:
            return self.selected_organe[
                "maintenance_history"
            ]
        return []

    @rx.var
    def failures(self) -> List[MaintenanceEntry]:
        return [
            entry
            for entry in self.maintenance_history_for_selected_organe
            if entry["is_failure"]
        ]

    @rx.var
    def corrective_maintenances(
        self,
    ) -> List[MaintenanceEntry]:
        return [
            entry
            for entry in self.maintenance_history_for_selected_organe
            if entry["type"].lower() == "corrective"
            or entry["is_failure"]
        ]

    @rx.var
    def num_failures(self) -> int:
        return len(self.failures)

    @rx.var
    def mtbf(self) -> float:
        if self.selected_organe and self.num_failures > 0:
            return round(
                self.selected_organe[
                    "total_operational_time_h"
                ]
                / self.num_failures,
                2,
            )
        return 0.0

    @rx.var
    def total_repair_duration(self) -> float:
        return sum(
            (
                entry["duration_h"]
                for entry in self.corrective_maintenances
            )
        )

    @rx.var
    def num_corrective_interventions(self) -> int:
        return len(self.corrective_maintenances)

    @rx.var
    def mttr(self) -> float:
        if self.num_corrective_interventions > 0:
            return round(
                self.total_repair_duration
                / self.num_corrective_interventions,
                2,
            )
        return 0.0

    @rx.var
    def lambda_val(self) -> float:
        if self.mtbf > 0:
            return round(1 / self.mtbf, 5)
        return 0.0

    @rx.var
    def availability(self) -> float:
        if self.mtbf + self.mttr > 0:
            return round(
                self.mtbf / (self.mtbf + self.mttr) * 100, 2
            )
        return 0.0 if self.mtbf == 0 else 100.0

    @rx.var
    def reliability_rt(self) -> float:
        if self.lambda_val > 0:
            try:
                return round(
                    math.exp(
                        -self.lambda_val
                        * self.slider_t_value
                    ),
                    3,
                )
            except OverflowError:
                return 0.0
        return 1.0 if self.lambda_val == 0 else 0.0

    @rx.var
    def preventive_periodicity(self) -> float:
        if (
            self.lambda_val > 0
            and 0 < self.slider_r0_value < 1
        ):
            try:
                return round(
                    -math.log(self.slider_r0_value)
                    / self.lambda_val,
                    2,
                )
            except (ValueError, OverflowError):
                return 0.0
        return 0.0

    @rx.event
    def select_organe(self, organe_id: str):
        self.selected_organe_id = organe_id

    @rx.event
    def set_slider_t_value(self, value: str):
        try:
            self.slider_t_value = float(value)
        except ValueError:
            pass

    @rx.event
    def set_slider_r0_value(self, value: str):
        try:
            r0 = float(value) / 100
            if 0 < r0 < 1:
                self.slider_r0_value = r0
        except ValueError:
            pass

    @rx.event
    def toggle_add_organe_dialog(self):
        self.show_add_organe_dialog = (
            not self.show_add_organe_dialog
        )
        if not self.show_add_organe_dialog:
            self._clear_new_organe_form()

    def _clear_new_organe_form(self):
        self.new_organe_id = ""
        self.new_organe_name = ""
        self.new_organe_function = ""
        self.new_organe_image_url = ""
        self.new_organe_total_op_time = "50000"

    @rx.event
    def add_new_organe_from_form(
        self, form_data: Dict[str, str]
    ):
        try:
            total_op_time = float(
                form_data.get(
                    "total_operational_time_h", "50000"
                )
            )
        except ValueError:
            total_op_time = 50000.0
        new_organe_id = form_data.get("id", "")
        new_organe_name = form_data.get("name", "")
        new_organe_function = form_data.get("function", "")
        if (
            not new_organe_id
            or not new_organe_name
            or (not new_organe_function)
        ):
            yield rx.toast.error(
                "ID, Name, and Function are required."
            )
            return
        new_organe: Organe = {
            "id": new_organe_id,
            "name": new_organe_name,
            "function": new_organe_function,
            "image_url": form_data.get("image_url")
            or "/favicon.ico",
            "maintenance_history": [],
            "total_operational_time_h": total_op_time,
        }
        if any(
            (
                o["id"] == new_organe["id"]
                for o in self.organes
            )
        ):
            yield rx.toast.error(
                f"Organe ID '{new_organe['id']}' already exists."
            )
            return
        self.organes.append(new_organe)
        self._clear_new_organe_form()
        self.show_add_organe_dialog = False
        yield rx.toast.success(
            f"Organe '{new_organe['name']}' added successfully."
        )

    @rx.event
    def load_organes_from_json(self):
        if not self.json_input.strip():
            yield rx.toast.warning("JSON input is empty.")
            return
        try:
            loaded_data = json.loads(self.json_input)
            if not isinstance(loaded_data, list):
                yield rx.toast.error(
                    "JSON data must be a list of organes."
                )
                return
            newly_added_count = 0
            for item in loaded_data:
                if not all(
                    (
                        k in item
                        for k in ["id", "name", "function"]
                    )
                ):
                    yield rx.toast.warning(
                        f"Skipping item due to missing fields: {item.get('id', 'Unknown ID')}"
                    )
                    continue
                if any(
                    (
                        o["id"] == item["id"]
                        for o in self.organes
                    )
                ):
                    yield rx.toast.info(
                        f"Organe ID '{item['id']}' already exists. Skipping."
                    )
                    continue
                maintenance_history = item.get(
                    "maintenance_history", []
                )
                validated_maintenance_history: List[
                    MaintenanceEntry
                ] = []
                if isinstance(maintenance_history, list):
                    for entry in maintenance_history:
                        if isinstance(entry, dict) and all(
                            (
                                k in entry
                                for k in [
                                    "date",
                                    "type",
                                    "duration_h",
                                    "action",
                                    "remarks",
                                    "is_failure",
                                ]
                            )
                        ):
                            try:
                                validated_maintenance_history.append(
                                    {
                                        "date": str(
                                            entry["date"]
                                        ),
                                        "type": str(
                                            entry["type"]
                                        ),
                                        "duration_h": float(
                                            entry[
                                                "duration_h"
                                            ]
                                        ),
                                        "action": str(
                                            entry["action"]
                                        ),
                                        "remarks": str(
                                            entry["remarks"]
                                        ),
                                        "is_failure": bool(
                                            entry[
                                                "is_failure"
                                            ]
                                        ),
                                    }
                                )
                            except (ValueError, TypeError):
                                yield rx.toast.warning(
                                    f"Skipping invalid maintenance entry in organe {item['id']}"
                                )
                        else:
                            yield rx.toast.warning(
                                f"Skipping malformed maintenance entry in organe {item['id']}"
                            )
                else:
                    yield rx.toast.warning(
                        f"Maintenance history for {item['id']} is not a list, skipping."
                    )
                organe: Organe = {
                    "id": item["id"],
                    "name": item["name"],
                    "function": item["function"],
                    "image_url": item.get("image_url")
                    or "/favicon.ico",
                    "maintenance_history": validated_maintenance_history,
                    "total_operational_time_h": float(
                        item.get(
                            "total_operational_time_h",
                            50000.0,
                        )
                    ),
                }
                self.organes.append(organe)
                newly_added_count += 1
            if newly_added_count > 0:
                yield rx.toast.success(
                    f"Successfully loaded {newly_added_count} new organes from JSON."
                )
            else:
                yield rx.toast.info(
                    "No new organes loaded (possibly all duplicates or invalid format)."
                )
            self.json_input = ""
        except json.JSONDecodeError:
            yield rx.toast.error("Invalid JSON format.")
        except Exception as e:
            yield rx.toast.error(
                f"An error occurred: {str(e)}"
            )

    @rx.event
    def set_new_organe_id(self, value: str):
        self.new_organe_id = value

    @rx.event
    def set_new_organe_name(self, value: str):
        self.new_organe_name = value

    @rx.event
    def set_new_organe_function(self, value: str):
        self.new_organe_function = value

    @rx.event
    def set_new_organe_image_url(self, value: str):
        self.new_organe_image_url = value

    @rx.event
    def set_new_organe_total_op_time(self, value: str):
        self.new_organe_total_op_time = value

    @rx.event
    def set_json_input(self, value: str):
        self.json_input = value