# Cyber-Guard
Final Year Project
Here’s your full **detailed `README.md`** in proper markdown syntax for the **Cyber-Guard** GitHub repository, formatted cleanly with all essential sections:

4![image](https://github.com/user-attachments/assets/0115fe51-5f31-40dd-9f9c-25a1b5e1d562)


```markdown
# 🛡️ Cyber-Guard: AI-Powered Cybersecurity Assistant

**Cyber-Guard** is an AI-driven assistant crafted specifically for the modern cybersecurity landscape. Tailored for **DevSecOps**, **bug bounty hunters**, and **infosec researchers**, it offers advanced contextual understanding and deep analytical capabilities. This project was created as a **Final Year Capstone Project** by:

- **Hitarth Shah** – Core developer, bug bounty researcher, and creator of Deep Research feature  
- **Maharishi** – DevSecOps integration and testing lead  
- **Dhaarakh** – UI/UX, architecture design, and backend logic  

Cyber-Guard leverages a custom-trained **Ollama 3B-7 model with 10 million parameters**, fine-tuned using proprietary data from real-world bug bounty reports, red team exercises, and regulatory compliance frameworks.

---

## 🧠 Core Highlights

### ⚙️ Deep Research Mode *(By Hitarth)*
- Unique feature that simulates **multi-layered threat analysis**, CVE enumeration, and mitigation modeling.
- Capable of **multi-turn contextual reasoning**, pivoting between various attack vectors, threat actors, and mitigation strategies.
- Especially useful in red teaming, post-exploitation analysis, and high-quality report writing.

### 🔒 Cybersecurity-Aware Intelligence
- Understands security terminologies (OWASP Top 10, MITRE ATT&CK, CVEs, CVSS scoring).
- Generates PoCs, remediations, and threat intelligence summaries.
- Assists in triaging security reports and identifying real-world exploit chains.

### 🛠️ DevSecOps Integration
- Analyzes CI/CD pipelines (GitHub Actions, Jenkins, etc.)
- Provides guidance on hardening Docker containers, Kubernetes clusters, and IAC files (Terraform, Ansible).
- Offers best practices and checks based on **CIS Benchmarks**, **ISO 27001**, **NIST 800-53**, etc.

### 🎯 Bug Bounty Support
- Smart recon prompts: subdomain enum, directory brute force, parameter fuzzing.
- Suggests **WAF bypasses**, **payload mutations**, **SSRF/SQLi tricks**, and **CSP misconfig exploitation**.
- Report automation: explains vulnerabilities in structured format, provides impact/likelihood suggestions.

---

## 🧬 AI Model & Architecture

| Property         | Value                            |
|------------------|----------------------------------|
| Model Name       | CyberGuard 3B-7                  |
| Framework        | [Ollama](https://ollama.com)     |
| Architecture     | LLaMA-based (Custom fine-tuned)  |
| Parameters       | 10 Million                       |
| Training Dataset | Bug bounty reports, VAPT writeups, Cybersecurity whitepapers, MITRE/NIST/CIS standards |
| Tools Used       | Ollama, Streamlit, LangChain, Python |

---

## 📂 Project Structure

```bash
cyber-guard/
│
├── app.py                      # Main Streamlit app interface
├── backend/
│   ├── model_engine.py         # Model loading and response logic
│   ├── prompt_templates/       # Custom prompt templates (Deep Research, DevSecOps)
│   └── utils/                  # Helper functions
│
├── data/                       # Sample queries, datasets
├── screenshots/                # Screenshots and visual assets
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 📸 Screenshot

> A clean and simple UI designed using **Streamlit**, supports multi-turn chat history, advanced query chaining, and cybersec-specific prompts.

![UI Screenshot](screenshots/cyberguard-ui-preview.png)

---

## 🔧 Setup & Installation

### 📥 Clone the Repository

```bash
git clone https://github.com/your-username/cyber-guard.git
cd cyber-guard
```

### 📦 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 🧠 Download the Custom Ollama Model

Make sure you have Ollama installed and running:

```bash
ollama pull cyberguard:3b-7
```

### 🚀 Launch the Cyber-Guard Assistant

```bash
streamlit run app.py
```

---

## 💡 Example Use-Cases

| Role               | How Cyber-Guard Helps |
|--------------------|-----------------------|
| 🧑‍💻 Bug Bounty Hunters | Generates payloads, analyzes web apps, crafts reports |
| 🕵️ Red Teamers         | Assesses post-exploitation routes, attack chains |
| 🔒 Blue Teamers        | IOC mapping, SIEM rule testing, threat modeling |
| ⚙️ DevSecOps Engineers  | Pipeline audits, hardening guidance, SCA checks |
| 🧑‍🎓 Cybersecurity Learners | Learn via contextual examples, threat maps, compliance alignment |
---=-------------------------------------------------------------------------------------------

## 🛡️ Key Capabilities Matrix
----------------------------------------------
| Capability                 | Status         |
|---------------------------|-----------------|
| Deep Research Mode        | ✅ Implemented |
| CVE/CWE Analyzer          | ✅ Implemented |
| Streamlit Frontend        | ✅ Implemented |
| Ollama Model Integration  | ✅ Integrated  |
| DevSecOps Prompting       | ✅ Live        |
| Threat Modeling           | ✅ Basic       |
| Voice Input/Output        | 🔄 In Progress |
| Wazuh/SIEM Plugin Support | 🔜 Planned     |
| CLI-only mode             | 🔜 Planned     |
| PDF Report Generator      | 🔜 Planned     |
----------------------------------------------

## 🔐 Security Domains Covered

- OWASP Top 10: 2021/2023
- MITRE ATT&CK TTPs
- CIS Benchmarks (Linux, Docker, K8s)
- ISO 27001 Domain Controls
- Cloud Security (AWS S3 misconfigs, IAM attacks, etc.)
- VAPT Lifecycle Automation

---

## 🧠 Prompts in Action (Examples)

- *"Explain the impact of an IDOR in a financial system with session-based authentication."*
- *"Generate a bypass payload for XSS on a React-based SPA with CSP strict rules."*
- *"Analyze this Jenkinsfile and suggest security misconfigurations."*
- *"Simulate lateral movement techniques after SSH access to internal box."*

---

## 🧑‍🤝‍🧑 Contributors
------------------------------------------------------
| Name           | Role                             |
|----------------|----------------------------------|
| Hitarth Shah   | Lead Developer, Deep Research Creator |
| Maharishi      | DevSecOps Integration, Testing Lead |
| Dhaarakh       | UI/UX Designer, Backend Contributor |
--------------------------------------------------------

## 📢 Contact Us

- 📧 Email: `hitarthshahx`
- 🔗 LinkedIn: [Hitarth Shah]
- 🐦 Twitter: [@hits]

---

## 📜 License

Cyber-Guard is licensed under the [MIT License](LICENSE).  
Feel free to fork, contribute, or build on top of this project with credit.

---

## ✨ Closing Note

> *Built by hackers, for defenders. Cyber-Guard is not just a chatbot—it’s your AI analyst, researcher, and security companion.*

**🔐 Hack Smarter. Defend Stronger.**
