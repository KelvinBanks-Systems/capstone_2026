from fastapi import FastAPI, HTTPException
import aiosqlite
import time

app = FastAPI(title="Fountainhead Electronics Core POS API Subsystem")
DB_FILE = "inventory.db"

@app.get("/search/{part_number}")
async def search_part(part_number: str):
    # Capture highly precise system execution entry timestamp
    start_time = time.perf_counter()
    
    # Establish a non-blocking asynchronous connection context to the database file
    async with aiosqlite.connect(DB_FILE) as db:
        # Enforce Row factory layout to access data matching database column names
        db.row_factory = aiosqlite.Row
        
        # Query utilizing explicit parameters to prevent any injection bugs
        async with db.execute(
            "SELECT * FROM items WHERE part_number = ? LIMIT 1;", (part_number,)
        ) as cursor:
            row = await cursor.fetchone()
            
    # Calculate absolute delta duration transformed directly to milliseconds
    latency_ms = (time.perf_counter() - start_time) * 1000
    
    if not row:
        raise HTTPException(status_code=404, detail="Component Part Number Not Found")
        
    return {
        "part_number": row["part_number"],
        "description": row["description"],
        "stock": row["stock_count"],
        "server_latency_ms": round(latency_ms, 4)
    }

@app.post("/admin/index")
async def toggle_index(enabled: bool):
    """Admin operational control endpoint allowing programmatic index toggling."""
    async with aiosqlite.connect(DB_FILE) as db:
        if enabled:
            # Create a B-Tree structural constraint optimization over the search column
            await db.execute("CREATE INDEX IF NOT EXISTS idx_part ON items(part_number);")
            msg = "B-Tree Database Index Applied Successfully [O(log n) active]"
        else:
            # Drop structural index to purposefully simulate the legacy flat table configuration
            await db.execute("DROP INDEX IF EXISTS idx_part;")
            msg = "B-Tree Database Index Dropped [O(n) linear scanning active]"
        await db.commit()
    return {"status": msg}
