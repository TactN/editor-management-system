#!/usr/bin/env python3
"""
編集者管理システム - MCPサーバー（Claudeのカスタムコネクタ用）
URL:  https://<あなたのRenderのURL>/mcp/<MCP_TOKEN>
環境変数 MCP_TOKEN が未設定の場合、MCPは無効になります。
"""
import os
import hmac
from flask import Blueprint, request, jsonify, Response
from editor_db import (
    get_all_editors, get_editors_by_division,
    get_status_options, update_editor_status
)

mcp_bp = Blueprint('mcp', __name__)

SERVER_INFO = {"name": "hugandshake-editors", "version": "1.0.0"}
DEFAULT_PROTOCOL = "2025-03-26"

TOOLS = [
    {
        "name": "list_editors",
        "description": "動画編集者の一覧と現在のステータスを取得する。divisionで「継続発注」「候補」「見送り」に絞り込める。",
        "inputSchema": {
            "type": "object",
            "properties": {"division": {"type": "string", "description": "区分（任意）"}},
        },
    },
    {
        "name": "list_statuses",
        "description": "設定できるステータスの一覧を取得する。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "update_editor_status",
        "description": "編集者1名のステータスを更新する。nameは部分一致（例:「砂田」）。statusは list_statuses の値と完全一致させること。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "編集者名（部分一致可）"},
                "status": {"type": "string", "description": "新しいステータス"},
                "updated_by": {"type": "string", "description": "更新者名（任意）"},
            },
            "required": ["name", "status"],
        },
    },
    {
        "name": "update_all_editors_status",
        "description": "全編集者のステータスを一括更新する（例:「全員をテスト前に」）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "updated_by": {"type": "string"},
            },
            "required": ["status"],
        },
    },
]


def _text(msg, error=False):
    return {"content": [{"type": "text", "text": msg}], "isError": error}


def _fmt(editors):
    return "\n".join(
        f"- {e['name']} / {e['division']} / {e['current_status']}" for e in editors
    ) or "（該当なし）"


def call_tool(name, args):
    statuses = get_status_options()
    by = args.get("updated_by") or "Claude"

    if name == "list_editors":
        div = args.get("division")
        eds = get_editors_by_division(div) if div else get_all_editors()
        return _text(_fmt(eds))

    if name == "list_statuses":
        return _text("\n".join(statuses))

    if name == "update_editor_status":
        status = args.get("status", "")
        if status not in statuses:
            return _text(f"ステータス「{status}」は無効です。選択肢: {', '.join(statuses)}", True)
        key = (args.get("name") or "").replace("さん", "").strip()
        if not key:
            return _text("nameが空です", True)
        hits = [e for e in get_all_editors() if key in e["name"]]
        if not hits:
            return _text(f"「{key}」に一致する編集者がいません。\n" + _fmt(get_all_editors()), True)
        if len(hits) > 1:
            return _text(f"「{key}」に複数一致しました。特定してください。\n" + _fmt(hits), True)
        ok, msg = update_editor_status(hits[0]["name"], status, by)
        return _text(msg, not ok)

    if name == "update_all_editors_status":
        status = args.get("status", "")
        if status not in statuses:
            return _text(f"ステータス「{status}」は無効です。選択肢: {', '.join(statuses)}", True)
        n = 0
        for e in get_all_editors():
            ok, _ = update_editor_status(e["name"], status, by)
            n += 1 if ok else 0
        return _text(f"✅ {n}名を「{status}」に更新しました")

    return _text(f"不明なツール: {name}", True)


def handle(msg):
    """JSON-RPCメッセージ1件を処理。通知(idなし)はNoneを返す。"""
    method = msg.get("method")
    mid = msg.get("id")
    if mid is None:
        return None

    def ok(result):
        return {"jsonrpc": "2.0", "id": mid, "result": result}

    def err(code, message):
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}

    if method == "initialize":
        ver = (msg.get("params") or {}).get("protocolVersion") or DEFAULT_PROTOCOL
        return ok({
            "protocolVersion": ver,
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        })
    if method == "ping":
        return ok({})
    if method == "tools/list":
        return ok({"tools": TOOLS})
    if method == "tools/call":
        p = msg.get("params") or {}
        try:
            return ok(call_tool(p.get("name"), p.get("arguments") or {}))
        except Exception as e:  # noqa
            return ok(_text(f"エラー: {e}", True))
    return err(-32601, f"Method not found: {method}")


@mcp_bp.route('/mcp/<token>', methods=['POST', 'GET', 'DELETE'])
def mcp_endpoint(token):
    expected = os.environ.get('MCP_TOKEN', '')
    if not expected or not hmac.compare_digest(token, expected):
        return jsonify({'error': 'Not found'}), 404
    if request.method != 'POST':
        return Response(status=405, headers={'Allow': 'POST'})

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700, "message": "Parse error"}}), 400
    if isinstance(data, list):
        out = [r for r in (handle(m) for m in data) if r is not None]
        return (jsonify(out), 200) if out else Response(status=202)
    resp = handle(data)
    return (jsonify(resp), 200) if resp is not None else Response(status=202)
