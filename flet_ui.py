import flet as ft
from threading import Timer
from datetime import datetime
from aha import ClassRobber


class Timers(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


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

    def rob():
        count_code = list()
        for k in user_input_list:
            if k.value:
                count_code.append(k)
        if user_input_student_number.value and user_input_password.value and count_code.__len__():
            robber = ClassRobber(studentNum=user_input_student_number.value,
                                 password=user_input_password.value,
                                 code=count_code)
            now = datetime.now().strftime("%H:%M:%S\n")
            system_output.value += now + robber.all()
        else:
            print('Please input correct user info.')
            if paramter.running:
                handle_stop_button_click('just put it not mean what')
            page.snack_bar = ft.SnackBar(
                content=ft.Text('請輸入正確的學號密碼及課程代碼！')
            )
            page.snack_bar.open = True
            page.update()

    def countDownTimes():
        if count_down_text.value == '0':
            rob()
            count_down_text.value = paramter.countDelay
        else:
            count_down_text.value = str(int(count_down_text.value) - 1)
            page.update()

    def handle_start_button_click(_):
        if int(user_input_delay_time.value) <= 10:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(value='冷卻時間需大於299')
            )
            page.snack_bar.open = True
            page.update()
        elif paramter.timer is None or not paramter.running:
            paramter.countDelay = user_input_delay_time.value
            count_down_text.disabled = True
            page.update()
            paramter.timer = Timers(1, countDownTimes, )
            paramter.timer.start()
            paramter.running = True
            rob()

    def handle_stop_button_click(_):
        count_down_text.value = str(paramter.countDelay)
        paramter.timer.cancel()
        paramter.running = False
        count_down_text.disabled = False
        page.update()

    user_input_student_number = ft.TextField(
        hint_text='113316187', content_padding=ft.padding.only(top=10, left=10),
        width=220, height=30, text_size=15,
        bgcolor=ft.colors.PRIMARY_CONTAINER, border_color=ft.colors.WHITE,
        text_align='left', can_reveal_password=True)
    user_input_password = ft.TextField(
        hint_text='A123456789', content_padding=ft.padding.only(top=10, left=10),
        width=220, height=30, text_size=15,
        bgcolor=ft.colors.PRIMARY_CONTAINER, border_color=ft.colors.WHITE,
        text_align='left', password=True, can_reveal_password=True)
    user_input_delay_time = ft.TextField(
        label='冷卻時間', text_align='right', width=70, height=20, text_size=11
    )
    system_output = ft.TextField(
        multiline=True, height=200, value='')
    count_down_text = user_input_delay_time
    user_input_code1 = ft.TextField(
        label='代碼1', width=110, height=30, text_size=15,
        bgcolor=ft.colors.PRIMARY_CONTAINER, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_code2 = ft.TextField(
        label='代碼2', width=110, height=30, text_size=15,
        bgcolor=ft.colors.PRIMARY_CONTAINER, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_code3 = ft.TextField(
        label='代碼3', width=110, height=30, text_size=15,
        bgcolor=ft.colors.PRIMARY_CONTAINER, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_code4 = ft.TextField(
        label='代碼4', width=110, height=30, text_size=15,
        bgcolor=ft.colors.PRIMARY_CONTAINER, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_list = (user_input_code1, user_input_code2,
                       user_input_code3, user_input_code4)

    page.add(ft.Row([
        ft.Text(value='', width=200),
        count_down_text
    ]))
    page.add(ft.Row([
        ft.Text(value='學號：', width=50),
        user_input_student_number
    ]))
    page.add(ft.Row([
        ft.Text(value='密碼：', width=50),
        user_input_password
    ]))
    page.add(ft.Divider())
    page.add(ft.Text(value='課程代碼：', width=page.window_width - 30))
    page.add(ft.Row([
        user_input_code1,
        user_input_code2
    ]))
    page.add(ft.Row([
        user_input_code3,
        user_input_code4
    ]))

    page.add(ft.Row([
        ft.ElevatedButton(text='開始', on_click=handle_start_button_click,
                          width=page.window_width / 2 - 50),
        ft.ElevatedButton(text='停止', on_click=handle_stop_button_click,
                          width=page.window_width / 2 - 50)
    ]))
    page.add(system_output)


ft.app(target=main, assets_dir="assets")
