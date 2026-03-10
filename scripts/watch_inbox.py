"""
Vault Watcher Agent - Silver Tier AI Employee

This script continuously monitors the AI_Employee_Vault/Inbox folder
for new markdown files and automatically triggers the AI processing workflow.

Features:
- Real-time monitoring with configurable polling interval
- Detects only .md files (ignores other formats)
- Triggers task planner automatically
- Idempotent operation (never processes same file twice)
- Production-ready with comprehensive error handling
- Minimal resource usage
"""

import os
import time
import subprocess
import sys
import io
from datetime import datetime
from pathlib import Path

# Fix Windows Unicode encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Rich library for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.live import Live
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console(force_terminal=True, legacy_windows=False)
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Configuration
INBOX_FOLDER = os.path.join("AI_Employee_Vault", "Inbox")
LOGS_FOLDER = "logs"
ACTIONS_LOG = os.path.join(LOGS_FOLDER, "actions.log")
TASK_PLANNER_SCRIPT = os.path.join("scripts", "task_planner.py")

# Configurable polling interval (seconds)
WATCH_INTERVAL = int(os.environ.get("WATCH_INTERVAL", "15"))

# Track files we've already seen/processed
seen_files = set()

# Heartbeat counter
heartbeat_counter = 0
HEARTBEAT_INTERVAL = 10  # Log heartbeat every N cycles


def ensure_directories():
    """Create required directories if they don't exist."""
    os.makedirs(INBOX_FOLDER, exist_ok=True)
    os.makedirs(LOGS_FOLDER, exist_ok=True)


