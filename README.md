![Workflow Diagram](assets/automation.jpg)

# My Automated Life

## Overview

This repository is a collection of side projects focused on automating routine and repetitive problems in my daily life.  
The main motivation is to reduce the time and mental energy spent on tasks that are necessary but not valuable enough to do manually.

These projects are practical, personal, and problem-driven.  
I am open to further suggestions and ideas that could improve or extend this repository.  
Contact: alireza6836812@gmail.com

---

## Project Structure

At the current stage, this repository consists of three main automation projects:

### 1) Config_Automation

As an Iranian user, I spend a significant amount of time finding proxy configurations that are actually connectable and usable for accessing the international internet. This process is repetitive, time-consuming, and unreliable.

This project automates the entire workflow:
- Scraping configuration data
- Testing connectivity and performance
- Selecting the best available option
- Connecting automatically

The idea is simple: run it periodically (for example, every 10 minutes) and avoid manual searching.  
The goal is stable access with minimal human involvement.

---

### 2) Backup_Automation

I have lost important data multiple times due to issues such as device failure or theft.  
Although cloud services provide backup solutions, they have several limitations:

1. They require a stable internet connection and can be slow
2. Storage space is limited
3. Losing account credentials may result in permanent data loss

To address this, I decided to maintain distributed local backups.  
For example:
- A backup of my Ubuntu system on my phone
- A backup of my phone on my system

This way, losing one device does not mean losing all data.  
This project automates the backup process between different devices.

---

### 3) Update_Automation

This project targets a very common annoyance.

Examples:
- Your phone starts updating applications while you are browsing with a slow connection
- You forget to run system updates regularly and end up running `sudo apt upgrade` manually every time

The goal here is:
- To schedule updates at controlled times
- To be notified when updates are available
- To decide consciously when to migrate to newer versions

---

## Workflow

Each side project has its own internal workflow, but they all follow the same general logic:

1. Initial installation and environment setup
2. Configuration of time-based execution (e.g., cron jobs or schedulers)
3. Fully automated execution without manual intervention

---

## Installation

Most projects in this repository are based on Python.  
Additional languages or tools may be introduced in the future depending on requirements.

There is no global installation process. Each sub-project documents its own setup in its local `README.md`.

### Requirements

- Python
- Jupyter Notebook
- Internet connection
- Telegram API ID and API Hash (for Config_Automation)

Python packages commonly used:
- pandas
- numpy

---

## Setup

The setup process depends on the specific project.

Examples:
- SSH connections between devices for backup automation
- Network access for configuration and update automation

Each sub-project contains its own documentation explaining these steps in detail.

---

## Usage

The intended use of this repository is everyday life automation.

As someone who spends a lot of time working with technology and the internet, I noticed that a large portion of my time was spent repeating the same necessary tasks.  
By automating these workflows, I aim to reduce cognitive load and free time for more meaningful activities (or simply resting more).

---

## Data and Configuration

Different data formats are used across the projects, including:

- pandas DataFrames
- XLSX and CSV files
- JSON configuration and intermediate files

Sensitive data and local configuration files are excluded from version control.

---

## Status and Future Improvements

At the moment:
- `Config_Automation` is functional and stable
- Other projects are under development

This repository will grow over time as new automation ideas emerge.  
Suggestions and feedback are welcome.

Contact: alireza6836812@gmail.com

