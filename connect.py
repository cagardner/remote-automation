import paramiko
import os
import subprocess

def run_script(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    file_path = 'sudo -S bash code/PodSetup/loadMoxaPorts.sh'
    command = f'echo "{password}" | {file_path}'

    # Read the response from both stdout and stderr
    stdin, stdout, stderr = ssh.exec_command(command)
    response_stdout = stdout.read().decode()
    response_stderr = stderr.read().decode()

    # Print the response from both streams
    print(f"\
            \nStandard Output:\n{response_stdout}\
            \nError Output:\n{response_stderr}\
        ")
    # ...
    ssh.close()
    print("SSH connection closed.\n\n")


def stable_connection(hostname, username, password):
    print("Connecting...")
    try:
        sentence = "ssh antfarm-poc@192.168.131.93"
        other = "cd code/PodSetup"
        command = f"{sentence};{other}"
        while True:
            userinput = int(input("Use current config for this connection?\
                                  \n1. Yes\
                                  \n2. No\
                                  \n3. Exit"))
            if userinput == 1:
                subprocess.run(command, capture_output=True, shell=True)
            else:
                os.system(f"ssh {username}@{hostname}")
    except Exception as e:
        print("ERROR\nIncorrect spelling. Check your commands.")
