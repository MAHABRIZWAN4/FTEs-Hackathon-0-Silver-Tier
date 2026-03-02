# AI Employee Agent Skills - Silver Tier

A collection of autonomous agent skills for task management, monitoring, human-in-the-loop approval, email automation, and social media automation.

## 🎯 Overview

This project contains five production-ready agent skills that work together to create an autonomous AI employee system:

1. **Task Planner Agent** - Analyzes markdown files and generates actionable plans
2. **Vault Watcher Agent** - Monitors inbox for new files and triggers processing
3. **Human Approval Agent** - Synchronous approval workflow for critical decisions
4. **Email Sender Agent** - Sends emails via SMTP with environment credentials
5. **LinkedIn Auto-Post Agent** - Automates LinkedIn posting with browser automation

## 📁 Project Structure

```
F:\Hackathon 0 Mahab\Silver Tier\
├── .claude/
│   └── skills/
│       ├── task-planner/
│       │   └── SKILL.md
│       ├── vault-watcher/
│       │   └── SKILL.md
│       ├── human-approval/
│       │   └── SKILL.md
│       ├── mcp-executor/
│       │   └── SKILL.md
│       ├── silver-scheduler/
│       │   └── SKILL.md
│       └── linkedin-post/
│           └── SKILL.md
├── scripts/
│   ├── task_planner.py          # Analyzes files & creates plans
│   ├── watch_inbox.py           # Monitors inbox & triggers planner
│   ├── request_approval.py      # Human-in-the-loop approval workflow
│   ├── send_email.py            # Email sender via SMTP
│   ├── post_linkedin.py         # LinkedIn automation
│   ├── mcp_executor.py          # External action executor
│   └── run_ai_employee.py       # Scheduler & orchestrator
├── AI_Employee_Vault/
│   ├── Inbox/                   # Drop new tasks here
│   ├── Needs_Action/            # Generated plans appear here
│   ├── Needs_Approval/          # Approval requests
│   ├── Done/                    # Completed tasks
│   ├── Dashboard.md             # System status dashboard
│   └── Company_Handbook.md      # Policies & workflows
├── logs/
│   ├── actions.log              # All activity logs
│   ├── processed.json           # Idempotency tracking
│   ├── page_source.html         # Debug HTML snapshots
│   └── screenshots/             # Debug screenshots
├── .env.example                 # Credentials template
├── .gitignore                   # Security configuration
├── requirements.txt             # Core dependencies (rich)
├── requirements_linkedin.txt    # LinkedIn dependencies
├── setup_scheduler.bat          # Windows Task Scheduler setup
├── SCHEDULER_SETUP.md          # Scheduler configuration guide
├── LINKEDIN_SETUP.md           # LinkedIn setup guide
├── EMAIL_SETUP.md              # Email configuration guide
└── COLORFUL_UI.md              # Terminal UI documentation
```

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Git (for cloning the repository)
- Internet connection (for LinkedIn automation)

### Basic Setup (Task Planner + Vault Watcher + Human Approval)

**Step 1: Install Rich Library (for colorful terminal UI)**

```bash
# Install rich for beautiful, colorful terminal output
pip install rich
```

**Step 2: Verify Installation**

```bash
# 1. Clone or navigate to the project directory
cd "F:\Hackathon 0 Mahab\Silver Tier"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify directory structure
ls AI_Employee_Vault/

# 4. Test Task Planner (with colorful output!)
python scripts/task_planner.py

# 5. Test Vault Watcher (with colorful output!)
python scripts/watch_inbox.py

# 6. Test Human Approval (in Python)
python -c "from scripts.request_approval import request_approval; print('Import successful')"
```

### LinkedIn Setup (Optional)

LinkedIn automation requires additional dependencies:

```bash
# 1. Install Python dependencies
pip install playwright python-dotenv

# 2. Install Chromium browser
playwright install chromium

# 3. Configure credentials
cp .env.example .env

# 4. Edit .env file with your LinkedIn credentials
# LINKEDIN_EMAIL=your.email@example.com
# LINKEDIN_PASSWORD=your_password_here

# 5. Test LinkedIn posting
python scripts/post_linkedin.py "Test post from AI Employee" --headless=false
```

