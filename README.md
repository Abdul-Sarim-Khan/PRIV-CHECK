# 🔐 PrivCheck – Privileged Command Analysis Tool

**PrivCheck** is a cybersecurity-focused static analysis tool that detects **high-privileged system commands** in scripts using **Deterministic Finite Automata (DFA)**. Built for a university project in *Theory of Automata*, it helps developers and system admins identify potentially risky operations like `sudo`, `chmod 777`, `rm -rf`, `net user`, and more.

## 🚀 Features

- ✅ **DFA-based pattern detection** for efficient scanning
- 🧾 **Supports** `.sh`, `.bat`, `.ps1`, `.txt`, `.sql`, and `.js` scripts
- 📊 **Risk scoring system** ranks detected commands as Clean, Medium, High, or Critical
- 🌐 **Streamlit-powered web app** for interactive analysis
- 📈 **Plotly gauge chart** shows risk severity visually
- 🎬 **Lottie animations** enhance UI feedback

## 🔎 What It Detects

PrivCheck scans for the following types of privileged commands:

- 🔼 **Privilege Escalation** (`sudo`, `su`, `doas`)
- 👤 **User Management** (`useradd`, `net user`, `passwd`)
- 🔐 **File Permissions** (`chmod`, `icacls`, `setfacl`)
- ⚙️ **System Configuration** (`systemctl`, `reg add`)
- 💣 **Destructive Commands** (`rm -rf`, `format`, `mkfs`)
- 🌐 **Network Configuration** (`iptables`, `route`)
- 🔍 **Information Gathering** (`cat /etc/shadow`, `sudo -l`)

## 📁 Project Structure

├── app.py # Streamlit interface
├── detector.py # DFA-based matching engine
├── patterns.py # Regex-based pattern library
├── threats/ # Sample test scripts
├── assets/ # Lottie animations, CSS
