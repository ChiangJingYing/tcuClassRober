import flet as ft
from page.main_page import show_main_page


class Parameter():
    def __init__(self):
        self.running = False
        self.timer = None
        self.page_windows_width = 300
        self.page_windows_height = 550
        self.countDelay = 10


def show_setting_page():
    def pick_files_result(e: ft.FilePickerResultEvent):
        picker_path.value += (
            ", ".join(
                map(lambda f: f.path, e.files)
            ) if e.files else "Cancelled!"
        )
        picker_path.update()

    picker_path = ft.TextField(
        height=30,
        text_size=14,
        content_padding=ft.padding.symmetric(.0, 10.0),
    )
    file_picker = ft.FilePicker(
        on_result=pick_files_result,
    )
    file_picker_button = ft.ElevatedButton(
        "選取檔案",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False
        ),
    )

    page = []
    page.append(
        ft.AppBar(
            title=ft.Text(
                "設定"
            ),
            actions=[
                ft.IconButton(
                    icon=ft.icons.KEYBOARD_BACKSPACE_SHARP,
                    on_click=lambda e: e.page.go('/')
                )
            ],
            toolbar_height=40,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
    )
    return page


def main(page: ft.Page):
    paramter = Parameter()

    page.window_width = paramter.page_windows_width
    page.window_height = paramter.page_windows_height

    def on_route_change(route):
        page.views.clear()
        if page.route == '/':
            page.views.append(
                ft.View(
                    '/',
                    [control for control in show_main_page(paramter)]
                )
            )
        elif page.route == '/setting':
            page.views.append(
                ft.View(
                    '/setting',
                    [control for control in show_setting_page()]
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.on_view_pop = view_pop
    page.on_route_change = on_route_change
    page.go('/')


ft.app(target=main, assets_dir="assets")
