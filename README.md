# Route Pilot

**Route Pilot** is a conversational flight optimizer that helps users find the cheapest flight routes through voice interaction. Unlike traditional flight search engines, Route Pilot acts as an AI travel agent that explores unconventional routes, multi-city hacks, positioning flights, and nearby airports to find the best deals.

## 🎬 Demo

**👉 [Watch the Demo Video](https://www.loom.com/share/602b34c8bafe4ef9b9a3b06a45eb5929)**

See Route Pilot in action! The demo shows how the conversational AI assistant helps find the best flight deals through natural voice interaction.

## 🎯 Overview

Route Pilot combines:
- **Voice AI** (via VAPI) for natural conversation about travel needs
- **Flight search** (via Amadeus API) for real-time flight data
- **Smart routing** that considers price vs. time tradeoffs, nearby airports, and overnight layovers
- **A modern landing page** that explains the service

> **📹 [Watch the demo](https://www.loom.com/share/602b34c8bafe4ef9b9a3b06a45eb5929) to see Route Pilot in action!**

## ✨ Features

- **Conversational Interface**: Call Route Pilot and describe your travel needs in plain language
- **Intelligent Route Optimization**: Finds cheaper routes through:
  - Multi-city flight hacks
  - Positioning flights
  - Nearby airport alternatives
  - Overnight layover tradeoffs
- **Flexible Search**: Supports budget ceilings, flexible dates, and constraint-based optimization
- **Smart Scoring**: Routes are scored and ranked based on user preferences (price vs. time)
- **Real-time Flight Data**: Integrates with Amadeus API for live flight information

## 🏗️ Architecture

The project consists of three main components:

1. **Backend Agent** (`agent/`): Flask API that handles flight search requests
2. **VAPI Assistant** (`agent/vapi_assistant.py`): Configures the voice AI assistant
3. **Website** (`website/`): Static landing page for the service

## 📁 Project Structure

```
routepilot/
├── agent/                    # Backend Flask application
│   ├── app.py               # Main Flask app with flight search logic
│   ├── vapi_assistant.py    # VAPI assistant configuration script
│   ├── route-schema.json    # Example request/response schema
│   ├── requirements.txt     # Python dependencies
│   ├── fly.toml            # Fly.io deployment config
│   ├── railway.json        # Railway deployment config
│   └── README.md           # Agent-specific README
├── website/                 # Static landing page
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Stylesheet
│   ├── script.js           # Progressive enhancement JS
│   └── README.md           # Website-specific README
├── agent_sys_prompt.txt    # System prompt for the AI assistant
└── README.md               # This file
```

## 🎨 How It Works

1. **User calls** Route Pilot via phone
2. **VAPI assistant** engages in conversation to understand:
   - Origin and destination
   - Travel dates (flexible or fixed)
   - Budget constraints
   - Preferences (price vs. time, layovers, nearby airports)
3. **Assistant calls** the Flask API with search parameters
4. **Flask API** queries Amadeus API for flight options
5. **Routes are scored** based on user preferences
6. **Results are returned** to the assistant, which explains options to the user

## 🔍 Route Scoring

Routes are scored using a weighted algorithm:

- **Price weight**: 1.0 if optimizing for price, 0.7 otherwise
- **Time weight**: 1.0 if optimizing for time, 0.7 otherwise
- **Score formula**: `1.0 / (1.0 + (price_weight * price/100 + time_weight * duration/60))`

Higher scores indicate better routes. Results are sorted by score (descending).

## 📝 Notes

- The Amadeus API is currently configured for **test mode** (see `hostname="test"` in `app.py`)
- Update the phone number in `website/index.html` when you have a real VAPI number
- The system prompt in `agent_sys_prompt.txt` can be customized to change the assistant's behavior

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- [Amadeus API](https://developers.amadeus.com) for flight data
- [VAPI](https://vapi.ai) for voice AI infrastructure
- [Flask](https://flask.palletsprojects.com/) for the web framework

