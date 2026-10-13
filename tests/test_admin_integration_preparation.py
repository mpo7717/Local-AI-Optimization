import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("preparation", Path(__file__).parents[1] / "tools/prepare_admin_integrations.py")
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)


class PreparationTests(unittest.TestCase):
    def test_plan_is_not_installable_and_has_no_active_connections(self):
        plan = prep.plan()
        self.assertFalse(plan["installable"])
        self.assertFalse(plan["model_requests_allowed"])
        self.assertFalse(plan["provider_writes_allowed"])
        self.assertEqual(len(plan["candidates"]), 10)
        for item in plan["candidates"]:
            connection = item["webui_connection_reference"]
            self.assertFalse(connection["config"]["enable"])
            self.assertFalse(connection["forward_cookies"])
            self.assertEqual(connection["headers"], {})
            self.assertEqual(connection["key"], "")
            self.assertNotIn("oauth_client_secret", connection["info"])

    def test_google_scope_candidates_exclude_writes_and_directory(self):
        for item in prep.plan()["candidates"]:
            for scope in item["scope_candidates"]:
                self.assertTrue(scope.endswith((".readonly", ".freebusy", "userinfo.profile")))
                self.assertNotIn("directory", scope)
                self.assertNotIn("compose", scope)

    def test_unknown_suffix_collision_and_writes_are_excluded(self):
        catalog = {"tools": [{"name": name, "inputSchema": {"type": "object"}} for name in
                             ("read_doc", "overwrite_read_doc", "update_doc")]}
        result = prep.review_catalog(catalog, ["read_doc"])
        self.assertEqual([entry["name"] for entry in result["accepted"]], ["read_doc"])
        self.assertEqual(result["excluded"], ["overwrite_read_doc", "update_doc"])
        self.assertFalse(result["execution_authorized"])

    def test_missing_names_do_not_get_repaired(self):
        result = prep.review_catalog({"tools": [{"name": "docs.read_doc", "inputSchema": {"type": "object"}}]}, ["read_doc"])
        self.assertEqual(result["missing"], ["read_doc"])
        self.assertEqual(result["accepted"], [])

    def test_duplicate_names_and_conflicting_annotations_fail(self):
        tool = {"name": "read_doc", "inputSchema": {"type": "object"}}
        with self.assertRaises(ValueError):
            prep.review_catalog({"tools": [tool, tool]}, ["read_doc"])
        for annotation in ({"destructiveHint": True}, {"readOnlyHint": False}):
            with self.assertRaises(ValueError):
                prep.review_catalog({"tools": [{**tool, "annotations": annotation}]}, ["read_doc"])

    def test_schema_drift_changes_digest_and_descriptions_are_not_copied(self):
        first = {"name": "read_doc", "description": "untrusted synthetic content", "inputSchema": {"type": "object"}}
        second = {**first, "inputSchema": {"type": "object", "required": ["id"]}}
        a = prep.review_catalog({"tools": [first]}, ["read_doc"])
        b = prep.review_catalog({"tools": [second]}, ["read_doc"])
        self.assertNotEqual(a["accepted"][0]["schema_sha256"], b["accepted"][0]["schema_sha256"])
        self.assertNotIn("untrusted synthetic content", json.dumps(a))

    def test_invalid_catalog_schema_and_allowlist_are_rejected(self):
        for catalog in ([], {"tools": None}, {"tools": [{}]}, {"tools": [{"name": "read_doc", "inputSchema": []}]}):
            with self.assertRaises(ValueError):
                prep.review_catalog(catalog, ["read_doc"])
        for names in ([], ["read_doc", "read_doc"], [None]):
            with self.assertRaises(ValueError):
                prep.review_catalog({"tools": []}, names)

    def test_build_only_writes_workspace_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            prep.build(directory)
            files = list(Path(directory).iterdir())
            self.assertEqual([path.name for path in files], ["connection-candidates.json"])
            self.assertEqual(json.loads(files[0].read_text()), prep.plan())


if __name__ == "__main__":
    unittest.main()
