# HUG&SHAKE 編集者管理システム - ホスティングガイド

完全に独立した Web システムを公開インターネットで利用可能にする手順です。

## システム構成

```
クラウド環境（Render/Heroku）
├─ Flask Web アプリケーション
├─ SQLite データベース
└─ 静的ファイル（テンプレート、CSS）
```

## 推奨ホスティング: **Render（無料・簡単）**

### ステップ 1: Render にサインアップ

1. https://render.com にアクセス
2. GitHub アカウントで新規登録またはサインイン
3. メールアドレスで認証

### ステップ 2: GitHub にコードをアップロード

1. GitHub に新規リポジトリを作成（名前: `editor-management-system` など）
2. 以下のファイルをアップロード：
   ```
   editor_management/
   ├─ app.py
   ├─ editor_db.py
   ├─ requirements.txt
   ├─ runtime.txt
   ├─ templates/
   │  ├─ base.html
   │  ├─ index.html
   │  ├─ all_editors.html
   │  └─ division_view.html
   └─ static/
      └─ (必要に応じて CSS ファイル)
   ```

3. リポジトリを GitHub にプッシュ

### ステップ 3: Render で Web Service を作成

1. Render ダッシュボードで「New +」→「Web Service」
2. GitHub を接続し、リポジトリを選択
3. 以下を設定：
   - **Name**: `editor-management` など分かりやすい名前
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
4. 「Create Web Service」をクリック

### ステップ 4: デプロイ完了

数分でデプロイが完了し、自動的に URL が割り当てられます。
例: `https://editor-management.onrender.com`

チーム全員に URL を共有すると、ブラウザから編集者管理ダッシュボードにアクセス可能になります。

---

## 代替案: Heroku でのホスティング

### ステップ 1: Heroku にサインアップ

1. https://www.heroku.com にアクセス
2. 新規登録またはサインイン

### ステップ 2: Procfile を作成

```bash
echo "web: python app.py" > Procfile
```

### ステップ 3: Heroku にデプロイ

```bash
# Heroku CLI をインストール
# 参考: https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create editor-management
git push heroku main
```

---

## ローカルテスト

デプロイ前に、ローカルで動作確認：

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# Flask 開発サーバーを起動
python app.py
```

ブラウザで `http://localhost:5000` にアクセスしてテスト

---

## システム動作フロー

### 1. Web UI（閲覧・更新）
- メンバーが `https://editor-management.onrender.com` にアクセス
- ダッシュボードで編集者情報を確認
- Web フォームからステータスを直接更新可能

### 2. Claude チャット（自動更新）
- Claude チャットで `"みつゆうを継続発注中に"`
- Python スクリプトが自動的にメッセージを解析
- SQLite データベースが更新される
- Web UI がリアルタイムで反映

---

## トラブルシューティング

### 1. デプロイがエラーで失敗する

**原因**: requirements.txt が見つからない、または build command が間違っている

**解決**:
- `requirements.txt` がリポジトリのルートにあることを確認
- Render 側のログを確認

### 2. ページが表示されない

**原因**: Flask アプリケーションがクラッシュしている

**解決**:
- Render のログを確認
- ローカルで `python app.py` を実行してエラーを確認

### 3. データベースが空

**原因**: SQLite がホスト環境で初期化されていない

**解決**:
- `editor_db.py` を実行してデータベースを初期化
- またはデプロイ時に init スクリプトを自動実行

---

## セキュリティ考慮事項

このシステムは以下の前提で設計されています：

- **社内利用前提**: インターネット公開してもよい（ただし誰がアクセスできるか確認）
- **認証なし**: チーム全員が更新可能（信頼ベース）
- **HTTPS**: Render/Heroku は自動的に HTTPS を適用

より厳格なセキュリティが必要な場合：
- 基本認証の追加
- API キー認証の実装
- アクセスログの記録

---

## 日常的な管理

### バックアップ

SQLite データベースを定期的にバックアップ：

```bash
cp editor_management.db editor_management_backup.db
```

### データベースクリア（初期化）

```bash
python editor_db.py  # 既存データを上書きする
```

### ログ確認

Render ダッシュボールの「Logs」セクションでアクセスログを確認

---

## 次のステップ

- [ ] GitHub にコードを上載する
- [ ] Render で Web Service をデプロイ
- [ ] チーム全員に URL を共有
- [ ] Claude チャットでテストメッセージを送信
- [ ] Web UI でステータスが更新されたことを確認

