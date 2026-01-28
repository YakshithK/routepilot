from flask import Flask, jsonify, request

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

    example_option = {
        "id": "dummy-1",
        "price": 412.00,
        "currency": "USD",
        "routes": [{
            "from": origin,
            "to": destination,
            "airline": "Air Skibdi",
            "flight_number": "CityBoy67",
            "departure": f"{date_from}T10:00:00",
            "arrival": f"{date_from}T10:00:00",
            "layovers": []
        }],
        "total_travel_time_hours": 10,
        "self_transfer": False,
        "explanation": (
            "This is an example flight route used for testing. Replace with real logic once the Flight API integration is made."
        )
    }

    response = {
        "search_params": {
            "origin": origin,
            "destination": destination,
            "date_from": date_from,
            "date_to": date_to
        },
        "options": [example_option]
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)