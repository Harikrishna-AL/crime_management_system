from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from routes import (
    role_router,
    station_router,
    officer_router,
    fir_router,
    crime_router,
    investigation_router,
    criminal_router,
    investigation_officers_router,
    crimes_involved_router,
    part_of_router,
    validate_router,
)

app = FastAPI()
app.include_router(role_router)
app.include_router(station_router)
app.include_router(officer_router)
app.include_router(fir_router)
app.include_router(crime_router)
app.include_router(investigation_router)
app.include_router(criminal_router)
app.include_router(investigation_officers_router)
app.include_router(crimes_involved_router)
app.include_router(part_of_router)
app.include_router(validate_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
