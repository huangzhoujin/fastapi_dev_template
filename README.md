# FastAPI Demo Application

A simple REST API demo built with FastAPI that demonstrates CRUD operations for items, with system tray controls for easy server management.

## Features

- RESTful API endpoints for managing items
- Automatic API documentation with Swagger UI
- Input validation using Pydantic models
- CORS middleware enabled
- In-memory database for demonstration
- System tray application for easy server control
- Can be packaged as a standalone executable

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- Windows:

```bash
.\venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

Start the application with:

```bash
python main.py
```

A blue system tray icon will appear in your system tray (notification area).

### Building Standalone Executable

To create a standalone executable using PyInstaller:

1. Make sure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

2. Build the executable:

```bash
pyinstaller --noconsole --icon=icon.ico --add-data "icon.ico;." main.py
```

The executable will be created in the `dist` directory. You can run it directly without needing Python installed.

Note: If you don't have an icon file, you can omit the `--icon` and `--add-data` options:

```bash
pyinstaller --noconsole main.py
```

### System Tray Controls

Right-click the system tray icon to access the following controls:

- **Start Server**: Starts the FastAPI server
- **Stop Server**: Stops the FastAPI server
- **Exit**: Completely exits the application

The server will run in the background, and you can control it through the system tray icon without keeping a terminal window open.

## API Access

Once the server is started, it will be available at `http://localhost:8000`

## API Documentation

When the server is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

- `GET /`: Welcome message
- `GET /items`: List all items
- `GET /items/{item_id}`: Get a specific item
- `POST /items`: Create a new item
- `PUT /items/{item_id}`: Update an existing item
- `DELETE /items/{item_id}`: Delete an item

## Example Item Structure

```json
{
  "name": "Example Item",
  "description": "This is an example item",
  "price": 29.99,
  "is_available": true
}
```

## Usage Tips

1. The application runs in the background with a system tray icon
2. You can start/stop the server without closing the application
3. The server can be restarted multiple times without restarting the application
4. Use the system tray icon to completely exit the application when done

## Distribution

### Windows
1. Build the executable using build-gui.bat
2. The standalone executable will be in the `dist` directory
3. The standalone executable name is ‘fastapi_dev_temp.exe’
3. Copy the executable to the target machine
4. Run the executable directly - no Python installation required

