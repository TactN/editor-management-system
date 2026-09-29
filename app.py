#!/usr/bin/env python3
"""
HUG&SHAKE 編集者管理システム - Flask Web アプリケーション
"""

from flask import Flask, render_template, jsonify, request
from editor_db import (
    get_all_editors, get_editors_by_division,
    get_status_options, update_editor_status, DB_PATH, init_database
)
import json
import os
from datetime import datetime

app = Flask(__name__)

# DBが無ければ初期化（Render初回起動用。既存DBは消さない）
if not os.path.exists(DB_PATH):
    init_database()

# ========== API エンドポイント ==========

@app.route('/api/editors', methods=['GET'])
def api_get_editors():
    """全編集者を取得"""
    editors = get_all_editors()
    return jsonify(editors)

@app.route('/api/editors/division/<division>', methods=['GET'])
def api_get_by_division(division):
    """区分でフィルタ"""
    editors = get_editors_by_division(division)
    return jsonify(editors)

@app.route('/api/editors/update', methods=['POST'])
def api_update_editor():
    """編集者のステータスを更新"""
    data = request.json
    name = data.get('name')
    new_status = data.get('status')
    updated_by = data.get('updated_by', 'API')
    
    success, message = update_editor_status(name, new_status, updated_by)
    return jsonify({'success': success, 'message': message})

@app.route('/api/statuses', methods=['GET'])
def api_get_statuses():
    """ステータス選択肢を取得"""
    statuses = get_status_options()
    return jsonify(statuses)

# ========== ウェブビュー ==========

@app.route('/')
def index():
    """メインページ"""
    all_editors = get_all_editors()
    statuses = get_status_options()
    
    # 区分別に分類
    active_editors = get_editors_by_division('継続発注')
    candidate_editors = get_editors_by_division('候補')
    rejected_editors = get_editors_by_division('見送り')
    
    # ステータス別の集計
    status_summary = {}
    for status in statuses:
        count = sum(1 for e in all_editors if e['current_status'] == status)
        status_summary[status] = count
    
    return render_template('index.html',
        all_editors=all_editors,
        active_editors=active_editors,
        candidate_editors=candidate_editors,
        rejected_editors=rejected_editors,
        statuses=statuses,
        status_summary=status_summary,
        last_updated=datetime.now().strftime('%Y年%m月%d日 %H:%M')
    )

@app.route('/all-editors')
def all_editors_view():
    """全編集者一覧"""
    editors = get_all_editors()
    statuses = get_status_options()
    
    return render_template('all_editors.html',
        editors=editors,
        statuses=statuses
    )

@app.route('/active-editors')
def active_editors_view():
    """継続発注者一覧"""
    editors = get_editors_by_division('継続発注')
    statuses = get_status_options()
    
    return render_template('division_view.html',
        title='継続発注者一覧',
        editors=editors,
        division='継続発注',
        statuses=statuses
    )

@app.route('/candidate-editors')
def candidate_editors_view():
    """候補者一覧"""
    editors = get_editors_by_division('候補')
    statuses = get_status_options()
    
    return render_template('division_view.html',
        title='候補者一覧',
        editors=editors,
        division='候補',
        statuses=statuses
    )

@app.route('/rejected-editors')
def rejected_editors_view():
    """見送り者一覧"""
    editors = get_editors_by_division('見送り')
    statuses = get_status_options()
    
    return render_template('division_view.html',
        title='見送り者一覧',
        editors=editors,
        division='見送り',
        statuses=statuses
    )

# ========== エラーハンドリング ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)

