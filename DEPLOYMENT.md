# Deployment Checklist

Use this checklist to ensure proper deployment of the Discord Backup Bot.

## Pre-Deployment

### Discord Developer Portal Setup
- [ ] Create Discord Application
- [ ] Create Bot User
- [ ] Copy Bot Token
- [ ] Enable SERVER MEMBERS INTENT
- [ ] Enable MESSAGE CONTENT INTENT (optional)
- [ ] Generate OAuth2 URL with proper scopes:
  - [ ] `bot`
  - [ ] `applications.commands`
- [ ] Set Bot Permissions:
  - [ ] Read Messages/View Channels
  - [ ] Send Messages
  - [ ] Manage Messages
  - [ ] Embed Links
  - [ ] Read Message History
  - [ ] Add Reactions
  - [ ] Use Slash Commands
  - [ ] Manage Roles
  - [ ] Create Invite

### Server Setup
- [ ] Install Python 3.8 or higher
- [ ] Install Git (for cloning repository)
- [ ] Ensure internet connectivity
- [ ] Have admin access to Discord server

## Installation

### Repository Setup
- [ ] Clone repository: `git clone <repo_url>`
- [ ] Navigate to directory: `cd discord`
- [ ] Create virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # Unix/Linux/Mac
  venv\Scripts\activate     # Windows
  ```

### Dependencies
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Verify installation:
  - [ ] `python -c "import discord; print(discord.__version__)"`
  - [ ] `python -c "import aiosqlite; print('OK')"`
  - [ ] `python -c "import dotenv; print('OK')"`

### Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` file:
  - [ ] Set `DISCORD_TOKEN` (from Developer Portal)
  - [ ] Set `ADMIN_USER_ID` (your Discord user ID)
- [ ] Verify `.env` is in `.gitignore`
- [ ] Test configuration: `python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Token:', 'Set' if os.getenv('DISCORD_TOKEN') else 'Missing')"`

### Bot Invitation
- [ ] Use OAuth2 URL to invite bot to server
- [ ] Verify bot appears in member list
- [ ] Check bot has proper role permissions
- [ ] Verify bot can read and send messages in test channel

## First Run

### Initial Startup
- [ ] Run bot: `python bot.py` or use startup script
- [ ] Check for startup message: `{BotName} has connected to Discord!`
- [ ] Verify command sync message: `Synced X command(s)`
- [ ] Wait 5-10 minutes for Discord to sync commands
- [ ] Check for any error messages in console

### Command Verification
- [ ] Open Discord and type `/` in a channel
- [ ] Verify all 5 commands appear:
  - [ ] `/verify`
  - [ ] `/count`
  - [ ] `/backup`
  - [ ] `/admin`
  - [ ] `/license`
- [ ] If commands don't appear:
  - [ ] Wait additional 5 minutes
  - [ ] Restart Discord client
  - [ ] Check bot has `applications.commands` scope

## Functionality Testing

### Test `/verify` Command
- [ ] Run `/verify` in a test channel
- [ ] Verify DM received with backup_id and password
- [ ] Check authentication panel appears in channel
- [ ] Verify embed formatting:
  - [ ] Title: "🔐認証パネル"
  - [ ] White color
  - [ ] Footer: "developer @7zea"
  - [ ] VPN warning present
- [ ] Click "認証" button
- [ ] Verify confirmation message
- [ ] Click "利用規約を確認" button
- [ ] Verify terms display

### Test `/count` Command
- [ ] Run `/count` with valid backup_id and password
- [ ] Verify DM received with count (should be 1 after above test)
- [ ] Test with invalid credentials
- [ ] Verify error message

### Test `/backup` Command
- [ ] Run `/backup` with valid credentials
- [ ] Verify status report appears
- [ ] Check report shows correct member status
- [ ] Verify ephemeral response (only you can see it)

### Test `/license` Command
- [ ] Ensure you're using the ADMIN_USER_ID account
- [ ] Run `/license <target_user_id>`
- [ ] Verify success message
- [ ] Test with non-admin account
- [ ] Verify permission denied message

### Test `/admin` Command
- [ ] Try command without license
- [ ] Verify permission denied
- [ ] Grant yourself license using `/license`
- [ ] Run `/admin` again
- [ ] Verify panel displays with user count
- [ ] Click "全メンバーのbackup" button
- [ ] Verify backup report appears

## Production Deployment

### Security Checks
- [ ] `.env` file is NOT in Git repository
- [ ] `.env` contains no placeholder values
- [ ] Bot token is kept secret
- [ ] Database file will be created with proper permissions
- [ ] Admin user ID is set correctly
- [ ] Server has firewall rules (if applicable)

### Monitoring Setup
- [ ] Set up log monitoring
- [ ] Configure log rotation (if long-term deployment)
- [ ] Set up process monitoring (systemd, pm2, etc.)
- [ ] Configure automatic restart on failure
- [ ] Set up backup schedule for database

### Documentation
- [ ] Team members know how to use commands
- [ ] README.md is accessible to users
- [ ] SETUP.md is available for future deployments
- [ ] QUICKREF.md is bookmarked for quick reference
- [ ] Emergency contact information is documented

### Backup Strategy
- [ ] Database backup script created
- [ ] Backup schedule configured (daily/weekly)
- [ ] Backup restoration procedure tested
- [ ] Off-site backup location configured
- [ ] `.env` file backup (secure location)

## Post-Deployment

### First 24 Hours
- [ ] Monitor bot logs for errors
- [ ] Verify commands are responding
- [ ] Check database file is being created/updated
- [ ] Monitor DM delivery success rate
- [ ] Watch for any Discord API rate limits

### First Week
- [ ] Collect user feedback
- [ ] Monitor authentication success rate
- [ ] Check backup report accuracy
- [ ] Verify license system working
- [ ] Review database size and growth

### Ongoing Maintenance
- [ ] Weekly database backups
- [ ] Monthly review of logs
- [ ] Update dependencies when needed
- [ ] Monitor Discord.py changelog for breaking changes
- [ ] Review and update terms of service

## Rollback Plan

If issues occur:
- [ ] Stop bot process
- [ ] Restore previous database backup
- [ ] Restore previous `.env` configuration
- [ ] Revert to previous Git commit if needed
- [ ] Document the issue
- [ ] Test fix in development environment

## Support Contacts

- **Bot Developer**: @7zea
- **Discord API Issues**: https://discord.com/developers/docs
- **Repository Issues**: [GitHub Issues](repository_url)

## Additional Resources

- **README.md** - User guide
- **SETUP.md** - Setup instructions
- **QUICKREF.md** - Quick command reference
- **IMPLEMENTATION.md** - Technical details
- **ARCHITECTURE.md** - System architecture

---

## Deployment Status

**Date Deployed**: _______________  
**Deployed By**: _______________  
**Server**: _______________  
**Bot Name**: _______________  
**Version**: 1.0.0  

**Notes**:
_______________________________________________
_______________________________________________
_______________________________________________

**Checklist Completed**: [ ] Yes [ ] No  
**Issues Found**: [ ] Yes [ ] No  
**Production Ready**: [ ] Yes [ ] No  
