from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

AUTH_SERVICE_URL = "http://auth-service:80"


@app.get("/")
async def root():
    return {"message": "Gateway Service is active"}


@app.post("/auth/login")
async def auth_login(request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{AUTH_SERVICE_URL}/token", data=await request.form())
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="Auth service is unavailable") from exc
