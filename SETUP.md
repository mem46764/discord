# Discord Backup Bot - Setup Guide

このガイドでは、Discord Backup Botのセットアップ手順を詳しく説明します。

## 前提条件

- Python 3.8以上がインストールされていること
- Discord アカウントを持っていること
- Discordサーバーの管理者権限があること

## 1. Discord Bot の作成

### 1.1 Discord Developer Portal にアクセス

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 右上の「New Application」をクリック
3. アプリケーション名を入力（例: "Backup Bot"）して「Create」

### 1.2 Bot を作成

1. 左側のメニューから「Bot」を選択
2. 「Add Bot」をクリックして確認
3. Bot のユーザー名を設定（必要に応じて）
4. 「Reset Token」をクリックしてトークンをコピー（後で使用）
   - ⚠️ このトークンは誰にも共有しないでください

### 1.3 必要な権限を設定

1. Botページで以下の設定を有効化:
   - **Privileged Gateway Intents** セクション:
     - ✅ `SERVER MEMBERS INTENT` を ON
     - ✅ `MESSAGE CONTENT INTENT` を ON（必要に応じて）

### 1.4 OAuth2 URL を生成

1. 左側のメニューから「OAuth2」→「URL Generator」を選択
2. **Scopes** で以下を選択:
   - ✅ `bot`
   - ✅ `applications.commands`
3. **Bot Permissions** で以下を選択:
   - ✅ `Read Messages/View Channels`
   - ✅ `Send Messages`
   - ✅ `Manage Messages`
   - ✅ `Embed Links`
   - ✅ `Read Message History`
   - ✅ `Add Reactions`
   - ✅ `Use Slash Commands`
   - ✅ `Manage Roles`（メンバー管理用）
   - ✅ `Create Invite`（招待作成用）
   
   または簡単に:
   - ✅ `Administrator`（全権限）

4. 生成されたURLをコピーしてブラウザで開く
5. Botを追加したいサーバーを選択して「認証」

## 2. Bot のインストール

### 2.1 リポジトリのクローン

```bash
git clone <repository_url>
cd discord
```

### 2.2 仮想環境の作成（推奨）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2.4 環境変数の設定

1. `.env.example`をコピーして`.env`を作成:
```bash
cp .env.example .env
```

2. `.env`ファイルを編集:
```
DISCORD_TOKEN=ここに先ほどコピーしたBotトークンを貼り付け
ADMIN_USER_ID=ライセンス付与権限を持つユーザーID
```

**自分のユーザーIDの取得方法:**
1. Discordで「設定」→「詳細設定」→「開発者モード」を有効化
2. 自分のプロフィールを右クリック→「ユーザーIDをコピー」

## 3. Bot の起動

```bash
python bot.py
```

成功すると以下のようなメッセージが表示されます:
```
Bot名#1234 has connected to Discord!
Synced 5 command(s)
```

## 4. コマンドの確認

Discordサーバーで`/`を入力すると、以下のコマンドが表示されるはずです:
- `/verify`
- `/count`
- `/backup`
- `/admin`
- `/license`

⚠️ コマンドが表示されない場合は、数分待ってからDiscordを再起動してください。

## 5. 初期設定

### 5.1 管理者ライセンスの付与

`.env`ファイルで設定した`ADMIN_USER_ID`のユーザーでログインして:
```
/license <管理者にしたいユーザーID>
```

### 5.2 認証パネルの作成

任意のチャンネルで:
```
/verify
```

これで基本的なセットアップは完了です！

## トラブルシューティング

### コマンドが同期されない

1. Botを一度サーバーから削除
2. OAuth2 URLを使って再招待
3. 5-10分待つ
4. Discordクライアントを再起動

### DMが送信できない

ユーザーのプライバシー設定を確認:
1. サーバーを右クリック → 「プライバシー設定」
2. 「サーバーメンバーからのダイレクトメッセージを許可する」を有効化

### "SERVER MEMBERS INTENT" のエラー

1. Discord Developer Portal に戻る
2. Bot設定で「SERVER MEMBERS INTENT」が有効になっているか確認
3. Botを再起動

## セキュリティ

- `.env`ファイルは`.gitignore`に含まれており、Gitにコミットされません
- Botトークンは絶対に公開しないでください
- データベースファイル（`backup_bot.db`）も定期的にバックアップしてください

## サポート

問題が発生した場合は、以下を確認してください:
1. Python のバージョン（3.8以上）
2. すべての依存関係がインストールされているか
3. `.env`ファイルが正しく設定されているか
4. Botに必要な権限が付与されているか
5. SERVER MEMBERS INTENT が有効になっているか
