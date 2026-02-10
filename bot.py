import discord
from discord import app_commands
from discord.ext import commands
import os
import random
import string
import aiosqlite
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '568353089791328273'))  # User who can grant licenses
DATABASE_FILE = 'backup_bot.db'

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


class Database:
    """Database handler for backup bot"""
    
    def __init__(self, db_file: str):
        self.db_file = db_file
    
    async def init_db(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_file) as db:
            # Table for backup credentials
            await db.execute('''
                CREATE TABLE IF NOT EXISTS backup_credentials (
                    backup_id TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    owner_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for authenticated users
            await db.execute('''
                CREATE TABLE IF NOT EXISTS authenticated_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    authenticated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (backup_id) REFERENCES backup_credentials(backup_id),
                    UNIQUE(backup_id, user_id)
                )
            ''')
            
            # Table for licensed admins
            await db.execute('''
                CREATE TABLE IF NOT EXISTS licensed_admins (
                    user_id INTEGER PRIMARY KEY,
                    licensed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await db.commit()
    
    async def create_backup(self, backup_id: str, password: str, owner_id: int, guild_id: int):
        """Create a new backup credential entry"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                'INSERT INTO backup_credentials (backup_id, password, owner_id, guild_id) VALUES (?, ?, ?, ?)',
                (backup_id, password, owner_id, guild_id)
            )
            await db.commit()
    
    async def verify_credentials(self, backup_id: str, password: str) -> Optional[dict]:
        """Verify backup credentials"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                'SELECT backup_id, owner_id, guild_id FROM backup_credentials WHERE backup_id = ? AND password = ?',
                (backup_id, password)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {'backup_id': row[0], 'owner_id': row[1], 'guild_id': row[2]}
                return None
    
    async def add_authenticated_user(self, backup_id: str, user_id: int, guild_id: int):
        """Add an authenticated user"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                'INSERT OR IGNORE INTO authenticated_users (backup_id, user_id, guild_id) VALUES (?, ?, ?)',
                (backup_id, user_id, guild_id)
            )
            await db.commit()
    
    async def get_authenticated_count(self, backup_id: str) -> int:
        """Get count of authenticated users for a backup ID"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                'SELECT COUNT(*) FROM authenticated_users WHERE backup_id = ?',
                (backup_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_authenticated_users(self, backup_id: str) -> list:
        """Get list of authenticated user IDs for a backup ID"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                'SELECT user_id FROM authenticated_users WHERE backup_id = ?',
                (backup_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    async def get_all_authenticated_count(self) -> int:
        """Get total count of all authenticated users across all backups"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                'SELECT COUNT(DISTINCT user_id) FROM authenticated_users'
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_all_authenticated_users(self) -> list:
        """Get all authenticated users across all backups"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                'SELECT DISTINCT user_id, guild_id FROM authenticated_users'
            ) as cursor:
                rows = await cursor.fetchall()
                return [{'user_id': row[0], 'guild_id': row[1]} for row in rows]
    
    async def add_licensed_admin(self, user_id: int):
        """Add a licensed admin"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                'INSERT OR IGNORE INTO licensed_admins (user_id) VALUES (?)',
                (user_id,)
            )
            await db.commit()
    
    async def is_licensed_admin(self, user_id: int) -> bool:
        """Check if user is a licensed admin"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                'SELECT user_id FROM licensed_admins WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row is not None


# Initialize database
db = Database(DATABASE_FILE)


def generate_backup_id() -> str:
    """Generate a 12-digit random backup ID"""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])


def generate_password(length: int = 16) -> str:
    """Generate a random password with Discord-safe characters"""
    # Use alphanumeric and safe special characters only (exclude quotes, backticks, etc.)
    characters = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}|;:,.<>?'
    return ''.join(random.choice(characters) for _ in range(length))


class VerifyView(discord.ui.View):
    """View for the verify panel with buttons"""
    
    def __init__(self, backup_id: str, guild_id: int):
        super().__init__(timeout=None)
        self.backup_id = backup_id
        self.guild_id = guild_id
    
    @discord.ui.button(label='認証', style=discord.ButtonStyle.gray, emoji='✅')
    async def authenticate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle authentication button click"""
        # Add user to authenticated users
        await db.add_authenticated_user(self.backup_id, interaction.user.id, self.guild_id)
        
        # Send confirmation to user
        await interaction.response.send_message(
            '✅ 認証が完了しました。',
            ephemeral=True
        )
    
    @discord.ui.button(label='利用規約を確認', style=discord.ButtonStyle.gray)
    async def terms_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle terms of service button click"""
        # TODO: Replace with actual terms of service content
        terms_text = """
**利用規約**

1. **サービスの利用**
   - 本Botは認証とバックアップ機能を提供します
   - 不正利用は禁止されています

2. **データの取り扱い**
   - ユーザーIDと認証情報を保存します
   - データは適切に管理され、第三者に提供されません

3. **免責事項**
   - サービスの利用は自己責任で行ってください
   - データの損失や不具合について一切の責任を負いません

4. **規約の変更**
   - 利用規約は予告なく変更される場合があります

詳細は管理者にお問い合わせください。
        """
        await interaction.response.send_message(terms_text, ephemeral=True)


class AdminView(discord.ui.View):
    """View for the admin panel with backup button"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='全メンバーのbackup', style=discord.ButtonStyle.green)
    async def backup_all_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle backup all members button click"""
        # Check if user is licensed
        if not await db.is_licensed_admin(interaction.user.id):
            await interaction.response.send_message(
                '❌ このコマンドを実行する権限がありません。',
                ephemeral=True
            )
            return
        
        # Get all authenticated users
        users = await db.get_all_authenticated_users()
        
        if not users:
            await interaction.response.send_message(
                '認証済みユーザーが見つかりません。',
                ephemeral=True
            )
            return
        
        # Defer the response as this might take time
        await interaction.response.defer(ephemeral=True)
        
        # Process authenticated users
        # Note: Discord bots cannot force re-invite users without OAuth2 permissions
        # This implementation identifies users and prepares backup data
        active_count = 0
        left_count = 0
        failed_users = []
        
        for user_data in users:
            user_id = user_data['user_id']
            guild_id = user_data['guild_id']
            
            try:
                guild = bot.get_guild(guild_id)
                if guild:
                    member = guild.get_member(user_id)
                    if member:
                        active_count += 1
                    else:
                        left_count += 1
                        # Note: Actual force re-invite requires:
                        # 1. OAuth2 authorization with guilds.join scope
                        # 2. User's OAuth2 access token
                        # 3. PUT request to add member to guild
            except Exception:
                failed_users.append(user_id)
        
        # Send result
        result_msg = f'📊 バックアップ状態:\n'
        result_msg += f'✅ サーバー内: {active_count}人\n'
        result_msg += f'📤 退出済み: {left_count}人\n'
        if failed_users:
            result_msg += f'❌ エラー: {len(failed_users)}人\n'
        result_msg += f'\n⚠️ 注意: メンバーの強制復帰にはOAuth2認証が必要です。'
        
        await interaction.followup.send(result_msg, ephemeral=True)


@bot.event
async def on_ready():
    """Event handler for when bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    
    # Initialize database
    await db.init_db()
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


@bot.tree.command(name='verify', description='認証パネルを生成し、backup IDとpasswordを設定')
@app_commands.describe(
    password='バックアップパスワード（省略時は自動生成）'
)
async def verify(interaction: discord.Interaction, password: Optional[str] = None):
    """Create a verification panel"""
    # Generate password if not provided
    if password is None:
        password = generate_password()
    
    # Generate backup ID
    backup_id = generate_backup_id()
    
    # Store credentials in database
    await db.create_backup(backup_id, password, interaction.user.id, interaction.guild.id)
    
    # Send credentials to user via DM
    try:
        dm_embed = discord.Embed(
            title='🔐 バックアップ認証情報',
            description='以下の情報を安全に保管してください。',
            color=discord.Color.blue()
        )
        dm_embed.add_field(name='Backup ID', value=f'`{backup_id}`', inline=False)
        dm_embed.add_field(name='Password', value=f'`{password}`', inline=False)
        dm_embed.set_footer(text='この情報は他人に共有しないでください。')
        
        await interaction.user.send(embed=dm_embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            '❌ DMを送信できませんでした。DMを許可してください。',
            ephemeral=True
        )
        return
    
    # Create verification panel
    embed = discord.Embed(
        title='🔐認証パネル',
        description='利用規約を確認後、下のボタンを押して認証してください。',
        color=discord.Color.from_rgb(255, 255, 255)
    )
    embed.add_field(
        name='⚠️ 注意',
        value='VPNを使用していると認証できない場合があります。\n認証時はVPNをオフにしてください。',
        inline=False
    )
    embed.set_footer(text='developer @7zea')
    
    # Create view with buttons
    view = VerifyView(backup_id, interaction.guild.id)
    
    # Send panel to channel
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name='count', description='認証済みメンバー数を確認')
@app_commands.describe(
    backup_id='バックアップID（12桁）',
    password='バックアップパスワード'
)
async def count(interaction: discord.Interaction, backup_id: str, password: str):
    """Check authenticated member count"""
    # Verify credentials
    credentials = await db.verify_credentials(backup_id, password)
    
    if not credentials:
        await interaction.response.send_message(
            '❌ 無効なBackup IDまたはPasswordです。',
            ephemeral=True
        )
        return
    
    # Get authenticated count
    auth_count = await db.get_authenticated_count(backup_id)
    
    # Send count to user via DM
    try:
        await interaction.user.send(f'認証数は {auth_count} 人です。')
        await interaction.response.send_message(
            '✅ DMに認証数を送信しました。',
            ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            f'認証数は {auth_count} 人です。',
            ephemeral=True
        )


