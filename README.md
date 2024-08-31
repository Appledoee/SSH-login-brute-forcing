# SSH-login-brute-forcing

# Description
A Python script for SSH password brute forcing using a list of possible common credentials. This activity is not suitable for excessive authentication attempts; it is advisable to use a wordlist with up to 10 passwords. In this instance, my text file contains 816 passwords, which resulted in SSH blocking my authentication attempts after less than 20 attempts. Alternatively, I added SSHException handling to manage the error if I choose to continue using a wordlist with more than 10 entries.

# Features:
- pwn library
- paramiko library
- a list of passwords 

# Steps

<b>1) Importing modules</b>
- Import <code>pwn</code> module and import <code>paramiko</code> module

```python
from pwn import *
import paramiko
```

*<code>pwn</code> module is used to interact with SSH service

*<code>paramiko</code> module is used for error handling


<b>2) Defining variables</b>

```python
host = "127.0.0.1"
username = "kali"
attempts = 0
```
*host=your target IP
*username=your target username
*attempts= start from 0

<b>3) Iterating over some lists of passwords</b>

To be able to perform brute-forcing tasks, we need to iterate over some lists of passwords
- Open your file

```python
with open("passwords.txt", "r") as password_list:
  for password in password_list:
  password = password.strip("\n")
```
*replace <code>passwords.txt</code> with the <code>txt</code> file that you have


(similar list can be download here: https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials)

*<code>for</code> is a loop 


*<code>"r"</code> indicates that the file is on read mode

*<code>password.strip("\n")</code> is a combination which is used to remove newline character, this is to ensure that your code is functioning correctly and presents your list of passwords without adding/removing characters in your passwords. <code>.strip</code> is used to remove or truncates the given characters from the beginning and the end of the original string while <code>\n"</code> is a type of escape character that will create a new line when used, which basically functions as 'enter' key in physical.


<b>4) Handling authentication errors</b>

Codes are broken down into two parts for easier understanding:

A) For valid password response

```python
try:
  print("[{}] Attempting password: '{}'!".format(attempts,password))
  response = ssh(host=host, user=username, password=password, timeout=1)
  if response.connected():
    print("[>] Valid password found: '{}'!".format(password))
    response.close()
    break
```

*<code>try</code> is used to manage errors and exceptions

*<code>ssh(host=host, user=username, password=password, timeout=1)</code> is imported from <code>pwn</code> module

*<code>timeout</code> is set up to 1s

*<code>if response.connected():</code> indicates if the connection has made, we will print out <code>Valid password found</code>

*<code>response.close()</code> indicates when we know there is a valid connection, we can close the connection

*<code>break</code> is used to break the loop because when we have found the password, we do not want to keep continuing the loop.

B) For invalid password response

```python
  response.close()
except paramiko.ssh_exception.AuthenticationException:
  print("[X] Invalid password!")
attempts += 1
```
*<code>response.close()</code> is used to close the connection and start with new

*<code>except</code> is an exception

*<code>except paramiko.ssh_exception.AuthenticationException:</code> is an exception class from the Paramiko library, which is used for handling SSH connections in Python. This exception is raised when an authentication attempt fails—meaning the username or password used to connect via SSH is incorrect.

*when the <code>except</code> fails, it will print out <code>Invalid password!</code>

*<code>attempts +=1</code> is used to count how many passwords you have tried and failed so you can keep track how many failed attempts you encounter. So every failed attempt will increase by 1

*<code>[X]</code> is just a decorative element, it does not affect the output. You can print the string without it.

The output if you use <code>attempts += 1</code>
![Screenshot 2024-08-25 at 3 23 06 AM](https://github.com/user-attachments/assets/5d67bc84-2e3b-4782-945b-f721a760bd4f)

*I was wondering why we should use <code>+=</code> instead of <code>=</code>, so I changed my code to <code>=</code> and I found that you won't be able to keep track of the failed attempts and it will remain [1] instead of [1],[2],[3],[4]... 
![Screenshot 2024-08-25 at 3 33 24 AM](https://github.com/user-attachments/assets/9144ef71-18ca-4e5c-bc89-4dc55e689d58)

# Result

![photo_2024-08-25 05 28 42](https://github.com/user-attachments/assets/ec60c157-f081-453a-b945-059279740730)

# Documents 
<a href="https://docs.pwntools.com/en/latest/tubes/ssh.html">pwntools for SSH</a>

<a href="https://docs.paramiko.org/en/latest/api/ssh_exception.html">paramiko</a>


# Troubleshooting

1) This activity can test out up to 10 attempts

Solution:

Use a wordlist that has less than 10 passwords or you can opt for .SSHException to fix the error (refer next)

2) EOF Error & Error reading SSH protocol banner

![Screenshot 2024-08-25 at 5 34 22 AM](https://github.com/user-attachments/assets/85c7b9cd-1c3d-41c7-b91f-5794addbf7ec)

Solution:

Added another <code>.SSHException</code> to the code to function normally after exception and before <code>attempts +=1</code>. Compare the codes between <code>ssh-brute.py</code> file and <code>fix-ssh-brute.py</code> file:

```python
except paramiko.ssh_exception.SSHException as e:
  print(f"[!] SSHException: {e}")
except Exception as e:
  print(f"[!] Unexpected Exception: {e}")
```

*<code>[!]</code> is just a decorative element, it does not affect the output. You can print the string without it.

3) Timeout=1s is too short
   
Solution:

Timeout has increased to 10s because 1s is too short and might disrupt the SSH connection. Preferably 10s-30s.

