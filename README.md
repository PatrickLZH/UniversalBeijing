登录用户：
/auth/login
POST：
{
    "mobile":"13712345678",
    "mypassword":"abcd"
}

创建会话：
/message
POST：
{
    "user_id":1,
    "session_id":null,
    "content":"你好！"
}

会话下提问：
/message
POST：
{
    "user_id":1,
    "session_id":150,
    "content":"我问的上一个问题是什么？"
}

获取会话列表：
/message/session
POST:
{
    "session_id":150
}

获取用户所有会话列表：
/message/all
POST:
{
    "user_id":1
}

获取文件列表：
/files
GET:

上传文件：
/files
POST:
formdata：
"directory": "docx",
"file_name": "探索护照介绍.docx",
"file":<上传具体的文件>

删除文件：
/files
DELETE:
{
    "directory": "docx",
    "file_name": "探索护照介绍.docx",
    "manage_id": 7,
}

点赞：
/islike
POST:
{
    "msg_id":42,
    "sender_type":"assistant",
    "islike":1,
    "feedback":null
}

点踩：
/islike
POST:
{
    "msg_id":42,
    "sender_type":"assistant",
    "islike":-1,
    "feedback":"test"
}

下载文件：
/documents/<directory>/<filename>
GET: