# main.py (The Chairman's brain)
import asyncio
from stage1_opinions import run_stage_1
from stage2_review import run_stage_2

async def main():
    query = input("Ask the Council: ")
    
    # STAGE 1
    print("\n--- STAGE 1: Gathering Opinions ---")
    opinions = await run_stage_1(query)
    
    # STAGE 2
    print("\n--- STAGE 2: Peer Review ---")
    reviews = await run_stage_2(query, opinions)
    
    for r in reviews:
        print(f"\n[{r['reviewer']}'s Review]:\n{r['review']}")

    # Save these for Stage 3!
    return query, opinions, reviews

if __name__ == "__main__":
    asyncio.run(main())