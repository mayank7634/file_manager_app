from waitress import serve
from app import app  # make sure your main Flask app is called `app`

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
