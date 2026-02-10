# Discord Backup Bot Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Discord Backup Bot                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Slash Commands Layer                         │ │
│  │                                                           │ │
│  │  /verify    /count    /backup    /admin    /license      │ │
│  │     │         │          │          │          │          │ │
│  └─────┼─────────┼──────────┼──────────┼──────────┼──────────┘ │
│        │         │          │          │          │            │
│  ┌─────▼─────────▼──────────▼──────────▼──────────▼──────────┐ │
│  │           Command Handlers & Logic                        │ │
│  │                                                           │ │
│  │  • Credential Generation    • Member Status Check        │ │
│  │  • Authentication Flow      • License Management         │ │
│  │  • Backup Analysis         • Access Control              │ │
│  └───────────────────┬───────────────────────────────────────┘ │
│                      │                                         │
│  ┌───────────────────▼───────────────────────────────────────┐ │
│  │              Button Interaction Layer                     │ │
│  │                                                           │ │
│  │  VerifyView         AdminView                            │ │
│  │  • 認証 Button      • 全メンバーのbackup Button            │ │
│  │  • 利用規約 Button                                        │ │
│  └───────────────────┬───────────────────────────────────────┘ │
│                      │                                         │
│  ┌───────────────────▼───────────────────────────────────────┐ │
│  │              Database Layer (SQLite)                      │ │
│  │                                                           │ │
│  │  ┌─────────────────┐  ┌──────────────────┐              │ │
│  │  │backup_credentials│  │authenticated_users│              │ │
│  │  ├─────────────────┤  ├──────────────────┤              │ │
│  │  │backup_id        │  │backup_id         │              │ │
│  │  │password         │  │user_id           │              │ │
│  │  │owner_id         │  │guild_id          │              │ │
│  │  │guild_id         │  │authenticated_at  │              │ │
│  │  └─────────────────┘  └──────────────────┘              │ │
│  │                                                           │ │
│  │  ┌──────────────────┐                                    │ │
│  │  │licensed_admins   │                                    │ │
│  │  ├──────────────────┤                                    │ │
│  │  │user_id           │                                    │ │
│  │  │licensed_at       │                                    │ │
│  │  └──────────────────┘                                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Data Flow                                │
└─────────────────────────────────────────────────────────────────┘

1. /verify Command Flow:
   User → /verify → Generate ID/Password → Store in DB → Send DM
                  → Create Panel → User clicks 認証 → Store auth in DB

2. /count Command Flow:
   User → /count + credentials → Verify in DB → Count users → Send DM

3. /backup Command Flow:
   User → /backup + credentials → Verify in DB → Check members
                                → Generate report → Send ephemeral

4. /admin Command Flow:
   User → /admin → Check license → Count all users → Show panel
                                 → User clicks backup button
                                 → Process all authenticated users

5. /license Command Flow:
   Admin → /license + user_id → Verify admin → Grant license → Store in DB

┌─────────────────────────────────────────────────────────────────┐
│                    Security Features                            │
└─────────────────────────────────────────────────────────────────┘

• Environment-based Configuration (.env file)
• Credential Verification (backup_id + password)
• License-based Access Control (admin commands)
• Ephemeral Responses (private data)
• DM Delivery (sensitive credentials)
• Input Validation (all user inputs)
• Safe Password Generation (no special Discord chars)
• Parameterized Queries (SQL injection prevention)

┌─────────────────────────────────────────────────────────────────┐
│                    File Structure                               │
└─────────────────────────────────────────────────────────────────┘

discord/
├── bot.py                 # Main bot implementation
├── requirements.txt       # Python dependencies
├── .env.example          # Configuration template
├── .gitignore            # Git exclusions
├── README.md             # User documentation
├── SETUP.md              # Setup guide
├── IMPLEMENTATION.md     # Implementation details
├── start.sh              # Unix startup script
└── start.bat             # Windows startup script

Generated at runtime:
├── backup_bot.db         # SQLite database (gitignored)
└── .env                  # Configuration (gitignored)
```
