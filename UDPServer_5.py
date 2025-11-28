# 代码使用pycharm编译

# 导入socket模块的所有功能（无需逐个指定函数/类，直接使用如socket()、AF_INET等）
from socket import *

# 定义服务器监听端口（需与客户端端口保持一致，此处固定为12000）
serverPort = 12000
# 创建UDP Socket对象：AF_INET表示使用IPv4协议，SOCK_DGRAM表示UDP传输模式
serverSocket = socket(AF_INET, SOCK_DGRAM)
# 绑定端口到本地所有网卡（空字符串''表示监听本机所有IP地址，端口为12000）
serverSocket.bind(('', serverPort))
# 打印启动提示，告知用户服务器已就绪
print("Server已启动，等待客户端连接...")
# 初始化客户端地址变量（后续存储连接的客户端IP和端口）
clientAddr = None
# 设置Socket接收超时为None（即无限等待，确保能持续监听客户端消息，不会因超时断开）
serverSocket.settimeout(None)

# --------------------------
# 阶段1：模拟TCP三次握手（手动输入触发，确保连接可控）
# 三次握手逻辑简化：客户端发连接请求 → 服务器手动确认 → 连接建立
# --------------------------
# 循环监听客户端消息（直到收到有效连接请求）
while True:
    # 接收客户端数据（缓冲区大小2048字节），返回数据内容和客户端地址（IP+端口）
    msg, clientAddr = serverSocket.recvfrom(2048)
    # 解码UDP接收的字节流为字符串，判断是否是客户端的连接请求指令（约定为'connect'）
    if msg.decode() == 'connect':
        # 打印连接请求信息，显示客户端的IP和端口
        print(f"\n收到客户端{clientAddr}的连接请求！")
        # 手动输入确认指令（需输入约定的's-ack'，模拟服务器对连接的手动确认）
        server_input = input("请输入's-ack'确认连接：")
        # 判断输入是否为正确的确认指令
        if server_input == 's-ack':
            # 向客户端发送连接确认消息（编码为字节流后传输）
            serverSocket.sendto('s-ack'.encode(), clientAddr)
            # 打印连接建立成功提示
            print("连接建立完成！")
            # 跳出循环，结束连接建立阶段
            break

# --------------------------
# 阶段2：手动触发文件接收（等待用户输入指令后，再开始接收文件数据）
# --------------------------
# 提示用户输入接收指令（约定为'recv'，手动触发文件接收流程）
recv_input = input("\n请输入'recv'开始接收文件：")
# 判断输入是否为正确的接收指令
if recv_input == 'recv':
    # 以二进制写入模式（wb）创建/打开接收文件（支持文本、图片等所有文件类型）
    with open("received_file.txt", "wb") as f:
        # 提示已进入等待接收状态
        print("正在等待客户端发送文件...")
        # 循环接收文件数据块（直到收到客户端的结束标记）
        while True:
            # 接收客户端发送的文件数据块（缓冲区2048字节，与客户端分块大小一致）
            data, _ = serverSocket.recvfrom(2048)
            # 判断是否收到文件传输结束标记（约定为二进制流b"EOF"）
            if data == b"EOF":
                # 打印文件接收完成提示
                print("文件接收完成！")
                # 跳出循环，结束文件接收
                break
            # 将接收的数据块写入文件
            f.write(data)

# --------------------------
# 阶段3：模拟TCP连接释放（手动输入触发，确保断开可控）
# 释放逻辑：客户端发断开请求 → 服务器手动确认 → 连接释放
# --------------------------
# 提示用户已进入等待断开请求状态
print("\n等待客户端发起断开请求...")
# 循环监听客户端的断开请求
while True:
    # 接收客户端发送的消息
    msg, _ = serverSocket.recvfrom(2048)
    # 解码消息，判断是否是断开请求指令（约定为'bye'）
    if msg.decode() == 'bye':
        # 打印收到断开请求的提示，显示客户端地址
        print(f"\n收到客户端{clientAddr}的断开请求！")
        # 手动输入断开确认指令（约定为's-bye'，模拟服务器对断开的手动确认）
        close_input = input("请输入's-bye'确认断开：")
        # 判断输入是否为正确的断开确认指令
        if close_input == 's-bye':
            # 向客户端发送断开确认消息
            serverSocket.sendto('s-bye'.encode(), clientAddr)
            # 打印连接释放完成提示
            print("连接已释放！")
            # 跳出循环，结束连接释放阶段
            break

# 关闭服务器Socket，释放资源

serverSocket.close()
