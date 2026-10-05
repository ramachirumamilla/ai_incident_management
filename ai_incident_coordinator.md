# AI Incident Triage & Response Coordinator

## Purpose

The AI Incident Triage & Response Coordinator assists TPMs, SRE teams, and Incident Commanders by:

- Classifying incidents
- Identifying impacted services
- Recommending ownership
- Suggesting mitigation actions
- Creating executive summaries
- Accelerating incident triage

---

## Inputs

The agent accepts:

- Incident ID
- Severity
- Service Name
- Customer Impact
- Business Impact
- Symptoms
- Recent Changes

---

## Outputs

The agent generates:

- Incident Classification
- Executive Summary
- Recommended Owners
- Suggested Actions
- Confidence Score

---

## Supported Incident Types

### Capacity Management

Examples:

- Storage Full
- Disk Space Exhausted

### Performance Degradation

Examples:

- High Latency
- Slow API Responses

### Database Incidents

Examples:

- Database Unavailable
- Connection Pool Exhausted

### Network Incidents

Examples:

- Connectivity Issues
- Packet Loss

### Release Incidents

Examples:

- Failed Deployment
- Application Outage After Release

---

## Human-in-the-Loop Controls

The agent:

✅ Recommends actions

✅ Recommends ownership

✅ Generates summaries

The agent DOES NOT:

❌ Restart services

❌ Approve rollbacks

❌ Deploy code

❌ Close incidents

Human responders remain accountable.