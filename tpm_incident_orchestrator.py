"""
TPM Incident Orchestrator Copilot

Executable prototype generated from TPM_Incident_Orchestrator_Placeholder.md.

The agent supports a Technical Program Manager during and after a production
incident. It coordinates ownership, records decisions, translates approved
technical updates into business terms, assesses delivery risk, creates
stakeholder updates, and tracks follow-up actions.

MCP integrations are placeholders. They do not make network calls or execute
production changes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import argparse
import json
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class IncidentStatus(str, Enum):
    DECLARED = "DECLARED"
    INVESTIGATING = "INVESTIGATING"
    MITIGATING = "MITIGATING"
    MONITORING = "MONITORING"
    RESOLVED = "RESOLVED"


class WorkStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"


@dataclass
class TimelineEvent:
    timestamp: str
    category: str
    summary: str
    owner: Optional[str] = None


@dataclass
class Investigation:
    name: str
    owner: str
    status: WorkStatus = WorkStatus.OPEN
    latest_update: str = ""
    blocker: Optional[str] = None


@dataclass
class Decision:
    timestamp: str
    decision: str
    owner: str
    rationale: str
    approval: str


@dataclass
class ActionItem:
    action_id: str
    description: str
    owner: str
    due_date: str
    priority: str
    status: WorkStatus = WorkStatus.OPEN


@dataclass
class DeliveryRisk:
    commitment: str
    level: str
    reason: str
    next_step: str


@dataclass
class Incident:
    incident_id: str
    title: str
    severity: str
    service: str
    customer_impact: str
    business_impact: str
    status: IncidentStatus = IncidentStatus.DECLARED
    resolution: Optional[str] = None
    timeline: List[TimelineEvent] = field(default_factory=list)
    investigations: List[Investigation] = field(default_factory=list)
    decisions: List[Decision] = field(default_factory=list)
    actions: List[ActionItem] = field(default_factory=list)
    delivery_risks: List[DeliveryRisk] = field(default_factory=list)


class MCPPlugin(ABC):
    """Common placeholder contract for a future MCP server integration."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> List[str]:
        raise NotImplementedError

    def health(self) -> Dict[str, Any]:
        return {
            "plugin": self.name,
            "connected": False,
            "mode": "PLACEHOLDER",
            "capabilities": self.capabilities(),
        }

    @abstractmethod
    def get_context(self, incident: Incident) -> Dict[str, Any]:
        raise NotImplementedError

    def create_or_update(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "plugin": self.name,
            "executed": False,
            "mode": "PLACEHOLDER",
            "message": "Write operation requires a configured MCP server and approval.",
            "record": record,
        }


class PlaceholderPlugin(MCPPlugin):
    def __init__(self, name: str, plugin_capabilities: List[str]):
        self._name = name
        self._capabilities = plugin_capabilities

    @property
    def name(self) -> str:
        return self._name

    def capabilities(self) -> List[str]:
        return self._capabilities

    def get_context(self, incident: Incident) -> Dict[str, Any]:
        return {
            "plugin": self.name,
            "connected": False,
            "synthetic_data": False,
            "status": "NO_LIVE_CONTEXT",
            "incident_id": incident.incident_id,
            "message": "Configure this MCP plugin to retrieve live context.",
        }


def default_plugins() -> List[MCPPlugin]:
    return [
        PlaceholderPlugin("jira-mcp", ["releases", "milestones", "dependencies", "delivery-risk"]),
        PlaceholderPlugin("servicenow-mcp", ["incidents", "changes", "problems"]),
        PlaceholderPlugin("confluence-mcp", ["runbooks", "ownership", "past-incidents"]),
        PlaceholderPlugin("pagerduty-mcp", ["on-call", "escalations"]),
        PlaceholderPlugin("teams-mcp", ["communications", "decisions", "action-items"]),
        PlaceholderPlugin("datadog-mcp", ["business-dashboards", "service-health"]),
        PlaceholderPlugin("splunk-mcp", ["technical-summaries", "incident-context"]),
        PlaceholderPlugin("github-deployment-mcp", ["deployments", "release-correlation"]),
    ]


