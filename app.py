#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Project :   fastapi_dev_template
@File    :   app.py.py
@Contact :   zhoujin.huang@genpact.com
@License :   https://www.genpact.com/privacy/terms-and-conditions
@Revised              @Author           @Version    @Desciption
------------------    --------------    --------    -----------
5/23/2025 6:26 AM       Zhoujin Huang     1.0.0       None
'''
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
from starlette.staticfiles import StaticFiles

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

if getattr(sys, 'frozen', False):
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    static_dir = os.path.join(sys._MEIPASS, "static")
else:
    static_dir = "static"

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


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
