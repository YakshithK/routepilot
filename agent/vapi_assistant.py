import requests
import os

VAPI_API_KEY = os.getenv("VAPI_API_KEY")

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

agent_payload = {
    "name": "RoutePilot",
    "model": {
        "provider": "openai",
        "model": "gpt-4o"
    },
    "voice": {
        "provider": "elevenlabs",
        "voiceId": "Rachel"
    },
    "systemPrompt": """
            You are a professional flight deal finder.

        Rules:
        - Never invent prices, routes, airlines, or times.
        - You may ONLY speak about flight info returned by tools.
        - If flight data is unavailable, say so clearly.
        - Always confirm search constraints before calling tools, make sure you have all of the required info.
        - Optimize based on the user's stated priorities.
        - Explain WHY a route is cheaper or faster based on the summaries and info received from the tool.
        - Speak concisely and confidently.
    """,

    "tools": [
        {
            "type": "functions",
            "function": {
                "name": "search_flights",
                "description": "Search for flight routes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string"},
                        "destination": {"type": "string"},
                        "departure_date": {"type": "string", "format": "date"},
                        "return_date": {"type": ["string", "null"]},
                        "adults": {"type": "integer"},
                        "currency_code": {"type": "string"},
                        "max_price": {"type": ["integer", "null"]},
                        "allow_nearby_airports": {"type": "boolean"},
                        "max_results": {"type": "integer"},
                        "preferences": {
                            "type": "object",
                            "properties": {
                                "optimize_for": {"type": "string"},
                                "carry_on_only": {"type": "boolean"},
                                "allow_overnight_layovers": {"type": "boolean"},
                                "allow_self_transfer": {"type": "boolean"}
                            }
                        }
                    },
                    "required": ["origin", "destination", "departure_date", "adults"]
                }
            }
        }
    ],
    "server": {
        "url": "https://routepilot-agent.onrender.com/flightsearch"
    }
}

res = requests.post(
    "https://api.vapi.ai/assistant",
    headers=headers,
    json=agent_payload
)

print(res.json())