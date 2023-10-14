from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from fake_useragent import UserAgent

from enviornment_check.webdriver_path import Webdriver_Path
from get_resource_path.resource_path import resource_path

import platform
import pandas as pd


class ClassRobber:
    def __init__(self, studentNum: str, password: str, code):
        self._web_driver_path = Webdriver_Path().webdriver_path
        self.ua = UserAgent(
            use_external_data=True,
            cache_path=resource_path('assets/browsers.json'),
            browsers=['chrome']
        )
        self.user_agent = self.ua.random

        self.webDriverOption = Options()
        self.webDriverOption.add_argument("--disable-notifications")
        self.webDriverOption.add_argument("--incognito")
        self.webDriverOption.add_argument("--headless")
        self.webDriverOption.add_argument("--disable-notifications")
        self.webDriverOption.add_argument(f"user-agent={self.user_agent}")
        self.webDriverService = Service(
            executable_path=self._web_driver_path)
        while True:
            try:
                self.chrome = webdriver.Chrome(
                    service=self.webDriverService, options=self.webDriverOption)
            except WebDriverException:
                tmp = Path(self._web_driver_path)
                if tmp.exists():
                    tmp.unlink()
                    tmp.parent.rmdir()
                    self._web_driver_path = Webdriver_Path().webdriver_path
            else:
                break

        self.studentNum = studentNum
        self.password = password
        self.code = code
        self.table = None

    def login(self) -> str:
        self.chrome.get(
            f"https://cos.tcu.edu.tw/ScasWebSite/Default.aspx?id={self.studentNum}")
        inputPassword = self.chrome.find_element("id", "logUser_Password")
        btn = self.chrome.find_element("id", "logUser_LoginButton")
        inputPassword.send_keys(self.password)
        btn.click()
        if self.chrome.current_url.__contains__("ErrorLoginIn"):
            msg = self.chrome.find_element("id", "lblMsg").text
            msg = f"登入錯誤!\n{msg}\n"
            self.chrome.close()
            return msg
        msg = "登入成功\n"
        return msg

    def logout(self):
        self.chrome.execute_script(
            "location.href = 'https://cos.tcu.edu.tw/ScasWebSite/LogOut.aspx'")
        self.chrome.close()

    def __searchClass(self):
        self.chrome.get(
            "https://cos.tcu.edu.tw/ScasWebSite/SelectAddCode.aspx")
        i = 0
        for c in self.code:
            t = self.chrome.find_element("id",
                                         f"ctl00_ContentPlaceHolder1_WcClassAddSwitch1_WcClassQueryCode1_txtCode{i}")
            t.send_keys(f"{c}")
            i += 1
        btn = self.chrome.find_element(
            "id", "ctl00_ContentPlaceHolder1_WcClassAddSwitch1_WcClassQueryCode1_btnQuery")
        btn.click()
        self.table = pd.read_html(self.chrome.page_source)
        self.table[30].columns = [c.replace(' ', '') for c in self.table[30]]
        self.table = self.table[30][["加選人數", "名額上限", "課程名稱"]]

    def __executeAddClass(self, MSG: str) -> str:
        executeTimes = 0
        for d in self.table.iterrows():
            executeTimes = 0
            className = d[1].loc["課程名稱"]
            index = d[1].name
            now = d[1].loc["加選人數"]
            maxNum = d[1].loc["名額上限"]
            if maxNum > now:
                self.chrome.execute_script(
                    f"javascript:__doPostBack('ctl00$ContentPlaceHolder1$WcClassListSelect1$gvStepFullClassList$ctl0{index + 3}$btnAdd','')")  # 執行加選
                alert = self.chrome.switch_to.alert
                alertMessage = alert.text.replace("\n\n", "\n")
                alert.accept()
                executeTimes += 1

                MSG += f"{index}: {now}/{maxNum}\n"
                MSG += f"{className}: {alertMessage}\n"
            else:
                MSG += f"{className}: 人數已滿\n"
        if executeTimes == 0:
            MSG += "所有課程皆無名額\n"
        return MSG

    def all(self) -> str:
        MSG = self.login()
        if MSG[0:4].__contains__("成功"):
            self.__searchClass()
            MSG = self.__executeAddClass(MSG)
            self.logout()
        MSG += '----------分割線-----------\n'
        return MSG
