# Scheduler Setup Guide

## Overview

The AI Employee Scheduler (`scripts/run_ai_employee.py`) orchestrates the vault monitoring and task planning workflow. This guide shows how to set up automated scheduling so the AI Employee runs continuously in the background.

## 🪟 Windows Setup (Automated)

### Quick Setup with Batch File

1. **Run the setup script** (as Administrator):
   ```cmd
   setup_scheduler.bat
   ```

2. **Follow the prompts**:
   - Confirm you want to create the scheduled task
   - The script will configure Task Scheduler automatically

3. **Verify the task was created**:
   ```cmd
   schtasks /Query /TN "AI_Employee_Scheduler"
   ```

### What the Script Does

- Creates a scheduled task named `AI_Employee_Scheduler`
- Runs `scripts/run_ai_employee.py` every 5 minutes
- Starts automatically on system boot
- Runs with highest privileges
- Logs all activity to `logs/actions.log`

---

## 🪟 Windows Setup (Manual)

If the automated script doesn't work, follow these manual steps:

### Method 1: Task Scheduler GUI

1. **Open Task Scheduler**:
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**:
   - Click "Create Basic Task" in the right panel
   - Name: `AI_Employee_Scheduler`
   - Description: `Runs AI Employee orchestrator every 5 minutes`
   - Click Next

3. **Set Trigger**:
   - Select "Daily"
   - Click Next
   - Set start date and time
   - Click Next

4. **Set Action**:
   - Select "Start a program"
   - Click Next
   - Program/script: `python` (or full path to python.exe)
   - Add arguments: `"F:\Hackathon 0 Mahab\Silver Tier\scripts\run_ai_employee.py"`
   - Start in: `F:\Hackathon 0 Mahab\Silver Tier`
   - Click Next

5. **Configure Advanced Settings**:
   - Check "Open the Properties dialog"
   - Click Finish
   - In Properties dialog:
     - Go to "Triggers" tab
     - Edit the trigger
     - Check "Repeat task every: 5 minutes"
     - For a duration of: Indefinitely
     - Click OK

6. **Set Permissions**:
   - Go to "General" tab
   - Select "Run whether user is logged on or not"
   - Check "Run with highest privileges"
   - Click OK

### Method 2: Command Line

```cmd
schtasks /Create ^
    /TN "AI_Employee_Scheduler" ^
    /TR "python \"F:\Hackathon 0 Mahab\Silver Tier\scripts\run_ai_employee.py\"" ^
    /SC MINUTE ^
    /MO 5 ^
    /F ^
    /RL HIGHEST
```

---

## 🐧 Linux/Mac Setup (Cron)

### Setup Cron Job

1. **Open crontab editor**:
   ```bash
   crontab -e
   ```

2. **Add cron job** (runs every 5 minutes):
   ```bash
   */5 * * * * cd "/path/to/Silver Tier" && python3 scripts/run_ai_employee.py >> logs/scheduler.log 2>&1
   ```

3. **Save and exit**:
   - Press `Ctrl + X`
   - Press `Y` to confirm
   - Press Enter

### Verify Cron Job

```bash
# List all cron jobs
crontab -l

# Check cron logs
grep CRON /var/log/syslog
```

### Alternative: systemd Timer (Linux)

1. **Create service file** (`/etc/systemd/system/ai-employee.service`):
   ```ini
   [Unit]
   Description=AI Employee Scheduler
   After=network.target

   [Service]
   Type=oneshot
   User=your-username
   WorkingDirectory=/path/to/Silver Tier
   ExecStart=/usr/bin/python3 scripts/run_ai_employee.py
   StandardOutput=append:/path/to/Silver Tier/logs/scheduler.log
   StandardError=append:/path/to/Silver Tier/logs/scheduler.log

   [Install]
   WantedBy=multi-user.target
   ```

2. **Create timer file** (`/etc/systemd/system/ai-employee.timer`):
   ```ini
   [Unit]
   Description=Run AI Employee every 5 minutes
   Requires=ai-employee.service

   [Timer]
   OnBootSec=1min
   OnUnitActiveSec=5min
   Unit=ai-employee.service

   [Install]
   WantedBy=timers.target
   ```

3. **Enable and start**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ai-employee.timer
   sudo systemctl start ai-employee.timer
   ```

4. **Check status**:
   ```bash
   sudo systemctl status ai-employee.timer
   sudo systemctl list-timers
   ```

---

## ✅ Verification

### Check Task is Running (Windows)

```cmd
# Query task status
schtasks /Query /TN "AI_Employee_Scheduler" /V /FO LIST

# Check if task is enabled
schtasks /Query /TN "AI_Employee_Scheduler" | findstr "Status"

# View task history
eventvwr.msc
# Navigate to: Applications and Services Logs > Microsoft > Windows > TaskScheduler > Operational
```

### Check Cron is Running (Linux/Mac)

```bash
# Check cron service
sudo systemctl status cron  # Linux
sudo launchctl list | grep cron  # Mac

# View cron logs
tail -f /var/log/syslog | grep CRON  # Linux
tail -f /var/log/system.log | grep cron  # Mac
```

### Check AI Employee Logs

```bash
# Real-time monitoring
tail -f logs/actions.log

# Check recent activity
tail -n 50 logs/actions.log

# Check for scheduler runs
grep "SCHEDULER" logs/actions.log

# Check for errors
grep "ERROR" logs/actions.log
```

---

## 🔧 Management Commands

### Windows Task Scheduler

```cmd
# View task details
schtasks /Query /TN "AI_Employee_Scheduler" /V /FO LIST

# Run task immediately
schtasks /Run /TN "AI_Employee_Scheduler"

