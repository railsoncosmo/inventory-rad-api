from app import app

@app.route("/")
def health():
  return "Server is running"