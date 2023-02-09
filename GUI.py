import tkinter
from tkinter import ttk

from threading import Timer

import customtkinter

from aha import ClassRobber

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.timer = None
        self.running = False
        self.delay = 10
        self.countDown = self.delay

        self.geometry("500x300")
        self.title("small example app")
        self.minsize(500, 300)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky='ew')

        self.frame.grid_rowconfigure('21', weight=5)
        self.frame.grid_columnconfigure(0, weight=3)
        self.frame.grid_columnconfigure(1, weight=8)
        self.frame.grid_columnconfigure(2, weight=1)
        self.countDownLabel = customtkinter.CTkLabel(master=self.frame, text='執行倒數：')
        self.countDownLabel.grid(row=0, column=0, columnspan=2, sticky='e')
        self.countDownTimeLabel = tkinter.Label(self.frame, text=str(self.countDown))
        self.countDownTimeLabel.grid(row=0, column=2)

        self.inUsernameLabel = customtkinter.CTkLabel(master=self.frame, text="學號: ")
        self.inUsernameLabel.grid(row=1, column=0, sticky='w')
        self.inUsername = customtkinter.CTkEntry(self.frame, placeholder_text="119316199")
        self.inUsername.grid(row=1, column=1, sticky='we', columnspan=2)
        self.inPasswordLabel = customtkinter.CTkLabel(master=self.frame, text="密碼: ")
        self.inPasswordLabel.grid(row=2, column=0, sticky='w')
        self.inPassword = customtkinter.CTkEntry(self.frame, placeholder_text="A12345678", show='*')
        self.inPassword.grid(row=2, column=1, sticky='we', columnspan=2)

        self.btnFrame = customtkinter.CTkFrame(self)
        self.btnFrame.grid(row=1, column=0)
        self.line = ttk.Separator(master=self.btnFrame, orient='horizontal')
        self.line.grid(row=0, column=0, sticky='ew', columnspan=2, pady=5)
        self.startbtn = customtkinter.CTkButton(self.btnFrame, text="開始", command=self.start)
        self.startbtn.grid(row=1, column=0)
        self.stopbtn = customtkinter.CTkButton(self.btnFrame, text="停止", command=self.stop)
        self.stopbtn.grid(row=1, column=1)

        self.frame.configure(width=self.btnFrame.winfo_width())

    def start(self):
        self.startbtn.configure(state=tkinter.DISABLED)
        self.rob()
        self.running = True
        self.timer = self.Timers(1, self.countDownTime, )
        self.timer.start()

    def stop(self):
        self.startbtn.configure(state=tkinter.NORMAL)
        if self.running:
            self.running = False
            self.timer.cancel()
        self.countDown = self.delay
        self.countDownTimeLabel.configure(text=str(self.delay))
        self.frame.update()

    def rob(self):
        robber = ClassRobber(studentNum=self.inUsername.get(), password=self.inPassword.get(), code=(901098, 901095))
        print(robber.all())

    def countDownTime(self):
        if self.running and self.timer is not None:
            if self.countDown == 0:
                self.rob()
                self.countDown = self.delay
            else:
                self.countDown -= 1
                self.countDownTimeLabel.configure(text=str(self.countDown))
                self.frame.update()

    class Timers(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)
                print('running')


if __name__ == '__main__':
    app = App()
    app.mainloop()