def log_action(message, level="INFO"):
    """
    Log an action to the actions.log file with timestamp.

    Args:
        message (str): The message to log
        level (str): Log level (INFO, ERROR, WARNING, SUCCESS)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    try:
        with open(ACTIONS_LOG, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[bold red]✗ Failed to write to log: {e}[/bold red]")
        else:
            print(f"[ERROR] Failed to write to log: {e}")


def print_banner():
    """Print a colorful banner for the Vault Watcher."""
    if RICH_AVAILABLE:
        console.print()
        console.print(Panel.fit(
            "[bold magenta]👁️  VAULT WATCHER AGENT[/bold magenta]\n"
            "[dim]Silver Tier AI Employee[/dim]\n"
            "[yellow]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/yellow]\n"
            f"[cyan]📂 Monitoring:[/cyan] [white]{INBOX_FOLDER}[/white]\n"
            f"[cyan]⏱️  Interval:[/cyan] [white]{WATCH_INTERVAL}s[/white]",
            border_style="magenta",
            padding=(1, 2)
        ))
        console.print()
    else:
        print()
        print("=" * 60)
        print("  VAULT WATCHER AGENT - Silver Tier AI Employee")
        print("=" * 60)
        print()


def initialize_seen_files():
    """
    Initialize the seen_files set with existing files in Inbox.
    This prevents processing files that were already there before watcher started.
    """
    if not os.path.exists(INBOX_FOLDER):
        return

    try:
        for filename in os.listdir(INBOX_FOLDER):
            filepath = os.path.join(INBOX_FOLDER, filename)
            if os.path.isfile(filepath) and filename.endswith('.md'):
                seen_files.add(filename)

        if seen_files:
            log_action(f"WATCHER_INIT | Initialized with {len(seen_files)} existing file(s)", "INFO")
            if RICH_AVAILABLE:
                console.print(f"[cyan]📋 Initialized with {len(seen_files)} existing .md file(s) in Inbox[/cyan]")
            else:
                print(f"[INFO] Initialized with {len(seen_files)} existing .md file(s) in Inbox")
    except Exception as e:
        log_action(f"WATCHER_INIT_ERROR | {str(e)}", "ERROR")
        if RICH_AVAILABLE:
            console.print(f"[bold red]✗ Failed to initialize seen files: {e}[/bold red]")
        else:
            print(f"[ERROR] Failed to initialize seen files: {e}")


def get_md_files():
    """
    Get list of all .md files currently in Inbox.

    Returns:
        set: Set of .md filenames
    """
    if not os.path.exists(INBOX_FOLDER):
        return set()

    try:
        md_files = set()
        for filename in os.listdir(INBOX_FOLDER):
            filepath = os.path.join(INBOX_FOLDER, filename)
            if os.path.isfile(filepath) and filename.endswith('.md'):
                md_files.add(filename)
        return md_files
    except Exception as e:
        log_action(f"SCAN_ERROR | {str(e)}", "ERROR")
        print(f"[ERROR] Failed to scan Inbox: {e}")
        return set()


def trigger_task_planner(filename):
    """
    Trigger the task planner script to process a file.

    Args:
        filename (str): Name of the file to process

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        log_action(f"PROCESSING | Triggering task planner for: {filename}", "INFO")
        if RICH_AVAILABLE:
            console.print(f"[bold blue]⚙️  Triggering task planner for: {filename}[/bold blue]")
        else:
            print(f"[PROCESSING] Triggering task planner for: {filename}")

        # Check if task planner script exists
        if not os.path.exists(TASK_PLANNER_SCRIPT):
            log_action(f"PLANNER_NOT_FOUND | Script not found: {TASK_PLANNER_SCRIPT}", "ERROR")
            if RICH_AVAILABLE:
                console.print(f"[bold red]✗ Task planner script not found: {TASK_PLANNER_SCRIPT}[/bold red]")
            else:
                print(f"[ERROR] Task planner script not found: {TASK_PLANNER_SCRIPT}")
            return False

        # Execute task planner
        result = subprocess.run(
            [sys.executable, TASK_PLANNER_SCRIPT],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60  # 60 second timeout
        )

        if result.returncode == 0:
            log_action(f"SUCCESS | Task planner completed for: {filename}", "SUCCESS")
            if RICH_AVAILABLE:
                console.print(f"[bold green]✓ Task planner completed for: {filename}[/bold green]")
            else:
                print(f"[SUCCESS] Task planner completed for: {filename}")
            return True
        else:
            log_action(f"PLANNER_ERROR | Exit code {result.returncode} for: {filename}", "ERROR")
            if RICH_AVAILABLE:
                console.print(f"[bold red]✗ Task planner failed with exit code {result.returncode}[/bold red]")
            else:
                print(f"[ERROR] Task planner failed with exit code {result.returncode}")
            if result.stderr:
                if RICH_AVAILABLE:
                    console.print(f"[red]{result.stderr[:200]}[/red]")
                else:
                    print(f"[ERROR] {result.stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        log_action(f"TIMEOUT | Task planner timed out for: {filename}", "ERROR")
        if RICH_AVAILABLE:
            console.print(f"[bold red]⏱️  Task planner timed out for: {filename}[/bold red]")
        else:
            print(f"[ERROR] Task planner timed out for: {filename}")
        return False
    except Exception as e:
        log_action(f"TRIGGER_ERROR | {str(e)} for: {filename}", "ERROR")
        if RICH_AVAILABLE:
            console.print(f"[bold red]✗ Failed to trigger task planner: {e}[/bold red]")
        else:
            print(f"[ERROR] Failed to trigger task planner: {e}")
        return False


def process_new_file(filename):
    """
    Process a newly detected file.

    Args:
        filename (str): Name of the new file

    Returns:
        bool: True if processed successfully
    """
    log_action(f"DETECTED | New file: {filename}", "INFO")
    if RICH_AVAILABLE:
        console.print()
        console.print(Panel(
            f"[bold green]🆕 New file detected![/bold green]\n"
            f"[cyan]📄 File:[/cyan] [white]{filename}[/white]",
            border_style="green",
            padding=(0, 2)
        ))
    else:
        print(f"\n[DETECTED] New file: {filename}")

    # Trigger task planner
    success = trigger_task_planner(filename)

    if success:
        # Mark as seen
        seen_files.add(filename)
        log_action(f"TRACKED | Added to processed registry: {filename}", "INFO")
        if RICH_AVAILABLE:
            console.print(f"[green]✓ File marked as processed: {filename}[/green]")
        else:
            print(f"[TRACKED] File marked as processed: {filename}")
        return True
    else:
        # Even if processing failed, mark as seen to avoid retry loops
        # The task planner has its own retry logic
        seen_files.add(filename)
        log_action(f"TRACKED_FAILED | Marked as seen despite failure: {filename}", "WARNING")
        if RICH_AVAILABLE:
            console.print(f"[yellow]⚠ File marked as seen despite processing failure[/yellow]")
        else:
            print(f"[WARNING] File marked as seen despite processing failure")
        return False


def watch_inbox():
    """
    Main watching loop. Continuously monitors Inbox for new .md files.
    """
    global heartbeat_counter

    print_banner()

    if RICH_AVAILABLE:
        console.print(f"[cyan]📂 Monitoring:[/cyan] [white]{INBOX_FOLDER}[/white]")
        console.print(f"[cyan]⏱️  Polling interval:[/cyan] [white]{WATCH_INTERVAL} seconds[/white]")
        console.print(f"[cyan]🔧 Task planner:[/cyan] [white]{TASK_PLANNER_SCRIPT}[/white]")
        console.print("[yellow]" + "━" * 60 + "[/yellow]")
        console.print()
    else:
        print(f"[INFO] Monitoring: {INBOX_FOLDER}")
        print(f"[INFO] Polling interval: {WATCH_INTERVAL} seconds")
        print(f"[INFO] Task planner: {TASK_PLANNER_SCRIPT}")
        print("-" * 60)

    # Ensure directories exist
    ensure_directories()

    # Initialize with existing files
    initialize_seen_files()

    # Log startup
    log_action("WATCHER_START | Vault Watcher started", "INFO")
    if RICH_AVAILABLE:
        console.print("[bold green]✓ Vault Watcher started successfully![/bold green]")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
        console.print()
    else:
        print("[INFO] Vault Watcher started successfully!")
        print("[INFO] Press Ctrl+C to stop")
        print()

    try:
        while True:
            # Get current .md files
            current_files = get_md_files()

            # Find new files (files that exist now but weren't seen before)
            new_files = current_files - seen_files

            # Process each new file
            if new_files:
                for filename in new_files:
                    process_new_file(filename)
                    if RICH_AVAILABLE:
                        console.print()

            # Heartbeat logging (every N cycles)
            heartbeat_counter += 1
            if heartbeat_counter >= HEARTBEAT_INTERVAL:
                log_action(f"HEARTBEAT | Watching... ({len(seen_files)} files tracked)", "INFO")
                if RICH_AVAILABLE:
                    console.print(f"[dim cyan]💓 Heartbeat: {len(seen_files)} files tracked, monitoring...[/dim cyan]")
                heartbeat_counter = 0

            # Sleep before next check
            time.sleep(WATCH_INTERVAL)

    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print()
            console.print(Panel(
                "[bold yellow]⚠️  Vault Watcher stopped by user[/bold yellow]\n"
                f"[cyan]Total files tracked:[/cyan] [white]{len(seen_files)}[/white]",
                border_style="yellow",
                padding=(0, 2)
            ))
            console.print()
        else:
            print("\n[INFO] Vault Watcher stopped by user")
            print(f"[INFO] Total files tracked: {len(seen_files)}")
        log_action(f"WATCHER_STOP | Stopped by user. Total tracked: {len(seen_files)}", "INFO")
    except Exception as e:
        if RICH_AVAILABLE:
            console.print()
            console.print(f"[bold red]✗ Unexpected error: {e}[/bold red]")
            console.print()
        else:
            print(f"\n[ERROR] Unexpected error: {e}")
        log_action(f"WATCHER_ERROR | {str(e)}", "ERROR")
        raise

    # Ensure directories exist
    ensure_directories()

    # Initialize with existing files
    initialize_seen_files()

    # Log watcher start
    log_action(f"WATCHER_START | Monitoring {INBOX_FOLDER} (interval: {WATCH_INTERVAL}s)", "INFO")
    print(f"[INFO] Watcher started. Press Ctrl+C to stop.")
    print("-" * 60)

    files_processed_this_session = 0

    try:
        while True:
            # Get current .md files
            current_files = get_md_files()

            # Find new files (not in seen_files)
            new_files = current_files - seen_files

            # Process each new file
            if new_files:
                print(f"\n[INFO] Found {len(new_files)} new file(s)")
                for filename in sorted(new_files):
                    if process_new_file(filename):
                        files_processed_this_session += 1
                print("-" * 60)

            # Heartbeat logging
            heartbeat_counter += 1
            if heartbeat_counter >= HEARTBEAT_INTERVAL:
                log_action(
                    f"HEARTBEAT | Watcher active - {files_processed_this_session} file(s) processed this session",
                    "INFO"
                )
                heartbeat_counter = 0

            # Sleep until next check
            time.sleep(WATCH_INTERVAL)

    except KeyboardInterrupt:
        print("\n")
        print("-" * 60)
        print("[STOP] Vault Watcher stopped by user")
        print(f"[SUMMARY] Processed {files_processed_this_session} file(s) this session")
        print("-" * 60)
        log_action(
            f"WATCHER_STOP | Stopped by user - {files_processed_this_session} file(s) processed",
            "INFO"
        )
    except Exception as e:
        print(f"\n[ERROR] Unexpected error in watcher loop: {e}")
        log_action(f"WATCHER_ERROR | Unexpected error: {str(e)}", "ERROR")
        raise


def main():
    """
    Main entry point for the vault watcher.
    """
    try:
        watch_inbox()
    except Exception as e:
        print(f"[FATAL] Vault Watcher crashed: {e}")
        log_action(f"WATCHER_CRASH | {str(e)}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
