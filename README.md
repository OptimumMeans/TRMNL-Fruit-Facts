# TRMNL Plugin Boilerplate

A boilerplate template for creating TRMNL e-ink display plugins.

## Features

- Flask-based webhook endpoint with CORS support
- E-ink display optimization
- Built-in caching system
- Comprehensive error handling
- Structured logging
- Environment-based configuration management
- Display generator service with error display support
- API service template with caching
- Extensive utility functions for formatting and validation

## Prerequisites

- Python 3.12+
- TRMNL device and API key
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/your-plugin.git
cd your-plugin
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.template .env
```

5. Update .env with your configuration:
```
TRMNL_API_KEY=your_api_key_here
TRMNL_PLUGIN_UUID=your_plugin_uuid_here
```

## Development

### Running Locally

```bash
python -m src.app
```

The development server will automatically open your default browser to the webhook endpoint. You can access:
- Home page: http://localhost:8080/
- Webhook endpoint: http://localhost:8080/webhook

### Project Structure
```
├── .env.template         # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── render.yaml          # Render deployment configuration
├── requirements.txt     # Python dependencies
├── src/                 # Source code directory
│   ├── app.py          # Main application entry point
│   ├── config.py       # Configuration management
│   ├── services/       # Core services
│   │   ├── api_service.py    # API interaction service
│   │   └── display.py        # Display generation service
│   └── utils/          # Utility functions
│       ├── __init__.py      # Package exports
│       ├── formatters.py    # Data formatting utilities
│       └── validators.py    # Data validation utilities
└── tests/              # Test files
    └── test_display.py  # Display service tests
```

### Core Components

1. **API Service** (`src/services/api_service.py`)
   - Handles all API interactions
   - Implements caching mechanism
   - Tracks last update timestamp

2. **Display Generator** (`src/services/display.py`)
   - Creates optimized images for e-ink display
   - Handles error displays
   - Supports status bar and content layout

3. **Utility Functions**
   - `formatters.py`: Date/time formatting, API response formatting
   - `validators.py`: Data validation, string sanitization
   - Common utilities exported through `__init__.py`

4. **Configuration** (`src/config.py`)
   - Environment-based configuration
   - Validation for required settings
   - Default values for optional settings

### Creating Your Plugin

1. Modify `src/services/api_service.py` to implement your data fetching logic
2. Update `src/services/display.py` to customize the display layout
3. Add any additional utilities in `src/utils/`
4. Update configuration in `src/config.py` as needed

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Current test coverage includes:
- Display generator initialization
- Error display generation
- API service functionality
- Display creation with mock data

## Deployment

Deploy using render.yaml configuration:

```bash
render deploy
```

The render.yaml file includes:
- Python 3.12.0 runtime
- Gunicorn web server
- Environment variable configuration
- Build and start commands

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT