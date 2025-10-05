from utils.Manager.Log.notice import log_notice_event
from utils.Manager.Log.message import log_message_event
from utils.Manager.Log.request import log_request_event
from utils.Manager.Log_Manager import Log

async def cmd_Log(post_type, original_event):
    logger = Log()

    if post_type == "事件":
        await log_notice_event(logger, original_event)
    elif post_type == "消息":
        event_Message_From = original_event.get("message_type", "")
        if event_Message_From == "群聊":
            await log_message_event(logger, original_event, "group_message")
        elif event_Message_From == "好友":
            await log_message_event(logger, original_event, "friend_message")
    elif post_type == "请求":
        await log_request_event(logger, original_event, "request")
    else:
        logger.info(f"[未知] {original_event}", flag="Log")