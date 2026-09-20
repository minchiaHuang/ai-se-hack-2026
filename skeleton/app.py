"""Demo shell. Standard library only: python3 skeleton/app.py

One page per scenario: run the pipeline, show what it suggests, what it
withholds, what it cannot answer, and what it refuses outright. A human
confirms every row before anything counts.
"""
import html
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Run by path (python3 skeleton/app.py) and sys.path holds skeleton/, not the
# repo root, so the package imports below fail. Put the root back.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from skeleton.core.model import CANNED, StubModel
from skeleton.core.pipeline import run
from skeleton.core.schema import AggregationError
from skeleton.directions import d2_triage, d3_evidence, d6_outcomes

DIRECTIONS = {"d2": d2_triage, "d3": d3_evidence, "d6": d6_outcomes}
SCENARIOS = json.loads(
    (Path(__file__).resolve().parent / "demo_data" / "payloads.json").read_text(encoding="utf-8")
)


def direction_for(scenario_key):
    return DIRECTIONS[scenario_key.split("_")[0]]


def model_for(scenario_key):
    """Canned output lives next to the scenario, so a scenario can show a
    different model response for the same direction."""
    direction = direction_for(scenario_key)
    path = CANNED / f"{scenario_key}.json"
    if not path.exists():
        path = CANNED / f"{direction.KEY}.json"
    canned = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    return StubModel({direction.KEY: canned})


def render_index():
    rows = "".join(
        f'<li><a href="/run?s={key}">{html.escape(payload["label"])}</a>'
        f' <span class="k">{html.escape(direction_for(key).NAME)}</span></li>'
        for key, payload in SCENARIOS.items()
    )
    return f"""<h1>Direction skeleton</h1>
<p class="note">Stub model, no network. Every scenario below runs offline.</p>
<ul class="scenarios">{rows}</ul>"""


def render_result(scenario_key):
    direction = direction_for(scenario_key)
    payload = SCENARIOS[scenario_key]
    back = '<p><a href="/">&larr; back</a></p>'
    head = f'<h1>{html.escape(direction.NAME)}</h1><p class="note">{html.escape(payload["label"])}</p>'

    try:
        result = run(direction, payload, model_for(scenario_key))
    except AggregationError as refused:
        return (head + '<div class="refused"><strong>Refused</strong><p>'
                + html.escape(str(refused)) + "</p></div>" + back)

    parts = [head]
    if result.suggestions:
        parts.append("<h2>Suggested &mdash; confirm each</h2><table>")
        for s in result.suggestions:
            sources = "; ".join(f"{x.label}: {x.locator}" for x in s.sources)
            parts.append(
                f"<tr><td><input type=checkbox></td><td><b>{html.escape(s.field)}</b></td>"
                f"<td>{html.escape(str(s.displayed_value()))}</td>"
                f"<td>{s.confidence:.2f}</td>"
                f"<td class=src>{html.escape(s.reason)}<br><i>{html.escape(sources)}</i></td></tr>"
            )
        parts.append("</table>")
    if result.needs_human:
        parts.append("<h2>Not confident enough &mdash; a person decides</h2><ul>")
        for s in result.needs_human:
            parts.append(
                f"<li><b>{html.escape(s.field)}</b>: value withheld "
                f"(confidence {s.confidence:.2f}) &mdash; {html.escape(s.reason)}</li>"
            )
        parts.append("</ul>")
    if result.gaps:
        parts.append("<h2>No evidence &mdash; left blank on purpose</h2><ul>"
                     + "".join(f"<li>{html.escape(g)}</li>" for g in result.gaps) + "</ul>")
    value = "not supplied" if result.metric_value is None else result.metric_value
    parts.append(f'<div class="metric">{html.escape(result.metric_name)}: <b>{html.escape(str(value))}</b></div>')
    parts.append(back)
    return "".join(parts)


PAGE = """<!doctype html><meta charset=utf-8><title>Direction skeleton</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}}
h1{{font-size:1.3rem}} h2{{font-size:1rem;margin-top:1.5rem}}
.note{{color:#666}} .k{{color:#888;font-size:.85em}}
table{{border-collapse:collapse;width:100%}} td{{border-top:1px solid #ddd;padding:.4rem;vertical-align:top}}
.src{{color:#555;font-size:.85em}}
.metric{{margin-top:1.5rem;padding:.6rem;background:#f4f4f4}}
.refused{{margin-top:1rem;padding:.8rem;border-left:4px solid #b00;background:#fff4f4}}
.scenarios li{{margin:.3rem 0}}
</style>{body}"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        scenario = parse_qs(parsed.query).get("s", [None])[0]
        if parsed.path == "/run" and scenario in SCENARIOS:
            body = render_result(scenario)
        else:
            body = render_index()
        encoded = PAGE.format(body=body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *args):
        pass


def check():
    """Offline smoke check: render every scenario, print nothing on success."""
    for key in SCENARIOS:
        render_result(key)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        print("http://127.0.0.1:8000")
        HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
