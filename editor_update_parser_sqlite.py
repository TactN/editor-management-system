#!/usr/bin/env python3
"""
チャットメッセージから編集者更新リクエストを自動抽出・実行（SQLite版）
例：
  "砂田さんをテスト中に"
  "じぇいをテスト合格に変更"
  "全員をテスト前に"
"""

import re
from editor_db import update_editor_status, get_all_editors, get_status_options
from datetime import datetime

EDITORS_MAPPING = {
    "じぇい": "じぇい",
    "めんだこちゃん": "めんだこちゃん",
    "葵": "葵",
    "砂田": "砂田さん（サンライズ）",
    "砂田さん": "砂田さん（サンライズ）",
    "池田": "池田さん（monoworks）",
    "池田さん": "池田さん（monoworks）",
    "芹田": "芹田みなみ",
    "芹田みなみ": "芹田みなみ",
    "山本": "山本久美（株式会社Vuild）",
    "山本久美": "山本久美（株式会社Vuild）",
    "下川": "下川弓絵",
    "下川弓絵": "下川弓絵",
    "越前": "越前舞子",
    "越前舞子": "越前舞子",
    "みつゆう": "みつゆう",
}

STATUSES = get_status_options()

def extract_update_request(message):
    """
    メッセージから編集者名とステータスを抽出
    パターン例:
    - "砂田さんをテスト中に"
    - "じぇいをテスト合格に変更"
    - "全員をテスト前に"
    """

    updates = {}

    # パターン1: "【編集者】を【ステータス】に"
    pattern = r'(.+?)(?:を|を\s*)(.+?)(?:に|に変更|に更新)'
    matches = re.findall(pattern, message)

    for editor_part, status_part in matches:
        # 編集者名を正規化
        editor_part = editor_part.strip()
        status_part = status_part.strip()

        if editor_part == "全員":
            # 全員更新
            if status_part in STATUSES:
                all_editors = get_all_editors()
                updates = {editor['name']: status_part for editor in all_editors}
                break
        else:
            # 個別更新
            editor_full_name = None
            for short_name, full_name in EDITORS_MAPPING.items():
                if short_name in editor_part or editor_part in short_name:
                    editor_full_name = full_name
                    break

            if editor_full_name and status_part in STATUSES:
                updates[editor_full_name] = status_part

    return updates

def apply_updates(updates, updated_by='Claude'):
    """SQLiteに更新を適用"""
    if not updates:
        return False

    success_count = 0
    for name, status in updates.items():
        success, message = update_editor_status(name, status, updated_by)
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"⚠️  {message}")

    if success_count > 0:
        print(f"\n更新日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        return True
    return False

def process_message(message):
    """メッセージを処理して更新を実行"""
    print(f"📝 入力: {message}\n")

    updates = extract_update_request(message)

    if not updates:
        print("❌ 更新内容が検出されませんでした")
        print("\n使用例:")
        print('  "砂田さんをテスト中に"')
        print('  "じぇいをテスト合格に変更"')
        print('  "全員をテスト前に"')
        return False

    return apply_updates(updates, updated_by='Claude')

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = input("更新内容を入力: ")

    process_message(message)

