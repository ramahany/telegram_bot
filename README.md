# IdeaPop - Late Night Idea Companion 💡

> A Telegram bot that helps you validate, refine, and document your brilliant late-night ideas—before they disappear into the void.

**Created by:** r4m4

---

## 🎯 What is IdeaPop?

We've all been there: it's 2 AM, you have an idea that feels genius, but by morning you've forgotten half the details. IdeaPop is your brutally honest brainstorming companion living inside Telegram.

This bot:
- **Listens** to your half-baked ideas
- **Challenges** your assumptions with sharp, honest questions
- **Refines** vague concepts into something buildable
- **Documents** your final plan automatically in Obsidian

**Perfect for:** Entrepreneurs, creators, developers, and anyone who gets brilliant ideas at inconvenient hours and actually wants to execute them.

---

## ✨ Features

- **Async Telegram Bot**: Handles multiple conversations simultaneously
- **Smart Session Management**: Maintains conversation history (resets after 6 hours of inactivity)
- **AI-Powered Conversations**: Uses Groq's LLM for witty, honest, and genuinely helpful feedback
- **Obsidian Integration**: Automatically creates structured notes in your Obsidian vault
- **MCP Server Support**: Connects to Obsidian via Model Context Protocol (MCP)
- **Tool Calling**: LLM can invoke functions like creating notes when appropriate
- **Local & Docker Support**: Run locally for development or containerize for deployment

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Bot Framework** | `pyTelegramBotAPI` (async) | Telegram bot client |
| **LLM** | Groq (llama-3.3-70b-versatile) | AI conversation engine |
| **Config Management** | Pydantic Settings | Environment-based configuration |
| **MCP Client** | `mcp-use` | Connect to Obsidian MCP server |
| **Package Manager** | `uv` | Fast Python package management |
| **Containerization** | Docker | Production deployment |

### Tools & Integrations

- **Groq API**: Provides the LLM backend for conversational AI
- **Obsidian mcp-obsidian Server**: Local MCP server for interacting with your Obsidian vault
- **LangChain**: Tool definition and integration

---

## 📋 Prerequisites

