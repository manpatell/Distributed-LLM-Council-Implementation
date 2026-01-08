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
| **Member 2** | `10.1.170.132` | `mistral` | Council Node |
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