import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")


def chat(system_prompt: str, messages: list, user_input: str, stream: bool = True) -> str:
    messages_to_send = messages + [{"role": "user", "content": user_input}]

    payload = {
        "model": MODEL_NAME,
        "system": system_prompt,
        "messages": messages_to_send,
        "stream": stream,
    }

    try:
        if stream:
            response = requests.post(
                f"{OLLAMA_HOST}/api/chat",
                json=payload,
                stream=True,
                timeout=120,
            )
            response.raise_for_status()

            full_reply = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    print(token, end="", flush=True)
                    full_reply += token
                    if chunk.get("done"):
                        break
            print()
            return full_reply

        else:
            response = requests.post(
                f"{OLLAMA_HOST}/api/chat",
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            return response.json()["message"]["content"]

    except requests.exceptions.ConnectionError:
        msg = "[Bell] Ollama isn't running. Start it with: ollama serve"
        print(msg)
        return msg
    except requests.exceptions.Timeout:
        msg = "[Bell] Request timed out. Ollama may be overloaded — try again."
        print(msg)
        return msg
    except Exception as e:
        msg = f"[Bell] Something went wrong: {e}"
        print(msg)
        return msg
