#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

api_id = 33968863
api_hash = "2832f4c8d66dcc1ff0ca7436ad469dfc"
phone = "+9809105832375"
session_name = "session2"
channel_username = "v2ray_dalghak"


# In[5]:


import socks
import re
import pandas as pd
from telethon import TelegramClient

# === Configuration ===
channel_usernames = ["v2ray_dalghak", "Argo_VPN1", "vpn_shield", "configshere", "mrsoulb", "PrivateVPNs", "YamYamProxy",
                     "DirectVPN", "V2rayNGX"]  # list of channels
messages_limit = 100

proxy = (socks.SOCKS5, '127.0.0.1', 10808)

# Regex patterns
URL_REGEX   = re.compile(r'https?://[^\s]+')
PROXY_REGEX = re.compile(r'\b(?:vmess|vless|trojan|ss|socks5)://[^\s]+', re.IGNORECASE)

async def scrape_to_links():
    async with TelegramClient('my_saved_session', api_id, api_hash, proxy=proxy) as client:
        all_links = []

        for channel_username in channel_usernames:
            channel = await client.get_entity(channel_username)

            async for msg in client.iter_messages(channel, limit=messages_limit):
                text = msg.text
                if not text:
                    continue

                # find all standard URLs
                urls = URL_REGEX.findall(text)

                # find all proxy format links
                proxy_links = PROXY_REGEX.findall(text)

                # combine
                all_links.extend(urls)
                all_links.extend(proxy_links)

        # deduplicate while preserving order
        unique_links = list(dict.fromkeys(all_links))

        # create DataFrame
        df_links = pd.DataFrame({"links": unique_links})
        return df_links

# Run in a Jupyter cell
df_links = await scrape_to_links()

# show
df_links


# In[9]:


import requests

url = "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_Sub.txt"

proxies = {
    "http":  "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808"
}
response = requests.get(url, proxies=proxies, timeout=30)

if response.status_code == 200:
    content = response.text
    # Split into lines, remove empty lines
    urls2 = [line.strip() for line in content.splitlines() if line.strip()]
    print(f"Found {len(urls2)} URLs")
else:
    print("Failed to fetch file:", response.status_code)

vless_df = pd.DataFrame({'links': urls2})
vless_df = pd.concat([df_links, vless_df], ignore_index=True)
vless_df = vless_df[vless_df['links'].str.startswith(('vmess'))]
vless_df = vless_df.dropna()
vless_df = vless_df.drop_duplicates(subset="links").reset_index(drop=True)
vless_df


# In[12]:


import base64
import json


def vmess_url_to_xray_config(vmess_url: str) -> dict:
    try:
        if not vmess_url.startswith("vmess://"):
            raise ValueError("Not a vmess URL")

        # Remove scheme
        encoded = vmess_url[len("vmess://"):]

        # Fix base64 padding if needed
        padding = '=' * (-len(encoded) % 4)
        decoded_bytes = base64.b64decode(encoded + padding)
        vmess_data = json.loads(decoded_bytes.decode("utf-8"))

        # Build Xray config
        config = {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": [
                {
                    "port": 10808,
                    "listen": "127.0.0.1",
                    "protocol": "socks",
                    "settings": {
                        "udp": True
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "vmess",
                    "settings": {
                        "vnext": [
                            {
                                "address": vmess_data["add"],
                                "port": int(vmess_data["port"]),
                                "users": [
                                    {
                                        "id": vmess_data["id"],
                                        "alterId": int(vmess_data.get("aid", 0)),
                                        "security": vmess_data.get("scy", "auto")
                                    }
                                ]
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": vmess_data.get("net", "tcp")
                    }
                }
            ]
        }

        # TCP settings
        if vmess_data.get("net") == "tcp":
            config["outbounds"][0]["streamSettings"]["tcpSettings"] = {
                "header": {
                    "type": vmess_data.get("type", "none")
                }
            }

        # TLS settings
        if vmess_data.get("tls") == "tls":
            config["outbounds"][0]["streamSettings"]["security"] = "tls"
            config["outbounds"][0]["streamSettings"]["tlsSettings"] = {
                "serverName": vmess_data.get("sni", ""),
                "allowInsecure": vmess_data.get("insecure", "0") == "1"
            }

        return config
    except:
        return None


vless_df['json_config'] = vless_df['links'].apply(vmess_url_to_xray_config)
vless_df = vless_df.dropna(subset=['json_config'])
vless_df["json_config"] = vless_df["json_config"].apply(
    lambda x: str(x).replace("'", '"').replace("True", "true").replace("False", "false")
    if pd.notnull(x) else x
)

vless_df.to_excel('config_scrapper_result.xlsx')
vless_df