class BusinessTranslator:
    """Translates confirmed technical facts without diagnosing root cause."""

    RULES = {
        "orders not processing": "Customers cannot successfully place orders.",
        "service unresponsive": "The customer order workflow is temporarily unavailable.",
        "restart completed": "The recovery action has been completed.",
        "orders processing normally": "Customers can successfully place orders again.",
        "monitoring": "Teams are validating that the customer experience remains stable.",
    }

    def translate(self, technical_update: str) -> str:
        normalized = technical_update.lower()
        matches = [business for phrase, business in self.RULES.items() if phrase in normalized]
        if matches:
            return " ".join(dict.fromkeys(matches))
        return "Engineering is investigating. Customer and business impact remain under assessment."


class TPMIncidentOrchestrator:
    """Coordinates incident-management work without performing technical recovery."""

    def __init__(self, plugins: Optional[List[MCPPlugin]] = None):
        self.plugins = plugins or default_plugins()
        self.translator = BusinessTranslator()

    def _event(self, incident: Incident, category: str, summary: str, owner: Optional[str] = None) -> None:
        incident.timeline.append(TimelineEvent(utc_now(), category, summary, owner))

    def activate(self, incident: Incident) -> Dict[str, Any]:
        incident.status = IncidentStatus.INVESTIGATING
        self._event(incident, "ACTIVATION", f"{incident.severity} incident activated", "TPM")
        return {
            "incident_id": incident.incident_id,
            "status": incident.status.value,
            "coordination_checklist": [
                "Confirm incident commander and technical decision owner",
                "Engage service owner, SRE, support, and business representative",
                "Start timeline, decision log, and action tracker",
                "Confirm customer and business impact",
                "Set stakeholder-update cadence",
            ],
        }

    def plugin_health(self) -> List[Dict[str, Any]]:
        return [plugin.health() for plugin in self.plugins]

    def collect_context(self, incident: Incident) -> List[Dict[str, Any]]:
        results = [plugin.get_context(incident) for plugin in self.plugins]
        self._event(incident, "CONTEXT", "Requested context from configured MCP plugins", "Agent")
        return results

    def assign_investigation(self, incident: Incident, name: str, owner: str) -> Investigation:
        item = Investigation(name=name, owner=owner, status=WorkStatus.IN_PROGRESS)
        incident.investigations.append(item)
        self._event(incident, "OWNERSHIP", f"Assigned investigation: {name}", owner)
        return item

    def update_investigation(
        self, incident: Incident, name: str, update: str,
        status: WorkStatus, blocker: Optional[str] = None
    ) -> None:
        item = next((x for x in incident.investigations if x.name == name), None)
        if item is None:
            raise ValueError(f"Investigation not found: {name}")
        item.latest_update = update
        item.status = status
        item.blocker = blocker
        self._event(incident, "INVESTIGATION", f"{name}: {update}", item.owner)

    def record_decision(
        self, incident: Incident, decision: str, owner: str,
        rationale: str, approval: str
    ) -> Decision:
        item = Decision(utc_now(), decision, owner, rationale, approval)
        incident.decisions.append(item)
        self._event(incident, "DECISION", decision, owner)
        return item

    def add_delivery_risk(
        self, incident: Incident, commitment: str, level: str,
        reason: str, next_step: str
    ) -> DeliveryRisk:
        risk = DeliveryRisk(commitment, level, reason, next_step)
        incident.delivery_risks.append(risk)
        self._event(incident, "DELIVERY_RISK", f"{commitment}: {level}", "TPM")
        return risk

    def stakeholder_update(self, incident: Incident, technical_update: str, next_update: str) -> str:
        translated = self.translator.translate(technical_update)
        return (
            f"INCIDENT UPDATE\n\n"
            f"Incident: {incident.title}\n"
            f"Severity: {incident.severity}\n"
            f"Status: {incident.status.value}\n\n"
            f"Current situation: {translated}\n"
            f"Customer impact: {incident.customer_impact}\n"
            f"Business impact: {incident.business_impact}\n"
            f"Technical response: Engineering owns diagnosis and recovery decisions.\n"
            f"TPM coordination: Owners, decisions, risks, communications, and delivery impacts are tracked.\n"
            f"Next update: {next_update}"
        )

    def start_monitoring(self, incident: Incident, confirmed_update: str) -> None:
        incident.status = IncidentStatus.MONITORING
        self._event(incident, "MONITORING", confirmed_update, "Engineering Lead")

    def resolve(self, incident: Incident, resolution: str, technical_owner: str) -> None:
        incident.status = IncidentStatus.RESOLVED
        incident.resolution = resolution
        self._event(incident, "RESOLUTION", resolution, technical_owner)

    def add_action(
        self, incident: Incident, description: str, owner: str,
        due_date: str, priority: str
    ) -> ActionItem:
        action = ActionItem(str(uuid.uuid4()), description, owner, due_date, priority)
        incident.actions.append(action)
        self._event(incident, "FOLLOW_UP", description, owner)
        return action

    def report(self, incident: Incident) -> Dict[str, Any]:
        return {
            "incident": {
                "incident_id": incident.incident_id,
                "title": incident.title,
                "severity": incident.severity,
                "service": incident.service,
                "status": incident.status.value,
                "customer_impact": incident.customer_impact,
                "business_impact": incident.business_impact,
                "resolution": incident.resolution,
            },
            "investigations": [
                {**asdict(x), "status": x.status.value} for x in incident.investigations
            ],
            "decisions": [asdict(x) for x in incident.decisions],
            "delivery_risks": [asdict(x) for x in incident.delivery_risks],
            "follow_up_actions": [
                {**asdict(x), "status": x.status.value} for x in incident.actions
            ],
            "timeline": [asdict(x) for x in incident.timeline],
        }


