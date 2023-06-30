from Api import *


class Plugin:
    async def Notice_join(self,event_original):#加群事件
        pass
    async def Notice_leave(self,event_original):#退群事件
        pass
    async def Requst(event_Requst_From,event_original):#请求事件 如:好友申请和加群申请
        event_Requst_From = event_original["request_type"]#请求的来源
        if event_Requst_From == "friend":#好友
            pass
        if event_Requst_From == "group":#群聊
            pass
    async def GroupMessage(self, event_original): #消息事件
        pass