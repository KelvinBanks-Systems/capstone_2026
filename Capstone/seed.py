import asyncio
import aiosqlite

async def seed_database():
    print("Initializing SQLite Database Generation...")
    # Connects and automatically creates the local database file
    async with aiosqlite.connect("inventory.db") as db:
        # Clear out any old versions to ensure a fresh, clean test environment
        await db.execute("DROP TABLE IF EXISTS items;")
        
        # Create a flat-file table layout with absolutely NO indexing or keys on part_number
        await db.execute("""
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_number TEXT NOT NULL,
                description TEXT NOT NULL,
                stock_count INTEGER NOT NULL
            );
        """)
        
        print("Generating exactly 40,000 unique electronic component rows...")
        # Construct sequential alphanumeric string keys from PART-00001 to PART-40000
        mock_items = [
            (f"PART-{str(i).zfill(5)}", f"Component Specification Node Type {i}", 100 + (i % 50))
            for i in range(1, 40001)
        ]
        
        # Batch insert the rows rapidly into the local disk block
        await db.executemany(
            "INSERT INTO items (part_number, description, stock_count) VALUES (?, ?, ?);", 
            mock_items
        )
        await db.commit()
        print("Database generation complete! File saved as 'inventory.db'.")

if __name__ == "__main__":
    asyncio.run(seed_database())
