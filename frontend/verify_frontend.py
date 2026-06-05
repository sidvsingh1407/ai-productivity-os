from playwright.sync_api import sync_playwright
import time

def verify():
    with sync_playwright() as p:
        # The backend isn't properly running, but since the workflow details page will fetch by id
        # it might fail unless we intercept the request and return mock data.
        # Let's write a script that mocks the API response to demonstrate the frontend change.

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        mock_response = {
            "id": "123",
            "org_id": "temp-org",
            "user_id": "temp-user",
            "status": "completed",
            "input_config": {"mode": "diagnostic"},
            "created_at": "2023-10-27T10:00:00Z",
            "blueprints": [],
            "intelligence": {
                "executive_summary": {
                    "most_critical_bottleneck": "Manual Approval Dependencies",
                    "primary_root_cause": "Decision authority concentrated in a small number of stakeholders.",
                    "highest_priority_intervention": "Introduce parallel approval paths.",
                    "workflow_risk_level": "High",
                    "workflow_maturity": "Reactive"
                },
                "workflow_maturity": "Reactive",
                "workflow_risk_level": "High",
                "most_critical_bottleneck": "Manual Approval Dependencies",
                "primary_root_cause": "Decision authority concentrated in a small number of stakeholders.",
                "highest_priority_intervention": "Introduce parallel approval paths.",
                "bottlenecks": [
                    {
                        "title": "Manual Approval Dependencies",
                        "severity": "Critical",
                        "impacted_area": "Decision Making",
                        "rationale": "Workflow execution is paused waiting on human authorization, leading to execution delays.",
                        "root_cause": {
                            "root_cause": "Decision authority concentrated in a small number of stakeholders.",
                            "evidence": "Multiple workflow stages require sequential approvals or manual sign-off.",
                            "impact": "Slower workflow throughput and delayed execution."
                        }
                    }
                ],
                "risks": [],
                "recommendations": []
            }
        }

        page.route("**/api/workflows/123", lambda route: route.fulfill(json=mock_response))
        page.route("**/api/audits/?limit=100", lambda route: route.fulfill(json=[]))

        page.goto("http://localhost:5173/workflows/123")
        time.sleep(2)

        page.screenshot(path="/home/jules/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    verify()
