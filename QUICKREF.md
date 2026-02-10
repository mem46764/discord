# Quick Reference Guide

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure bot
cp .env.example .env
# Edit .env with your DISCORD_TOKEN and ADMIN_USER_ID

# 3. Run bot
python bot.py
# OR use startup scripts:
./start.sh         # Unix/Linux/Mac
start.bat          # Windows
```

---

## 📋 Command Reference

### `/verify [password]`
認証パネルを作成

**引数:**
- `password` (optional): カスタムパスワード（省略時は自動生成）

**動作:**
1. 12桁のbackup IDを生成
2. パスワードを生成または使用
3. DMで認証情報を送信
4. チャンネルに認証パネルを表示

**パネルボタン:**
- ✅ **認証**: ユーザーを認証済みとして登録
- 📋 **利用規約を確認**: 利用規約を表示

---

### `/count <backup_id> <password>`
認証済みメンバー数を確認

**引数:**
- `backup_id`: 12桁のバックアップID
- `password`: バックアップパスワード

**動作:**
1. 認証情報を検証
2. 認証済みユーザー数をカウント
3. DMで結果を送信

**応答例:**
```
認証数は 5 人です。
```

---

### `/backup <backup_id> <password>`
メンバーのバックアップ状態を確認

**引数:**
- `backup_id`: 12桁のバックアップID
- `password`: バックアップパスワード

**動作:**
1. 認証情報を検証
2. サーバー内メンバーと退出メンバーを分析
3. 詳細レポートを表示

**応答例:**
```
📊 バックアップレポート

✅ サーバー内のメンバー: 3人
   User1, User2, User3

📤 退出済みメンバー: 2人
   User4, User5

⚠️ 注意: メンバーの強制復帰には以下が必要です：
• OAuth2認証 (guilds.join scope)
• 各ユーザーのOAuth2アクセストークン
現在のバージョンでは、退出メンバーの検出のみが可能です。
```

---

### `/admin`
管理者パネルを表示（要ライセンス）

**権限:** ライセンス保有者のみ

**動作:**
1. ライセンスを確認
2. 全体の認証済みユーザー数を表示
3. 管理パネルを表示

**パネルボタン:**
- 🔄 **全メンバーのbackup**: 全認証済みユーザーの状態を確認

**応答例:**
```
🛠️ 管理パネル

Bot全体の認証済みユーザー数: 50人

[全メンバーのbackupボタン]
```

---

### `/license <user_id>`
管理者ライセンスを付与（要管理者権限）

**権限:** ADMIN_USER_IDで設定されたユーザーのみ

**引数:**
- `user_id`: ライセンスを付与するユーザーのDiscord ID

**動作:**
1. 管理者権限を確認
2. 指定ユーザーにライセンスを付与
3. 確認メッセージを表示

**応答例:**
```
✅ @User にライセンスを付与しました。
```

---

## 🔧 Configuration

### Environment Variables

```env
# Required
DISCORD_TOKEN=your_bot_token_here

# Optional (defaults to 568353089791328273)
ADMIN_USER_ID=your_admin_user_id
```

### Getting Your User ID

1. Discordで「設定」を開く
2. 「詳細設定」→「開発者モード」を有効化
3. 自分のプロフィールを右クリック
4. 「ユーザーIDをコピー」をクリック

---

## 🔐 Security Best Practices

### For Bot Owners
- ✅ Never commit `.env` file to Git
- ✅ Keep bot token secret
- ✅ Regularly backup `backup_bot.db`
- ✅ Use strong passwords for backups
- ✅ Limit admin licenses to trusted users
- ✅ Monitor bot logs for suspicious activity

### For Users
- ✅ Don't share backup ID and password
- ✅ Keep DM with credentials private
- ✅ Use VPN-free connection for authentication
- ✅ Report any issues to server admins

---

## ❓ Common Issues

### "コマンドが表示されない"
**Solution:**
1. Botに`applications.commands`スコープがあるか確認
2. 5-10分待つ
3. Discordを再起動
4. Botをサーバーから削除して再招待

### "DMが送信できませんでした"
**Solution:**
1. サーバーを右クリック→「プライバシー設定」
2. 「サーバーメンバーからのDMを許可する」を有効化

### "SERVER MEMBERS INTENT のエラー"
**Solution:**
1. Discord Developer Portalにアクセス
2. Bot設定で「SERVER MEMBERS INTENT」を有効化
3. Botを再起動

### "認証できない（VPN使用時）"
**Solution:**
1. VPNを一時的にオフにする
2. 認証ボタンをクリック
3. 認証完了後、VPNを再度オンにしても問題なし

---

## 📊 Database Schema

```sql
-- Backup credentials
CREATE TABLE backup_credentials (
    backup_id TEXT PRIMARY KEY,      -- 12桁のランダムID
    password TEXT NOT NULL,          -- 認証パスワード
    owner_id INTEGER NOT NULL,       -- 作成者のユーザーID
    guild_id INTEGER NOT NULL,       -- サーバーID
    created_at TIMESTAMP            -- 作成日時
);

-- Authenticated users
CREATE TABLE authenticated_users (
    id INTEGER PRIMARY KEY,
    backup_id TEXT NOT NULL,         -- バックアップID
    user_id INTEGER NOT NULL,        -- 認証ユーザーID
    guild_id INTEGER NOT NULL,       -- サーバーID
    authenticated_at TIMESTAMP,     -- 認証日時
    UNIQUE(backup_id, user_id)
);

-- Licensed admins
CREATE TABLE licensed_admins (
    user_id INTEGER PRIMARY KEY,     -- 管理者のユーザーID
    licensed_at TIMESTAMP           -- ライセンス付与日時
);
```

---

## 🎨 Embed Colors

- **認証パネル**: White (#FFFFFF)
- **認証情報DM**: Blue (#5865F2)
- **管理パネル**: Blue (#5865F2)

---

## 📞 Support

問題が発生した場合:
1. README.mdのトラブルシューティングセクションを確認
2. SETUP.mdの詳細手順を確認
3. Botログを確認（`python bot.py`の出力）
4. 開発者に連絡: @7zea

---

## 📝 Notes

- Botは常時実行している必要があります
- データベースファイル（`backup_bot.db`）は自動的に作成されます
- コマンドの同期には最大10分かかる場合があります
- メンバーの強制復帰にはOAuth2実装が必要です（今後のアップデート予定）

---

**Developer:** @7zea  
**Version:** 1.0.0  
**Last Updated:** 2024