### Required
- **Python 3.9+**
- **uv** package manager ([install here](https://docs.astral.sh/uv/getting-started/installation/))
- **Telegram Bot Token** - Get one from [@BotFather](https://t.me/botfather)
- **Groq API Key** - Sign up at [console.groq.com](https://console.groq.com)

### Optional (for Obsidian integration)
- **Obsidian** (desktop or web)
- **Obsidian API Key** - Enable via Obsidian settings → Local REST API
- **mcp-obsidian** - Install separately via `pip install mcp-obsidian` or `uv run mcp-obsidian`

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ideapop.git
cd ideapop
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
OBSIDIAN_API_KEY=your_obsidian_local_api_key_here
```

**Note:** The OBSIDIAN_API_KEY is only needed if you want to enable Obsidian integration. Leave it blank if you're just testing the chat functionality.

### 3. Install Dependencies

Using **uv** (recommended):
```bash
uv sync
```

Or using **pip**:
```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
python main.py
```

The bot will start polling for messages. Look for the console output:
```
bot is running ...
```

---

## 🐳 Docker Deployment

### Build the Docker Image
```bash
docker build -t ideapop:latest .
```

### Run the Container

**Important:** Since Obsidian REST API runs locally, you have two options:

#### Option A: Without Obsidian Support
```bash
docker run -e BOT_TOKEN="your_token" \
           -e GROQ_API_KEY="your_key" \
           ideapop:latest
```

#### Option B: With Obsidian Support (Host Network)
```bash
docker run --network host \
           -e BOT_TOKEN="your_token" \
           -e GROQ_API_KEY="your_key" \
           -e OBSIDIAN_API_KEY="your_key" \
           ideapop:latest
```

**Note:** If deploying to the cloud, you'll need to:
- Map the Obsidian API port (default: 27123) via tunneling or exposed services
- Or use a cloud-based Obsidian sync solution with a custom MCP server

---

## 📁 Project Structure

```
telegram_bot/
├── main.py                      # Entry point - runs the Telegram bot
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── .env.example                 # Example environment variables
├── helpers/
│   ├── __init__.py
│   ├── config.py               # Pydantic settings for configuration
│   └── prompts.py              # System prompt for LLM behavior
├── llm/
│   ├── __init__.py
│   └── GroqClient.py           # Groq LLM client & tool calling logic
├── servers/
│   ├── __init__.py
│   └── ObsidianMcpServer.py   # Obsidian MCP server wrapper
└── tools/
    ├── __init__.py
    └── add_obsidian_note_groq.py  # Obsidian note creation tool
```

---

## 🔄 How It Works

### Architecture Flow

```
User Message (Telegram)
    ↓
main.py (AsyncTeleBot)
    ↓
GroqClient.responce_with_local_tools()
    ↓
    ├─→ [System Prompt] + [Conversation History]
    ├─→ Groq LLM (llama-3.3-70b-versatile)
    ├─→ Tool Check: Does LLM want to call a tool?
    │    ├─ YES: execute create_obsidian_note()
    │    │         ↓
    │    │    ObsidianMcpServer.obsidian_add_note_async()
    │    │         ↓
    │    │    MCP Server (local)
    │    │         ↓
    │    │    Obsidian Vault
    │    │
    │    └─ NO: Continue conversation
    ↓
Response sent back to Telegram
```

### Session Management

- **Conversation History**: Stored per user (per chat ID) in memory
- **Session Timeout**: After 6 hours of inactivity, conversation history is cleared
- **Fresh Start**: Each session reset allows for new topic discussions

### Tool Calling Flow

1. LLM receives conversation and determines if `create_obsidian_note` is needed
2. If triggered, LLM generates `note_title` and `note_content` parameters
3. Tool is executed via `add_obsidian_note_groq.py`
4. Note is sent to Obsidian via MCP server
5. LLM receives confirmation and sends a brief message to user

---

## 💬 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initializes the bot and explains its purpose |
| `/hello` | Casual greeting |
| *Any message* | Starts a brainstorming conversation |

---

## 🤖 LLM Behavior

The bot uses a detailed system prompt that guides it to:

1. **Unpack** your idea (understand the problem, target user, motivation)
2. **Shape** your concept (scope it down to an MVP)
3. **Document** when ready (create an Obsidian note with structured format)

**Tone:** Like your smartest friend—witty, sarcastic, brutally honest, but genuinely helpful.

The bot will:
- ✅ Call out bad ideas and suggest improvements
- ✅ Ask one clarifying question at a time
- ✅ Push for concrete details over vague concepts
- ✅ Keep responses short and Telegram-friendly
- ❌ Never hype up ideas without addressing problems
- ❌ Never create notes without being explicitly asked

---

## ⚙️ Configuration

### Environment Variables

```env
BOT_TOKEN              # Your Telegram bot token
GROQ_API_KEY          # Your Groq API key for LLM access
OBSIDIAN_API_KEY      # Your Obsidian Local REST API key (optional)
```

### Modifying Prompts

Edit `helpers/prompts.py` to customize the LLM's system prompt and behavior.

### Groq Model Selection

In `llm/GroqClient.py`, the default model is `llama-3.3-70b-versatile`. You can change it:

```python
model:str="llama-3.3-70b-versatile"  # Change this
```

Other available models:
- `llama-3.1-8b-instant` (faster, less capable)
- `mixtral-8x7b-32768` (alternative)

---

## 🐛 Limitations

1. **Obsidian is Local-Only**: The mcp-obsidian server runs on your local machine. This means:
   - For local development: Works seamlessly
   - For Docker deployment: Requires port mapping or network access to your local Obsidian instance
   - For cloud deployment: You'd need to set up tunneling (ngrok, cloudflare tunnel) or a custom MCP server

2. **Memory is Non-Persistent**: Conversation history is stored in-memory only:
   - Restarting the bot clears all history
   - For production, consider adding database persistence

3. **Telegram Rate Limits**: The bot respects Telegram's rate limits; very rapid messages may be queued

4. **MCP Server Dependency**: Obsidian integration requires the mcp-obsidian package to be running in the same environment

---

## 📅 Planned Features

- [ ] **More Tools**: Add integrations with other services (GitHub, Notion, Google Drive, etc.)
- [ ] **Database Persistence**: Store conversation history in a database
- [ ] **Web Dashboard**: View and manage ideas through a web interface
- [ ] **Idea Templates**: Provide starter templates for different idea types
- [ ] **Analytics**: Track idea success rates and common obstacles
- [ ] **Voice Notes**: Accept voice messages and transcribe them
- [ ] **Collaborative Brainstorming**: Multiple users can brainstorm together
- [ ] **Scheduled Reminders**: Get reminders to revisit ideas after specific intervals
- [ ] **Export Options**: Export ideas as PDF, Word, or other formats

---

## 🤝 Contributing

Contributions are welcome! Areas where help is needed:

- Adding new tools and integrations
- Improving the system prompt
- Database persistence
- Web dashboard
- Bug fixes and optimizations

Feel free to open an issue or submit a pull request.

---

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🧊 Example Conversation

```
User: "I want to make an app"

Bot: "Cool, so does every failed startup. What's the one thing it does better than 
     anything else?"

User: "It helps people organize their tasks better"

Bot: "You mean Todoist, Microsoft To Do, Asana? What makes yours different, or are 
     you reinventing that wheel?"

User: "It uses AI to predict how long tasks take"

Bot: "Now that's interesting. Who specifically needs this? A project manager? A 
     developer? Someone else?"

User: "Freelancers mostly"

Bot: "Perfect. So the problem: freelancers overbookend themselves because they can't 
     estimate time. The solution: AI predicts based on their history. 
     
     Before we go further—do you already have sample data, or would users need to 
     build history first?"

[Bot eventually creates a structured Obsidian note when the user says they're ready]
```

---

## ❓ FAQ

**Q: Can I use this without Obsidian?**  
A: Yes! The bot works perfectly fine for conversations. Obsidian integration is optional—just leave `OBSIDIAN_API_KEY` blank.

**Q: How do I get a Groq API key?**  
A: Go to [console.groq.com](https://console.groq.com), sign up, and create an API key in your dashboard.

**Q: Can I modify what the bot says?**  
A: Yes! Edit the system prompt in `helpers/prompts.py` to change tone, behavior, or instructions.

**Q: What if I want to use a different LLM?**  
A: The architecture supports any LLM with function/tool calling. Modify `llm/GroqClient.py` to use OpenAI, Anthropic, or other providers.

---

## 🔗 Resources

- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [Groq API Documentation](https://console.groq.com/docs)
- [Obsidian REST API](https://github.com/ryanjamurphy/obsidian-local-rest-api)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

---

## 💬 Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Made with ❤️ by r4m4**