### Verify Installation

```bash
# Check all scripts are accessible
python scripts/task_planner.py --help 2>/dev/null || echo "Task Planner: OK"
python scripts/watch_inbox.py --help 2>/dev/null || echo "Vault Watcher: OK"
python scripts/request_approval.py --help
python scripts/post_linkedin.py --help 2>/dev/null || echo "LinkedIn: Check if playwright installed"

# Check directory structure
ls AI_Employee_Vault/Inbox/
ls AI_Employee_Vault/Needs_Action/
ls AI_Employee_Vault/Needs_Approval/
ls AI_Employee_Vault/Done/
ls logs/
```

## 🚀 Quick Start

### 1. Task Planner Agent

**Purpose**: Automatically analyze task files and generate step-by-step plans.

```bash
# Run manually
python scripts/task_planner.py

# What it does:
# - Scans AI_Employee_Vault/Inbox/ for .md files
# - Analyzes content (priority, type, complexity)
# - Generates structured plans
# - Saves to AI_Employee_Vault/Needs_Action/
```

**Example**:
```bash
# Create a task file
echo "# Fix login bug\nUsers can't login with special characters in password" > AI_Employee_Vault/Inbox/fix_login.md

# Run planner
python scripts/task_planner.py

# Result: Plan_fix_login.md created in Needs_Action/
```

### 2. Vault Watcher Agent

**Purpose**: Continuously monitor inbox and automatically trigger task planner.

```bash
# Start watcher (runs continuously)
python scripts/watch_inbox.py

# What it does:
# - Monitors AI_Employee_Vault/Inbox/ every 15 seconds
# - Detects new .md files
# - Automatically runs task planner
# - Logs all activity
```

**Background operation**:
```bash
# Linux/Mac
nohup python scripts/watch_inbox.py > logs/watcher.log 2>&1 &

# Windows PowerShell
Start-Process python -ArgumentList "scripts/watch_inbox.py" -WindowStyle Hidden
```

### 3. Human Approval Agent

**Purpose**: Synchronous human-in-the-loop approval workflow for critical decisions.

```bash
# Use in Python scripts
from scripts.request_approval import request_approval, ApprovalTimeout

try:
    approved = request_approval(
        title="Send Email to Client",
        description="Email contains project status update",
        details={"recipient": "client@example.com", "subject": "Project Update"}
    )

    if approved:
        send_email()
    else:
        print("Action rejected by human")

except ApprovalTimeout:
    print("Approval request timed out")
```

**What it does**:
- Creates approval request file in `AI_Employee_Vault/Needs_Approval/`
- Blocks execution until human responds
- Polls every 10 seconds for decision
- Detects "APPROVED" or "REJECTED" in file (case-insensitive)
- Moves completed requests to `Done/` folder
- Configurable timeout (default: 1 hour)

**Command-line usage**:
```bash
python scripts/request_approval.py \
  --title "Deploy to Production" \
  --description "Deploy version 2.0 to production servers" \
  --details '{"version": "2.0", "environment": "production"}' \
  --priority high \
  --timeout 3600
```

**How to respond**:
1. Open the file in `AI_Employee_Vault/Needs_Approval/`
2. Read the request details
3. Add your decision at the bottom: `**YOUR DECISION**: APPROVED` or `**YOUR DECISION**: REJECTED`
4. Save the file
5. Script automatically detects and proceeds

### 4. Email Sender Agent

**Purpose**: Send emails via SMTP using environment credentials.

**Setup**:
```bash
# Install dependencies (if not already installed)
pip install python-dotenv

# Configure credentials in .env
cp .env.example .env
# Edit .env with your email credentials
```

**Usage**:
```bash
# Send plain text email
python scripts/send_email.py \
  --to recipient@example.com \
  --subject "Test Email" \
  --body "Hello, this is a test email!"

# Send HTML email
python scripts/send_email.py \
  --to recipient@example.com \
  --subject "HTML Email" \
  --body "<h1>Hello</h1><p>This is <strong>HTML</strong> content!</p>" \
  --html

# Send email with file content
python scripts/send_email.py \
  --to recipient@example.com \
  --subject "Report" \
  --body "$(cat report.txt)"
```

