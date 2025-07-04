# LeadGen AI 🚀

An AI-powered lead generation system that automatically researches companies, matches them with your solutions, and generates personalized outreach emails. Built with AutoGen multi-agent orchestration and powered by Groq's LLM API.

## 🎯 What It Does

LeadGen AI automates the entire lead generation pipeline:

1. **Research**: Finds relevant companies based on your industry/location criteria
2. **Analysis**: Matches companies with your specific solutions and capabilities  
3. **Outreach**: Generates personalized emails for each potential lead
4. **Export**: Saves everything to Excel and JSON for easy follow-up

Perfect for **Replicant Systems** (industrial automation + vision AI) or any B2B company looking to scale their outreach.

## 🏗️ Architecture

```
ag/
├── src/
│   ├── config/          # Environment & LLM configuration
│   ├── agents/          # AI agent definitions
│   ├── utils/           # Parsing, validation, file handling
│   └── core/            # Main orchestration logic
├── main.py              # CLI interface
├── lead_tracker.xlsx    # Generated leads (Excel)
├── emails.json          # Generated emails (JSON)
└── .env                 # API keys (create this)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- uv (recommended) or pip
- Groq API key ([Get one free](https://console.groq.com/))

### 2. Installation

```bash
# Clone/download the project
cd ag/

# Install dependencies
uv sync
# or with pip: pip install -r req.txt

# Create environment file
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Usage

```bash
# Basic usage
python main.py "Find manufacturing companies in Texas that need automation"

# More specific prompts work better
python main.py "Find food processing companies in California that could benefit from vision AI quality control systems"

python main.py "Research automotive suppliers in Michigan who might need industrial automation solutions"
```

### 4. Results

The system generates:
- **`lead_tracker.xlsx`**: Structured lead data with company info, websites, and match suggestions
- **`emails.json`**: Personalized email templates ready for outreach

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
Output: Excel file + JSON emails ready to send
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
GROQ_API_KEY=your_groq_api_key_here
```

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

### Adding New Agents
1. Create new agent file in `src/agents/`
2. Inherit from `BaseAgent`
3. Add to `src/agents/__init__.py`
4. Include in orchestrator workflow

### Custom Prompts
The system works best with specific prompts:
- ✅ "Find food processing companies in California that could benefit from vision AI quality control"
- ✅ "Research automotive suppliers in Michigan who might need industrial automation"
- ❌ "Find companies" (too vague)

## 📝 Project Structure Details

```
src/
├── config/
│   ├── settings.py      # LLM config & environment loading
│   └── __init__.py
├── agents/
│   ├── base.py          # Base agent class
│   ├── researcher.py    # Company research agent
│   ├── matcher.py       # Solution matching agent
│   ├── logger.py        # Lead logging agent
│   ├── emailer.py       # Email generation agent
│   └── __init__.py
├── utils/
│   ├── json_parser.py   # JSON extraction from LLM outputs
│   ├── validators.py    # Data structure validation
│   ├── file_handler.py  # Excel/JSON file operations
│   └── __init__.py
└── core/
    ├── orchestrator.py  # Main workflow coordination
    └── __init__.py
```

## 🛠️ Development

### Running Tests
```bash
# Test with a simple prompt
python main.py "Find 3 manufacturing companies in Ohio"

# Check output files
ls -la *.xlsx *.json
```

### Adding Features
1. **New Agent Types**: Add to `src/agents/`
2. **Enhanced Parsing**: Modify `src/utils/json_parser.py`
3. **Different Outputs**: Update `src/utils/file_handler.py`
4. **Workflow Changes**: Edit `src/core/orchestrator.py`

### Debugging
- Check agent outputs with `console.print()` statements
- Validate JSON structure with the built-in validators
- Monitor API usage in Groq console

## 🔍 Troubleshooting

### Common Issues

**"Missing GROQ_API_KEY"**
- Create `.env` file with your API key
- Get free API key from [Groq Console](https://console.groq.com/)

**"No valid data generated"**
- Try more specific prompts
- Check if API key has sufficient credits
- Verify network connection

**"Invalid JSON structure"**
- LLM sometimes returns malformed JSON
- System automatically retries parsing
- Check raw output in console logs

**Empty Excel/JSON files**
- Increase `max_round` in orchestrator
- Verify agent system messages
- Check API rate limits

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [AutoGen](https://github.com/microsoft/autogen) for multi-agent orchestration
- [Groq](https://groq.com/) for fast LLM inference
- [Rich](https://github.com/Textualize/rich) for beautiful CLI output
- [Typer](https://github.com/tiangolo/typer) for CLI framework

## 🚧 Roadmap

- [ ] Add more output formats (CSV, PDF reports)
- [ ] Implement agent memory/context persistence
- [ ] Add web scraping for deeper company research
- [ ] Create GUI interface
- [ ] Add email sending integration
- [ ] Support multiple LLM providers
- [ ] Add lead scoring and prioritization

---

**Made with ❤️ for efficient B2B lead generation**

Need help? Open an issue or reach out to the team!