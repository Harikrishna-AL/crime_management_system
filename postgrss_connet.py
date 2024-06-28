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
)
from dotenv import load_dotenv
import os
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

load_dotenv()

config = {
    "dbname": os.getenv("DB_NAME"),
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": os.getenv("DB_PORT"),
}

def connect_to_db():
    return psycopg2.connect(**config)

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

class Search(BaseModel):
    search: str
    db: str
    parameter: str

@app.get("/get_by_search")
def get_by_search(search: Search):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Convert table name to lowercase and ensure no quotes around it
    table_name = sql.Identifier(search.db.lower()).as_string(conn).strip('"')
    
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.SQL(table_name),
        sql.Identifier(search.parameter),
        sql.Literal(f'{search.search}%')
    )
    print(query)
    
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
