from fastapi import FastAPI

app = FastAPI(title="AutoDigital Digest", version="1.0.0")
@app.get("/")
def health_check():
    return {"status": "ok", "message": "AutoDigital Digest is running!"}