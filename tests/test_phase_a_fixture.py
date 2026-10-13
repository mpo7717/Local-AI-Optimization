import asyncio
import importlib.util
import json
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location("fixture", Path(__file__).parents[1] / "tools" / "phase_a_fixture.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FixtureTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tool = module.Tools()
        self.context = {"__model__": {"id": "administrative-assistant"},
                        "__metadata__": {"model_id": "administrative-assistant", "message_id": "synthetic-message"},
                        "__user__": {"id": "synthetic-user"}}

    async def read(self, **kwargs):
        return json.loads(await self.tool.read_project(**kwargs, **self.context))

    async def test_multistep_receipts_and_validated_data(self):
        found = json.loads(await self.tool.find_project("Alder", **self.context))
        read = await self.read(project_id=found["data"]["project_id"])
        self.assertEqual(read["data"], {"project_id": "ALDER-001", "owner": "Alex", "due_day": "Friday", "status": "draft"})
        self.assertTrue(read["validated"])
        self.assertEqual(read["calls_used"], 2)
        self.assertNotEqual(found["receipt"], read["receipt"])

    async def test_wrong_profile_denied_before_record_access(self):
        self.context["__model__"]["id"] = "synthetic-other-profile"
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "PROFILE_DENIED")
        self.assertFalse(self.tool.states)

    async def test_spoofed_metadata_cannot_override_profile(self):
        self.context["__metadata__"]["model_id"] = "synthetic-other-profile"
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "PROFILE_DENIED")

    async def test_missing_user_or_workflow_fails_closed(self):
        self.context["__user__"] = {}
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "USER_DENIED")
        self.context["__user__"] = {"id": "synthetic-user"}
        self.context["__metadata__"].pop("message_id")
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "CONTEXT_DENIED")

    async def test_malformed_arguments_not_coerced(self):
        for value in [None, [], {}, 123, True, "../private", "UNKNOWN"]:
            self.setUp()
            result = await self.read(project_id=value)
            self.assertEqual(result["error"], "INVALID_ARGUMENT")
            self.assertNotIn("data", result)

    async def test_fault_scenario_is_allowlisted(self):
        self.assertEqual((await self.read(project_id="ALDER-001", scenario="arbitrary"))["error"], "INVALID_ARGUMENT")

    async def test_permission_denied_has_no_success_payload(self):
        result = await self.read(project_id="ALDER-001", scenario="permission_denied")
        self.assertFalse(result["ok"])
        self.assertFalse(result["retryable"])
        self.assertNotIn("data", result)

    async def test_bad_provider_result_never_reaches_model_as_success(self):
        result = await self.read(project_id="ALDER-001", scenario="malformed_result")
        self.assertEqual(result["error"], "INVALID_RESULT")
        self.assertNotIn("data", result)

    async def test_timeout_once_then_verified_retry(self):
        first = await self.read(project_id="ALDER-001", scenario="timeout_once")
        second = await self.read(project_id="ALDER-001", scenario="timeout_once")
        self.assertEqual(first["error"], "TIMEOUT")
        self.assertTrue(first["retryable"])
        self.assertTrue(second["ok"])
        self.assertTrue(second["validated"])

    async def test_two_timeouts_latch_stop_across_subsequent_calls(self):
        await self.read(project_id="ALDER-001", scenario="persistent_timeout")
        second = await self.read(project_id="ALDER-001", scenario="persistent_timeout")
        self.assertTrue(second["stop"])
        self.assertFalse(second["retryable"])
        third = await self.read(project_id="BIRCH-002")
        self.assertEqual(third["error"], "BUDGET_STOP")

    async def test_eight_execution_budget_cannot_be_bypassed_with_alternating_calls(self):
        for i in range(8):
            self.assertTrue((await self.read(project_id=["ALDER-001", "BIRCH-002"][i % 2]))["ok"])
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "BUDGET_STOP")

    async def test_no_progress_stop(self):
        await self.read(project_id="ALDER-001")
        await self.read(project_id="ALDER-001")
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "NO_PROGRESS_STOP")

    async def test_wall_time_and_capacity_do_not_reset_active_budgets(self):
        await self.read(project_id="ALDER-001")
        state = next(iter(self.tool.states.values()))
        state["started"] -= 121
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "BUDGET_STOP")
        self.setUp()
        for i in range(64):
            self.context["__metadata__"]["message_id"] = f"synthetic-{i}"
            await self.read(project_id="ALDER-001")
        self.context["__metadata__"]["message_id"] = "synthetic-overflow"
        self.assertEqual((await self.read(project_id="ALDER-001"))["error"], "CAPACITY_STOP")

    async def test_untrusted_note_separate_from_validated_record(self):
        result = await self.read(project_id="ALDER-001", scenario="prompt_injection")
        self.assertTrue(result["validated"])
        self.assertIn("untrusted_note", result)
        self.assertNotIn("untrusted_note", result["data"])

    async def test_old_context_does_not_receive_a_fresh_budget(self):
        await self.read(project_id="ALDER-001")
        next(iter(self.tool.states.values()))["started"] -= 301
        result = await self.read(project_id="ALDER-001")
        self.assertEqual(result["error"], "BUDGET_STOP")


if __name__ == "__main__":
    unittest.main()
