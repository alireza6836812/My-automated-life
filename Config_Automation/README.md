## Overview

This project focuses on automating the process of obtaining, validating, and maintaining a **stable and usable internet connection via proxy configurations**. It is designed primarily for environments where direct access to the internet is unstable or restricted.

The automation pipeline is divided into **three main stages**, each with its own set of scripts and responsibilities:

1. Configuration scraping
2. Configuration testing
3. Configuration selection and connection

---

## Project Structure

### 1. Config Scraper

This stage is responsible for collecting proxy configurations from multiple sources. Currently, three types of sources are supported:

#### 1.1 Telegram Channels

In this method, proxy configurations are scraped directly from Telegram channels.

To use this feature, you must create a Telegram `.session` file using your own Telegram account credentials.

Steps:

* Visit [https://my.telegram.org/](https://my.telegram.org/)
* Obtain your **API ID** and **API Hash**
* Place them into the `Info.txt` file
* Run the script and provide:

  * Phone number
  * Login code
  * Telegram password (if enabled)

After successful authentication, a session file will be created and used to scrape configurations from Telegram channels.

**Note for Iranian users:**
Due to filtering and access restrictions, logging into `my.telegram.org` may require an external IP address (VPN or proxy). This step may need to be completed outside Iran. Once the session is created, future runs usually do not require a VPN.

#### 1.2 Configuration Provider Servers

These are third-party servers that aggregate and provide proxy configurations using their own scraping methods.

Currently:

* One trusted and safe provider server is included

#### 1.3 Custom Configurations

You may also add your own configuration sources manually by providing links to custom proxy configurations. These are treated as an additional input source during the scraping phase.

#### Output of the Scraping Stage

* All scraped VMess configurations are saved in:

  * `1)Scrapped_VMESS_Configs.xlsx`
* A JSON representation of these configurations (compatible with tools such as Xray) is generated and saved in:

  * `2)Scrapped_VMESS_Configs_json.xlsx`

---

### 2. Config Testing

In this stage, the scraped configurations are validated and filtered.

The testing process consists of two steps:

1. **TCP Connectivity Test**
   Used to separate valid and invalid configurations.

2. **Full Functional Test**
   Each valid configuration is tested against the following essential services:

   * YouTube
   * Telegram
   * Instagram
   * ChatGPT

These platforms were chosen because they represent common real-world usage. If a configuration can successfully access these services, it is likely suitable for general internet access.

After testing, the validated configurations are stored in a dedicated Excel file (generated automatically by the scripts).

---

### 3. Config Connection

In the final stage, the **best-performing configuration** is selected automatically and used to establish a live connection.

This is achieved using:

* **Xray** for proxy tunneling
* **Redsocks** for redirecting system traffic

⚠ **Warning:**
Before running this stage, carefully review the scripts. They modify network routing and proxy settings and may interfere with other networking tools or VPNs installed on your system.

---

## Requirements

### System

* Linux distribution (Ubuntu recommended)

### Core Tools

* Python 3
* Xray
* Redsocks

### Python Libraries

* pandas
* requests
* socks
* telethon
* playwright

### Standard Python Modules

* re
* base64
* json
* urllib
* socket
* time
* asyncio
* subprocess
* tempfile
* copy

---

## How to Use

1. Create a Telegram `.session` file as described in the **Config Scraper** section.
2. Configure the scripts and place them in a scheduled execution cycle.

   * The author uses **cron**, but any scheduler is acceptable.
3. Run the automation and allow it to manage proxy scraping, testing, and connection.
4. To stop the process and restore network settings, run the provided cleanup script, which disables previous configurations.

---

## Limitations

* Currently, only **VMess** configurations are supported.
* The project is developed and tested specifically for **Ubuntu**.
* Performance is currently limited and may be slow in some scenarios.
* Initial Telegram scraping may require an external VPN or proxy.
* Mobile support is experimental.

---

## Current Status and Future Development

At the current stage:

* The project works reliably on Ubuntu systems with a valid Telegram account and internet access.
* Mobile usage is possible via **Termux**, but requires manual setup.

Planned future improvements include:

* Support for additional configuration types (VLESS, Trojan, etc.)
* Performance optimizations
* Improved compatibility with mobile devices
* Cleaner automation and error handling

---
