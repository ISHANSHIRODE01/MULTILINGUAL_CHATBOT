import sys
import os
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.backend.logger import app_logger

async def test_backend():
    print("\n1. Testing Backend Health...")
    try:
        from src.backend.app import app
        print("✅ Backend module imported successfully")
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False
    return True

async def test_asr():
    print("\n2. Testing ASR Module...")
    try:
        from src.backend import asr
        # Just check if model loads (mocking or using small model)
        # We won't actually load the model here to save time/memory in CI, 
        # but we check if the module is valid.
        print("✅ ASR module imported successfully")
        return True
    except Exception as e:
        print(f"❌ ASR module failed: {e}")
        return False

async def test_tts():
    print("\n3. Testing TTS Module (Edge-TTS)...")
    try:
        from src.backend import tts
        # Test synthesis
        out_path = "test_tts.mp3"
        await tts.synthesize_to_file("Hello", out_path, lang="en")
        if os.path.exists(out_path):
            print(f"✅ TTS generated file: {out_path}")
            os.remove(out_path)
            return True
        else:
            print("❌ TTS failed to generate file")
            return False
    except Exception as e:
        print(f"❌ TTS module failed: {e}")
        return False

async def test_orchestrator():
    print("\n4. Testing Orchestrator (Imports only)...")
    try:
        from src.agents import orchestrator
        print("✅ Orchestrator imported successfully")
        return True
    except Exception as e:
        print(f"❌ Orchestrator import failed: {e}")
        return False

async def main():
    print("=== Multilingual Chatbot System Test ===")
    
    results = [
        await test_backend(),
        await test_asr(),
        await test_tts(),
        await test_orchestrator()
    ]
    
    if all(results):
        print("\n=== All Tests Passed ===")
        sys.exit(0)
    else:
        print("\n=== Some Tests Failed ===")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
