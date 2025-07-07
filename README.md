# LeadGen AI 🚀

An AI-powered lead generation system that automatically researches companies, matches them with your solutions, and generates personalized outreach emails. Built with AutoGen multi-agent orchestration, powered by Groq's LLM API, and featuring a modern full-stack architecture with Docker deployment.

## 🎯 What It Does

LeadGen AI automates the entire lead generation pipeline:

1. **Research**: Finds relevant companies based on your industry/location criteria
2. **Analysis**: Matches companies with your specific solutions and capabilities  
3. **Outreach**: Generates personalized emails for each potential lead
4. **Export**: Saves everything to Excel and JSON for easy follow-up
5. **Web Interface**: Modern React frontend for easy interaction and lead management

Perfect for **Replicant Systems** (industrial automation + vision AI) or any B2B company looking to scale their outreach.

## 🏗️ Architecture

```
ag/
├── src/                 # Core AI agents and logic
│   ├── config/          # Environment & LLM configuration
│   ├── agents/          # AI agent definitions
│   ├── utils/           # Parsing, validation, file handling
│   └── core/            # Main orchestration logic
├── api/                 # FastAPI backend server
│   ├── routes/          # API endpoints
│   ├── models/          # Data models
│   └── services/        # Business logic
├── frontend/            # React web interface
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── services/    # API client
│   └── public/          # Static assets
├── main.py              # CLI interface (legacy)
├── docker-compose.yml   # Full-stack deployment
├── Dockerfile           # Container configuration
├── lead_tracker.xlsx    # Generated leads (Excel)
├── emails.json          # Generated emails (JSON)
└── .env                 # API keys and configuration
```

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Clone/download the project
cd ag/

# Create environment file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Start the full stack
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Development Setup

```bash
# Install dependencies
uv sync
# or with pip: pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Start API server
uvicorn api.main:app --reload --port 8000

# Start frontend (in another terminal)
cd frontend
npm start

# Or use CLI directly
python main.py "Find manufacturing companies in Texas that need automation"
```

### Option 3: CLI Only (Legacy)

```bash
# Install dependencies
uv sync

# Create environment file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run directly
python main.py "Find food processing companies in California that could benefit from vision AI quality control systems"
```

## 🌐 Web Interface Features

### Dashboard
- **Lead Generation**: Submit research queries through an intuitive interface
- **Real-time Progress**: Watch AI agents work in real-time
- **Lead Management**: View, filter, and export generated leads
- **Email Templates**: Review and customize generated outreach emails

### API Endpoints
- `POST /api/generate-leads` - Start lead generation process
- `GET /api/leads` - Retrieve generated leads
- `GET /api/emails` - Get email templates
- `POST /api/export` - Export data in various formats

## 🤖 How It Works

### Multi-Agent Pipeline

1. **Researcher Agent**: Finds 3-5 relevant companies based on your prompt
2. **Matcher Agent**: Analyzes how your solutions can help each company
3. **Logger Agent**: Combines research + matches into structured leads
4. **Emailer Agent**: Generates personalized outreach emails
5. **Orchestrator**: Coordinates the entire workflow

### Example Workflow

```
Input: "Find manufacturing companies in Texas that need vision AI"
    ↓
Researcher: Finds companies like "Texas Instruments", "Dell Technologies"
    ↓
Matcher: "TI could use vision AI for semiconductor inspection"
    ↓
Logger: Creates structured lead records
    ↓
Emailer: "Dear Texas Instruments team, I noticed your focus on semiconductor manufacturing..."
    ↓
Output: Excel file + JSON emails + Web dashboard display
```

## 📊 Output Examples

### Lead Tracker (Excel)
| Company | Website | Description | Products | Match |
|---------|---------|-------------|----------|--------|
| Texas Instruments | ti.com | Semiconductor manufacturer | Chips, processors | Vision AI for quality control in semiconductor fabrication |
| Dell Technologies | dell.com | Computer manufacturer | Laptops, servers | Automation for assembly line optimization |

### Email Output (JSON)
```json
[
  {
    "company": "Texas Instruments",
    "email": "Subject: Partnership Opportunity - Vision AI for Semiconductor Manufacturing\n\nDear Texas Instruments Team,\n\nI hope this email finds you well. I'm reaching out from Replicant Systems, a company specializing in AI-powered vision systems and industrial automation solutions.\n\nI noticed your focus on semiconductor manufacturing and believe our vision AI technology could significantly enhance your quality control processes...\n\nBest regards,\nReplicant Systems Team"
  }
]
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
```

### Docker Configuration
The `docker-compose.yml` includes:
- **API Service**: FastAPI backend with auto-reload
- **Frontend Service**: React development server
- **Reverse Proxy**: Nginx for production routing
- **Volume Mounts**: Persistent data storage

### LLM Settings
The system uses Groq's `llama-4-scout-17b-16e-instruct` model by default. You can modify the model in `src/config/settings.py`:

```python
"model": "meta-llama/llama-4-scout-17b-16e-instruct",
"temperature": 0.4  # Adjust for creativity vs consistency
```

## 🎨 Customization

### For Your Company
Edit the user proxy system message in `src/agents/base.py`:
```python
system_message="You are the founder of [YOUR COMPANY], a company that builds [YOUR SOLUTIONS]."
```

### Frontend Customization
- **Branding**: Update `frontend/src/components/Header.js`
- **Styling**: Modify `frontend/src/styles/`
- **Features**: Add new components in `frontend/src/components/`