**Features**:
- SMTP email sending (Gmail, Outlook, Yahoo, custom)
- Environment variable credential management
- HTML and plain text support
- Comprehensive error handling
- Colorful terminal output
- Detailed logging

**Gmail Setup**:
For Gmail, use an App Password instead of your regular password:
1. Go to https://myaccount.google.com/apppasswords
2. Generate an App Password
3. Use it in `EMAIL_PASSWORD` in `.env`

See `EMAIL_SETUP.md` for detailed configuration guide.

### 5. Scheduler Setup (Automated Background Execution)

**Purpose**: Run the AI Employee orchestrator automatically in the background.

**Windows Setup (Automated)**:
```cmd
# Run the setup script as Administrator
setup_scheduler.bat
```

This creates a Windows Task Scheduler task that runs `scripts/run_ai_employee.py` every 5 minutes automatically.

**Linux/Mac Setup (Cron)**:
```bash
# Edit crontab
crontab -e

# Add this line (runs every 5 minutes)
*/5 * * * * cd "/path/to/Silver Tier" && python3 scripts/run_ai_employee.py >> logs/scheduler.log 2>&1
```

**What the Scheduler Does**:
- Runs vault monitoring and task planning every 5 minutes
- Processes new files in Inbox/ automatically
- Generates plans without manual intervention
- Logs all activity to `logs/actions.log`
- Runs in the background continuously

**Management Commands**:
```cmd
# Windows - Check status
schtasks /Query /TN "AI_Employee_Scheduler"

# Windows - Run immediately
schtasks /Run /TN "AI_Employee_Scheduler"

# Windows - Disable
schtasks /Change /TN "AI_Employee_Scheduler" /DISABLE

# Windows - Delete
schtasks /Delete /TN "AI_Employee_Scheduler" /F

# Linux/Mac - List cron jobs
crontab -l

# Linux/Mac - Edit cron jobs
crontab -e
```

See `SCHEDULER_SETUP.md` for detailed configuration, troubleshooting, and advanced options.

### 6. LinkedIn Auto-Post Agent
- Moves completed requests to `Done/` folder
- Configurable timeout (default: 1 hour)

**Command-line usage**:
```bash
python scripts/request_approval.py \
  --title "Deploy to Production" \
  --description "Deploy version 2.0 to production servers" \
  --details '{"version": "2.0", "environment": "production"}' \
  --priority high \
  --timeout 3600
```

**How to respond**:
1. Open the file in `AI_Employee_Vault/Needs_Approval/`
2. Read the request details
3. Add your decision at the bottom: `**YOUR DECISION**: APPROVED` or `**YOUR DECISION**: REJECTED`
4. Save the file
5. Script automatically detects and proceeds

### 4. LinkedIn Auto-Post Agent

**Purpose**: Automate posting to LinkedIn using browser automation.

**Setup**:
```bash
# Install dependencies
pip install playwright python-dotenv
playwright install chromium

# Configure credentials
cp .env.example .env
# Edit .env with your LinkedIn credentials
```

**Usage**:
```bash
# Post to LinkedIn
python scripts/post_linkedin.py "Just shipped a new feature! 🚀"

# Debug mode (visible browser)
python scripts/post_linkedin.py "Test post" --headless=false

# Custom timeout
python scripts/post_linkedin.py "My post" --timeout 60000
```

**Features**:
- Automated login with CAPTCHA detection
- Multiple selector strategies for reliability
- Keyboard typing for natural content entry
- Semantic locators (aria-label, role, text)
- JavaScript fallback for stubborn elements
- Debug mode with HTML snapshots and screenshots
- Retry logic with exponential backoff

## 🔄 Integrated Workflow

Here's how all four skills work together:

