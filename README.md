# TRMNL Fruit Facts

A TRMNL e-ink display plugin that shows rotating fruit facts and nutritional information using the Fruityvice API. Perfect for learning about different fruits and their nutritional content.

## Features

- Displays detailed fruit information including:
  - Nutritional facts (calories, carbs, protein, fat, sugar)
  - Scientific classification (family, genus, order)
  - Common name and identification
- Automatically rotates through different fruits
- Optimized for e-ink displays
- Built-in caching to minimize API calls
- Development mode for easy testing

## Prerequisites

- Python 3.12+
- TRMNL device and API key (for production use)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/OptimumMeans/TRMNL-Fruit-Facts.git
cd TRMNL-Fruit-Facts
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

4. Run in development mode:
```bash
python -m src.app
```

The application will start and open your browser to display the fruit facts.

## Configuration

### Development Mode
No configuration needed - just run the application and it will work with default settings.

### Production Mode
Create a `.env` file with your TRMNL credentials:
```
DEV_MODE=False
TRMNL_API_KEY=your_api_key_here
TRMNL_PLUGIN_UUID=your_plugin_uuid_here
REFRESH_INTERVAL=3600  # How often to refresh the display (in seconds)
FRUIT_ROTATION_INTERVAL=86400  # How often to change fruits (in seconds)
```

## Display Layout

The plugin uses a clean, organized layout that includes:
- Large fruit name header
- Nutrition facts panel with key nutritional information
- Scientific classification panel
- Status bar showing update time and fruit count

## Development

### Project Structure
```
├── src/
│   ├── app.py              # Main application
│   ├── config.py           # Configuration management
│   ├── services/
│   │   ├── api_service.py  # Fruityvice API integration
│   │   └── display.py      # E-ink display generation
│   └── utils/
│       ├── formatters.py   # Data formatting utilities
│       └── validators.py   # Data validation
└── tests/
    └── test_display.py     # Display tests
```

### Testing
Run the test suite:
```bash
python -m pytest tests/
```

## Production Deployment

1. Set up your TRMNL device and get your API credentials

2. Update your `.env` file with production settings:
```
DEV_MODE=False
DEBUG=False
HOST=0.0.0.0
PORT=8080
```

3. Deploy using render.yaml configuration:
```bash
render deploy
```

## Customization

### Refresh Intervals
- `REFRESH_INTERVAL`: How often the display updates
- `FRUIT_ROTATION_INTERVAL`: How often to show a new fruit
- `CACHE_TIMEOUT`: How long to cache API responses

### Display Settings
- `DISPLAY_WIDTH`: Width of the display (default: 800)
- `DISPLAY_HEIGHT`: Height of the display (default: 480)

## Troubleshooting

### Common Issues
1. **JSON response instead of bitmap**: Make sure you're accessing the `/webhook` endpoint
2. **Connection errors**: Check your internet connection for API access
3. **Display not updating**: Verify your refresh intervals are set correctly

## Credits

- Fruit data provided by [Fruityvice API](https://fruityvice.com/)
- Based on [TRMNL Plugin Boilerplate](https://github.com/OptimumMeans/TRMNL-Boilerplate)

## License

MIT