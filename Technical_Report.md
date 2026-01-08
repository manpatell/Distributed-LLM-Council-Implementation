# Technical Report: Distributed LLM Council Implementation

## 1. Project Overview
This project refactors the original "LLM Council" concept—originally designed for cloud-based APIs—into a fully **local, distributed system**. The objective was to orchestrate multiple Large Language Models (LLMs) running on separate physical machines to collaborate on answering, reviewing, and synthesizing user queries without relying on external internet services.

## 2. System Architecture
We implemented a **Hub-and-Spoke Network Topology**:
* **The Hub (Chairman):** A central orchestration node that manages the workflow state, aggregates responses, and performs the final synthesis.
* **The Spokes (Council Members):** Three distributed worker nodes running distinct LLMs, accessible via REST API over the local network (LAN).

### Communication Protocol
All inter-machine communication is handled via **REST APIs** provided by Ollama.
* **Request Method:** `POST /api/generate`
* **Data Format:** JSON payloads containing prompts and model parameters.
* **Transport Layer:** HTTP over Local Wi-Fi (IP-based addressing).

## 3. Key Design Decisions

### A. Asynchronous Orchestration
In a distributed local network, latency is unpredictable. A sequential approach (asking Member 1, waiting, then asking Member 2) would result in unacceptable wait times.
* **Solution:** We utilized Python's `asyncio` and `httpx` libraries.
* **Impact:** This allows the Chairman to broadcast the User Query to all 3 council members simultaneously. The total wait time for Stage 1 is now determined by the *slowest* single model, rather than the sum of all models.

### B. Memory Optimization & Resource Management
During development, the Chairman machine (hosting the orchestration logic) encountered severe hardware constraints, specifically a **500 Internal Server Error** caused by insufficient RAM (2.3 GiB available vs. 4.8 GiB required for Llama 3).
* **Pivot:** We adopted a **heterogeneous model strategy**.
* **Implementation:** While Council Members ran standard 7B/3B models (Mistral, Phi-3), the Chairman was switched to a **Small Language Model (SLM)**, specifically `SmolLM2-135M` (and tested with `Qwen 2B`).
* **Result:** This reduced the Chairman's memory footprint by ~90%, ensuring 100% system stability without crashing the Python runtime or the operating system.

### C. Robust Error Handling
Distributed systems are prone to network timeouts and "zombie" processes.
* **Solution:** We implemented "Defensive Programming" in the synthesis logic.
* **Detail:** The synthesis script (`stage3_chairman.py`) validates that incoming reviews are well-formed dictionaries before processing. If a node fails (e.g., timeout), the system logs the error but continues the council session using the remaining available data, preventing a total system crash.

## 4. Model Selection Rationale

| Role | Model | Reason for Selection |
| :--- | :--- | :--- |
| **Council Member** | **Mistral 7B** | High reasoning capability; acts as the "Heavy Lifter" for complex logic. |
| **Council Member** | **Phi-3 Mini** | Excellent balance of speed and performance; provides a diverse perspective from Mistral. |
| **Chairman** | **SmolLM2-135M** | **Critical engineering decision.** Selected to fit within the strict 2.3 GB RAM limit of the central node while maintaining the ability to synthesize text. |

## 5. Improvements Over Original Implementation
1.  **Zero-Cost Operation:** Removed dependency on paid APIs (OpenAI/OpenRouter).
2.  **Privacy:** All data remains on the local LAN; no queries are sent to the cloud.
3.  **Blind Review:** We implemented a prompt-injection layer in Stage 2 that strips model identities, ensuring that Council Members review the *content* of an answer, not the *author*, effectively removing bias.

## 6. Conclusion
The project successfully demonstrates that a **Multi-Agent System** can be deployed effectively on consumer-grade hardware by combining efficient networking (Asynchronous I/O) with strategic model selection (SLMs). The final system is robust, cost-effective, and fully distributed.