```
┌─────────────────────────────────────────────────────────────┐
│  1. User drops task file in Inbox/                         │
│     Example: "implement_feature.md"                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Vault Watcher detects new file (within 15 seconds)     │
│     Logs: [DETECTED] New file: implement_feature.md        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Task Planner automatically triggered                    │
│     - Analyzes content                                      │
│     - Extracts priority (high/medium/low)                   │
│     - Identifies task type (feature/bug/research)           │
│     - Generates step-by-step plan                           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Plan created in Needs_Action/                           │
│     File: Plan_implement_feature.md                         │
│     Contains: steps, risks, effort estimate                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  5. (If high priority) Request human approval               │
│     - Creates approval request in Needs_Approval/           │
│     - Blocks execution until human responds                 │
│     - Human writes APPROVED or REJECTED in file             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  6. (Optional) Post update to LinkedIn                      │
│     "Working on exciting new feature! 🚀"                   │
└─────────────────────────────────────────────────────────────┘
```

## 💡 Usage Examples

### Example 1: Autonomous Task Processing

```bash
# Terminal 1: Start the watcher
python scripts/watch_inbox.py

# Terminal 2: Drop tasks in inbox
echo "# Research cloud providers
Compare AWS, Azure, GCP for our migration" > AI_Employee_Vault/Inbox/cloud_research.md

# Watcher automatically detects and processes
# Check Needs_Action/ for the generated plan
```

### Example 2: Batch Processing

```bash
# Create multiple tasks
echo "# Fix payment bug" > AI_Employee_Vault/Inbox/fix_payment.md
echo "# Add dark mode" > AI_Employee_Vault/Inbox/dark_mode.md
echo "# Update docs" > AI_Employee_Vault/Inbox/update_docs.md

# Process all at once
python scripts/task_planner.py

# All plans created in Needs_Action/
```

### Example 3: Human Approval Workflow

```python
# scripts/deploy_with_approval.py
from scripts.request_approval import request_approval, ApprovalTimeout

def deploy_to_production(version):
    """Deploy with human approval."""
    try:
        # Request approval
        approved = request_approval(
            title=f"Deploy Version {version} to Production",
            description="This will deploy the new version to production servers",
            details={
                "version": version,
                "environment": "production",
                "estimated_downtime": "5 minutes"
            },
            priority="high",
            timeout_seconds=1800  # 30 minutes
        )

        if approved:
            print("✅ Deployment approved, proceeding...")
            # Perform deployment
            return True
        else:
            print("❌ Deployment rejected")
            return False

    except ApprovalTimeout:
        print("⏱️ Approval request timed out")
        return False

# Run deployment
deploy_to_production("2.0.1")
```

### Example 4: LinkedIn Integration

```python
# scripts/post_task_completion.py
from scripts.post_linkedin import LinkedInPoster
import os

# Read completed task
task_file = "AI_Employee_Vault/Done/task_feature.md"
with open(task_file, 'r') as f:
    content = f.read()

# Extract task title
title = content.split('\n')[0].strip('# ')

# Post to LinkedIn
poster = LinkedInPoster()
poster.post(f"✅ Just completed: {title}\n\n#productivity #automation")
```

## 📊 Features

### Task Planner
- ✅ Smart priority detection (high/medium/low)
- ✅ Task type classification (bug_fix, feature, research, etc.)
- ✅ Step-by-step plan generation
- ✅ Risk assessment and mitigation
- ✅ Effort estimation
- ✅ Idempotent operation (no duplicates)

### Vault Watcher
- ✅ Real-time monitoring (15s polling)
- ✅ Automatic workflow triggering
- ✅ Comprehensive logging
- ✅ Error recovery
- ✅ Production-ready
- ✅ Minimal resource usage

### Human Approval Agent
- ✅ Synchronous approval workflow
- ✅ Blocking execution until decision
- ✅ Configurable timeout (default: 1 hour)
- ✅ Case-insensitive approval detection
- ✅ Automatic file movement to Done/
- ✅ Comprehensive logging
- ✅ Priority levels (low/medium/high)
- ✅ Detailed request context
- ✅ Timeout handling with exceptions
- ✅ Polling mechanism (10s intervals)

### LinkedIn Auto-Post
- ✅ Automated login with credential management
- ✅ Text post creation and publishing
- ✅ Retry logic with exponential backoff (max 2 retries)
- ✅ CAPTCHA and 2FA detection with manual intervention
- ✅ Screenshot debugging on errors
- ✅ Headless and visible browser modes
- ✅ Multiple selector strategies (5 methods)
- ✅ Semantic locators (aria-label, role, text)
- ✅ JavaScript evaluation fallback
- ✅ Keyboard typing for natural input
- ✅ HTML snapshot capture for debugging
- ✅ Comprehensive error logging

