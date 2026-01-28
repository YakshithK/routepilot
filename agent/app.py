from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    
    @app.post("flight-search")
    def flight_search():
        

    return app


app = create_app()


if __name__ == "__main__":
    # Local dev default; override with env vars if needed.
    app.run(host="0.0.0.0", port=5000)


