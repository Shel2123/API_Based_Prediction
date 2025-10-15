from nicegui import ui
from submission import submission

class MainPageController:
    def __init__(self, *, age, gender, has_house, marital_status, income, result_box):
        self.age = age
        self.gender = gender
        self.has_house = has_house
        self.marital_status = marital_status
        self.income = income
        self.result_box = result_box

    async def on_submit(self):
        try:
            payload = {
                'age': int(self.age.value) if self.age.value is not None else None,
                'gender': str(self.gender.value),
                'has_house': str(self.has_house.value),
                'marital_status': str(self.marital_status.value),
                'income': float(self.income.value) if self.income.value is not None else None,
            }
            missing = [k for k, v in payload.items() if v in (None, '')]
            if missing:
                ui.notify(f"Fill required fields: {', '.join(missing)}", type='warning')
                return

            result, err = submission(**payload)
            if err:
                ui.notify(f"Error: {err}", type='negative')
                return

            is_accept = (str(result).upper() == 'ACCEPTED') or (int(result) == 1)
            label = 'ACCEPTED' if is_accept else 'DENIED'
            color = '#22c55e' if is_accept else '#ef4444'
            icon  = 'check_circle' if is_accept else 'cancel'

            self.result_box.clear()
            with self.result_box:
                with ui.card().style(
                    f'max-width: 640px; width: 100%; text-align: center; '
                    f'padding: 32px; border: 3px solid {color}; '
                    f'background: {color}20; border-radius: 16px;'
                ):
                    ui.icon(icon).style(f'font-size: 80px; color: {color}')
                    ui.label(label).style(f'font-size: 36px; font-weight: 800; color: {color}')
        except Exception as e:
            ui.notify(f"Unexpected error: {e}", type='negative')