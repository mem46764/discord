# Discord Backup Bot

Discord バックアップBotは、サーバーメンバーの認証とバックアップ機能を提供するDiscord Botです。

## 機能概要

### コマンド一覧

#### 1. `/verify`
認証パネルを生成し、backup IDとpasswordを設定します。

**使用方法:**
```
/verify [password]
```

**機能:**
- backup passwordを指定（省略時は自動生成）
- 12桁のbackup IDを自動生成
- パスワードとIDをDMで送信
- 認証パネルをチャンネルに表示

**認証パネルの機能:**
- ✅ 認証ボタン: ユーザーを認証済みとして登録
- 利用規約ボタン: 利用規約を表示

---

#### 2. `/count`
backup IDとpasswordを使用して、認証済みメンバー数を確認します。

**使用方法:**
```
/count <backup_id> <password>
```

**機能:**
- 認証情報を検証
- 認証済みメンバー数をDMで送信

---

#### 3. `/backup`
サーバーを抜けたメンバーを強制復帰させます。

**使用方法:**
```
/backup <backup_id> <password>
```

**機能:**
- 認証情報を検証
- 認証済みで退出したメンバーを検出
- 対象メンバーの復帰処理を実行
- 結果をコマンド実行者に送信

---

#### 4. `/admin`
Bot全体の認証データを管理する管理者専用コマンドです。

**使用方法:**
```
/admin
```

**権限:**
- `/license`でライセンスを付与されたユーザーのみ実行可能

**機能:**
- Bot全体の認証済みユーザー数を表示
- 全メンバーのバックアップボタンを提供

---

#### 5. `/license`
`/admin`コマンドを実行できるライセンスを付与します。

**使用方法:**
```
/license <user_id>
```

**権限:**
- ユーザーID `568353089791328273` のみ実行可能

**機能:**
- 指定したユーザーIDに管理者ライセンスを付与
- ライセンス付与後、対象ユーザーは`/admin`を実行可能

---

## セットアップ

### 必要な環境
- Python 3.8以上
- Discord Bot Token
- Discord Bot の必要な権限:
  - `applications.commands` (スラッシュコマンド)
  - `bot` スコープ
  - Server Members Intent (メンバー情報へのアクセス)

### インストール手順

1. **リポジトリをクローン**
```bash
git clone <repository_url>
cd discord
```

2. **依存関係をインストール**
```bash
pip install -r requirements.txt
```

3. **環境変数を設定**
`.env.example`をコピーして`.env`を作成:
```bash
cp .env.example .env
```

`.env`ファイルを編集してBot Tokenを設定:
```
DISCORD_TOKEN=your_actual_bot_token_here
```

4. **Bot Tokenの取得方法**
- [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
- 新しいアプリケーションを作成
- Botセクションでボットを作成
- TokenをコピーしてDISCORD_TOKENに設定
- OAuth2セクションでBot ScopeとPermissionsを設定:
  - Scopes: `bot`, `applications.commands`
  - Bot Permissions: `Administrator`（または必要な権限を個別に選択）
- Privileged Gateway Intentsで`SERVER MEMBERS INTENT`を有効化

5. **Botを起動**
```bash
python bot.py
```

6. **コマンドの同期**
初回起動時、BotがDiscordにコマンドを自動的に同期します。
同期完了までに数分かかる場合があります。

---

## データベース

BotはSQLiteデータベース（`backup_bot.db`）を使用してデータを保存します。

### テーブル構造

#### backup_credentials
- `backup_id`: バックアップID（主キー）
- `password`: パスワード
- `owner_id`: 作成者のユーザーID
- `guild_id`: サーバーID
- `created_at`: 作成日時

#### authenticated_users
- `id`: 自動採番ID
- `backup_id`: バックアップID（外部キー）
- `user_id`: 認証済みユーザーID
- `guild_id`: サーバーID
- `authenticated_at`: 認証日時

#### licensed_admins
- `user_id`: ライセンス付与されたユーザーID（主キー）
- `licensed_at`: ライセンス付与日時

---

## 使用例

### 基本的なワークフロー

1. **認証パネルの作成**
```
/verify
```
→ DMでbackup IDとpasswordを受信
→ チャンネルに認証パネルが表示される

2. **ユーザーの認証**
→ 認証パネルの「認証」ボタンをクリック
→ 認証完了メッセージが表示される

3. **認証数の確認**
```
/count <backup_id> <password>
```
→ DMで認証済みユーザー数を受信

4. **メンバーのバックアップ**
```
/backup <backup_id> <password>
```
→ 退出したメンバーの復帰処理が実行される

### 管理者機能

1. **ライセンスの付与**（特定ユーザーのみ）
```
/license 123456789012345678
```
→ 指定したユーザーに管理者権限を付与

2. **管理パネルの表示**（ライセンス保有者のみ）
```
/admin
```
→ 全体の認証数と管理機能が表示される

---

## セキュリティに関する注意事項

1. **Tokenの管理**: `.env`ファイルは絶対にGitにコミットしないでください。
2. **パスワードの管理**: backup passwordは安全に管理してください。
3. **権限の設定**: Botに必要最小限の権限のみを付与してください。
4. **データベースのバックアップ**: `backup_bot.db`を定期的にバックアップしてください。

---

## トラブルシューティング

### コマンドが表示されない
- Botに`applications.commands`スコープが付与されているか確認
- Botを一度サーバーから削除して再招待
- 数分待ってからDiscordクライアントを再起動

### DMが送信できない
- ユーザーのプライバシー設定でサーバーメンバーからのDMが許可されているか確認

### メンバー情報が取得できない
- Discord Developer PortalでSERVER MEMBERS INTENTが有効化されているか確認

---

## 開発者情報

Developer: @7zea

## ライセンス

このプロジェクトは個人利用および学習目的で提供されています。
