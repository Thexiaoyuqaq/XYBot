from Api import *

async def cmd_Log(event_Time,event_Post_Type,event_original):
    if event_Post_Type == "notice":
        print(str(event_Time) + "[信息][事件][接收]" + str(event_original))
    if event_Post_Type == "message":
        event_Message_From = event_original["message_type"]
        if event_Message_From == "group":
            event_message_Self_ID = event_original["user_id"]
            event_message_Self_Name = event_original["sender"]["nickname"]
            event_message_Self_Role = event_original["sender"]["role"]
            event_message_Messages = event_original["message"]
            event_message_Group_ID = event_original["group_id"]
            event_message_Message_ID = event_original["message_id"]
            event_message_Group_Name = await get_group_info(event_message_Group_ID)
            event_message_Group_Name = event_message_Group_Name["data"]["group_name"]
            print(str(event_Time) + "[信息][消息][接收][群聊]["+str(event_message_Group_Name) + "](" + str(event_message_Group_ID)+ ") [" + str(event_message_Self_Role) + "]" + str(event_message_Self_Name) + "(" + str(event_message_Self_ID) + ")" + ": " + str(event_message_Messages) + "   (" + str(event_message_Message_ID) + ")")
        if event_Message_From == "private":
            event_message_Self_Name = event_original["sender"]["nickname"]
            event_message_Messages = event_original["message"]
            event_message_Self_ID = event_original["user_id"]
            print(str(event_Time) + "[信息][消息][接收][好友] " + event_message_Self_Name +"(" +str(event_message_Self_ID) + ") : " + str(event_message_Messages))