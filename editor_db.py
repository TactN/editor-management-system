#!/usr/bin/env python3
"""
HUG&SHAKE 編集者管理システム - SQLite データベース定義
"""

import sqlite3
from datetime import datetime
import os

# Render: 永続ディスク(/data)があればそこに保存、なければアプリと同じフォルダ
_default_dir = '/data' if os.path.isdir('/data') else os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DB_PATH', os.path.join(_default_dir, 'editor_management.db'))

def init_database():
    """データベースを初期化"""
    # 既存のDBがあれば削除（初期化用）
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 編集者テーブル
    cursor.execute('''
        CREATE TABLE editors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            division TEXT NOT NULL,
            current_status TEXT NOT NULL,
            company_type TEXT,
            invoice_registration TEXT,
            num_editors TEXT,
            gender_ratio TEXT,
            portfolio TEXT,
            response_range TEXT,
            software TEXT,
            impressions TEXT,
            price TEXT,
            price_conditions TEXT,
            normal_delivery TEXT,
            fastest_delivery TEXT,
            revision_support TEXT,
            monthly_capacity TEXT,
            contact_method TEXT,
            notes TEXT,
            qualitative_doc_url TEXT,
            first_contact_date TEXT,
            last_updated TEXT,
            updated_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ステータス定義テーブル
    cursor.execute('''
        CREATE TABLE status_options (
            id INTEGER PRIMARY KEY,
            status_name TEXT UNIQUE NOT NULL,
            category TEXT,
            display_order INTEGER
        )
    ''')
    
    # 区分定義テーブル
    cursor.execute('''
        CREATE TABLE division_options (
            id INTEGER PRIMARY KEY,
            division_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # ステータスマスターデータを挿入
    statuses = [
        ('未接触', 'candidate', 1),
        ('ヒアリング済', 'candidate', 2),
        ('テスト前', 'candidate', 3),
        ('テスト中', 'candidate', 4),
        ('テスト合格', 'candidate', 5),
        ('継続発注中', 'active', 6),
        ('一時休止', 'paused', 7),
        ('見送り', 'rejected', 8),
    ]
    cursor.executemany(
        'INSERT INTO status_options (status_name, category, display_order) VALUES (?, ?, ?)',
        statuses
    )
    
    # 区分マスターデータを挿入
    divisions = [
        ('継続発注',),
        ('候補',),
        ('見送り',),
    ]
    cursor.executemany(
        'INSERT INTO division_options (division_name) VALUES (?)',
        divisions
    )
    
    # 初期データ: みつゆうを含む10名の編集者
    today = datetime.now().strftime('%Y/%m/%d')
    initial_editors = [
        ('じぇい', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('めんだこちゃん', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('葵', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('砂田さん（サンライズ）', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('池田さん（monoworks）', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('芹田みなみ', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('山本久美（株式会社Vuild）', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('下川弓絵', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('越前舞子', '候補', 'テスト前', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
        ('みつゆう', '継続発注', '継続発注中', '', '', '', '', '', '納期対応の柔軟性が高い、ミスが少ない、情報共有が丁寧、重要度の高い案件対応', '', '', '', '', '', '', '', '', '', '', '', today, today, 'Tact'),
    ]
    
    cursor.executemany(
        '''INSERT INTO editors (
            name, division, current_status, company_type, invoice_registration,
            num_editors, gender_ratio, portfolio, response_range, software,
            impressions, price, price_conditions, normal_delivery, fastest_delivery,
            revision_support, monthly_capacity, contact_method, notes, 
            qualitative_doc_url, first_contact_date, last_updated, updated_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        initial_editors
    )
    
    conn.commit()
    conn.close()
    print(f"✅ データベース初期化完了: {DB_PATH}")
    print(f"   編集者数: 10名")
    print(f"   ステータス: 8種類")

def update_editor_status(name, new_status, updated_by='System'):
    """編集者のステータスを更新"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            '''UPDATE editors 
               SET current_status = ?, last_updated = ?, updated_by = ?
               WHERE name = ?''',
            (new_status, datetime.now().strftime('%Y/%m/%d'), updated_by, name)
        )
        conn.commit()
        
        if cursor.rowcount > 0:
            return True, f"✅ {name} を {new_status} に更新しました"
        else:
            return False, f"❌ 編集者が見つかりません: {name}"
    except sqlite3.Error as e:
        return False, f"❌ エラー: {e}"
    finally:
        conn.close()

def get_all_editors():
    """全編集者を取得"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM editors ORDER BY id')
    editors = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in editors]

def get_editors_by_division(division):
    """区分でフィルタ"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM editors WHERE division = ? ORDER BY id', (division,))
    editors = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in editors]

def get_status_options():
    """ステータス選択肢を取得"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT status_name FROM status_options ORDER BY display_order')
    statuses = cursor.fetchall()
    conn.close()
    
    return [s[0] for s in statuses]

if __name__ == '__main__':
    init_database()

