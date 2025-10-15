from nicegui import ui
from ui_handler import MainPageController

@ui.page("/")
def main_page():
    ui.label("Hello, Customer!")
    ui.label("Please, fill out the form below:")
    ui.input(label="Name")

    age = ui.input(label="Age")
    gender = ui.radio(options=['Male', 'Female'], value='Male').props('inline')

    ui.label("Do you have a house or renting?")
    has_house = ui.select(options=['Owned', 'Rented'], value='Owned')  # <-- было 'House'

    ui.label("What is your current marital status?")  # пробел поправил
    marital_status = ui.select(options=['Single', 'Married'], value='Single')

    ui.label("What is your current income?")
    income = ui.input(label="Income")
    result_box = ui.column().style('width: 100%; align-items: center; margin-top: 24px;')

    controller = MainPageController(
        age=age,
        gender=gender,
        has_house=has_house,
        marital_status=marital_status,
        income=income,
        result_box=result_box,
    )

    ui.button("Submit", on_click=controller.on_submit)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()