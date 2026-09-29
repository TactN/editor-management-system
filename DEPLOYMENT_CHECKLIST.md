# デプロイメントチェックリスト

このファイルに従って、段階的にデプロイを進めてください。

---

## フェーズ1: ローカルテスト

- [ ] Python 3.8以上がインストールされている
- [ ] `pip install -r requirements.txt` で成功
- [ ] `python editor_db.py` で データベース初期化が成功
- [ ] `python app.py` で Flask が起動できる
- [ ] `http://localhost:5000` でダッシュボードが表示される
- [ ] 編集者情報が正しく表示されている
- [ ] ウェブUIでステータス変更ができる
- [ ] `python editor_update_parser_sqlite.py "砂田さんをテスト中に"` が成功

✅ 問題がなければ、フェーズ2に進む

---

## フェーズ2: GitHub へのアップロード

### ステップ1: GitHub アカウントの準備
- [ ] GitHub アカウントがある（https://github.com）
- [ ] GitHub にログイン可能

### ステップ2: GitHub リポジトリを作成
1. https://github.com/new にアクセス
2. 以下を入力：
   - Repository name: `editor-management-system`
   - Description: `HUG&SHAKE 編集者管理システム`
   - Public を選択
3. **Create repository** をクリック
4. リポジトリページの URL をコピー（例: `https://github.com/YOUR_USERNAME/editor-management-system.git`）

### ステップ3: ローカルで Git を初期化
```bash
cd /mnt/user-data/outputs

# Git を初期化
git init

# ユーザー情報を設定
git config user.name "Tact"
git config user.email "t.nakaura@hugandshake.fun"

# ファイルをすべて追加
git add .

# コミット
git commit -m "Initial commit: Complete editor management system"

# ブランチを main に変更
git branch -M main

# リモートを追加
git remote add origin https://github.com/YOUR_USERNAME/editor-management-system.git

# GitHub にプッシュ
git push -u origin main
```

※ `YOUR_USERNAME` を自分の GitHub ユーザー名に置き換えてください

### ステップ4: GitHub で確認
- [ ] GitHub リポジトリにすべてのファイルが表示される
- [ ] `.gitignore` により、`__pycache__` や `*.db` は除外されている
- [ ] `README.md`, `DEPLOY_GUIDE.md` など ドキュメントが含まれている

✅ GitHub へのアップロードが完了したら、フェーズ3に進む

---

## フェーズ3: Render へのデプロイ

### ステップ1: Render アカウントの準備
- [ ] Render アカウントがある（https://render.com）
- [ ] GitHub と連携している

### ステップ2: Render で Web Service を作成
1. Render ダッシュボード (https://dashboard.render.com) にログイン
2. **New +** → **Web Service** をクリック
3. **Connect a repository** をクリック
4. `editor-management-system` を検索して選択
5. 以下の設定を入力：
   - **Name**: `editor-management-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free（無料枠でOK）
6. **Create Web Service** をクリック

### ステップ3: デプロイ待機
- [ ] Render が自動的にビルドを開始
- [ ] ログで以下を確認：
  - `pip install` が成功
  - `gunicorn` が起動している
- [ ] デプロイが完了（ログが止まる）

### ステップ4: デプロイ完了の確認
- [ ] Render ダッシュボードに割り当てられた URL が表示される
  - 例: `https://editor-management-system-xxxx.onrender.com`
- [ ] URL をクリックしてアクセス可能か確認
- [ ] ダッシュボードが正常に表示される
- [ ] 編集者情報が表示される

✅ デプロイが完了したら、フェーズ4に進む

---

## フェーズ4: 運用テスト

### ステップ1: チームメンバーに URL を共有
以下の情報を Land さんと水野さんに共有：

```
【HUG&SHAKE 編集者管理システムがデプロイされました】

📊 ダッシュボードURL:
https://editor-management-system-xxxx.onrender.com

【使い方】
1. このClaudeチャットで以下のように送信：
   「砂田さんをテスト中に」
   「全員をテスト前に」

2. システムが自動的にデータベースを更新

3. 上記URLのダッシュボードで即座に確認可能

詳しくは OPERATION_GUIDE.md を参照してください
```

### ステップ2: チームメンバーによるテスト
- [ ] Land さんが Claude チャットでメッセージを送信
- [ ] 水野さんが Claude チャットでメッセージを送信
- [ ] ダッシュボードにそれぞれの更新が反映される
- [ ] 複数人による同時更新も問題なく機能する

### ステップ3: 本運用の確認
- [ ] 2日間にわたり正常に動作する
- [ ] エラーが発生していない
- [ ] ダッシュボード表示が遅くない

✅ すべてのテストが成功したら、本運用開始

---

## フェーズ5: 本運用開始

- [ ] チーム全員が システムの使い方を理解
- [ ] OPERATION_GUIDE.md をチーム全員で確認
- [ ] 日次でダッシュボードを確認する習慣がついた
- [ ] 月1回、Render のログを確認する習慣をつける

---

## トラブル時の対応

### ❌ GitHub へのプッシュが失敗
**原因**: リモート URL が正しくない

**解決**:
```bash
git remote -v  # 現在のリモートを確認
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/editor-management-system.git
git push -u origin main
```

### ❌ Render のデプロイが失敗
**原因**: ビルドエラー

**確認方法**:
1. Render ダッシュボードで **Logs** を確認
2. エラーメッセージを読む
3. 一般的なエラー：
   - `pip install` 失敗 → requirements.txt を確認
   - `gunicorn` 起動失敗 → app.py のエラーを確認

**再デプロイ**:
```bash
git commit -m "Fix deployment issue" --allow-empty
git push origin main
# Render が自動的に再デプロイ
```

### ❌ ダッシュボードが 502 エラー
**原因**: アプリケーション実行時エラー

**確認方法**:
- Render の **Logs** で Python エラーを確認
- ローカルで同じエラーが発生するか確認

**解決**:
1. ローカルで問題を修正
2. GitHub に push
3. Render が自動的に再デプロイ

---

## よくある質問

**Q: Render の無料枠で十分？**  
A: はい。HUG&SHAKE のような社内ツールであれば問題ありません。

**Q: データベースは安全？**  
A: Render の永続ストレージに保存され、デプロイ後も保持されます。

**Q: 複数人での同時更新は？**  
A: SQLite は読取は並行可能で、書込は自動キューイングされます。

**Q: バックアップは？**  
A: 必要に応じて、定期的にダッシュボードのデータをエクスポートしてください。

---

## 完了
デプロイが完全に完了しました！🎉

不明な点がある場合は、このドキュメントを再確認するか、
Claude チャットで質問してください。
