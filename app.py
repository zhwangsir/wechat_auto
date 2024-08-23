from wxauto import *
import time
import re
wx = WeChat()
def judgeChar(string,char):
    pattern = re.compile(char)
    if re.search(pattern,string):
        return True
    else:
        return False
def SelectContent(string):
    pattern = r"{}(\w+)".format("查询")
    matches = re.findall(pattern,string)
    for match in matches:
        return match
def auto_reply():
        msgs = wx.GetNextNewMessage()
        current = wx.CurrentChat()
        if msgs != {}:
            for msg in msgs.get(current):
                message = str(msg)
                if judgeChar(message,"查询"):
                    reContent = "https://cn.bing.com/search?q="+SelectContent(message)
                    wx.SendMsg(reContent)
                    print(message)
        time.sleep(2)

def New_friend():
    newfriend = wx.GetNewFriends()
    if newfriend != []:
        newfriend[0].Accept()
    else:
        wx.SwitchToChat()
def main():
    while True:
        auto_reply()
        time.sleep(10)
        New_friend()
if __name__ == "__main__":
    main()