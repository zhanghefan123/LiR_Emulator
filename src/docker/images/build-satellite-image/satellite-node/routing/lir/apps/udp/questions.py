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

