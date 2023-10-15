import flet as ft

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def show_setting_page():
    def pick_files_result(e: ft.FilePickerResultEvent):
        picker_path.value = (
            ", ".join(
                map(lambda f: f.path, e.files)
            ) if e.files else e.page.client_storage.set("webDriver_path", e.control.value)
        )
        picker_path.focus()

    def handle_path_textfield_focus(e: ft.ControlEvent):
        if e.control.value != e.page.client_storage.get("webDriver_path"):
            try:
                webDriverOption = Options()
                webDriverOption.add_argument("--disable-notifications")
                webDriverOption.add_argument("--incognito")
                webDriverOption.add_argument("--headless")
                webdriver.Chrome(
                    executable_path=e.control.value, options=webDriverOption)
            except AttributeError:
                e.page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='請選擇正確的檔案')
                )
                e.page.snack_bar.open = True
                picker_path.value = e.page.client_storage.get("webDriver_path")
                e.page.update()
            else:
                e.page.snack_bar = ft.SnackBar(
                    content=ft.Text(value='設定成功')
                )
                e.page.snack_bar.open = True
                e.page.client_storage.set("webDriver_path", e.control.value)
                e.page.update()

    picker_path = ft.TextField(
        height=30,
        text_size=14,
        content_padding=ft.padding.symmetric(.0, 10.0),

        on_focus=handle_path_textfield_focus
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
    page.append(
        ft.Text(
            "webDriver:",
            size=16,
        )
    )
    page.append(file_picker)
    page.append(
        ft.Row([
            picker_path,
            file_picker_button,
        ])
    )
    page.append(ft.Divider())

    return page
