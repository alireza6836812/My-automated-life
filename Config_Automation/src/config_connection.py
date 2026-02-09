#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

vless_df = pd.read_excel('config_test_result.xlsx')

config = str(vless_df['json_config'].loc[3]).replace("'",'"').replace('True','true').replace('False','false')
print(config)

# Open file in write mode ('w' - creates new file or overwrites existing)
with open('/home/alireza/Desktop/proxy/config.json', 'w') as file:
    file.write(config)


# In[2]:


import subprocess
import sys

# WARNING:
# Hardcoding sudo password is insecure.
# Acceptable only for personal/local automation.
PASSWORD = "6836\n"

def run_sudo_command(command):
    """
    Runs a sudo command and prints its output.
    """
    process = subprocess.Popen(
        ["sudo", "-S"] + command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = process.communicate(PASSWORD)


run_sudo_command(["gsettings", "set", "org.gnome.system.proxy", "mode", "none"])
run_sudo_command(["sudo", "pkill", "xray"])

# 1. Bring up loopback interface
run_sudo_command(["ip", "link", "set", "lo", "up"])

# 2. Reload systemd units
run_sudo_command(["systemctl", "daemon-reload"])

# 3. Start and enable redsocks
run_sudo_command(["systemctl", "start", "redsocks"])
run_sudo_command(["systemctl", "enable", "redsocks"])


# 4. GNOME proxy settings (NO sudo here — must run as user)
def run_user_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = process.communicate()


run_user_command(["gsettings", "set", "org.gnome.system.proxy", "mode", "manual"])

run_user_command(["gsettings", "set", "org.gnome.system.proxy.http", "host", "127.0.0.1"])
run_user_command(["gsettings", "set", "org.gnome.system.proxy.http", "port", "10808"])

run_user_command(["gsettings", "set", "org.gnome.system.proxy.https", "host", "127.0.0.1"])
run_user_command(["gsettings", "set", "org.gnome.system.proxy.https", "port", "10808"])

run_user_command(["gsettings", "set", "org.gnome.system.proxy.socks", "host", "127.0.0.1"])
run_user_command(["gsettings", "set", "org.gnome.system.proxy.socks", "port", "10808"])

run_user_command(["gsettings", "set", "org.gnome.system.proxy.ftp", "host", "127.0.0.1"])
run_user_command(["gsettings", "set", "org.gnome.system.proxy.ftp", "port", "10808"])



process = subprocess.Popen(
    ["sudo", "-S", "xray", "run", "-c", "/home/alireza/Desktop/proxy/config.json"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# Send sudo password
process.stdin.write(PASSWORD)
process.stdin.flush()

# Stream Xray output in real time
for line in process.stdout:
    sys.stdout.write(line)
    sys.stdout.flush()

process.wait()


# In[3]:


run_user_command(["gsettings", "set", "org.gnome.system.proxy", "mode", "none"])
run_user_command(["sudo", "pkill", "xray"])

