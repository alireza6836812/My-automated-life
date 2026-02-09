#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.parse
import base64
import json
import socket
import time
import pandas as pd


vless_df = pd.read_excel('config_scrapper_result.xlsx')

def extract_host_port(proxy_link):
    """
    Extract host and port from VLESS or VMESS proxy links
    """
    if not isinstance(proxy_link, str):
        return None, None

    proxy_link = proxy_link.strip()

    # Handle VLESS links
    if proxy_link.startswith("vless://"):
        try:
            parsed = urllib.parse.urlparse(proxy_link)
            if "@" not in parsed.netloc:
                return None, None
            netloc = parsed.netloc.split("@", 1)[1]
            if ":" not in netloc:
                return None, None
            host, port = netloc.rsplit(":", 1)
            return host, int(port)
        except Exception:
            return None, None

    # Handle VMESS links
    elif proxy_link.startswith("vmess://"):
        try:
            # Remove vmess:// prefix and decode base64
            base64_config = proxy_link[8:]

            # Add padding if needed
            padding = 4 - len(base64_config) % 4
            if padding != 4:
                base64_config += "=" * padding

            # Decode base64
            json_config = base64.urlsafe_b64decode(base64_config).decode('utf-8')

            # Parse JSON
            vmess_data = json.loads(json_config)

            # Extract address and port
            address = vmess_data.get("add", "")
            port = vmess_data.get("port", "")

            if not address or not port:
                return None, None

            return address, int(port)
        except Exception:
            return None, None

    return None, None

def tcp_ping(host, port, timeout=2):
    """
    Perform TCP ping to check latency
    """
    try:
        start = time.time()
        with socket.create_connection((host, port), timeout=timeout):
            return (time.time() - start) * 1000  # latency in milliseconds
    except Exception:
        return None  # unreachable

def batch_tcp_ping(proxy_links, timeout=2, max_workers=10):
    """
    Perform TCP pings for multiple proxy links with optional threading
    """
    import concurrent.futures

    results = []

    def ping_link(link):
        host, port = extract_host_port(link)
        if host is not None and port is not None:
            return tcp_ping(host, port, timeout)
        return None

    # Single-threaded for simplicity
    for link in proxy_links:
        host, port = extract_host_port(link)
        if host is not None:
            latency = tcp_ping(host, port, timeout)
            results.append(latency)
        else:
            results.append(None)

    return results

def enhanced_tcp_ping(host, port, timeout=3, retries=2):
    """
    Enhanced TCP ping with retries and better error handling
    """
    for attempt in range(retries):
        try:
            start = time.time()
            with socket.create_connection((host, port), timeout=timeout):
                latency = (time.time() - start) * 1000
                return latency
        except socket.timeout:
            continue
        except ConnectionRefusedError:
            return None  # Port closed
        except socket.gaierror:
            return None  # DNS resolution failed
        except Exception:
            continue

    return None

# Main execution
latencies = []
successful_count = 0
failed_count = 0

for link in vless_df["links"]:
    host, port = extract_host_port(link)
    if host is not None and port is not None:
        print(f"Testing {host}:{port}...", end=" ")
        latency = enhanced_tcp_ping(host, port)
        if latency is not None:
            print(f"✓ {latency:.2f} ms")
            successful_count += 1
        else:
            print("✗ Failed")
            failed_count += 1
        latencies.append(latency)
    else:
        print(f"Could not parse: {link}")
        latencies.append(None)
        failed_count += 1

print(f"\nSummary: {successful_count} successful, {failed_count} failed")

# Add latency column to DataFrame
vless_df["tcp_latency_ms"] = latencies
# Sort by latency (fastest first)
vless_df = vless_df.sort_values("tcp_latency_ms", na_position='last').reset_index(drop=True)
vless_df = vless_df.dropna(subset=['tcp_latency_ms'])
vless_df


# In[6]:


import asyncio
import pandas as pd
import json
import subprocess
import socket
import time
import tempfile
import copy
from playwright.async_api import async_playwright

# --------------------------
# System Chrome path
# --------------------------
CHROME_PATH = "/usr/bin/google-chrome"

# --------------------------
# Websites to test
# --------------------------
TEST_SITES = {
    "youtube": "https://www.youtube.com",
    "telegram": "https://web.telegram.org",
    "instagram": "https://www.instagram.com",
    "chatgpt": "https://chat.openai.com",
}

# --------------------------
# Test a single config with async Playwright
# --------------------------
async def test_single_config_async(config_dict, local_port):
    result = {"proxy_alive": False}

    if not isinstance(config_dict, dict):
        return result

    config = copy.deepcopy(config_dict)

    # Override SOCKS port
    for inbound in config.get("inbounds", []):
        if inbound.get("protocol") == "socks":
            inbound["port"] = local_port

    # Write temporary JSON config
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump(config, f, indent=2)
        config_path = f.name

    # Start Xray
    proc = subprocess.Popen(
        ["xray", "run", "-c", config_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for SOCKS port
    start = time.time()
    while time.time() - start < 15:
        try:
            with socket.create_connection(("127.0.0.1", local_port), timeout=1):
                result["proxy_alive"] = True
                break
        except Exception:
            await asyncio.sleep(0.5)

    if not result["proxy_alive"]:
        proc.terminate()
        proc.wait()
        return result

    # Launch Playwright browser through SOCKS5 proxy
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            proxy={"server": f"socks5://127.0.0.1:{local_port}"},
            headless=True
        )
        context = await browser.new_context()
        page = await context.new_page()

        for name, url in TEST_SITES.items():
            try:
                t0 = time.time()
                await page.goto(url, timeout=30000)  # 30s max
                latency_ms = (time.time() - t0) * 1000
                result[f"{name}_latency_ms"] = latency_ms
                result[f"{name}_status"] = 200
            except Exception:
                result[f"{name}_latency_ms"] = None
                result[f"{name}_status"] = None

        await browser.close()

    proc.terminate()
    proc.wait()
    return result

# --------------------------
# Batch test DataFrame
# --------------------------
async def test_vless_df_async(df, start_port=10808):
    results = [{} for _ in range(len(df))]

    tasks = []
    for i in range(len(df)):
        tasks.append(test_single_config_async(df.loc[i, "json_config"], start_port + i))

    completed = 0
    final_results = []
    for coro in asyncio.as_completed(tasks):
        res = await coro
        final_results.append(res)
        completed += 1
        print(f"✅ Finished {completed}/{len(df)}")

    results_df = pd.DataFrame(final_results)
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)

# --------------------------
# Usage
# --------------------------
# Make sure 'json_config' column has actual dicts
vless_df["json_config"] = vless_df["json_config"].apply(json.loads)

# Run async test in Jupyter
vless_df = await test_vless_df_async(vless_df)

# Keep only working proxies
vless_df = vless_df[vless_df["proxy_alive"]].reset_index(drop=True)

vless_df.to_excel('config_test_result.xlsx')
vless_df

