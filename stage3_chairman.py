import httpx
from network_config import CHAIRMAN

async def run_stage_3(original_query, opinions, reviews):
    print(f"👑 Chairman ({CHAIRMAN['model']}) is synthesizing the final answer...")
    
    # 1. Start building the dossier
    dossier = f"USER QUERY: {original_query}\n\n"
    
    # 2. Add Opinions (with safety check)
    dossier += "--- COUNCIL OPINIONS ---\n"
    for i, op in enumerate(opinions):
        # Use .get() to avoid crashes if 'answer' is missing
        content = op.get('answer', "No response provided.") if op else "Missing response."
        dossier += f"Model {i+1}: {content}\n\n"
        
    # 3. Add Reviews (with safety check - THIS IS WHERE IT CRASHED)
    dossier += "--- PEER REVIEWS & RANKINGS ---\n"
    for i, rev in enumerate(reviews):
        # Safe check: if 'rev' is None or 'review' key is missing
        content = rev.get('review', "Review not available.") if rev else "Review failed."
        dossier += f"Review from Model {i+1}: {content}\n\n"

    system_prompt = """
    You are the Chairman of the LLM Council. 
    Synthesize a final, authoritative response based on the council's input.
    """

    url = f"{CHAIRMAN['ip']}/api/generate"
    payload = {
        "model": CHAIRMAN['model'],
        "system": system_prompt,
        "prompt": dossier,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client: # Increased timeout for Chairman
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get('response', "Chairman failed to synthesize.")
            else:
                return f"Chairman Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Chairman Connection Error: {e}"