def run_demo() -> Dict[str, Any]:
    """Demonstrates the order-placement incident using only supplied facts."""
    agent = TPMIncidentOrchestrator()
    incident = Incident(
        incident_id="INC-DEMO-001",
        title="Orders Not Getting Placed",
        severity="SEV-1",
        service="Order Processing Service",
        customer_impact="Customers are unable to place orders.",
        business_impact="Revenue-generating transactions are disrupted.",
    )

    activation = agent.activate(incident)
    context = agent.collect_context(incident)

    agent.assign_investigation(incident, "Coordinate Order Service assessment", "Order Service Lead")
    agent.assign_investigation(incident, "Confirm platform and dependency status", "SRE Lead")
    agent.assign_investigation(incident, "Assess customer impact", "Customer Support Lead")

    before_update = agent.stakeholder_update(
        incident, "Orders not processing", "15 minutes"
    )

    agent.record_decision(
        incident,
        "Restart the Order Processing Service",
        "Authorized Engineering Lead",
        "Engineering selected a service restart as the recovery action.",
        "Approved by authorized technical owner",
    )

    agent.start_monitoring(
        incident,
        "Restart completed; orders processing normally; stability validation in progress.",
    )

    after_update = agent.stakeholder_update(
        incident,
        "Restart completed. Orders processing normally. Monitoring.",
        "After stability validation",
    )

    agent.resolve(
        incident,
        "Order placement recovered after the Order Processing Service was restarted.",
        "Authorized Engineering Lead",
    )

    agent.add_action(incident, "Determine why the service became unresponsive", "Order Service Lead", "TBD", "P1")
    agent.add_action(incident, "Review service health monitoring and alert coverage", "SRE Lead", "TBD", "P1")
    agent.add_action(incident, "Update the recovery runbook", "Service Owner", "TBD", "P2")
    agent.add_action(incident, "Facilitate post-incident review and track closure", "TPM", "TBD", "P2")

    return {
        "notice": "MCP plugins are placeholders; no external systems were queried or changed.",
        "activation": activation,
        "plugin_health": agent.plugin_health(),
        "plugin_context": context,
        "stakeholder_update_before_recovery": before_update,
        "stakeholder_update_after_recovery": after_update,
        "final_report": agent.report(incident),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="TPM Incident Orchestrator Copilot prototype")
    parser.add_argument("--demo", action="store_true", help="Run the order-placement incident demo")
    parser.add_argument("--output", default="incident_report.json", help="JSON output path")
    args = parser.parse_args()

    result = run_demo() if args.demo else {
        "message": "Use --demo to execute the sample incident.",
        "plugin_health": TPMIncidentOrchestrator().plugin_health(),
    }

    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nSaved report to: {output}")


if __name__ == "__main__":
    from pathlib import Path
    main()
