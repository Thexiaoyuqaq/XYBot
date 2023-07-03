import requests
import urllib.parse
# 自己改
cqhttp_url = None


def get_response_text(endpoint: str, params: dict = ""):
    """
    请求一个 API
    @param endpoint:终结点
    @param params:所需参数
    """
    params = params
    # /终结点?参数名=参数值&参数名=参数值......
    """
    GET无法传入复杂的数据结构, 
    一些需要嵌套数据的 API 是无法通过 HTTP GET 来调用的,
    例如 send_group_forward_msg 接口
    """
    url = cqhttp_url + f"{endpoint}?" + urlencode(params)
    response = requests.get(url=url)
    """
    响应说明
    使用 HTTP 调用 API 的时候, HTTP 的响应状态码:
    401	access token 未提供
    403	access token 不符合
    406	Content-Type 不支持 (非 application/json 或 application/x-www-form-urlencoded
    404	API 不存在
    200	除上述情况外所有情况 (具体 API 调用是否成功, 需要看 API 的 响应数据
    """
    return response.text


class CQApi:
    class Bot:
        """
        有关 Bot 账号的相关 API
        """

        @staticmethod
        def get_login_info():
            """
            获取登录号信息
            """
            return get_response_text(endpoint="get_login_info")

        @staticmethod
        def set_qq_profile(nickname: str, company: str, email: str, college: str, personal_note: str):
            """
            设置登录号资料
            @param nickname:名称
            @param company:公司
            @param email:邮箱
            @param college:学校
            @param personal_note:个人说明
            """
            params = {
                'nickname': nickname,
                'company': company,
                'email': email,
                'college': college,
                'personal_note': personal_note,
            }
            return get_response_text(endpoint="set_qq_profile", params=params)

        @staticmethod
        def qidian_get_account_info():
            """
            获取企点账号信息，该API只有企点协议可用
            """
            return get_response_text(endpoint="qidian_get_account_info")

        @staticmethod
        def _get_model_show(model: str):
            """
            获取在线机型
            @param model:机型名称
            """
            params = {
                'model': model,
            }
            return get_response_text(endpoint="_get_model_show", params=params)

        @staticmethod
        def _set_model_show(model: str, model_show: str):
            """
            设置在线机型
            @param model:机型名称
            @param model_show:
            """
            params = {
                'model': model,
                'model_show': model_show,
            }
            return get_response_text(endpoint="_set_model_show", params=params)

        @staticmethod
        def get_online_clients(no_cache: bool):
            """
            获取当前账号在线客户端列表
            @param no_cache:是否无视缓存
            """
            params = {
                'no_cache': no_cache,
            }
            return get_response_text(endpoint="get_online_clients", params=params)

    class FriendInfo:
        """
        好友信息相关 API
        """

        @staticmethod
        def get_stranger_info(user_id: int, no_cache: bool = False):
            """
            获取陌生人信息
            @param user_id:QQ 号
            @param no_cache:是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
            """
            params = {
                'user_id': user_id,
                'no_cache': no_cache,
            }
            return get_response_text(endpoint="get_stranger_info", params=params)

        @staticmethod
        def get_friend_list():
            """
            获取好友列表
            """
            return get_response_text(endpoint="get_friend_list")

        @staticmethod
        def get_unidirectional_friend_list():
            """
            获取单向好友列表
            """
            return get_response_text(endpoint="get_unidirectional_friend_list")

    class FriendHandler:
        """
        好友操作 API
        """

        @staticmethod
        def delete_friend(user_id: int):
            """
            删除好友
            @param user_id:好友 QQ 号
            """
            params = {
                'user_id': user_id,
            }
            return get_response_text(endpoint="delete_friend", params=params)

        @staticmethod
        def delete_unidirectional_friend(user_id: int):
            """
            删除单向好友
            @param user_id:单向好友QQ号
            """
            params = {
                'user_id': user_id,
            }
            return get_response_text(endpoint="delete_unidirectional_friend", params=params)

    class Message:
        """
        有关消息操作的 API
        """

        @staticmethod
        def send_private_msg(user_id: int, group_id: int, message: str, auto_escape: bool = False):
            """
            发送私聊消息
            @param user_id:对方 QQ 号
            @param group_id:主动发起临时会话时的来源群号(可选, 机器人本身必须是管理员/群主)
            @param message:要发送的内容
            @param auto_escape:消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
            """
            params = {
                'user_id': user_id,
                'group_id': group_id,
                'message': message,
                'auto_escape': auto_escape,
            }
            return get_response_text(endpoint="send_private_msg", params=params)

        @staticmethod
        def send_group_msg(group_id: int, message: str, auto_escape: bool = False):
            """
            发送群聊消息
            @param group_id:群号
            @param message:要发送的内容
            @param auto_escape:消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
            """
            params = {
                'group_id': group_id,
                'message': message,
                'auto_escape': auto_escape,
            }
            return get_response_text(endpoint="send_group_msg", params=params)

        @staticmethod
        def send_msg(user_id: int = None, group_id: int = None, message: str = "", message_type: str = "",
                     auto_escape: bool = False):
            """
            发送消息
            @param user_id:对方 QQ 号 ( 消息类型为 private 时需要 )
            @param group_id:群号 ( 消息类型为 group 时需要 )
            @param message:要发送的内容
            @param message_type:消息类型, 支持 private、group , 分别对应私聊、群组, 如不传入, 则根据传入的 *_id 参数判断
            @param auto_escape:	消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
            """
            if message_type == "" and user_id is not None and group_id is None:
                message_type = "private"
            elif message_type == "" and user_id is not None and group_id is not None:
                message_type = "private"
            elif message_type == "" and group_id is not None and user_id is None:
                message_type = "group"
            if message_type == "private":
                params = {
                    'user_id': user_id,
                    'message': message,
                    'group_id': group_id,
                    'auto_escape': auto_escape,
                }
                return get_response_text(endpoint="send_private_msg", params=params)

            elif message_type == "group":
                params = {
                    'group_id': group_id,
                    'message': message,
                    'auto_escape': auto_escape,
                }
                return get_response_text(endpoint="send_group_msg", params=params)

        @staticmethod
        def get_msg(message_id: int):
            """
            获取消息
            @param message_id:消息 ID
            """
            params = {
                'message_id': message_id,
            }
            return get_response_text(endpoint="get_msg", params=params)

        @staticmethod
        def delete_msg(message_id: int):
            """
            撤回消息
            @param message_id:消息 ID
            """
            params = {
                'message_id': message_id,
            }
            return get_response_text(endpoint="delete_msg", params=params)

        @staticmethod
        def mark_msg_as_read(message_id: int):
            """
            标记消息已读
            @param message_id: 消息 ID
            """
            params = {
                'message_id': message_id,
            }
            return get_response_text(endpoint="mark_msg_as_read", params=params)

        @staticmethod
        def get_forward_msg(message_id: int):
            """
            获取合并转发内容
            @param message_id:消息 ID
            """
            params = {
                'message_id': message_id,
            }
            return get_response_text(endpoint="get_forward_msg", params=params)

        @staticmethod
        def send_group_forward_msg(group_id: int, messages: list):
            """
            发送合并转发 ( 群聊 )
            @param group_id:群号
            @param messages:自定义转发消息
            """
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                'group_id': group_id,
                'messages': messages,
            }
            response = requests.post(url=cqhttp_url + "/send_group_forward_msg", json=params, headers=headers)
            return response.text

        @staticmethod
        def send_private_forward_msg(user_id: int, messages: list):
            """
            发送合并转发 ( 好友 )
            @param user_id:好友QQ号
            @param messages:自定义转发消息
            """
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                'user_id': user_id,
                'messages': messages,
            }
            response = requests.post(url=cqhttp_url + "/send_private_forward_msg", json=params, headers=headers)
            return response.text

        @staticmethod
        def get_group_msg_history(message_seq: int, group_id: int):
            """
            获取群消息历史记录
            @param message_seq:起始消息序号, 可通过 get_msg 获得
            @param group_id:群号
            """
            params = {
                'message_seq': message_seq,
                'group_id': group_id,
            }
            return get_response_text(endpoint="get_group_msg_history", params=params)

    class Image:
        """
        图片相关 API
        """

        @staticmethod
        def get_image(file: str):
            """
            获取图片信息
            @param file:图片缓存文件名
            """
            params = {
                'file': file,
            }
            return get_response_text(endpoint="get_image", params=params)

        @staticmethod
        def can_send_image():
            """
            检查是否可以发送图片
            """
            return get_response_text(endpoint="can_send_image")

        @staticmethod
        def ocr_image(image: str):
            """
            图片 OCR
            @param image:图片ID
            """
            params = {
                'image': image,
            }
            return get_response_text(endpoint=".ocr_image", params=params)

    class Voice:
        """
        语音相关 API
        """

        @staticmethod
        def get_record(file: str, out_format: str):
            """
            获取语音
            @param file:收到的语音文件名（消息段的 file 参数）, 如 0B38145AA44505000B38145AA4450500.silk
            @param out_format:要转换到的格式, 目前支持 mp3、amr、wma、m4a、spx、ogg、wav、flac
            """
            params = {
                'file': file,
                'out_format': out_format,
            }
            return get_response_text(endpoint="get_record", params=params)

        @staticmethod
        def can_send_record():
            """
            检查是否可以发送语音
            """
            return get_response_text(endpoint="can_send_record")

    class Request:
        """
        上报处理相关 API
        """

        @staticmethod
        def set_friend_add_request(flag: str, approve: bool = True, remark: str = ""):
            """
            处理加好友请求
            @param flag:加好友请求的 flag（需从上报的数据中获得）
            @param approve:是否同意请求
            @param remark:添加后的好友备注（仅在同意时有效）
            """
            params = {
                'flag': flag,
                'approve': approve,
                'remark': remark,
            }
            return get_response_text(endpoint="set_friend_add_request", params=params)

        @staticmethod
        def set_group_add_request(flag: str, sub_type: str, approve: bool = True, reason: str = ""):
            """
            处理加群请求／邀请
            @param flag:加群请求的 flag（需从上报的数据中获得）
            @param sub_type:add 或 invite, 请求类型（需要和上报消息中的 sub_type 字段相符）
            @param approve:是否同意请求／邀请
            @param reason:拒绝理由（仅在拒绝时有效）
            """
            params = {
                'flag': flag,
                'sub_type': sub_type,
                'approve': approve,
                'reason': reason,
            }
            return get_response_text(endpoint="set_group_add_request", params=params)

    class GroupInfo:
        """
        群信息相关 API
        """

        @staticmethod
        def get_group_info(group_id: int, no_cache: bool = False):
            """
            获取群信息
            @param group_id:群号
            @param no_cache:是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
            """
            params = {
                'group_id': group_id,
                'no_cache': no_cache,
            }
            return get_response_text(endpoint="get_group_info", params=params)

        @staticmethod
        def get_group_list(no_cache: bool = False):
            """
            获取群列表
            @param no_cache:是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
            """
            params = {
                'no_cache': no_cache,
            }
            return get_response_text(endpoint="get_group_list", params=params)

        @staticmethod
        def get_group_member_info(group_id: int, user_id: int, no_cache: bool = False):
            """
            获取群成员信息
            @param group_id:群号
            @param user_id:QQ 号
            @param no_cache:是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
            """
            params = {
                'group_id': group_id,
                'user_id': user_id,
                'no_cache': no_cache,
            }
            return get_response_text(endpoint="get_group_member_info", params=params)

        @staticmethod
        def get_group_member_list(group_id: int, no_cache: bool = False):
            """
            获取群成员列表
            @param group_id:群号
            @param no_cache:是否不使用缓存（使用缓存可能更新不及时, 但响应更快）
            """
            params = {
                'group_id': group_id,
                'no_cache': no_cache,
            }
            return get_response_text(endpoint="get_group_member_list", params=params)

        @staticmethod
        def get_group_honor_info(group_id: int, honor_type: str):
            """
            获取群荣誉信息
            @param group_id:群号
            @param honor_type:要获取的群荣誉类型, 可传入 talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据, 或传入 all 获取所有数据
            """
            params = {
                'group_id': group_id,
                'honor_type': honor_type,
            }
            return get_response_text(endpoint="get_group_honor_info", params=params)

        @staticmethod
        def get_group_system_msg():
            """
            获取群系统消息
            """
            return get_response_text(endpoint="get_group_system_msg")

        @staticmethod
        def get_essence_msg_list(group_id: int):
            """
            获取精华消息列表
            @param group_id:群号
            """
            params = {
                'group_id': group_id,
            }
            return get_response_text(endpoint="get_essence_msg_list", params=params)

        @staticmethod
        def get_group_at_all_remain(group_id: int):
            """
            获取群 @全体成员 剩余次数
            @param group_id:群号
            """
            params = {
                'group_id': group_id,
            }
            return get_response_text(endpoint="get_group_at_all_remain", params=params)

    class GroupSet:
        """
        群设置相关 API
        """

        @staticmethod
        def set_group_name(group_id: int, group_name: str):
            """
            设置群名
            @param group_id:群号
            @param group_name:新群名
            """
            params = {
                'group_id': group_id,
                'group_name': group_name,
            }
            return get_response_text(endpoint="set_group_name", params=params)

        @staticmethod
        def set_group_portrait(group_id: int, file: str, cache: int):
            """
            设置群头像
            @param group_id:群号
            @param file:图片文件名
            @param cache:表示是否使用已缓存的文件
            """
            params = {
                'group_id': group_id,
                'file': file,
                'cache': cache,
            }
            return get_response_text(endpoint="set_group_portrait", params=params)

        @staticmethod
        def set_group_admin(group_id: int, user_id: int, enable: bool = True):
            """
            设置群管理员
            @param group_id:群号
            @param user_id:要设置管理员的 QQ 号
            @param enable:true 为设置, false 为取消
            """
            params = {
                'group_id': group_id,
                'user_id': user_id,
                'enable': enable,
            }
            return get_response_text(endpoint="set_group_admin", params=params)

        @staticmethod
        def set_group_card(group_id: int, user_id: int, card: str = ""):
            """
            设置群名片 ( 群备注 )
            @param group_id:群号
            @param user_id:要设置的 QQ 号
            @param card:群名片内容, 不填或空字符串表示删除群名片
            """
            params = {
                'group_id': group_id,
                'user_id': user_id,
                'card': card,
            }
            return get_response_text(endpoint="set_group_card", params=params)

        @staticmethod
        def set_group_special_title(group_id: int, user_id: int, special_title: str = "", duration: int = -1):
            """
            设置群组专属头衔
            @param group_id:群号
            @param user_id:要设置的 QQ 号
            @param special_title:专属头衔, 不填或空字符串表示删除专属头衔
            @param duration:专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果,
                            可能是只有某些特殊的时间长度有效, 有待测试
            """
            params = {
                'group_id': group_id,
                'user_id': user_id,
                'special_title': special_title,
                'duration': duration,
            }
            return get_response_text(endpoint="set_group_special_title", params=params)

    class GroupHandler:
        """
        群操作相关 API
        """

        @staticmethod
        def set_group_ban(group_id: int, user_id: int, duration: int = 30 * 60):
            """
            群单人禁言
            @param group_id:群号
            @param user_id:要禁言的 QQ 号
            @param duration:禁言时长, 单位秒, 0 表示取消禁言
            """
            params = {
                'group_id': group_id,
                'user_id': user_id,
                'duration': duration,
            }
            return get_response_text(endpoint="set_group_ban", params=params)

        @staticmethod
        def set_group_whole_ban(group_id: int, enable: bool = True):
            """
            群全员禁言
            @param group_id:群号
            @param enable:是否禁言
            """
            params = {
                'group_id': group_id,
                'enable': enable,
            }
            return get_response_text(endpoint="set_group_whole_ban", params=params)

        @staticmethod
        def set_group_anonymous_ban(group_id: int, anonymous_flag: str, duration: int = 30 * 60):
            """
            群匿名用户禁言
            @param group_id:群号
            @param anonymous_flag:要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
            @param duration:禁言时长, 单位秒, 无法取消匿名用户禁言
            """
            params = {
                'group_id': group_id,
                'anonymous_flag': anonymous_flag,
                'duration': duration,
            }
            return get_response_text(endpoint="set_group_anonymous_ban", params=params)

        @staticmethod
        def set_essence_msg(message_id: int):
            """
            设置精华消息
            @param message_id:消息ID
            """
            params = {
                'message_id': message_id,
            }
            return get_response_text(endpoint="set_essence_msg", params=params)

        @staticmethod
        def delete_essence_msg(message_id: int):
            """
            移出精华消息
            @param message_id:消息ID
            """
            params = {
                'message_id': message_id,
            }
            return get_response_text(endpoint="delete_essence_msg", params=params)

        @staticmethod
        def send_group_sign(group_id: int):
            """
            群打卡
            @param group_id:群号
            """
            params = {
                'group_id': group_id,
            }
            return get_response_text(endpoint="send_group_sign", params=params)

        @staticmethod
        def set_group_anonymous(group_id: int, enable: bool = True):
            """
            群设置匿名
            @param group_id:群号
            @param enable:是否允许匿名聊天
            """
            params = {
                'group_id': group_id,
                'enable': enable,
            }
            return get_response_text(endpoint="set_group_anonymous", params=params)

        @staticmethod
        def send_group_notice(group_id: int, content: str, image: str):
            """
            发送群公告
            @param group_id:群号
            @param content:公告内容
            @param image:图片路径（可选）
            """
            params = {
                'group_id': group_id,
                'content': content,
                'image': image,
            }
            return get_response_text(endpoint="_send_group_notice", params=params)

        @staticmethod
        def get_group_notice(group_id: int):
            """
            获取群公告
            @param group_id:群号
            """
            params = {
                'group_id': group_id,
            }
            return get_response_text(endpoint="_get_group_notice", params=params)

        @staticmethod
        def set_group_kick(group_id: int, user_id: int, reject_add_request: bool = False):
            """
            群组踢人
            @param group_id:群号
            @param user_id:要踢的 QQ 号
            @param reject_add_request:拒绝此人的加群请求
            @return:
            """
            params = {
                'group_id': group_id,
                'user_id': user_id,
                'reject_add_request': reject_add_request,
            }
            return get_response_text(endpoint="set_group_kick", params=params)

        @staticmethod
        def set_group_leave(group_id: int, is_dismiss: bool = False):
            """
            退出群组
            @param group_id:群号
            @param is_dismiss:是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散
            """
            params = {
                'group_id': group_id,
                'is_dismiss': is_dismiss,
            }
            return get_response_text(endpoint="set_group_leave", params=params)

    class File:
        """
        文件相关 API
        """

        @staticmethod
        def upload_group_file(group_id: int, file: str, name: str, folder: str):
            """
            上传群文件
            @param group_id:群号
            @param file:本地文件路径
            @param name:储存名称
            @param folder:父目录ID
            """
            params = {
                'group_id': group_id,
                'file': file,
                'name': name,
                'folder': folder,

            }
            return get_response_text(endpoint="upload_group_file", params=params)

        @staticmethod
        def delete_group_file(group_id: int, file_id: str, busid: int):
            """
            删除群文件
            @param group_id:群号
            @param file_id:文件ID 参考 File 对象
            @param busid:文件类型 参考 File 对象
            """
            params = {
                'group_id': group_id,
                'file_id': file_id,
                'busid': busid,

            }
            return get_response_text(endpoint="delete_group_file", params=params)

        @staticmethod
        def create_group_file_folder(group_id: int, name: str, parent_id: str):
            """
            创建群文件文件夹
            @param group_id:群号
            @param name:文件夹名称
            @param parent_id:仅能为 '/'
            """
            params = {
                'group_id': group_id,
                'name': name,
                'parent_id': parent_id,

            }
            return get_response_text(endpoint="create_group_file_folder", params=params)

        @staticmethod
        def delete_group_folder(group_id: int, folder_id: str):
            """
            删除群文件文件夹
            @param group_id:群号
            @param folder_id:文件夹ID 参考 Folder 对象
            """
            params = {
                'group_id': group_id,
                'folder_id': folder_id,

            }
            return get_response_text(endpoint="delete_group_folder", params=params)

        @staticmethod
        def get_group_file_system_info(group_id: int):
            """
            获取群文件系统信息
            @param group_id:群号
            """
            params = {
                'group_id': group_id,

            }
            return get_response_text(endpoint="get_group_file_system_info", params=params)

        @staticmethod
        def get_group_root_files(group_id: int):
            """
            获取群根目录文件列表
            @param group_id:群号
            """
            params = {
                'group_id': group_id,

            }
            return get_response_text(endpoint="get_group_root_files", params=params)

        @staticmethod
        def get_group_files_by_folder(group_id: int, folder_id: str):
            """
            获取群子目录文件列表
            @param group_id:群号
            @param folder_id:文件夹ID 参考 Folder 对象
            """
            params = {
                'group_id': group_id,
                'folder_id': folder_id,

            }
            return get_response_text(endpoint="get_group_files_by_folder", params=params)

        @staticmethod
        def get_group_file_url(group_id: int, file_id: str, busid: int):
            """
            获取群文件资源链接
            @param group_id:群号
            @param file_id:文件ID 参考 File 对象
            @param busid:文件类型 参考 File 对象
            """
            params = {
                'group_id': group_id,
                'file_id': file_id,
                'busid': busid,

            }
            return get_response_text(endpoint="get_group_file_url", params=params)

        @staticmethod
        def upload_private_file(user_id: int, file: str, name: str):
            """
            上传私聊文件
            @param user_id:对方 QQ 号
            @param file:本地文件路径
            @param name:文件名称
            """
            params = {
                'user_id': user_id,
                'file': file,
                'name': name,

            }
            return get_response_text(endpoint="upload_private_file", params=params)

    class GoCqHttp:
        """
        Go-CqHttp 相关
        """

        @staticmethod
        def get_version_info():
            """
            获取版本信息
            """
            return get_response_text(endpoint="get_version_info")

        @staticmethod
        def get_status():
            """
            获取状态
            """
            return get_response_text(endpoint="get_status")

        @staticmethod
        def reload_event_filter(file: str):
            """
            重载事件过滤器
            @param file:事件过滤器文件
            """
            params = {
                'file': file,
            }
            return get_response_text(endpoint="reload_event_filter", params=params)

        @staticmethod
        def download_file(url: str, thread_count: int, headers: list):
            """
            下载文件到缓存目录
            @param url:链接地址
            @param thread_count:下载线程数
            @param headers:自定义请求头
            """
            params = {
                'url': url,
                'thread_count': thread_count,
                'headers': headers,
            }
            return get_response_text(endpoint="reload_event_filter", params=params)

        @staticmethod
        def check_url_safely(url: str):
            """
            检查链接安全性
            @param url:需要检查的链接
            """
            params = {
                'url': url,
            }
            return get_response_text(endpoint="check_url_safely", params=params)