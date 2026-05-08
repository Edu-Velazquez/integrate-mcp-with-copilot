from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"
OUT_DIR = Path("/Users/eduardo.velazquez/Downloads/Working_directory-2026/integrate-mcp-with-copilot/test/pruebas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

results = []


def add_result(name: str, ok: bool, detail: str) -> None:
    status = "PASS" if ok else "FAIL"
    results.append((status, name, detail))


# API tests
try:
    resp = requests.get(f"{BASE_URL}/activities", timeout=10)
    ok = resp.status_code == 200 and isinstance(resp.json(), dict) and len(resp.json()) > 0
    add_result("GET /activities", ok, f"status={resp.status_code}, count={len(resp.json()) if resp.status_code == 200 else 'n/a'}")
except Exception as exc:
    add_result("GET /activities", False, f"exception={exc}")

activity_name = "Chess Club"
email = f"qa-{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
activity_path = quote(activity_name, safe="")

try:
    resp = requests.post(
        f"{BASE_URL}/activities/{activity_path}/signup",
        params={"email": email},
        timeout=10,
    )
    ok = resp.status_code == 200
    add_result("POST signup", ok, f"status={resp.status_code}, email={email}")
except Exception as exc:
    add_result("POST signup", False, f"exception={exc}")

try:
    resp = requests.delete(
        f"{BASE_URL}/activities/{activity_path}/unregister",
        params={"email": email},
        timeout=10,
    )
    ok = resp.status_code == 200
    add_result("DELETE unregister", ok, f"status={resp.status_code}, email={email}")
except Exception as exc:
    add_result("DELETE unregister", False, f"exception={exc}")

# Browser screenshots
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        page.goto(f"{BASE_URL}/", wait_until="networkidle", timeout=20000)
        page.screenshot(path=str(OUT_DIR / "01_home.png"), full_page=True)
        add_result("Screenshot home", True, "saved test/pruebas/01_home.png")

        page.goto(f"{BASE_URL}/activities", wait_until="networkidle", timeout=20000)
        page.screenshot(path=str(OUT_DIR / "02_activities.png"), full_page=True)
        add_result("Screenshot activities", True, "saved test/pruebas/02_activities.png")

        page.goto(f"{BASE_URL}/docs", wait_until="networkidle", timeout=20000)
        page.screenshot(path=str(OUT_DIR / "03_docs.png"), full_page=True)
        add_result("Screenshot docs", True, "saved test/pruebas/03_docs.png")

        browser.close()
except Exception as exc:
    add_result("Screenshots", False, f"exception={exc}")

report_path = OUT_DIR / "reporte_pruebas.txt"
with report_path.open("w", encoding="utf-8") as f:
    f.write("Reporte de pruebas y capturas\n")
    f.write(f"Fecha: {datetime.now().isoformat()}\n")
    f.write(f"Base URL: {BASE_URL}\n\n")
    for status, name, detail in results:
        f.write(f"[{status}] {name}: {detail}\n")

all_ok = all(status == "PASS" for status, _, _ in results)
print(f"Reporte generado: {report_path}")
for row in results:
    print(row)

raise SystemExit(0 if all_ok else 1)
