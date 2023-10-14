import flet as ft
from page.main_page import show_main_page
from page.setting_page import show_setting_page


class Parameter():
    def __init__(self):
        self.running = False
        self.timer = None
        self.page_windows_width = 300
        self.page_windows_height = 550
        self.countDelay = 10


def main(page: ft.Page):
    paramter = Parameter()

    page.window_width = paramter.page_windows_width
    page.window_height = paramter.page_windows_height

    def on_route_change(route):
        page.views.clear()
        if page.route == '/':
            page.window_width = paramter.page_windows_width
            page.views.append(
                ft.View(
                    '/',
                    [control for control in show_main_page(paramter)]
                )
            )
        elif page.route == '/setting':
            page.window_width += 200
            page.views.append(
                ft.View(
                    '/setting',
                    [control for control in show_setting_page()]
                )
            )
            page.views[0].controls[3].controls[0].value = page.client_storage.get('webDriver_path')

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.on_view_pop = view_pop
    page.on_route_change = on_route_change
    page.go('/')


ft.app(target=main, assets_dir="assets")
