import os
from flask import Flask, jsonify, request
from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()

def create_amadeus_client():
    return Client(
        client_id=os.getenv("AMADEUS_API_KEY"),
        client_secret=os.getenv("AMADEUS_SECRET"),
        hostname="test" if os.getenv("AMADEUS_ENV", "test") == "test" else "production"
    )

amadeus = create_amadeus_client()

app = Flask(__name__)

@app.route("/flightsearch", methods=["POST"])
def flightsearch():
    data = request.get_json(silent=True) or {}

    origin = data.get("origin")
    destination = data.get("destination")
    date_from = data.get("date_from")
    date_to = data.get("date_to")

    if not origin or not destination or not date_from or not date_to:
        return jsonify({
            "error": "Missing required fields: origin, destination, date_from, date_to"
        }), 400

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date_from,
        "returnDate": date_to,
        "adults": 1,
        "currencyCode": "USD",
        "max": 1 
    }

    try:
        response = amadeus.shopping.flight_offers_search.get(**params)
        data = response.data
        print(data)
    except ResponseError as error:
        return jsonify({"error": str(error)}), 500

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
                    except Exception:
                        pass

                segments_out.append({
                    "from": dep.get("iataCode"),
                    "to": arr.get("iataCode"),
                    "carrierCode": seg.get("carrierCode"),
                    "departure": dep_time,
                    "arrival": arr_time,
                    "number": seg.get("number")
                })

        routes.append({
            "id": f"route_{idx+1}",
            "price": total_price,
            "currency": "USD",
            "totalTravelTimeMinutes": total_duration_minutes,
            "segments": segments_out,
            "score": 0.0,
            "summary": ""
        })

    response = {
        "search_params": {
            "origin": origin,
            "destination": destination,
            "date_from": date_from,
            "date_to": date_to
        },
        "options": routes
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)