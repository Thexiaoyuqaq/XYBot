from Api import send_Groupmessage
from Api import send_FriendMessage


class Plugin:
    @staticmethod
    async def GroupMessage(event_original):
        group_id = event_original["group_id"]
        message = event_original["message"]
        await send_Groupmessage(Group_ID=group_id, Message_ID=0, Message=message, awa=False)

    @staticmethod
    async def FriendMessage(event_original):
        user_id = event_original["user_id"]
        message = event_original["message"]
        await send_FriendMessage(user_id=user_id, message=message)
