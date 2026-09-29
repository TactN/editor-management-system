# クイックスタート - ローカルテスト

本番環境へのデプロイ前に、ローカルで動作確認したい場合はこちら。

## ローカル環境でのセットアップ

### 1. Python 環境の確認
```bash
python3 --version  # Python 3.8 以上が必要
```

### 2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

### 3. データベースを初期化
```bash
python editor_db.py
```

出力例：
```
✅ データベース初期化完了: /mnt/user-data/outputs/editor_management.db
   編集者数: 10名
   ステータス: 8種類
```

### 4. ウェブアプリケーションを起動
```bash
python app.py
```

出力例：
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 5. ブラウザでアクセス
```
http://localhost:5000
```

---

## ローカルテストの操作方法

### ウェブダッシュボード
- `http://localhost:5000/` - メインダッシュボード
- `http://localhost:5000/all-editors` - 全編集者一覧
- `http://localhost:5000/active-editors` - 継続発注者
- `http://localhost:5000/candidate-editors` - 候補者

### API エンドポイント

**全編集者を取得**
```bash
curl http://localhost:5000/api/editors
```

**ステータスを更新**
```bash
curl -X POST http://localhost:5000/api/editors/update \
  -H "Content-Type: application/json" \
  -d '{
    "name": "砂田さん（サンライズ）",
    "status": "テスト中",
    "updated_by": "Tact"
  }'
```

---

## メッセージパーサーのテスト

### パーサーの単独実行
```bash
python editor_update_parser_sqlite.py "砂田さんをテスト中に"
```

出力例：
```
📝 入力: 砂田さんをテスト中に

✅ スプレッドシートを更新しました:
   • 砂田さん（サンライズ）→ テスト中

更新日時: 2026年09月29日 14:32:15
```

### 複数編集者の一括更新
```bash
python editor_update_parser_sqlite.py "全員をテスト前に"
```

---

## トラブルシューティング

### ❌ `ModuleNotFoundError: No module named 'flask'`
```bash
pip install Flask==3.0.0 Werkzeug==3.0.1
```

### ❌ `sqlite3.OperationalError: unable to open database file`
```bash
python editor_db.py  # 再初期化
```

### ❌ `Port 5000 is already in use`
別のポートで起動：
```bash
PORT=5001 python app.py
```

---

## デプロイ前のチェックリスト

- [ ] `python app.py` で起動できる
- [ ] `http://localhost:5000` でダッシュボードが表示される
- [ ] 編集者情報の表示に問題がない
- [ ] ステータス変更ボタンが機能する
- [ ] メッセージパーサーでテスト更新ができる
- [ ] データベースが正常に更新される

すべてチェックできたら、`DEPLOY_GUIDE.md` に進んでください！
