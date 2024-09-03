import paramiko

def run_remote_inference(hostname, username, password, script_path):
    # 建立 SSH 客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接到树莓派并启用X11转发
        print(f"Connecting to {hostname}...")
        ssh.connect(hostname, username=username, password=password)
        print("Connected!")
        
        # 启用X11转发（连接参数设置）
        # 使用 'exec_command' 启动命令，同时开启 DISPLAY 环境变量
        command = f"DISPLAY=:0 python {script_path}"
        stdin, stdout, stderr = ssh.exec_command(command)
        print("1!")

        # 获取输出并打印
        print(stdout.read().decode())
        print("5!")
        error = stderr.read().decode()
        if error:
            print("Error:", error)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 关闭 SSH 连接
        ssh.close()
        print("Connection closed.")

if __name__ == "__main__":
    # 树莓派的连接信息
    hostname = "192.168.137.65"  # 树莓派的 IP 地址
    username = "hadgy"
    password = "1"
    
    # 推理脚本的路径（在树莓派上）
    script_path = "/home/hadgy/Desktop/YOLO/main.py"
    
    # 运行远程推理
    run_remote_inference(hostname, username, password, script_path)
