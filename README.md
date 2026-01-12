# 🏛️ Distributed LLM Council: Local Deployment

## 👥 Team Information
* **Team Members:** Man Vijaybhai PATEL, Luthfi Juneeda SHAJ, Sandeep PIDUGU, Sid, setu
* **TD Group:** CDOF1
* **Project:** Gen AI

---

## 📜 Project Overview
This project is a local, distributed refactor of the **LLM Council** concept inspired by Andrej Karpathy. Instead of relying on cloud APIs, we have built a multi-stage reasoning system that runs entirely on local hardware across **four separate physical machines** communicating via a local network.

### The 3-Stage Workflow:
1.  **Stage 1 (First Opinions):** Three independent Council Members (distributed PCs) generate answers to a user query in parallel.
2.  **Stage 2 (Review & Ranking):** All responses are anonymized and sent back to the Council Members. Each model reviews and ranks the others to eliminate bias.
3.  **Stage 3 (Chairman Final Answer):** A dedicated Chairman machine synthesizes all original responses and peer rankings into a single, high-quality final response.

---

## 🏗️ Distributed Architecture
| Role | Machine Connection | Model Used | Note |
| :--- | :--- | :--- | :--- |
| **Chairman** | `127.0.0.1` (Local) | `phi3:mini` | Optimized for low VRAM stability |
| **Member 1** | `Remote IP` | `phi3` | Council Node |
| **Member 2** | `Remote IP` | `mistral` | Council Node |
| **Member 3** | `Remote IP` | `phi3` | Council Node |

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* **Ollama:** Installed on all machines ([ollama.com](https://ollama.com)).
* **Python 3.10+:** Installed on the Chairman PC.
* **Network:** All machines must be connected to the same local Wi-Fi.

### 2. Council Member Configuration
Every member machine must allow external network requests. In PowerShell/Terminal, run:
```powershell
$env:OLLAMA_HOST="0.0.0.0"
ollama serve
```
## 💻 Tech Stack

### Core Infrastructure
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-000000?style=for-the-badge&logo=ollama&logoColor=white)
![AsyncIO](https://img.shields.io/badge/AsyncIO-Concurrency-red?style=for-the-badge)

### Libraries & Protocols
![HTTPX](https://img.shields.io/badge/HTTPX-Async_Requests-blue?style=for-the-badge)
![REST API](https://img.shields.io/badge/REST_API-Communication-green?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data_Interchange-orange?style=for-the-badge)

### AI Models Utilized
| Role | Model | Size |
| :--- | :--- | :--- |
| **Orchestrator** | `SmolLM2` | 135M |
| **Worker Node** | `Mistral` | 7B |
| **Worker Node** | `Phi-3` | 3.8B |

## 👥 Team Roles & Responsibilities

To ensure efficient distributed development, our team of 5 divided the project tasks as follows:

### 1. Lead Architect (The "Chairman")
* **Focus:** Central Logic & Synthesis.
* **Responsibilities:**
    * Developed `final_council.py` (The main orchestrator).
    * Implemented `stage3_chairman.py` (The synthesis logic).
    * Managed the Chairman PC configuration and SLM (`smollm2`) integration.
    * **Deliverable:** A fully integrated orchestration script.

### 2. Network Engineer (The "Connector")
* **Focus:** Infrastructure & Connectivity.
* **Responsibilities:**
    * Configured Static/Local IPs for all 4 machines.
    * Managed `OLLAMA_HOST` variables and Firewall rules (Port 11434).
    * maintained `network_config.py` to ensure accurate routing.
    * **Deliverable:** Verified connectivity between all distributed nodes.

### 3. Backend Developer (The "Council")
* **Focus:** Worker Node Logic (Stages 1 & 2).
* **Responsibilities:**
    * Developed `stage1_opinions.py` for parallel asynchronous requests.
    * Developed `stage2_review.py` for anonymization and peer-review prompts.
    * Optimized prompts to ensure consistent JSON/Text outputs from models.
    * **Deliverable:** Functional opinion generation and review cycles.

### 4. QA & Reliability Engineer (The "Fixer")
* **Focus:** Error Handling & Stability.
* **Responsibilities:**
    * Implemented "Defensive Programming" checks (e.g., handling `NoneType` responses).
    * Stress-tested the system against network timeouts and memory limits.
    * **Deliverable:** A crash-resistant application with robust error logging.

### 5. Product Owner & Documentation Lead
* **Focus:** Presentation & Reporting.
* **Responsibilities:**
    * Authored the `README.md` and **Technical Report**.
    * Drafted the "Generative AI Usage Statement" for compliance.
    * **Live Demo Lead:** Narrates the council workflow during the professor's presentation.
    * **Deliverable:** Comprehensive project documentation and submission files.
