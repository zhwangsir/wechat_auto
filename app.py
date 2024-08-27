#coding=utf-8
from wxauto import *
import time
import threading
import re
import pyautogui as gui
import pygetwindow as gw
from tkinter import *

wx = WeChat()
delay_seconds = 2
screenSize = gui.size()
def judgeChar(string, char):
    pattern = re.compile(char)
    return bool(re.search(pattern, string))

def SelectContent(string):
    string = string.strip().replace(" ", "")
    pattern = r"{}(\w+)".format("查询")
    matches = re.findall(pattern, string)
    return matches[0] if matches else None

def auto_reply():
    try:
        # msgs = wx.GetAllNewMessage()
        # current = wx.CurrentChat()
        # if msgs != {}:
        #     for key in msgs.keys():
        #         if key == current:
        session = wx.GetSessionList()
        for sess in session:
            if session[sess] != 0:
                wx.ChatWith(sess)
                myMessage = wx.GetAllMessage()
                for msg in myMessage:
                    if msg.type == "friend":
                        sender = msg.sender
                        # print(f'{sender.rjust(3)}：{msg.content}')
                        message = str(msg.content)
                        if judgeChar(message, "查询"):
                            reContent = SelectContent(message)
                            overMessage = pickup_code(reContent)
                            print(overMessage)
                            dangdang = f"单号：{overMessage.get('单号')}\n状态：{overMessage.get('状态')}\n快递公司：{overMessage.get('快递公司')}\n取件码：{overMessage.get('取件码')}\n入库时间：{overMessage.get('入库时间')}\n温馨提示：为避免同学快递丢失请速速取走您的包裹，如有取错请及时联系工作人员。\n快递问题投诉：19178467032"
                            wx.SendMsg(dangdang)
                            clearMessage()
            else:
                thread = threading.Timer(delay_seconds, New_friend)
                thread.start()
                thread.join()  # 确保线程完成后再继续执行下一个循环

        time.sleep(0.5)
    except Exception as e:
        print("Error in auto_reply:", e)

def clearMessage():
    try:
        wx.ChatWith(wx.CurrentChat())
        gui.rightClick()
        img_position("./source/delchat.png")
        time.sleep(0.5)
        gui.keyDown("tab")
        time.sleep(0.5)
        gui.press("enter")
        time.sleep(0.5)
        chrome_top()
        inputclear()
        extract_value("clear()")
    except Exception as e:
        print("Error in clearMessage:", e)

def New_friend():
    try:
        newfriend = wx.GetNewFriends()
        if newfriend:
            newfriend[0].Accept()
        else:
            wx.SwitchToChat()
    except Exception as e:
        print("Error in New_friend:", e)

def menuClick():
    img_position("./source/select.png")

def inputClick():
    check_input = gui.locateOnScreen("./source/input.png")
    check_input_center = gui.center(check_input)
    gui.moveTo(check_input_center)
    gui.moveTo(gui.position().x+200,gui.position().y)
    gui.click()

def inputclear():
    inputClick()
    gui.doubleClick()
    gui.press("BackSpace")
    time.sleep(0.5)

def moveClick(x, y):
    gui.moveTo(x, y, duration=0.5)
    gui.click()

def queryInput(text):
    inputClick()
    gui.typewrite(text)

def ctrlv():
    tkr = Tk()
    data = tkr.clipboard_get()
    return data
def img_position(path):
    check_chrome = gui.locateOnScreen(path)
    click_check_chrome = gui.center(check_chrome)
    gui.moveTo(click_check_chrome)
    gui.click()
def extract_value(code):
    gui.moveTo(screenSize.width/2.0, screenSize.height/1.5)
    gui.rightClick()
    img_position("./source/check.png")
    img_position("./source/console.png")
    gui.typewrite(f"copy({code})")
    time.sleep(0.5)
    gui.keyDown("enter")
def ctlc(ctn):
    try:
        if ctn == "num":
            gui.moveTo(screenSize.width / 2.0, screenSize.height / 1.5)
            gui.rightClick()
            img_position("./source/check.png")
            img_position("./source/console.png")
            gui.typewrite(f"let table = document.querySelector('table')")
            time.sleep(0.5)
            gui.keyDown("enter")
            extract_value("table.rows[1].children[1].children[0].children[0].innerHTML")
            return ctrlv()
        if ctn == "code":
            extract_value("table.rows[1].children[4].children[0].innerHTML")
            return ctrlv()
        if ctn == "name":
            extract_value("table.rows[1].children[2].children[0].children[0].innerHTML")
            return ctrlv()
        if ctn == "status":
            extract_value("table.rows[1].children[6].children[0].children[0].children[0].innerHTML")
            return ctrlv()
        if ctn == "mes":
            extract_value(f'table.rows[1].children[6].children[0].children[0].children[1].innerHTML+" "+table.rows[1].children[6].children[0].children[0].children[2].innerHTML')
            return ctrlv()
    except Exception as e:
        print("Error in ctlc:", e)

def chrome_top():
    windows = gw.getWindowsWithTitle("多多买菜 - Google Chrome")
    window = windows[0]
    window.maximize()
    window.activate()

def wechat_top():
    windows = gw.getWindowsWithTitle("微信")
    window = windows[0]
    window.activate()

def clickSearch():
    img_master = gui.locateOnScreen("demo.png")
    illf = gui.center(img_master)
    gui.click(illf[0], illf[1])

def NotFound():
    try:
        gui.locateOnScreen("nf.png")
        return "true"
    except:
        return "false"

def pickup_code(text):
    try:
        chrome_top()
        time.sleep(1)
        menuClick()
        inputclear()
        queryInput(text)
        clickSearch()
        # time.sleep(0.5)
        if NotFound() == "false":
            nnbb = context()
            return nnbb
        else:
            wx.SendMsg("未查到相关数据")
    except Exception as e:
        print("Error in pickup_code:", e)

def context():
    need = {
        "单号": ctlc('num'),
        "状态": ctlc('status'),
        "快递公司": ctlc('name'),
        "取件码": ctlc('code'),
        "入库时间": ctlc('mes'),
    }
    for ee in need:
        print(ee, need[ee])
    return need

def main():
    while True:
        auto_reply()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
    time.sleep(0.5)
