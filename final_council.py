import asyncio
from stage1_opinions import run_stage_1
from stage2_review import run_stage_2
from stage3_chairman import run_stage_3

async def run_full_council():
    query = input("\n📝 Enter your question for the Council: ")
    
    # STAGE 1
    print("\n[STEP 1] Gathering independent opinions...")
    opinions = await run_stage_1(query)
    
    # STAGE 2
    print("\n[STEP 2] Council members are reviewing each other...")
    reviews = await run_stage_2(query, opinions)
    
    # STAGE 3
    print("\n[STEP 3] Chairman is finalizing the output...")
    final_answer = await run_stage_3(query, opinions, reviews)
    
    print("\n" + "="*50)
    print("FINAL CHAIRMAN RESPONSE")
    print("="*50)
    print(final_answer)
    print("="*50)

if __name__ == "__main__":
    asyncio.run(run_full_council())