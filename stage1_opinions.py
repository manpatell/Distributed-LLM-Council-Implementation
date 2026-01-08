import asyncio
import httpx
from network_config import COUNCIL_MEMBERS

async def get_opinion(member, user_query):
    print(f"📡 Requesting opinion from {member['name']}...")
    url = f"{member['ip']}/api/generate"
    payload = {
        "model": member['model'],
        "prompt": user_query,
        "stream": False
    }
    
    try:
        # Increased timeout to 120 seconds for slower local hardware
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                answer = response.json().get('response')
                if not answer:
                    return {"name": member['name'], "answer": "Error: Model returned an empty string."}
                return {"name": member['name'], "answer": answer}
            else:
                return {"name": member['name'], "answer": f"Error: HTTP {response.status_code}"}
                
    except Exception as e:
        print(f"❌ Error reaching {member['name']}: {e}")
        # We return a dict with the error message so Stage 2 doesn't find 'None'
        return {"name": member['name'], "answer": f"Technical failure: Could not connect to model."}

async def run_stage_1(query):
    tasks = [get_opinion(m, query) for m in COUNCIL_MEMBERS]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    query = input("Enter your question for the Council: ")
    opinions = asyncio.run(run_stage_1(query))
    
    print("\n--- STAGE 1 COMPLETE ---")
    for op in opinions:
        print(f"\n[{op['name']}'s Response]:\n{op['answer'][:200]}...") # Printing first 200 chars