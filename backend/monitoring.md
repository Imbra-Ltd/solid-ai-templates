# Backend — Monitoring
[ID: backend-monitoring]

## Key metrics
Every service MUST monitor at minimum:

| Metric | Why |
|--------|-----|
| CPU usage | Detect resource saturation and scaling needs |
| Memory usage | Detect leaks and container limit violations |
| Disk usage | Prevent storage exhaustion |
| Response time (p50, p95, p99) | Detect latency degradation |
| Error rate (4xx, 5xx) | Detect functional failures |
| Throughput (requests/sec) | Detect traffic spikes and capacity limits |

Add custom metrics for business-critical operations specific to the service
(e.g. orders processed, jobs queued, messages consumed).

## Thresholds and alerts
- Set thresholds based on historical data and expected usage — not arbitrary values
- MUST create alerts for all P1 and P2 scenarios before the service goes to production
- If an incident occurs without a corresponding alert, an alert MUST be created
  immediately after the incident is resolved to prevent recurrence
- Alerts MUST be actionable — every alert must have a clear response procedure

### Example thresholds
- CPU > 80% sustained for 5 minutes → alert
- Response time p95 > 3s for more than 100 requests in 5 minutes → alert
- Disk usage > 80% sustained for 30 minutes → alert
- Error rate > 1% sustained for 2 minutes → alert

## Dashboards
- Every service MUST have a service health dashboard
- Dashboard MUST show at minimum: error rate, response time, throughput,
  and resource usage
- Dashboards MUST be defined as code — no manually created dashboards in
  shared environments
- Non-technical dashboards (business KPIs, MAU) are encouraged alongside
  technical dashboards

## Status page
- Maintain a status page for user-facing services to communicate outages
  and planned maintenance
- The status page MUST be hosted outside the primary infrastructure — it
  must remain available during an infrastructure incident
- Update the status page manually during incidents — automation is not
  recommended as it can mask or misreport the true state
- Use the status page proactively to reduce duplicate incident reports from
  affected users

## Incident response
- P1/P2 incidents MUST have a post-mortem documented after resolution
- Post-mortem MUST include: timeline, root cause, impact, corrective actions
- Corrective actions MUST be tracked to completion — not just documented