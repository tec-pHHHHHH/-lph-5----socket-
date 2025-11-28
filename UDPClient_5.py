# 代码使用pycharm编译

# 导入socket模块的所有功能（可直接使用socket相关类和方法，无需前缀）
from socket import *


# 定义服务器的IP地址（127.0.0.1是本地回环地址，用于同一台电脑上的客户端和服务器通信）
serverName = '127.0.0.1'
# 定义服务器的监听端口（必须与服务器端代码中设置的端口一致，此处为12000）
serverPort = 12000
# 创建UDP Socket对象：AF_INET表示使用IPv4协议，SOCK_DGRAM表示采用UDP传输模式
clientSocket = socket(AF_INET, SOCK_DGRAM)

# --------------------------
# 阶段1：模拟TCP三次握手（手动输入触发，实现连接建立的交互逻辑）
# 三次握手简化流程：客户端发起连接请求 → 服务器确认 → 连接建立
# --------------------------
# 提示用户手动输入连接指令，只有输入约定的'connect'才会发起连接
client_input = input("请输入'connect'发起连接：")
# 判断用户输入是否为正确的连接指令
if client_input == 'connect':
    # 将连接请求指令（字符串'connect'）编码为字节流，通过UDP发送到指定服务器（IP+端口）
    clientSocket.sendto('connect'.encode(), (serverName, serverPort))
    # 等待接收服务器返回的连接确认消息（缓冲区大小2048字节），返回确认消息和服务器地址
    ack_msg, _ = clientSocket.recvfrom(2048)
    # 将服务器返回的字节流消息解码为字符串，判断是否是约定的确认指令's-ack'
    if ack_msg.decode() == 's-ack':
        # 打印连接建立成功的提示，告知用户已完成连接
        print("服务器已确认连接，连接建立完成！")

# --------------------------
# 阶段2：手动触发文件发送（用户输入指令后，开始向服务器传输文件数据）
# --------------------------
# 提示用户手动输入发送指令，只有输入约定的'send'才会启动文件发送
send_input = input("请输入'send'开始发送文件：")
# 判断用户输入是否为正确的发送指令
if send_input == 'send':
    # 定义要发送的文件路径（需确保该文件与客户端代码在同一目录下，此处为test.txt）
    file_path = "test.txt"
    # 以二进制读取模式（rb）打开文件（支持文本、图片、文档等所有类型文件）
    with open(file_path, "rb") as f:
        # 循环分块读取文件数据（每次读取2048字节，与缓冲区大小匹配，避免数据溢出）
        while True:
            data = f.read(2048)
            # 若读取到的数据为空（表示文件已读取完毕），跳出循环
            if not data:
                break
            # 将读取的文件数据块（字节流）通过UDP发送到服务器
            clientSocket.sendto(data, (serverName, serverPort))
    # 文件数据发送完毕后，发送约定的结束标记（b"EOF"，二进制格式），告知服务器传输结束
    clientSocket.sendto(b"EOF", (serverName, serverPort))
    # 打印文件发送完成的提示，告知用户数据已全部发送
    print("文件发送完成！")

# --------------------------
# 阶段3：模拟TCP连接释放（手动输入触发，实现连接断开的交互逻辑）
# 释放流程：客户端发起断开请求 → 服务器确认 → 连接释放
# --------------------------
# 提示用户手动输入断开指令，只有输入约定的'bye'才会发起断开请求
close_input = input("请输入'bye'发起断开：")
# 判断用户输入是否为正确的断开指令
if close_input == 'bye':
    # 将断开请求指令（字符串'bye'）编码为字节流，发送到服务器
    clientSocket.sendto('bye'.encode(), (serverName, serverPort))
    # 等待接收服务器返回的断开确认消息（缓冲区大小2048字节）
    bye_msg, _ = clientSocket.recvfrom(2048)
    # 将服务器返回的字节流解码为字符串，判断是否是约定的断开确认指令's-bye'
    if bye_msg.decode() == 's-bye':
        # 打印连接释放完成的提示，告知用户连接已断开
        print("服务器已确认断开，连接已释放！")

# 关闭客户端Socket，释放网络资源

clientSocket.close()
