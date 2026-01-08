# stage2_review.py
import asyncio
import httpx
from network_config import COUNCIL_MEMBERS
import traceback
import time

async def get_review(reviewer, all_opinions, original_query):
    print(f"📡 Requesting review from {reviewer['name']}...")
    # Filter out any None values or failed connections
    valid_opinions = [op for op in all_opinions if op and op.get('answer')]

    if not valid_opinions:
        return {"reviewer": reviewer['name'], "review": "No valid opinions were generated to review."}

    anonymized_text = f"Original Query: {original_query}\n\n"
    for i, op in enumerate(valid_opinions):
        content = op.get('answer', "No content provided.")
        anonymized_text += f"\n--- ANSWER {i+1} ---\n{content}\n"

    review_prompt = f"""
    You are a peer reviewer in the LLM Council. Review the following anonymized opinions on the query.
    For each answer:
    - Summarize its key points.
    - Rate its accuracy, completeness, and relevance (1-10).
    - Suggest improvements.
    Finally, rank the answers from best to worst.
    {anonymized_text}
    """

    url = f"{reviewer['ip']}/api/generate"
    payload = {
        "model": reviewer['model'],
        "prompt": review_prompt,
        "stream": False
    }

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    review = response.json().get('response')
                    if not review:
                        return {"reviewer": reviewer['name'], "review": "Error: Model returned an empty string."}
                    return {"reviewer": reviewer['name'], "review": review}
                else:
                    return {"reviewer": reviewer['name'], "review": f"Error: HTTP {response.status_code}"}
        except Exception as e:
            print(f"❌ Error reaching {reviewer['name']} (attempt {attempt+1}): {e}\n{traceback.format_exc()}")
            if attempt < 2:
                await asyncio.sleep(2)
            else:
                return {"reviewer": reviewer['name'], "review": f"Technical failure: Could not connect to model after 3 attempts."}

async def run_stage_2(original_query, opinions):
    tasks = [get_review(m, opinions, original_query) for m in COUNCIL_MEMBERS]
    reviews = await asyncio.gather(*tasks)
    return reviews