import hashlib
import os
import random
import subprocess
import sys


def calculate_md5_string(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


args = sys.argv[1:]
tot = 0

ssh_server = ""
auth_type = "NONE"
auth = ""
screen_id = ""

if __name__ == "__main__":

    if "-v" in args or "-V" in args or "--version" in args:
        if len(args) > 1:
            print(
                "Usage: hydrangea-screen-monitor [-p PASSWORD | -k PRIVATE_KEY] SSH_SERVER SCREEN_ID")
            sys.exit(1)
        else:
            print("hydrangea-screen-monitor 1.0.0")
            sys.exit(0)
    while tot < len(args)-2:
        if args[tot] in ["-v", "--version"]:
            print(
                "Usage: hydrangea-screen-monitor [-p PASSWORD | -k PRIVATE_KEY] SSH_SERVER SCREEN_ID")
        if args[tot] in ["-p", "-P", "--password"]:
            if auth_type != "NONE":
                print("Please provide only one authentication method.")
                sys.exit(1)
            auth_type = "PASSWORD"
            auth = args[tot+1]
            tot += 2
        elif args[tot] in ["-k", "-K", "--private-key"]:
            if auth_type != "NONE":
                print("Please provide only one authentication method.")
                sys.exit(1)
            auth_type = "PRIVATE_KEY"
            auth = args[tot+1]
            tot += 2
        else:
            print("Unknown option: " + args[tot])
            sys.exit(1)
    args = args[tot:]
    try:
        ssh_server = args[-2]
        screen_id = args[-1]
    except:
        print(
            "Usage: hydrangea-screen-monitor [-p PASSWORD | -k PRIVATE_KEY] SSH_SERVER SCREEN_ID")
        sys.exit(1)

    if auth_type == "PRIVATE_KEY" and not os.path.exists(auth):
        print(f"Private key file {auth} not found.")
        sys.exit(1)

    print(f"ssh_server: {ssh_server}")
    print(f"auth_type: {auth_type}")
    if auth_type != "NONE":
        print(f"auth: {auth}")
    print(f"screen_id: {screen_id}")
    if input("Proceed? [y/n] ") not in ["y", "Y"]:
        print("Aborted.")
        sys.exit(0)
    else:
        print("Proceeding...")

    INF = 2 ** 31 - 1
    log_dir = "~/.hydrangea-screen-monitor"
    log_filename = f"{calculate_md5_string(screen_id+str(random.randint(0, INF)))}.log"
    task = f"log_filename={log_dir}/{log_filename} && screen_id={screen_id} && screen -S $screen_id -X log on && screen -S $screen_id -X logfile $log_filename && tail -f $log_filename"

    if auth_type == "PASSWORD":
        subprocess.run(["sshpass", "-p", auth, "ssh", ssh_server,
                       "-o StrictHostKeyChecking=no", f"mkdir -p {log_dir}"])
        subprocess.run(["sshpass", "-p", auth, "ssh", ssh_server,
                       "-o StrictHostKeyChecking=no", f"chmod +x {log_dir}/tasks.sh"])
        subprocess.run(["clear"])
        subprocess.run(["ssh", ssh_server, task])
    elif auth_type == "PRIVATE_KEY":
        subprocess.run(["ssh", ssh_server, "-i", auth, f"mkdir -p {log_dir}"])
        subprocess.run(["ssh", "-i", auth, ssh_server,
                       f"chmod +x {log_dir}/tasks.sh"])
        subprocess.run(["clear"])
        subprocess.run(["ssh", "-i", auth, ssh_server, task])
    elif auth_type == "NONE":
        subprocess.run(["ssh", ssh_server, f"mkdir -p {log_dir}"])
        subprocess.run(["ssh", ssh_server, f"chmod +x {log_dir}/tasks.sh"])
        subprocess.run(["clear"])
        subprocess.run(["ssh", ssh_server, task])
