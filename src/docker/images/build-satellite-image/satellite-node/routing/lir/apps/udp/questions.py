# ------------- QUESTIONS FOR UDP CLIENT -------------
QUESTION_FOR_PROTOCOL = [
    {
        "type": "list",
        "name": "protocol",
        "message": "请输入要使用的网络层协议: ",
        "choices": ["IP", "LIR"]
    }
]

QUESTION_FOR_DESTINATION_PORT = [
    {
        "type": "input",
        "name": "port",
        "message": "请输入目的端口: ",
        "default": "31313"
    }
]

QUESTION_FOR_NUMBER_OF_DESTINATIONS = [
    {
        "type": "list",
        "name": "count",
        "message": "请输入目的节点的数量: ",
        "choices": ["2", "3", "4"]
    }
]

QUESTION_FOR_LIR_TRANSMISSION_PATTERN = [
    {
        "type": "list",
        "name": "transmission_pattern",
        "message": "请选择传输的模式: ",
        "choices": ["unicast", "multicast"]
    }
]
# ------------- QUESTIONS FOR UDP CLIENT -------------

# -------------- QUESTIONS FOR HANDLER ---------------
QUESTION_FOR_DESTINATION = [
    {
        "type": "list",
        "name": "destination",
        "message": "请选择目的节点: "
    }
]
# -------------- QUESTIONS FOR HANDLER ---------------

# -------------- QUESTIONS FOR SERVER ----------------
QUESTION_FOR_SERVER_LISTEN_PORT = [
    {
        "type": "input",
        "name": "port",
        "message": "请输入监听端口: ",
        "default": "31313"
    }
]
# -------------- QUESTIONS FOR SERVER ----------------

# -------------- 各种不同的消息类型  --------------
QUESTION_FOR_MESSAGE_COUNT = [
    {
        "type": "input",
        "name": "count",
        "message": "请输入想要发送消息的数量: ",
        "default": "500"
    }
]

QUESTION_FOR_INTERVAL = [
    {
        "type": "input",
        "name": "interval",
        "message": "请输入想要发送消息的时间间隔: ",
        "default": "0.01"
    }
]

QUESTION_FOR_CONTINUE = [
    {
        "type": "list",
        "name": "continue",
        "message": "是否需要继续",
        "choices": ["yes", "no"]
    }
]

QUESTION_FOR_SEND_PATTERN = [
    {
        "type": "list",
        "name": "pattern",
        "message": "请选择逐个[single]发送还是批量[batch]发送:",
        "choices": ["single", "batch"]
    }
]

# -------------- 各种不同的消息类型  --------------

