"""Offline preparation only. No network, service imports, credentials or installer."""

import argparse
import hashlib
import json
from pathlib import Path


GOOGLE = {
    "drive": ("https://drivemcp.googleapis.com/mcp/v1", ["drive.readonly"],
              ["search_files", "get_file_metadata", "read_file_content", "download_file_content", "list_recent_files", "get_file_permissions"]),
    "docs": ("https://docsmcp.googleapis.com/mcp/v1", ["documents.readonly", "drive.readonly"], ["read_doc"]),
    "sheets": ("https://sheetsmcp.googleapis.com/mcp/v1", ["spreadsheets.readonly", "drive.readonly"], ["get_values", "get_spreadsheet"]),
    "slides": ("https://slidesmcp.googleapis.com/mcp/v1", ["presentations.readonly", "drive.readonly"], ["read_presentation"]),
    "gmail": ("https://gmailmcp.googleapis.com/mcp/v1", ["gmail.readonly"],
              ["search_threads", "get_message", "get_thread", "list_labels", "list_drafts"]),
    "calendar": ("https://calendarmcp.googleapis.com/mcp/v1",
                 ["calendar.calendarlist.readonly", "calendar.events.readonly", "calendar.events.freebusy"],
                 ["list_calendars", "list_events", "get_event", "search_events", "suggest_time"]),
    "chat": ("https://chatmcp.googleapis.com/mcp/v1",
             ["chat.spaces.readonly", "chat.memberships.readonly", "chat.messages.readonly"],
             ["search_conversations", "list_messages", "search_messages", "list_memberships"]),
    "people": ("https://people.googleapis.com/mcp/v1", ["contacts.readonly", "userinfo.profile"],
               ["get_user_profile", "search_contacts"]),
}


def plan():
    candidates = []
    for name, (url, scopes, names) in GOOGLE.items():
        candidates.append({"id": "google_" + name, "provider": "google", "url": url,
            "scope_candidates": ["https://www.googleapis.com/auth/" + value for value in scopes],
            "read_tool_candidates": names, "prerequisites": ["preview_eligibility", "cloud_project", "approved_user_oauth"],
            "auth_type_candidate": "oauth_2.1_static"})
    candidates.extend([
        {"id": "canva", "provider": "canva", "url": "https://mcp.canva.com/mcp",
         "scope_candidates": [], "read_tool_candidates": ["search-designs", "search-folders", "list-folder-items",
            "get-design", "get-design-content", "get-design-pages", "get-presenter-notes", "list-comments"],
         "prerequisites": ["registered_oauth_client", "scope_review", "approved_user_oauth"],
         "auth_type_candidate": "oauth_2.1_static"},
        {"id": "zoom_meetings", "provider": "zoom", "url": "https://zoom.us/mcp/meeting/streamable",
         "scope_candidates": [], "read_tool_candidates": ["search_meetings", "get_meeting_assets", "recordings_list", "get_recording_resource"],
         "prerequisites": ["account_eligibility", "scope_review", "approved_user_oauth", "endpoint_and_client_registration_review"],
         "auth_type_candidate": "oauth_2.1"},
    ])
    for item in candidates:
        item["state"] = "PREPARED_NOT_CONNECTED"
        # Field shape inspected in installed WebUI. This is an individual
        # reference, NOT a complete global-config replacement or import file.
        item["webui_connection_reference"] = {
            "url": item["url"], "path": "", "type": "mcp", "auth_type": item["auth_type_candidate"],
            "forward_cookies": False, "headers": {}, "key": "",
            "config": {"enable": False, "access_grants": [], "function_name_filter_list": "__PREPARATION_ONLY__"},
            "info": {"id": "admin_test_" + item["id"], "name": "Admin integration test: " + item["id"],
                     "oauth_scope": " ".join(item["scope_candidates"])}
        }
    return {"format_version": 1, "status": "OFFLINE_PREPARATION_ONLY", "installable": False,
            "model_requests_allowed": False, "provider_writes_allowed": False,
            "candidates": candidates,
            "deferred_surfaces": ["forms", "tasks", "meet", "drawings", "vids", "keep", "sites", "apps_script", "local_project_files"],
            "required_before_live_test": ["owner_scope_consent", "approved_synthetic_resources", "backup_and_snapshot",
                "oauth_registration_and_callback", "protected_token_storage_review", "exact_schema_and_operation_review",
                "administrative_profile_guard", "resource_allowlist", "timeouts_and_result_limits", "rollback_ready"]}


def review_catalog(catalog, approved_names):
    """Exact-name offline schema review, not an execution/permission boundary.

    Trust in a tool's behavior must come from reviewed provider semantics,
    scopes and host executors, not readOnlyHint or its advertised name.
    """
    if not isinstance(catalog, dict):
        raise ValueError("CATALOG_INVALID")
    tools = catalog.get("tools")
    if not isinstance(tools, list) or len(tools) > 256:
        raise ValueError("CATALOG_INVALID")
    if (not isinstance(approved_names, list) or not approved_names
            or any(type(name) is not str or not name for name in approved_names)
            or len(set(approved_names)) != len(approved_names)):
        raise ValueError("ALLOWLIST_INVALID")
    seen, accepted, excluded = set(), [], []
    for tool in tools:
        if not isinstance(tool, dict) or type(tool.get("name")) is not str or not tool["name"]:
            raise ValueError("TOOL_INVALID")
        name = tool["name"]
        if len(name) > 128 or name in seen:
            raise ValueError("TOOL_NAME_INVALID")
        seen.add(name)
        if name not in approved_names:
            excluded.append(name)
            continue
        schema = tool.get("inputSchema")
        if not isinstance(schema, dict) or schema.get("type") != "object":
            raise ValueError("SCHEMA_INVALID")
        annotations = tool.get("annotations", {})
        if not isinstance(annotations, dict):
            raise ValueError("ANNOTATIONS_INVALID")
        if annotations.get("readOnlyHint") is False or annotations.get("destructiveHint") is True:
            raise ValueError("READ_CONTRACT_CONFLICT")
        digest = hashlib.sha256(json.dumps(schema, sort_keys=True, allow_nan=False).encode()).hexdigest()
        accepted.append({"name": name, "schema_sha256": digest})
    return {"accepted": accepted, "excluded": excluded,
            "missing": sorted(set(approved_names) - seen), "execution_authorized": False}


def build(target):
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(plan(), indent=2) + "\n"
    (target / "connection-candidates.json").write_text(payload, encoding="utf-8")
    print("Offline connection candidates prepared; nothing installed or connected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory")
    build(parser.parse_args().output_directory)