# Disable task
schtasks /Change /TN "AI_Employee_Scheduler" /DISABLE

# Enable task
schtasks /Change /TN "AI_Employee_Scheduler" /ENABLE

# Delete task
schtasks /Delete /TN "AI_Employee_Scheduler" /F

# Change schedule (every 10 minutes)
schtasks /Change /TN "AI_Employee_Scheduler" /SC MINUTE /MO 10
```

### Linux/Mac Cron

```bash
# Edit cron jobs
crontab -e

# List cron jobs
crontab -l

# Remove all cron jobs
crontab -r

# Remove specific cron job
crontab -e
# Delete the line and save
```

---

## 🛠️ Troubleshooting

### Windows Issues

**Problem:** Task doesn't run
```cmd
# Check task status
schtasks /Query /TN "AI_Employee_Scheduler"

# Check Task Scheduler service
sc query Schedule

# Start Task Scheduler service if stopped
net start Schedule
```

**Problem:** Permission denied
- Run `setup_scheduler.bat` as Administrator
- Right-click → "Run as administrator"

**Problem:** Python not found
```cmd
# Find Python path
where python

# Use full path in task
# Example: C:\Python39\python.exe
```

**Problem:** Script doesn't execute
- Check working directory is set correctly
- Verify script path has no typos
- Check Python is in PATH
- View Task Scheduler history for error details

### Linux/Mac Issues

**Problem:** Cron job doesn't run
```bash
# Check cron service
sudo systemctl status cron  # Linux
sudo launchctl list | grep cron  # Mac

# Check cron logs
tail -f /var/log/syslog | grep CRON  # Linux

# Verify cron syntax
# Use https://crontab.guru/ to validate
```

**Problem:** Permission denied
```bash
# Make script executable
chmod +x scripts/run_ai_employee.py

# Check file permissions
ls -la scripts/run_ai_employee.py
```

**Problem:** Python not found in cron
```bash
# Use full Python path in crontab
which python3
# Example: /usr/bin/python3

# Update crontab with full path
*/5 * * * * /usr/bin/python3 /full/path/to/scripts/run_ai_employee.py
```

---

## 📊 Monitoring

### Check Scheduler Activity

```bash
# View recent scheduler runs
grep "SCHEDULER" logs/actions.log | tail -20

# Count scheduler runs today
grep "$(date +%Y-%m-%d)" logs/actions.log | grep "SCHEDULER" | wc -l

# Check for errors
grep "ERROR" logs/actions.log | grep "SCHEDULER"
```

### Dashboard Monitoring

Check `AI_Employee_Vault/Dashboard.md` for real-time status:
- Last run timestamp
- Tasks processed
- Errors encountered
- System health

---

## ⚙️ Configuration

### Adjust Schedule Interval

**Windows:**
```cmd
# Change to every 10 minutes
schtasks /Change /TN "AI_Employee_Scheduler" /SC MINUTE /MO 10

# Change to hourly
schtasks /Change /TN "AI_Employee_Scheduler" /SC HOURLY /MO 1
```

**Linux/Mac:**
```bash
# Edit crontab
crontab -e

# Every 10 minutes
*/10 * * * * cd "/path/to/Silver Tier" && python3 scripts/run_ai_employee.py

# Every hour
0 * * * * cd "/path/to/Silver Tier" && python3 scripts/run_ai_employee.py

# Every day at 9 AM
0 9 * * * cd "/path/to/Silver Tier" && python3 scripts/run_ai_employee.py
```

### Environment Variables

For scheduled tasks, ensure environment variables are loaded:

**Windows:**
- Task Scheduler loads user environment variables automatically
- Verify `.env` file exists in project root

**Linux/Mac:**
```bash
# Add to crontab before the command
*/5 * * * * cd "/path/to/Silver Tier" && export $(cat .env | xargs) && python3 scripts/run_ai_employee.py
```

---

## 🔒 Security Considerations

1. **Credentials**: Ensure `.env` file has restricted permissions
   ```bash
   # Linux/Mac
   chmod 600 .env
   ```

2. **Logs**: Regularly review logs for suspicious activity
   ```bash
   grep "ERROR\|WARNING" logs/actions.log
   ```

3. **Task Permissions**: Run with minimum required privileges
   - Don't use "Run with highest privileges" unless necessary

4. **Monitoring**: Set up alerts for failed runs
   - Check logs daily
   - Monitor Dashboard.md for anomalies

---

## 📝 Best Practices

1. **Start with longer intervals** (15-30 minutes) and adjust based on workload
2. **Monitor resource usage** (CPU, memory) during scheduled runs
3. **Review logs regularly** to catch issues early
4. **Test manually first** before enabling scheduled task
5. **Keep backups** of `.env` and configuration files
6. **Document changes** to schedule or configuration
7. **Set up notifications** for critical errors

---

## 🚀 Quick Reference

### Windows Commands
```cmd
# Create task
setup_scheduler.bat

# Check status
schtasks /Query /TN "AI_Employee_Scheduler"

# Run now
schtasks /Run /TN "AI_Employee_Scheduler"

# Disable
schtasks /Change /TN "AI_Employee_Scheduler" /DISABLE

# Delete
schtasks /Delete /TN "AI_Employee_Scheduler" /F
```

### Linux/Mac Commands
```bash
# Edit cron
crontab -e

# List cron jobs
crontab -l

# View logs
tail -f logs/actions.log
```

---

## 📞 Support

For issues:
1. Check `logs/actions.log` for error details
2. Verify Python and script paths are correct
3. Ensure Task Scheduler/cron service is running
4. Test script manually first: `python scripts/run_ai_employee.py`
5. Check permissions and environment variables

---

**Last Updated:** February 28, 2026
**Version:** 1.0
