# 🌱 SMART_FARMING - AI-Powered Agriculture Assistant

A comprehensive smart farming application that combines AI, IoT, and machine learning to help farmers make data-driven decisions. The project includes a Streamlit web interface, MCP (Model Context Protocol) server for codebase analysis, and various agricultural tools.

## 🚀 Features

### Core Application
- **AI-Powered Chat Interface**: Interactive assistant for farming questions
- **Plant Disease Detection**: Upload images for disease analysis
- **Weather Integration**: Real-time weather data and forecasts
- **Codebase Analysis**: MCP server for analyzing the project structure

### MCP Server Tools
- `get_project_overview`: Get comprehensive project overview
- `analyze_python_files`: Analyze all Python files in the project
- `find_ml_components`: Identify machine learning components
- `analyze_iot_components`: Find IoT and sensor-related code
- `get_file_content`: Read specific file contents
- `search_in_project`: Search for terms across the codebase
- `generate_project_report`: Generate comprehensive project report

## 📁 Project Structure

```
SMART_FARMING/
├── app.py                          # Main Streamlit application
├── server.py                       # MCP server launcher
├── test_mcp_server.py             # MCP server test script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── models/                         # AI/ML models
│   ├── agent_creator.py           # LangChain agent setup
│   └── disease_predictor.py       # Plant disease detection
├── tools/                          # Utility tools
│   └── weather_tool.py            # Weather data integration
├── temp/                          # Temporary file storage
└── mcp-server-demo/               # MCP server package
    ├── main.py                    # MCP server implementation
    ├── __init__.py                # Package initialization
    ├── pyproject.toml             # Package configuration
    └── README.md                  # MCP server documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SMART_FARMING
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 4. Test the MCP Server
```bash
python test_mcp_server.py
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 🔧 MCP Server Usage

The MCP server provides powerful codebase analysis tools that can be used through the Streamlit interface or directly.

### Running the MCP Server
```bash
python server.py
```

### Available Tools
- **Project Overview**: Get high-level project information
- **Python Analysis**: Analyze all Python files for functions, classes, and imports
- **ML Components**: Find machine learning libraries and algorithms
- **IoT Components**: Identify sensor and IoT-related code
- **File Content**: Read specific files with line limits
- **Search**: Search for terms across the codebase
- **Project Report**: Generate comprehensive analysis report

## 🌐 Web Interface

The Streamlit application provides:
- **Chat Interface**: Ask questions about farming
- **Image Upload**: Upload plant images for disease analysis
- **MCP Tools**: Use codebase analysis tools in the sidebar
- **Weather Data**: Get weather information for your location

## 🤖 AI Features

### Plant Disease Detection
- Upload images of plant leaves
- AI-powered disease identification
- Confidence scores and recommendations

### Weather Integration
- Real-time weather data
- 5-day forecasts
- Agricultural weather insights

### Codebase Analysis
- Automatic project structure analysis
- Technology stack detection
- Code quality insights

## 📊 Technologies Used

- **Frontend**: Streamlit
- **AI/ML**: LangChain, Google Gemini, TensorFlow
- **MCP Server**: FastMCP, MCP Protocol
- **Weather**: OpenWeatherMap API
- **Image Processing**: PIL, OpenCV
- **Data Analysis**: Pandas, NumPy

## 🧪 Testing

Run the test script to verify everything is working:
```bash
python test_mcp_server.py
```

This will test:
- Repository path detection
- MCP server functionality
- Project overview generation

## 🚀 Usage Examples

### 1. Basic Chat
```
User: "What's the best time to plant tomatoes?"
Assistant: [Provides detailed planting advice]
```

### 2. Disease Detection
1. Upload an image of a plant leaf
2. Ask: "What's wrong with my plant?"
3. Get AI-powered disease analysis

### 3. Weather Check
```
User: "What's the weather like in Nuzividu?"
Assistant: [Provides current weather and forecast]
```

### 4. Codebase Analysis
1. Use the MCP tools in the sidebar
2. Select "Get Project Overview"
3. View comprehensive project analysis

## 🔧 Configuration

### MCP Server Configuration
The MCP server automatically detects the project structure. If you need to modify paths, edit `mcp-server-demo/main.py`.

### API Keys
- **OpenWeatherMap**: Get free API key from [OpenWeatherMap](https://openweathermap.org/api)
- **Google Gemini**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🐛 Troubleshooting

### Common Issues

1. **MCP Server Connection Failed**
   - Ensure all dependencies are installed
   - Check that `server.py` exists and is executable
   - Run `python test_mcp_server.py` to diagnose

2. **API Key Errors**
   - Verify `.env` file exists with correct API keys
   - Check API key permissions and quotas

3. **Image Upload Issues**
   - Ensure `temp/` directory exists
   - Check file permissions

### Debug Mode
Enable verbose logging by setting `verbose=True` in the agent executor configuration.

## 📈 Future Enhancements

- [ ] Real-time sensor data integration
- [ ] Advanced crop yield prediction
- [ ] Soil analysis integration
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced ML model training

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain for AI agent framework
- Streamlit for web interface
- OpenWeatherMap for weather data
- Google Gemini for AI capabilities
- FastMCP for MCP server implementation

---

**Happy Farming! 🌱**