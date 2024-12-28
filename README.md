# TRMNL Plugin Boilerplate

A boilerplate template for creating TRMNL e-ink display plugins.

## Features

- Flask-based webhook endpoint
- E-ink display optimization
- Caching system
- Error handling
- Logging
- Configuration management
- Display generator service
- API service template
- Utility functions for common tasks

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

### Project Structure
```
plugin/
├── src/
│   ├── services/     # Core services
│   ├── utils/        # Utility functions
│   ├── app.py        # Main application
│   └── config.py     # Configuration
├── tests/            # Test files
├── .env.template     # Environment template
├── requirements.txt  # Dependencies
└── render.yaml       # Deployment config
```

### Creating Your Plugin

1. Modify `src/services/api_service.py` to implement your data fetching logic
2. Update `src/services/display.py` to customize the display layout
3. Add any additional utilities in `src/utils/`
4. Update configuration in `src/config.py` as needed

## Testing

To run tests:

```bash
python -m pytest tests/
```

## Deployment

Deploy using render.yaml configuration:

```bash
render deploy
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT