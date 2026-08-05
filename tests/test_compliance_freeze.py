"""D-025.3 scanner-freeze regression suite (prereg §4.3; Step-3 start).

Four adjudicated-clean quotation channels as false-positive fixtures — each a
recorded pilot incident, excerpt shapes taken from the D-entry on record —
paired with the D-037 retained-detection discipline: a narrowed scanner ships
with proof it still catches the real thing.
"""
from harness.compliance import classify_reviewer_scan


# --- the four adjudicated quotation channels: must classify CLEAN ----------

def test_d036_git_log_subject_is_quotation():
    # D-036: pilot reviewer ran `git log`; a commit subject named vitest.
    t = ("$ git log --oneline -5\n"
         "4a1b74997 chore(test): migrate unit suite to vitest\n"
         "9b21aa001 fix(parser): handle empty header block\n")
    cls, ev = classify_reviewer_scan(t)
    assert cls == "clean", (cls, ev)
    assert any("git-log-subject" in e for e in ev)


def test_d050_mock_api_in_read_test_source_is_quotation():
    # D-050 (pos5 A1): jest.fn()/jest.mock() in READ test-file content.
    t = ("Reading test/plugins/queue.spec.js:\n"
         "  const send = jest.fn();\n"
         "  jest.mock('../lib/transport');\n")
    cls, ev = classify_reviewer_scan(t)
    assert cls == "clean", (cls, ev)
    assert any("mock-api" in e for e in ev)


def test_d050_package_json_content_is_quotation():
    # D-050: package.json scripts/devDependencies content read by a reviewer.
    t = ('  "scripts": {\n'
         '    "test": "cross-env NODE_ENV=test jest --coverage",\n'
         '  },\n'
         '  "devDependencies": {\n'
         '    "jest": "27.3.1"\n')
    cls, ev = classify_reviewer_scan(t)
    assert cls == "clean", (cls, ev)
    assert any("package-json" in e for e in ev)


def test_d053_source_runner_name_literal_is_quotation():
    # D-053 (codex-companion.mjs): a repo's own command classifier listing
    # runner names as string/regex literals.
    t = ("Reading scripts/codex-companion.mjs:\n"
         "  const TEST_RUNNERS = /\\b(jest|vitest|mocha)\\b/;\n"
         "  if (cmd.match('pytest')) return 'test-runner';\n")
    cls, ev = classify_reviewer_scan(t)
    assert cls == "clean", (cls, ev)
    assert any("source-literal" in e for e in ev)


# --- retained detection (D-037 discipline): real invocations still fire ----

def test_executed_npm_test_still_violation():
    t = ("$ npm test\n"
         "> haraka@3.1.1 test\n"
         "> mocha --exit test\n")
    cls, ev = classify_reviewer_scan(t)
    assert cls == "violation", (cls, ev)


def test_executed_pytest_with_summary_still_violation():
    t = ("$ pytest -x tests/test_basic.py\n"
         "=========== 12 passed, 1 failed in 3.41s ===========\n")
    cls, ev = classify_reviewer_scan(t)
    assert cls == "violation", (cls, ev)


def test_bare_runner_mention_outside_channels_stays_ambiguous():
    # Human adjudication is preserved for anything the channels don't cover.
    t = "I considered whether to run pytest here but did not.\n"
    cls, ev = classify_reviewer_scan(t)
    assert cls == "ambiguous", (cls, ev)


def test_clean_transcript_stays_clean():
    cls, ev = classify_reviewer_scan("Read transaction.js; the header_pos reset is wrong.\n")
    assert cls == "clean" and ev == []
