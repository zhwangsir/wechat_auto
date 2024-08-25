from wxauto import *
import time
import threading
import re
import pyautogui as gui
import pygetwindow as gw
from tkinter import *

wx = WeChat()
delay_seconds = 60
def judgeChar(string,char):
    pattern = re.compile(char)
    if re.search(pattern,string):
        return True
    else:
        return False

def SelectContent(string):
    string = string.strip().replace(" ","")
    pattern = r"{}(\w+)".format("查询")
    matches = re.findall(pattern,string)
    for match in matches:
        return match
def auto_reply():
    try:
        msgs = wx.GetAllNewMessage()
        psmes ="正在为您查询\n请稍后......\n如长时间未响应请重新查询"
        current = wx.CurrentChat()
        if msgs != {}:
            for key in msgs.keys():
                if key == current:
                    message = str(msgs.get(key)[-1])
                    if judgeChar(message,"查询"):
                        reContent = SelectContent(message)
                        overMessage = pickup_code(reContent)
                        dangdang = f"单号：{overMessage.get('单号')}\n状态：{overMessage.get('状态')}\n快递公司：{overMessage.get('快递公司')}\n取件码：{overMessage.get('取件码')}\n入库时间：{overMessage.get('入库时间')}\n温馨提示：为避免同学快递丢失请速速取走您的包裹，如有取错请及时联系工作人员。\n快递问题投诉：19178467032"
                        wx.SendMsg(dangdang)
        time.sleep(0.5)
    except Exception as e:
        print("Error in auto_reply:", e)


def New_friend():
    try:
        newfriend = wx.GetNewFriends()
        if newfriend != []:
            newfriend[0].Accept()
        else:
            wx.SwitchToChat()
    except Exception as e:
        print("Error in New_friend:", e)

def menuClick():
    moveClick(74,409)

def inputClick():
    moveClick(514,118)

def inputclear():
    inputClick()
    gui.doubleClick()
    gui.press("BackSpace")
    time.sleep(0.5)

def moveClick(x,y):
    gui.moveTo(x, y, duration=0.5)
    gui.click()

def queryInput(text):
    inputClick()
    gui.typewrite(text)

def ctrlv():
    tkr = Tk()
    data = tkr.clipboard_get()
    return data

def ctlc(ctn):
    try:
        if ctn == "num":
            gui.moveTo(480, 510)
            gui.dragRel(-200, 0, duration=0.5)
            gui.hotkey('ctrl', 'c')
            return ctrlv()
        elif ctn == "code":
            gui.moveTo(961, 510)
            gui.dragRel(-120, 0, duration=0.5)
            gui.hotkey('ctrl', 'c')
            return ctrlv()
        elif ctn == "name":
            gui.moveTo(685, 510)
            gui.dragRel(-120, 0, duration=0.5)
            gui.hotkey('ctrl', 'c')
            return ctrlv()
        elif ctn == "status":
            gui.moveTo(1250, 555)
            gui.dragRel(-80, -40, duration=0.5)
            gui.hotkey('ctrl', 'c')
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
        return True
    except:
        return False

def pickup_code(text):
    try:
        chrome_top()
        menuClick()
        inputclear()
        queryInput(text)
        clickSearch()
        time.sleep(0.5)
        if NotFound():
            wx.SendMsg("未查到相关数据")
        else:
            nnbb = context()
            return nnbb
    except Exception as e:
        print("Error in pickup_code:", e)

def context():
    status = ctlc('status').replace("\n", "")
    need = {
        "单号":ctlc('num'),
        "状态":status[:3],
        "快递公司":ctlc('name'),
        "取件码":ctlc('code'),
        "入库时间":status[3:],
    }
    return need

def main():
    while True:
        auto_reply()
        thread = threading.Timer(delay_seconds,New_friend())
        thread.start()
if __name__ == "__main__":
    main()
