"""
Email Sender Agent - Silver Tier AI Employee

This script sends emails using SMTP with credentials from environment variables.

Features:
- SMTP email sending (Gmail, generic SMTP)
- Environment variable credential management
- Command-line interface
- Comprehensive error handling and logging
- Colorful terminal output
- Support for HTML and plain text emails

Requirements:
- python-dotenv (pip install python-dotenv)

Environment Variables Required:
- EMAIL_ADDRESS: Sender email address
- EMAIL_PASSWORD: Email password or app-specific password
- SMTP_SERVER: SMTP server (default: smtp.gmail.com)
- SMTP_PORT: SMTP port (default: 587)

Usage:
    python scripts/send_email.py --to recipient@example.com --subject "Test" --body "Hello World"
    python scripts/send_email.py --to user@example.com --subject "Report" --body "$(cat report.txt)"
"""

import os
import sys
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

# Rich library for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Configuration
LOGS_FOLDER = "logs"
ACTIONS_LOG = os.path.join(LOGS_FOLDER, "actions.log")

# SMTP Defaults
DEFAULT_SMTP_SERVER = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587


def log_action(message: str, level: str = "INFO"):
    """
    Log a message to the actions log file.

    Args:
        message (str): Message to log
        level (str): Log level
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] [EMAIL] {message}\n"

    try:
        os.makedirs(LOGS_FOLDER, exist_ok=True)
        with open(ACTIONS_LOG, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # Colorful console output with rich
        if RICH_AVAILABLE:
            if level == "ERROR":
                console.print(f"[bold red]✗[/bold red] [red]{message}[/red]")
            elif level == "SUCCESS":
                console.print(f"[bold green]✓[/bold green] [green]{message}[/green]")
            elif level == "WARNING":
                console.print(f"[bold yellow]⚠[/bold yellow] [yellow]{message}[/yellow]")
            else:
                console.print(f"[bold cyan]ℹ[/bold cyan] [cyan]{message}[/cyan]")
        else:
            print(f"[{level}] {message}")
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[bold red]✗ Failed to write to log: {e}[/bold red]")
        else:
            print(f"[ERROR] Failed to write to log: {e}")


def load_email_config():
    """
    Load email configuration from environment variables.

    Returns:
        dict: Configuration dictionary with email settings
    """
    load_dotenv()

    config = {
        "email_address": os.getenv("EMAIL_ADDRESS"),
        "email_password": os.getenv("EMAIL_PASSWORD"),
        "smtp_server": os.getenv("SMTP_SERVER", DEFAULT_SMTP_SERVER),
        "smtp_port": int(os.getenv("SMTP_PORT", DEFAULT_SMTP_PORT))
    }

    return config


def validate_config(config):
    """
    Validate email configuration.

    Args:
        config (dict): Configuration dictionary

    Returns:
        bool: True if valid, False otherwise
    """
    if not config["email_address"]:
        log_action("EMAIL_ADDRESS not set in .env file", "ERROR")
        return False

    if not config["email_password"]:
        log_action("EMAIL_PASSWORD not set in .env file", "ERROR")
        return False

    return True


def send_email(to_address: str, subject: str, body: str, html: bool = False):
    """
    Send an email using SMTP.

    Args:
        to_address (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content
        html (bool): Whether body is HTML (default: False)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    # Load configuration
    config = load_email_config()

    if not validate_config(config):
        return False

    try:
        log_action(f"Preparing email to {to_address}", "INFO")

        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = config["email_address"]
        msg["To"] = to_address
        msg["Subject"] = subject

        # Attach body
        mime_type = "html" if html else "plain"
        msg.attach(MIMEText(body, mime_type))

        log_action(f"Connecting to SMTP server: {config['smtp_server']}:{config['smtp_port']}", "INFO")

        # Connect to SMTP server
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()  # Secure the connection

            log_action("Authenticating with SMTP server", "INFO")
            server.login(config["email_address"], config["email_password"])

            log_action("Sending email", "INFO")
            server.send_message(msg)

        log_action(f"Email sent successfully to {to_address}", "SUCCESS")
        return True

    except smtplib.SMTPAuthenticationError:
        log_action("SMTP authentication failed. Check EMAIL_ADDRESS and EMAIL_PASSWORD", "ERROR")
        if RICH_AVAILABLE:
            console.print("[yellow]Tip: For Gmail, use an App Password instead of your regular password[/yellow]")
            console.print("[yellow]Generate one at: https://myaccount.google.com/apppasswords[/yellow]")
        return False

    except smtplib.SMTPException as e:
        log_action(f"SMTP error: {str(e)}", "ERROR")
        return False

    except Exception as e:
        log_action(f"Failed to send email: {str(e)}", "ERROR")
        return False


def main():
    """
    Main entry point for command-line usage.
    """
    # Beautiful startup banner
    if RICH_AVAILABLE:
        console.print()
        console.print(Panel.fit(
            "[bold blue]📧 EMAIL SENDER AGENT[/bold blue]\n"
            "[dim]Silver Tier AI Employee[/dim]\n"
            "[yellow]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/yellow]",
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()

    parser = argparse.ArgumentParser(description="Send emails via SMTP")
    parser.add_argument("--to", type=str, required=True, help="Recipient email address")
    parser.add_argument("--subject", type=str, required=True, help="Email subject")
    parser.add_argument("--body", type=str, required=True, help="Email body content")
    parser.add_argument("--html", action="store_true", help="Send as HTML email")

    args = parser.parse_args()

    if RICH_AVAILABLE:
        console.print(f"[cyan]📧 To:[/cyan] [white]{args.to}[/white]")
        console.print(f"[cyan]📝 Subject:[/cyan] [white]{args.subject}[/white]")
        console.print(f"[cyan]📄 Body:[/cyan] [white]{args.body[:50]}{'...' if len(args.body) > 50 else ''}[/white]")
        console.print(f"[cyan]🌐 Format:[/cyan] [white]{'HTML' if args.html else 'Plain Text'}[/white]")
        console.print()

    # Send email
    success = send_email(args.to, args.subject, args.body, args.html)

    if RICH_AVAILABLE:
        console.print()
        if success:
            console.print(Panel(
                "[bold green]✓ Email sent successfully![/bold green]\n"
                f"[dim]Recipient: {args.to}[/dim]",
                border_style="green",
                padding=(1, 2)
            ))
        else:
            console.print(Panel(
                "[bold red]✗ Failed to send email[/bold red]\n"
                "[yellow]Check logs/actions.log for details[/yellow]\n"
                "[dim]Verify EMAIL_ADDRESS and EMAIL_PASSWORD in .env[/dim]",
                border_style="red",
                padding=(1, 2)
            ))
        console.print()
    else:
        if success:
            print("\n✓ Email sent successfully!")
        else:
            print("\n✗ Failed to send email. Check logs/actions.log for details.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
