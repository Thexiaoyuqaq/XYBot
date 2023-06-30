import datetime
import re
import aiohttp

API_URL = "http://localhost:25010/"

def extract_id(text):
    pattern = r"id=(-?\d+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None
def get_ban_time(text):
    result = re.search(r'\b(\d+)\b$', text)
    if result:
        number = result.group(1)
        return number  # 12345
def get_ban_id(text):
    result = re.search(r'qq=(\d+)', text)
    if result:
        qq_number = result.group(1)
        return qq_number
def cn_u(text):
    return(text.encode('unicode_escape').decode())
async def get_group_info(event_message_Group_ID):#获取群信息API
    url = f"{API_URL}get_group_info?group_id={event_message_Group_ID}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
async def set_group_card(event_message_Group_ID,card,user_id):#设置群员名片
    url = f"{API_URL}set_group_card?group_id={event_message_Group_ID}&user_id={user_id}&card={card}" #&r
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
async def set_group_ban(event_message_Group_ID,user_id,time):#设置群员名片
    if user_id != 3443135327:
        url = f"{API_URL}set_group_ban?group_id={event_message_Group_ID}&user_id={user_id}&duration={time}" #&r
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rsjson = await response.json()
                return rsjson
async def get_group_member_info(event_message_Group_ID,userid):#获取群成员信息API
    url = f"{API_URL}get_group_member_info?group_id={event_message_Group_ID}&user_id={userid}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
async def send_group_forward_msg(event_message_Group_ID,event_message_Message):#发送合并消息
    url = f"{API_URL}send_group_forward_msg?group_id={event_message_Group_ID}&messages={event_message_Message}&no_cache=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
async def send_Groupmessage(event_message_Group_ID,event_message_Message_ID, event_message_Message,awa):#发送群消息API
    if awa == True:
        url = f"{API_URL}send_group_msg?group_id={event_message_Group_ID}&message=[CQ:reply,id=" + str(event_message_Message_ID) + "]" + event_message_Message
    if awa == False:
         url = f"{API_URL}send_group_msg?group_id={event_message_Group_ID}&message={event_message_Message}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            event_send_message = rsjson["message"]
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time,'%H:%M:%S')
            if event_send_message != -1:
                event_message_Group_Name = await get_group_info(event_message_Group_ID)
                event_message_Group_Name = event_message_Group_Name["data"]["group_name"]
                print("["+str(time_str) + "][信息][消息][发送][群聊] {} --To {}({})   ({})".format(event_message_Message,event_message_Group_Name,event_message_Group_ID,rsjson["data"]["message_id"]))
                return rsjson
            else:
                print("["+str(time_str) + "][信息][消息][发送][群聊] {} --To {}".format(event_message_Message,event_message_Group_ID))
                return "Error:无法发送"
async def set_GroupRequest(flag,type):#同意加群操作API
    url = f"{API_URL}set_group_add_request?approve=true&type={type}&flag={flag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
async def set_FreindRequest(flag):#同意好友操作API
    url = f"{API_URL}set_friend_add_request?approve=true&flag={flag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson
async def delete_msg(message_id):#撤回消息API
    url = f"{API_URL}delete_msg?message_id={message_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rsjson = await response.json()
            return rsjson