@bot.tree.command(name='backup', description='サーバーを抜けたメンバーを強制復帰させる')
@app_commands.describe(
    backup_id='バックアップID（12桁）',
    password='バックアップパスワード'
)
async def backup(interaction: discord.Interaction, backup_id: str, password: str):
    """Force re-invite members who left the server"""
    # Verify credentials
    credentials = await db.verify_credentials(backup_id, password)
    
    if not credentials:
        await interaction.response.send_message(
            '❌ 無効なBackup IDまたはPasswordです。',
            ephemeral=True
        )
        return
    
    # Defer response as this might take time
    await interaction.response.defer(ephemeral=True)
    
    # Get authenticated users for this backup
    user_ids = await db.get_authenticated_users(backup_id)
    guild = interaction.guild
    
    if not user_ids:
        await interaction.followup.send(
            '認証済みユーザーが見つかりません。',
            ephemeral=True
        )
        return
    
    # Analyze backup status
    active_members = []
    left_members = []
    
    for user_id in user_ids:
        member = guild.get_member(user_id)
        if member:
            active_members.append(member.name)
        else:
            # User has left the server
            try:
                user = await bot.fetch_user(user_id)
                left_members.append(user.name)
            except Exception:
                left_members.append(f'User#{user_id}')
    
    # Send detailed backup report
    result_parts = []
    result_parts.append(f'📊 **バックアップレポート**\n')
    result_parts.append(f'✅ サーバー内のメンバー: {len(active_members)}人')
    if active_members:
        result_parts.append(f'   {", ".join(active_members[:10])}' + ('...' if len(active_members) > 10 else ''))
    
    result_parts.append(f'\n📤 退出済みメンバー: {len(left_members)}人')
    if left_members:
        result_parts.append(f'   {", ".join(left_members[:10])}' + ('...' if len(left_members) > 10 else ''))
    
    if left_members:
        result_parts.append(f'\n⚠️ **注意**: メンバーの強制復帰には以下が必要です：')
        result_parts.append(f'• OAuth2認証 (guilds.join scope)')
        result_parts.append(f'• 各ユーザーのOAuth2アクセストークン')
        result_parts.append(f'現在のバージョンでは、退出メンバーの検出のみが可能です。')
    
    await interaction.followup.send('\n'.join(result_parts), ephemeral=True)