## 🔒 Security

**Critical**: Never commit sensitive credentials!

```bash
# .env file is in .gitignore
# Always use .env for credentials
# Never hardcode passwords
```

**Checklist**:
- ✅ `.env` in `.gitignore`
- ✅ Strong, unique passwords
- ✅ Regular credential rotation
- ✅ Logs excluded from git
- ✅ Screenshots excluded from git

## 📝 Logging

All activities are logged to `logs/actions.log`:

```
[2026-02-28 10:30:00] [INFO] [WATCHER] Started monitoring
[2026-02-28 10:30:15] [INFO] [DETECTED] New file: task.md
[2026-02-28 10:30:16] [SUCCESS] Plan created: Plan_task.md
[2026-02-28 10:30:20] [INFO] [APPROVAL] Request created: approval_20260228_103020
[2026-02-28 10:30:30] [INFO] [APPROVAL] Waiting for human decision (timeout: 3600s)
[2026-02-28 10:35:45] [SUCCESS] [APPROVAL] Request approved: approval_20260228_103020
[2026-02-28 10:36:00] [INFO] [EMAIL] Preparing email to recipient@example.com
[2026-02-28 10:36:01] [INFO] [EMAIL] Connecting to SMTP server: smtp.gmail.com:587
[2026-02-28 10:36:02] [SUCCESS] [EMAIL] Email sent successfully to recipient@example.com
[2026-02-28 10:36:10] [INFO] [LINKEDIN] Starting LinkedIn post automation
[2026-02-28 10:36:25] [SUCCESS] [LINKEDIN] Post published successfully
```

**View logs**:
```bash
# Real-time monitoring
tail -f logs/actions.log

# Last 50 lines
tail -n 50 logs/actions.log

# Search for errors
grep ERROR logs/actions.log

# Filter by agent type
grep APPROVAL logs/actions.log
grep EMAIL logs/actions.log
grep LINKEDIN logs/actions.log
grep WATCHER logs/actions.log

# Check today's activity
grep "$(date +%Y-%m-%d)" logs/actions.log
```

## 🛠️ Troubleshooting

### Task Planner Issues
```bash
# No files processed
# Check: Are there .md files in Inbox?
ls AI_Employee_Vault/Inbox/*.md

# Check processed registry
cat logs/processed.json
```

### Vault Watcher Issues
```bash
# Watcher not detecting files
# Check: Is watcher running?
ps aux | grep watch_inbox

# Check logs
tail -f logs/actions.log
```

### Human Approval Issues
```bash
# Approval not detected
# Check: File contains APPROVED or REJECTED?
cat AI_Employee_Vault/Needs_Approval/approval_*.md

# Check: Correct format?
# Should be: **YOUR DECISION**: APPROVED (or REJECTED)

# Check logs for polling attempts
grep APPROVAL logs/actions.log

# Test approval detection
python -c "from scripts.request_approval import check_approval_status; print(check_approval_status('approval_20260228_120000'))"
```

### Email Issues
```bash
# Email authentication failed
# Check: Credentials in .env
cat .env | grep EMAIL

# For Gmail: Use App Password
# Generate at: https://myaccount.google.com/apppasswords

# Test email sending
python scripts/send_email.py \
  --to your.email@example.com \
  --subject "Test" \
  --body "Testing email configuration"

# Check logs for errors
grep EMAIL logs/actions.log | grep ERROR

# Verify SMTP settings
# Gmail: smtp.gmail.com:587
# Outlook: smtp.office365.com:587
# Yahoo: smtp.mail.yahoo.com:587
```
```

### Human Approval Issues
```bash
# Approval not detected
# Check: File contains APPROVED or REJECTED?
cat AI_Employee_Vault/Needs_Approval/approval_*.md

# Check: Correct format?
# Should be: **YOUR DECISION**: APPROVED (or REJECTED)

# Check logs for polling attempts
grep APPROVAL logs/actions.log

