# HUG&SHAKE 編集者管理システム デプロイガイド

## デプロイ概要
このガイドでは、GitHub と Render を使用してシステムを公開します。

## 必要な準備
- GitHub アカウント（無料）
- Render アカウント（無料）

---

## ステップ1: GitHub にコードをアップロード

### 1-1. GitHub でリポジトリを作成
1. https://github.com/new にアクセス
2. Repository name: `editor-management-system`
3. Description: `HUG&SHAKE 編集者管理システム`
4. Public を選択（他のメンバーがアクセス可能に）
5. **Create repository** をクリック

### 1-2. ローカルで Git を初期化
```bash
cd /mnt/user-data/outputs
git init
git config user.name "Tact"
git config user.email "t.nakaura@hugandshake.fun"
```

### 1-3. ファイルを追加してコミット
```bash
git add .
git commit -m "Initial commit: Complete editor management system

- SQLite database with editor information
- Flask web application with REST API
- Bootstrap responsive UI
- Message parser for Claude chat updates"
```

### 1-4. GitHub にプッシュ
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/editor-management-system.git
git push -u origin main
```
※ `YOUR_USERNAME` を自分の GitHub ユーザー名に置き換えてください

---

## ステップ2: Render にデプロイ

### 2-1. Render にサインアップ
1. https://render.com にアクセス
2. GitHub アカウントでサインアップ
3. GitHub と Render を連携

### 2-2. Web Service を作成
1. Render ダッシュボードで **New +** → **Web Service**
2. **Connect a repository** をクリック
3. `editor-management-system` を選択
4. 設定を入力：
   - **Name**: `editor-management-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. **Create Web Service** をクリック

### 2-3. デプロイ待機
- Render が自動的にデプロイを開始します
- ログで進捗を確認できます
- デプロイ完了後、以下のようなURL が割り当てられます：
  ```
  https://editor-management-system-xxxx.onrender.com
  ```

---

## ステップ3: 動作確認

### 3-1. ウェブダッシュボードにアクセス
割り当てられた URL にアクセスして、以下を確認：
- ✅ ダッシュボードが表示される
- ✅ 編集者リストが見える
- ✅ ステータス変更ボタンが機能する

### 3-2. Claude チャットで更新テスト
Claude のこのチャットで以下のコマンドを実行：
```
砂田さんをテスト中に
```

システムが以下を実行します：
1. メッセージをパース
2. SQLite データベースを更新
3. ウェブダッシュボードに反映

---

## ステップ4: チーム全員に共有

### 4-1. URL を共有
デプロイ完了後、以下を Land さんと水野さんに共有：

```
📊 編集者管理システムダッシュボード
URL: https://editor-management-system-xxxx.onrender.com

【使い方】
1. このチャットで「砂田さんをテスト中に」などと送信
2. システムが自動的にダッシュボードを更新
3. 上記URLでリアルタイムに確認可能
```

### 4-2. OPERATION_GUIDE.md を配布
同じフォルダにある `OPERATION_GUIDE.md` をチーム全員で確認

---

## トラブルシューティング

### ❌ デプロイが失敗する
**原因**: requirements.txt に不足しているパッケージ

**解決**:
```bash
cd /mnt/user-data/outputs
pip install -r requirements.txt
```

### ❌ ダッシュボードが 502 エラー
**原因**: アプリケーションエラー

**確認方法**:
1. Render ダッシュボードで **Logs** を確認
2. エラーメッセージを確認
3. ローカルで再テスト

### ❌ データベースが見つからない
**原因**: `/mnt/user-data/outputs/editor_management.db` がない

**解決**:
```bash
python editor_db.py
```
を実行して再初期化

---

## デプロイ後の更新

コードを更新する場合：

```bash
# ローカルで変更
git add .
git commit -m "Update: description of changes"
git push origin main
```

Render が自動的に GitHub の変更を検知して再デプロイします。

---

## 無料枠の注意事項

Render の無料枠：
- **メモリ**: 0.5GB
- **ストレージ**: 1GB
- **バンド幅**: 100GB/月
- **非アクティブ時**: 15分後に停止（再起動時に10秒程度遅延）

小規模な社内ツールであれば問題なく運用できます。

---

## よくある質問

### Q: データベースはどこに保存される？
A: Render の永続ストレージ（Disk）に保存されます。デプロイ後も保持されます。

### Q: 複数人が同時に更新できる？
A: はい。SQLite は読取アクセスが並行で可能で、書込は自動的にキューイングされます。

### Q: オフラインでも使える？
A: このシステムはオンライン前提です。ローカル版が必要な場合は別途検討してください。

---

デプロイが完了したら、このドキュメントをチーム全員と共有してください！