@bot.tree.command(name='admin', description='Bot全体の認証データを管理')
async def admin(interaction: discord.Interaction):
    """Admin command to manage all authentication data"""
    # Check if user is licensed
    if not await db.is_licensed_admin(interaction.user.id):
        await interaction.response.send_message(
            '❌ このコマンドを実行する権限がありません。\n`/license`でライセンスを取得してください。',
            ephemeral=True
        )
        return
    
    # Get total authenticated count
    total_count = await db.get_all_authenticated_count()
    
    # Create admin panel
    embed = discord.Embed(
        title='🛠️ 管理パネル',
        description=f'Bot全体の認証済みユーザー数: **{total_count}人**',
        color=discord.Color.blue()
    )
    embed.set_footer(text='管理者専用コマンド')
    
    # Create view with backup button
    view = AdminView()
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.tree.command(name='license', description='adminコマンドのライセンスを付与')
@app_commands.describe(
    user_id='ライセンスを付与するユーザーID'
)
async def license_cmd(interaction: discord.Interaction, user_id: str):
    """Grant license to use admin command"""
    # Check if user has permission (only specific user ID can grant licenses)
    if interaction.user.id != ADMIN_USER_ID:
        await interaction.response.send_message(
            '❌ このコマンドを実行する権限がありません。',
            ephemeral=True
        )
        return
    
    # Convert user_id to int
    try:
        target_user_id = int(user_id)
    except ValueError:
        await interaction.response.send_message(
            '❌ 無効なユーザーIDです。',
            ephemeral=True
        )
        return
    
    # Grant license
    await db.add_licensed_admin(target_user_id)
    
    # Try to get user info
    try:
        user = await bot.fetch_user(target_user_id)
        user_mention = user.mention
    except Exception:
        user_mention = f'<@{target_user_id}>'
    
    await interaction.response.send_message(
        f'✅ {user_mention} にライセンスを付与しました。',
        ephemeral=True
    )


# Run the bot
if __name__ == '__main__':
    if TOKEN is None:
        print('Error: DISCORD_TOKEN not found in environment variables.')
        print('Please create a .env file with your bot token.')
    else:
        bot.run(TOKEN)