### API Extensions
- **New Endpoints**: Add to `api/routes/`
- **Data Models**: Define in `api/models/`
- **Business Logic**: Implement in `api/services/`

### Custom Prompts
The system works best with specific prompts:
- ✅ "Find food processing companies in California that could benefit from vision AI quality control"
- ✅ "Research automotive suppliers in Michigan who might need industrial automation"
- ❌ "Find companies" (too vague)

## 📝 Project Structure Details

```
ag/
├── src/                    # Core AI system
│   ├── config/
│   │   ├── settings.py     # LLM config & environment loading
│   │   └── __init__.py
│   ├── agents/
│   │   ├── base.py         # Base agent class
│   │   ├── researcher.py   # Company research agent
│   │   ├── matcher.py      # Solution matching agent
│   │   ├── logger.py       # Lead logging agent
│   │   ├── emailer.py      # Email generation agent
│   │   └── __init__.py
│   ├── utils/
│   │   ├── json_parser.py  # JSON extraction from LLM outputs
│   │   ├── validators.py   # Data structure validation
│   │   ├── file_handler.py # Excel/JSON file operations
│   │   └── __init__.py
│   └── core/
│       ├── orchestrator.py # Main workflow coordination
│       └── __init__.py
├── api/                    # FastAPI backend
│   ├── main.py            # FastAPI application
│   ├── routes/
│   │   ├── leads.py       # Lead generation endpoints
│   │   └── __init__.py
│   ├── models/
│   │   ├── lead.py        # Lead data models
│   │   └── __init__.py
│   └── services/
│       ├── lead_service.py # Lead generation service
│       └── __init__.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── App.js         # Main application
│   ├── public/            # Static assets
│   └── package.json       # NPM dependencies
├── docker-compose.yml     # Full-stack deployment
├── Dockerfile             # Container configuration
├── requirements.txt       # Python dependencies (API)
├── requirements-api.txt   # Specific API dependencies
└── pyproject.toml         # Python project configuration
```

## 🛠️ Development

### Running Tests
```bash
# Test CLI
python main.py "Find 3 bottle manufacturing companies in Hyderabad"

# Test API
curl -X POST "http://localhost:8000/api/generate-leads" \
     -H "Content-Type: application/json" \
     -d '{"query": "Find manufacturing companies in Texas"}'

# Check output files
ls -la *.xlsx *.json
```

### Development Workflow
```bash
# Start development stack
docker-compose -f docker-compose.dev.yml up

# Or run individually
# Terminal 1: API
uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm start

# Terminal 3: CLI testing
python main.py "test query"
```

### Adding Features
1. **New Agent Types**: Add to `src/agents/`
2. **API Endpoints**: Add to `api/routes/`
3. **Frontend Components**: Add to `frontend/src/components/`
4. **Enhanced Parsing**: Modify `src/utils/json_parser.py`
5. **Different Outputs**: Update `src/utils/file_handler.py`

### Debugging
- **API Logs**: `docker-compose logs api`
- **Frontend Logs**: `docker-compose logs frontend`
- **Agent Outputs**: Check console with `console.print()` statements
- **API Documentation**: Visit `http://localhost:8000/docs`

## 🔍 Troubleshooting

### Common Issues

**"Missing GROQ_API_KEY"**
- Create `.env` file with your API key
- Get free API key from [Groq Console](https://console.groq.com/)

**"Docker services not starting"**
- Check Docker is running: `docker --version`
- Verify ports are available: `netstat -an | grep :8000`
- Check logs: `docker-compose logs`

**"Frontend not connecting to API"**
- Verify API is running on port 8000
- Check CORS settings in `api/main.py`
- Confirm `REACT_APP_API_URL` in frontend `.env`

**"No valid data generated"**
- Try more specific prompts
- Check if API key has sufficient credits
- Verify network connection
- Check agent system messages

**"Invalid JSON structure"**
- LLM sometimes returns malformed JSON
- System automatically retries parsing
- Check raw output in console logs

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production config
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to cloud platforms
# - AWS ECS
# - Google Cloud Run
# - Azure Container Instances
```

### Environment-Specific Configs
- **Development**: `docker-compose.yml`
- **Production**: `docker-compose.prod.yml`
- **Testing**: `docker-compose.test.yml`

## 🙏 Acknowledgments

- [AutoGen](https://github.com/microsoft/autogen) for multi-agent orchestration
- [Groq](https://groq.com/) for fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for modern API development
- [React](https://reactjs.org/) for frontend framework
- [Docker](https://www.docker.com/) for containerization
- [Rich](https://github.com/Textualize/rich) for beautiful CLI output
- [Typer](https://github.com/tiangolo/typer) for CLI framework

## 🚧 Roadmap

- [x] Full-stack web interface
- [x] Docker containerization
- [x] RESTful API
- [ ] Database integration (PostgreSQL)
- [ ] User authentication and multi-tenancy
- [ ] Real-time notifications (WebSocket)
- [ ] Advanced lead scoring and prioritization
- [ ] Email sending integration (SendGrid, Mailgun)
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Advanced analytics and reporting
- [ ] Mobile app (React Native)
- [ ] Kubernetes deployment configs
- [ ] CI/CD pipeline
- [ ] Monitoring and logging (Prometheus, Grafana)

---

**Ready to revolutionize your lead generation? Start with `docker-compose up -d` and visit `http://localhost:3000`** 🚀
