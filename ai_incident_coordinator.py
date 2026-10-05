"""
AI Incident Triage & Response Coordinator

Generic incident analysis engine designed to support:
- TPMs
- SRE Engineers
- Incident Commanders

This version is intentionally generic and works with
different incident types such as:

- Storage
- Database
- API
- Network
- Latency
- Capacity
- Deployment failures

Input:
    incident.json

Output:
    incident_report.json
"""

import json
import sys
from pathlib import Path


class AIIncidentCoordinator:

    def classify_incident(self, incident):

        text = (
            incident.get("title", "") + " "
            + " ".join(incident.get("symptoms", []))
        ).lower()

        if "storage" in text or "capacity" in text:
            return "Capacity Management"

        if "latency" in text:
            return "Performance Degradation"

        if "database" in text:
            return "Database Incident"

        if "network" in text:
            return "Network Incident"

        if "deployment" in text:
            return "Release Incident"

        return "General Service Incident"

    def recommend_owners(self, incident_type):

        mapping = {
            "Capacity Management": [
                "Storage Operations",
                "Infrastructure Engineering"
            ],
            "Performance Degradation": [
                "Application Team",
                "SRE Team"
            ],
            "Database Incident": [
                "Database Team",
                "Application Team"
            ],
            "Network Incident": [
                "Network Engineering",
                "SRE Team"
            ],
            "Release Incident": [
                "Release Engineering",
                "Application Team"
            ]
        }

        return mapping.get(
            incident_type,
            ["Application Team"]
        )

    def recommend_actions(self, incident_type):

        mapping = {

            "Capacity Management": [
                "Review utilization trends",
                "Add storage capacity",
                "Validate application health"
            ],

            "Performance Degradation": [
                "Review latency metrics",
                "Review recent deployments",
                "Validate dependencies"
            ],

            "Database Incident": [
                "Review database health",
                "Review connection pool",
                "Validate storage utilization"
            ],

            "Network Incident": [
                "Check connectivity",
                "Review routing changes",
                "Validate network health"
            ],

            "Release Incident": [
                "Review recent deployment",
                "Evaluate rollback requirement",
                "Validate service health"
            ]
        }

        return mapping.get(
            incident_type,
            ["Investigate service health"]
        )

    def generate_summary(self, incident):

        service = incident.get("service", "Unknown Service")

        return (
            f"The incident impacts {service}. "
            f"Engineering teams are currently investigating "
            f"the issue and appropriate mitigation actions "
            f"have been recommended."
        )

    def analyze(self, incident):

        incident_type = self.classify_incident(incident)

        return {
            "incident_id": incident.get("incident_id"),
            "severity": incident.get("severity"),
            "incident_type": incident_type,
            "executive_summary": self.generate_summary(incident),
            "recommended_owners":
                self.recommend_owners(incident_type),
            "recommended_actions":
                self.recommend_actions(incident_type),
            "confidence_score": 90
        }


def main():

    if len(sys.argv) < 2:
        print(
            "Usage: python ai_incident_coordinator.py incident.json"
        )
        return

    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        incident = json.load(f)

    agent = AIIncidentCoordinator()

    report = agent.analyze(incident)

    output = Path("incident_report.json")

    output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
