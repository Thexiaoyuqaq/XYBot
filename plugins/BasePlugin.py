class BasePlugin:
    @staticmethod
    async def Start():
        pass

    @staticmethod
    async def GroupMessage(event_original):
        pass

    @staticmethod
    async def FriendMessage(event_original):
        pass

    @staticmethod
    async def Request(event_request_from, event_original):
        pass

    @staticmethod
    async def Notice_Group_join(event_original):
        pass

    @staticmethod
    async def Notice_Group_leave(event_original):
        pass
