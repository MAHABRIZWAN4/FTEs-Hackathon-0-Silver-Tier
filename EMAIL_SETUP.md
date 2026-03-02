# Email Sender Setup Guide

## Overview

The Email Sender Agent (`scripts/send_email.py`) allows you to send emails via SMTP using credentials stored in environment variables.

## Prerequisites

```bash
pip install python-dotenv
```

## Configuration

### 1. Setup Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 2. Configure Email Credentials

Edit `.env` and add your email credentials:

```env
EMAIL_ADDRESS=your.email@example.com
EMAIL_PASSWORD=your_app_specific_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 3. Gmail Setup (Recommended)

For Gmail, you **must** use an App Password instead of your regular password:

1. Go to https://myaccount.google.com/apppasswords
2. Sign in to your Google Account
3. Select "Mail" and your device
4. Click "Generate"
5. Copy the 16-character password
6. Use this password in `EMAIL_PASSWORD`

**Note:** You need 2-Step Verification enabled to use App Passwords.

### 4. Other Email Providers

**Outlook/Office 365:**
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

**Yahoo Mail:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom SMTP:**
```env
SMTP_SERVER=your.smtp.server.com
SMTP_PORT=587  # or 465 for SSL
```

## Usage

### Basic Email

```bash
python scripts/send_email.py \
  --to recipient@example.com \
  --subject "Test Email" \
  --body "Hello, this is a test email!"
```

### HTML Email

```bash
python scripts/send_email.py \
  --to recipient@example.com \
  --subject "HTML Email" \
  --body "<h1>Hello</h1><p>This is <strong>HTML</strong> content!</p>" \
  --html
```

### Email with File Content

```bash
python scripts/send_email.py \
  --to recipient@example.com \
  --subject "Report" \
  --body "$(cat report.txt)"
```

### From Python Script

```python
import subprocess
import sys

result = subprocess.run([
    sys.executable,
    "scripts/send_email.py",
    "--to", "recipient@example.com",
    "--subject", "Automated Report",
    "--body", "Task completed successfully!"
])

if result.returncode == 0:
    print("Email sent!")
else:
    print("Email failed!")
```

## Features

- ✅ SMTP email sending (Gmail, Outlook, Yahoo, custom)
- ✅ Environment variable credential management
- ✅ Command-line interface
- ✅ HTML and plain text support
- ✅ Comprehensive error handling
- ✅ Colorful terminal output with rich library
- ✅ Detailed logging to `logs/actions.log`

## Troubleshooting

### Authentication Failed

**Problem:** `SMTP authentication failed`

**Solutions:**
1. For Gmail: Use App Password, not regular password
2. Enable "Less secure app access" (not recommended)
3. Check EMAIL_ADDRESS and EMAIL_PASSWORD are correct
4. Verify 2-Step Verification is enabled (for App Passwords)

### Connection Timeout

**Problem:** `Connection timed out`

**Solutions:**
1. Check SMTP_SERVER and SMTP_PORT are correct
2. Verify firewall allows outbound SMTP connections
3. Try port 465 (SSL) instead of 587 (TLS)
4. Check internet connection

### Invalid Recipient

**Problem:** `Recipient address rejected`

**Solutions:**
1. Verify recipient email address is valid
2. Check for typos in email address
3. Ensure recipient domain exists

## Security Best Practices

1. **Never commit .env file** - It's in `.gitignore`
2. **Use App Passwords** - Don't use your main password
3. **Rotate credentials regularly** - Change passwords periodically
4. **Limit access** - Only authorized users should have .env access
5. **Monitor logs** - Check `logs/actions.log` for suspicious activity

## Integration with MCP Executor

The email functionality is also integrated into `scripts/mcp_executor.py` for automated workflows:

```python
from scripts.mcp_executor import MCPExecutor

executor = MCPExecutor()
success, message = executor.execute_email_action({
    "to": "recipient@example.com",
    "subject": "Automated Email",
    "body": "This is automated!"
})
```

## Logging

All email operations are logged to `logs/actions.log`:

```
[2026-02-28 19:20:00] [INFO] [EMAIL] Preparing email to recipient@example.com
[2026-02-28 19:20:01] [INFO] [EMAIL] Connecting to SMTP server: smtp.gmail.com:587
[2026-02-28 19:20:02] [INFO] [EMAIL] Authenticating with SMTP server
[2026-02-28 19:20:03] [INFO] [EMAIL] Sending email
[2026-02-28 19:20:04] [SUCCESS] [EMAIL] Email sent successfully to recipient@example.com
```

## Examples

### Send Task Completion Notification

```bash
python scripts/send_email.py \
  --to manager@company.com \
  --subject "Task Completed: Fix Payment Bug" \
  --body "The payment bug has been fixed and deployed to production."
```

### Send Daily Report

```bash
#!/bin/bash
REPORT=$(cat daily_report.txt)
python scripts/send_email.py \
  --to team@company.com \
  --subject "Daily Report - $(date +%Y-%m-%d)" \
  --body "$REPORT"
```

### Send HTML Newsletter

```bash
python scripts/send_email.py \
  --to subscribers@company.com \
  --subject "Monthly Newsletter" \
  --body "$(cat newsletter.html)" \
  --html
```

## Testing

Test your email configuration:

```bash
# Test plain text email
python scripts/send_email.py \
  --to your.email@example.com \
  --subject "Test Email" \
  --body "If you receive this, email is working!"

# Check logs
tail -f logs/actions.log
```

## Support

For issues:
1. Check `logs/actions.log` for error details
2. Verify credentials in `.env`
3. Test with a simple email first
4. Consult provider-specific SMTP documentation

---

**Last Updated:** February 28, 2026