# Test approval detection
python -c "from scripts.request_approval import check_approval_status; print(check_approval_status('approval_20260228_120000'))"
```

### LinkedIn Issues
```bash
# Login failed
# Check: Credentials in .env
cat .env

# Check: Screenshots for visual debugging
ls -lt logs/screenshots/

# Check: HTML snapshot
cat logs/page_source.html | grep "Start a post"

# Run in visible mode
python scripts/post_linkedin.py "Test" --headless=false

# Check which selector worked
grep "Method.*SUCCESS" logs/actions.log
```

## 📚 Documentation

- **Task Planner**: `.claude/skills/task-planner/SKILL.md`
- **Vault Watcher**: `.claude/skills/vault-watcher/SKILL.md`
- **Human Approval**: `.claude/skills/human-approval/SKILL.md`
- **MCP Executor**: `.claude/skills/mcp-executor/SKILL.md`
- **Silver Scheduler**: `.claude/skills/silver-scheduler/SKILL.md`
- **LinkedIn Post**: `.claude/skills/linkedin-post/SKILL.md`
- **Scheduler Setup**: `SCHEDULER_SETUP.md` ⭐ NEW
- **Email Setup**: `EMAIL_SETUP.md` ⭐ NEW
- **LinkedIn Setup**: `LINKEDIN_SETUP.md`
- **Colorful UI**: `COLORFUL_UI.md`
- **Company Handbook**: `AI_Employee_Vault/Company_Handbook.md`

## ⚠️ Important Notes

### LinkedIn Automation
- LinkedIn's ToS generally prohibit automation
- Use for authorized personal use only
- Limit to 5-10 posts/day
- May require updates if LinkedIn changes UI
- Use at your own risk

### Rate Limiting
- Task Planner: No limits
- Vault Watcher: 15s polling (configurable)
- Human Approval: 10s polling (configurable)
- LinkedIn: 5-10 posts/day recommended

### Maintenance
- Monitor logs regularly (`tail -f logs/actions.log`)
- Update LinkedIn selectors if UI changes
- Rotate credentials periodically
- Review processed files registry (`logs/processed.json`)
- Clean up old approval requests in Done/ folder
- Check screenshot folder size (`logs/screenshots/`)
- Verify HTML snapshots for debugging (`logs/page_source.html`)

## 🚦 Status

| Skill | Status | Production Ready | External Dependencies |
|-------|--------|------------------|----------------------|
| Task Planner | ✅ Complete | Yes | None |
| Vault Watcher | ✅ Complete | Yes | None |
| Human Approval | ✅ Complete | Yes | None |
| Email Sender | ✅ Complete | Yes | python-dotenv |
| LinkedIn Post | ✅ Complete | Yes (with setup) | playwright, python-dotenv |
| MCP Executor | ✅ Complete | Yes | python-dotenv |
| Silver Scheduler | ✅ Complete | Yes | None |

## ✅ What's Working (Tested & Verified)

### 🎨 Beautiful Terminal UI (NEW!)
- ✅ Colorful output with rich library
- ✅ Eye-catching startup banners with borders
- ✅ Color-coded messages (green=success, red=error, yellow=warning, cyan=info)
- ✅ Beautiful summary tables with styling
- ✅ Progress bars for long-running operations
- ✅ Status icons (✓/✗/⚠/ℹ) for visual feedback
- ✅ Panels for important messages
- ✅ Graceful fallback to plain text if rich not installed

### Task Planner Agent
- ✅ Scans Inbox/ for .md files
- ✅ Extracts priority from content (high/medium/low keywords)
- ✅ Identifies task type (bug_fix, feature, research, etc.)
- ✅ Generates structured plans with steps, risks, effort
- ✅ Saves to Needs_Action/ with Plan_ prefix
- ✅ Idempotent processing (tracks in logs/processed.json)
- ✅ Comprehensive logging to logs/actions.log

### Vault Watcher Agent
- ✅ Continuous monitoring (15-second polling)
- ✅ Detects new .md files in Inbox/
- ✅ Automatically triggers Task Planner
- ✅ Logs all detection events
- ✅ Handles errors gracefully
- ✅ Can run as background process
- ✅ Minimal CPU/memory usage

### Human Approval Agent
- ✅ Creates approval request files in Needs_Approval/
- ✅ Blocks execution until human responds
- ✅ Detects "APPROVED" or "REJECTED" (case-insensitive)
- ✅ Works with any format: `**YOUR DECISION**:APPROVED` or `**YOUR DECISION**: APPROVED`
- ✅ Configurable timeout (default: 1 hour)
- ✅ Polling mechanism (10-second intervals)
- ✅ Moves completed requests to Done/
- ✅ Timeout exception handling
- ✅ Priority levels (low/medium/high)
- ✅ Detailed request context with frontmatter
- ✅ Command-line and Python API usage

### Email Sender Agent
- ✅ SMTP email sending (Gmail, Outlook, Yahoo, custom servers)
- ✅ Environment variable credential management (.env file)
- ✅ Command-line interface with arguments
- ✅ HTML and plain text email support
- ✅ Gmail App Password support
- ✅ Configurable SMTP server and port
- ✅ Comprehensive error handling with helpful messages
- ✅ Authentication error detection with tips
- ✅ Colorful terminal UI with rich library
- ✅ Detailed logging to logs/actions.log
- ✅ Integration with MCP executor
- ✅ Secure credential storage (never logged)

### LinkedIn Auto-Post Agent
- ✅ Moves completed requests to Done/
- ✅ Timeout exception handling
- ✅ Priority levels (low/medium/high)
- ✅ Detailed request context with frontmatter
- ✅ Command-line and Python API usage

### LinkedIn Auto-Post Agent
- ✅ Automated login with credentials from .env
- ✅ CAPTCHA detection with manual intervention prompt
- ✅ Multiple selector strategies (5 methods):
  - aria-label locator
  - Exact text match
  - JavaScript querySelector
  - Role-based locator
  - Filtered div[role='button']
- ✅ Keyboard typing for natural content entry
- ✅ Post button detection scoped to share dialog
- ✅ Retry logic with exponential backoff (2 retries)
- ✅ Screenshot capture on errors
- ✅ HTML snapshot for debugging (logs/page_source.html)
- ✅ Headless and visible browser modes
- ✅ Comprehensive logging with method success tracking
- ✅ Timeout configuration
- ✅ Error recovery and cleanup

## 🔧 Technical Highlights

### Robust Selector Strategy (LinkedIn)
The LinkedIn agent uses a fallback chain to handle UI variations:
1. Try aria-label attribute
2. Try exact text match with Playwright's semantic locators
3. Try JavaScript evaluation as fallback
4. Try role-based button locator
5. Try filtered div with role='button'

Each method logs success/failure for debugging.

### Approval Detection Algorithm
The Human Approval agent uses flexible pattern matching:
- Case-insensitive search for "APPROVED" or "REJECTED"
- Works with any spacing: `:APPROVED` or `: APPROVED`
- Strips whitespace before comparison
- Returns PENDING if neither keyword found

### Idempotency Tracking
Task Planner maintains a processed files registry:
- Stores MD5 hash of file content
- Prevents duplicate processing
- Persists in `logs/processed.json`
- Allows reprocessing if content changes

## 📦 Dependencies

**Core** (required for colorful terminal UI):
```bash
pip install rich
```

**Basic Agents** (task_planner.py, watch_inbox.py, request_approval.py):
- `rich>=13.0.0` - Beautiful, colorful terminal output with panels, tables, and progress bars

**LinkedIn** (requires additional installation):
```bash
pip install playwright python-dotenv
playwright install chromium
```

**All dependencies**:
```bash
# Install all at once
pip install rich playwright python-dotenv
playwright install chromium
```

**Optional** (for development):
```bash
pip install -r requirements.txt
pip install -r requirements_linkedin.txt
```

## 🎨 Terminal UI Features

All scripts now feature beautiful, colorful terminal output powered by the `rich` library:

### Visual Enhancements
- ✨ **Colorful Banners** - Eye-catching startup banners with borders
- 🎨 **Color-Coded Messages** - Green for success, red for errors, yellow for warnings, cyan for info
- 📊 **Beautiful Tables** - Summary tables with borders and styling
- 📦 **Panels** - Important messages displayed in bordered panels
- ⏳ **Progress Bars** - Real-time progress indicators for approval waiting
- 🔄 **Spinners** - Animated spinners for ongoing operations
- ✓/✗ **Status Icons** - Visual indicators for success/failure

### Fallback Support
If `rich` is not installed, all scripts gracefully fall back to plain text output. The functionality remains the same, just without colors and fancy formatting.

## 🎓 Learning Resources

- **Playwright Documentation**: https://playwright.dev/python/
- **Python dotenv**: https://pypi.org/project/python-dotenv/
- **LinkedIn Automation Best Practices**: See LINKEDIN_SETUP.md
- **Markdown Task Format**: See example files in AI_Employee_Vault/Inbox/

## 🔐 Security Best Practices

**Critical**: Never commit sensitive credentials!

```bash
# .env file is in .gitignore
# Always use .env for credentials
# Never hardcode passwords in scripts
```

**Security Checklist**:
- ✅ `.env` in `.gitignore`
- ✅ `.env.example` provided (no real credentials)
- ✅ Strong, unique passwords for LinkedIn
- ✅ Regular credential rotation
- ✅ Logs excluded from git (`logs/` in `.gitignore`)
- ✅ Screenshots excluded from git (`logs/screenshots/` in `.gitignore`)
- ✅ No credentials in code or comments
- ✅ Approval requests may contain sensitive data - review before committing

**What's Protected**:
```
.gitignore includes:
- .env
- logs/
- AI_Employee_Vault/Done/
- AI_Employee_Vault/Needs_Approval/
- __pycache__/
- *.pyc
```

## 🚀 Quick Start Guide

### 1. Basic Workflow (No Dependencies)
```bash
# Start the vault watcher
python scripts/watch_inbox.py

