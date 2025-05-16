#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Configure logging
import logging
import os
import sys
import threading
from typing import List, Optional

import pystray
import uvicorn
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI(
    title="FastAPI Demo",
    description="A simple FastAPI demo application",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for items
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True


# In-memory database
items_db = []
item_id_counter = 1


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Demo"}


@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    global item_id_counter
    item.id = item_id_counter
    item_id_counter += 1
    items_db.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item.id = item_id
    items_db[item_index] = updated_item
    return updated_item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db.pop(item_index)
    return {"message": "Item deleted successfully"}


class SystemTrayApp:
    def __init__(self):
        self.is_running = False
        self.server_thread = None
        self.icon = None
        self.config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            log_config=None  # Disable uvicorn's default logging config
        )
        self.server = uvicorn.Server(self.config)
        self.setup_tray()

    def setup_tray(self):
        # Create a simple icon (you can replace this with your own icon file)
        icon_image = Image.new('RGB', (64, 64), color='blue')

        # Create the system tray icon
        self.icon = pystray.Icon("fastapi_app")
        self.icon.icon = icon_image
        self.icon.title = "FastAPI Demo App"

        # Create the menu
        self.icon.menu = pystray.Menu(
            pystray.MenuItem(
                'Start Server',
                self.start_server,
                enabled=lambda _: not self.is_running
            ),
            pystray.MenuItem(
                'Stop Server',
                self.stop_server,
                enabled=lambda _: self.is_running
            ),
            pystray.MenuItem(
                'Exit',
                self.exit_app
            )
        )

    def start_server(self):
        if not self.is_running:
            self.is_running = True
            self.server_thread = threading.Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()

    def _run_server(self):
        try:
            self.server.run()
        except Exception as e:
            print(f"Error in server thread: {str(e)}")
            self.is_running = False

    def stop_server(self):
        if self.is_running:
            self.is_running = False
            self.server.should_exit = True
            if self.server_thread:
                self.server_thread.join(timeout=1)
                self.server_thread = None

    def exit_app(self):
        self.stop_server()
        self.icon.stop()
        os._exit(0)

    def run(self):
        self.icon.run()


if __name__ == "__main__":
    app = SystemTrayApp()
    app.run()
