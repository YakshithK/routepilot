import os
import json
import logging
from flask import Flask, jsonify, request
from amadeus import Client, ResponseError
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def create_amadeus_client():
    return Client(
        client_id=os.getenv("AMADEUS_API_KEY"),
        client_secret=os.getenv("AMADEUS_SECRET"),
        hostname="test"
    )

amadeus = create_amadeus_client()

app = Flask(__name__)

def compute_route_score(route, preferences):

    #higher score -> better

    opt_for = preferences.get("optimize_for", "price")
    price = route.get("price", 0)
    duration = route.get("total_travel_time_minutes", 0)

    # normalize with simple constants
    price_weight = 1.0 if opt_for == "price" else 0.7
    time_weight = 1.0 if opt_for == "time" else 0.7

    raw = price_weight * (price / 100.0) + time_weight * (duration / 60.0)

    #convert to 0-1 scale
    score = 1.0 / (1.0 + raw)

    return score

def summarize_route(route):
    segments = route.get("segments", [])
    price = route.get("price")
    currency = route.get("currency")
    total_minutes = route.get("total_travel_time_minutes", 0)

    num_legs = len(segments)
    stops = max(num_legs - 1, 0)
    hours = total_minutes // 60
    mins = total_minutes % 60

    if not segments:
        return f"Approximate price {price} {currency}."

    origin = segments[0]["from"]
    final = segments[-1]["to"]

    base = f"{stops} stop{'s' if stops != 1 else ''}" if stops > 0 else "non-stop"
    duration_text = f"{hours}h {mins}m" if total_minutes > 0 else "unknown duration"

    return (
        f"{base} trip from {origin} to {final}, about {duration_text}, "
        f"total price around {price} {currency}."
    )

@app.route("/flightsearch", methods=["POST"])
def flightsearch():
    raw_body = request.get_json(silent=True) or {}
    
    # Smart logging: log raw request first to understand structure
    logger.info("=" * 60)
    logger.info("Flight Search Request Received")
    logger.info("=" * 60)
    logger.info("Raw Request Body Structure:")
    try:
        logger.info(json.dumps(raw_body, indent=2, default=str))
    except Exception as e:
        logger.warning(f"Could not format raw body: {e}")
        logger.info(f"Raw body type: {type(raw_body)}")
        logger.info(f"Raw body: {raw_body}")
    
    # Extract function arguments from VAPI webhook structure
    # VAPI sends: { "message": { "toolCalls": [{ "function": { "arguments": {...} } }] } }
    try:
        if isinstance(raw_body, dict):
            # Try VAPI webhook structure
            if "message" in raw_body and "toolCalls" in raw_body["message"]:
                tool_calls = raw_body["message"]["toolCalls"]
                if tool_calls and len(tool_calls) > 0:
                    if "function" in tool_calls[0] and "arguments" in tool_calls[0]["function"]:
                        # Arguments might be a string (JSON) or dict
                        arguments = tool_calls[0]["function"]["arguments"]
                        if isinstance(arguments, str):
                            body = json.loads(arguments)
                        else:
                            body = arguments
                        logger.info("Extracted arguments from VAPI tool call structure")
                    else:
                        logger.warning("No 'function.arguments' found in tool call")
                        body = raw_body
                else:
                    logger.warning("No tool calls found in message")
                    body = raw_body
            else:
                # Assume body is already the arguments (direct call)
                body = raw_body
                logger.info("Using request body directly (not VAPI webhook structure)")
        else:
            body = raw_body
            logger.warning(f"Unexpected body type: {type(raw_body)}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"Error extracting arguments: {e}")
        logger.info("Falling back to raw body")
        body = raw_body
    
    logger.info("-" * 60)
    
    # Log individual key fields (always visible, won't truncate)
    logger.info(f"Origin: {body.get('origin', 'NOT PROVIDED')}")
    logger.info(f"Destination: {body.get('destination', 'NOT PROVIDED')}")
    logger.info(f"Departure Date: {body.get('departure_date', 'NOT PROVIDED')}")
    logger.info(f"Return Date: {body.get('return_date', 'NOT PROVIDED')}")
    logger.info(f"Adults: {body.get('adults', 'NOT PROVIDED')}")
    logger.info(f"Currency: {body.get('currency_code', 'NOT PROVIDED')}")
    logger.info(f"Max Price: {body.get('max_price', 'NOT PROVIDED')}")
    logger.info(f"Max Results: {body.get('max_results', 'NOT PROVIDED')}")
    
    # Log preferences if present
    if body.get('preferences'):
        logger.info(f"Preferences: {json.dumps(body.get('preferences'), indent=2)}")
    
    # Log full body as formatted JSON (may truncate in console, but structure is visible)
    try:
        body_str = json.dumps(body, indent=2, default=str)
        logger.info("Full Request Body:")
        logger.info(body_str)
    except Exception as e:
        logger.warning(f"Could not format body as JSON: {e}")
        logger.info(f"Raw body: {body}")
    
    logger.info("=" * 60)

    origin = body.get("origin")
    destination = body.get("destination")
    departure_date = body.get("departure_date")
    return_date = body.get("return_date") or None
    adults = int(body.get("adults"))
    currency = body.get("currency_code")
    max_price = body.get("max_price") or None
    max_results = int(body.get("max_results"))

    if not origin or not destination or not departure_date:
        return jsonify({
            "error": "Missing required fields: origin, destination, departure_date"
        }), 400

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "currencyCode": currency,
        "max": max_results
    }

    if return_date:
        params["return_date"] = return_date
    if max_price:
        params["max_price"] = int(max_price)

    try:
        response = amadeus.shopping.flight_offers_search.get(**params)
        data = response.data

    except ResponseError as error:
        return jsonify({"error": str(error)}), 500

    preferences = body.get("preferences") or {}
    routes = []
    for idx, offer in enumerate(data):
        price_info = offer.get("price", {})
        total_price = float(price_info.get("grandTotal", 0))
        itineraries = offer.get("itineraries", [])
        total_duration_minutes = 0
        segments_out = []

        if itineraries:
            first_itin = itineraries[0]
            for seg in first_itin.get("segments", []):
                dep = seg.get("departure", {})
                arr = seg.get("arrival", {})
                dep_time = dep.get("at")
                arr_time = arr.get("at")

                # compute duration
                if dep_time and arr_time:
                    try: 
                        dt_dep = datetime.fromisoformat(dep_time)
                        dt_arr = datetime.fromisoformat(arr_time)
                        total_duration_minutes += int((dt_arr - dt_dep).total_seconds() / 60)
                    except Exception as e:
                        print("error: ", e)
                        pass

                segments_out.append({
                    "from": dep.get("iataCode"),
                    "to": arr.get("iataCode"),
                    "carrierCode": seg.get("carrierCode"),
                    "departure": dep_time,
                    "arrival": arr_time,
                    "number": seg.get("number")
                })

        route_obj = {
            "id": f"route_{idx+1}",
            "price": total_price,
            "currency": currency,
            "total_travel_time_minutes": total_duration_minutes,
            "segments": segments_out,
            "score": 0.0,
            "summary": ""
        }

        route_obj["score"] = compute_route_score(route_obj, preferences)
        route_obj["summary"] = summarize_route(route_obj)
        routes.append(route_obj)

    routes.sort(key=lambda r: r["score"], reverse=True)

    response = {
        "routes": routes,
        "meta": params
    }
    return jsonify(response), 200

@app.route("/_health", methods=["GET"])
def _health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)