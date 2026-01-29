import os
from flask import Flask, jsonify, request
from amadeus import Client, ResponseError
from dotenv import load_dotenv

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
    """
    higher score -> better
    """

    opt_for = preferences.get("optimize_for", "price")
    price = route.get("price", 0)
    duration = route.

@app.route("/flightsearch", methods=["POST"])
def flightsearch():
    data = request.get_json(silent=True) or {}

    origin = data.get("origin")
    destination = data.get("destination")
    departure_date = data.get("departure_date")
    return_date = data.get("return_data")
    adults = int(data.get("adults"))
    currency = data.get("currency_code")
    max_price = body.get("max_price")
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
            "currency": currency,
            "totalTravelTimeMinutes": total_duration_minutes,
            "segments": segments_out,
            "score": 0.0,
            "summary": ""
        })

    response = {
        "routes": routes,
        "meta": params
    }
    return jsonify(response), 200

@app.route("/_health", methods["GET"])
def _health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)