# In another terminal, create a task
echo "# Fix login bug
Priority: high
Users cannot login with special characters" > "AI_Employee_Vault/Inbox/fix_login.md"

# Watch the logs
tail -f logs/actions.log

# Check the generated plan
cat "AI_Employee_Vault/Needs_Action/Plan_fix_login.md"
```

### 2. With Human Approval
```python
# Create a script that requires approval
from scripts.request_approval import request_approval

approved = request_approval(
    title="Delete Production Database",
    description="This will permanently delete all production data",
    priority="high",
    timeout_seconds=300
)

if approved:
    print("Proceeding with deletion...")
else:
    print("Operation cancelled")
```

### 3. With LinkedIn Integration
```bash
# Setup LinkedIn
cp .env.example .env
# Edit .env with credentials

# Post to LinkedIn
python scripts/post_linkedin.py "Just completed a major milestone! 🎉 #productivity"
```

## 📄 License

This project is for educational and personal use. Review LinkedIn's Terms of Service before using automation features.

## 🤝 Contributing

This is a hackathon project. Feel free to extend and customize for your needs.

Potential extensions:
- Add Slack/Discord integration
- Implement email notifications
- Add database storage for tasks
- Create web dashboard
- Add more social media platforms
- Implement task scheduling

## 📞 Support

Check logs for detailed error information:
- `logs/actions.log` - All activity logs
- `logs/screenshots/` - Visual debugging for LinkedIn
- `logs/page_source.html` - HTML snapshot for debugging
- `logs/processed.json` - Processed files registry
- Individual SKILL.md files for detailed documentation

**Common Issues**:
1. LinkedIn login fails → Check credentials in .env
2. Approval not detected → Verify "APPROVED" or "REJECTED" in file
3. Task not processed → Check logs/processed.json for duplicates
4. Watcher not detecting → Verify .md file extension

## 🎯 Project Goals Achieved

✅ **Silver Tier Requirements Met**:
- Multiple autonomous agent skills working together
- File-based task management system
- Human-in-the-loop approval workflow
- External service integration (LinkedIn)
- Comprehensive logging and monitoring
- Production-ready error handling
- Security best practices implemented
- Complete documentation

---

**Built with ❤️ for Hackathon 0 Mahab - Silver Tier**

**Last Updated**: February 28, 2026
