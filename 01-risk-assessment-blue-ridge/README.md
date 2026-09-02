# Information Security Risk Assessment — Blue Ridge Family Health Clinic

**Framework:** NIST SP 800-30 Rev. 1 (Guide for Conducting Risk Assessments)
**Type:** Portfolio project — fictional scenario
**Deliverables:** [Risk Assessment Report](./Blue_Ridge_Risk_Assessment_Report.docx) · [Risk Register](./Blue_Ridge_Risk_Register.xlsx)

## Scenario

Blue Ridge Family Health Clinic is a fictional 45-employee outpatient primary care practice used as a realistic scenario for this exercise. The Clinic operates a cloud-hosted EHR system, a practice management platform, networked clinical devices, and a small remote billing team, and is subject to the HIPAA Security Rule.

## What this project demonstrates

- Applying a **qualitative risk assessment methodology** (5x5 Likelihood × Impact matrix) per NIST SP 800-30
- Identifying threats and vulnerabilities across technical, administrative, physical, and third-party risk categories
- Building a **living risk register** with automated scoring, risk-level classification, and a heat map
- Writing a **formal risk assessment report** with executive summary, methodology, findings, and prioritized recommendations

## Key findings

13 risks were identified and scored. 4 were rated Critical or High:

| ID | Risk | Score | Level |
|----|------|-------|-------|
| R-01 | Phishing compromises staff O365 credentials | 16 | Critical |
| R-02 | Ransomware via compromised endpoint reaching EHR systems | 15 | Critical |
| R-06 | EHR remote access lacks multi-factor authentication | 15 | Critical |
| R-04 | Third-party billing vendor data breach exposing PHI | 10 | High |
| R-13 | Backup failure / untested disaster recovery | 10 | High |

**Top recommendations:** enforce MFA on all remote access, deploy EDR and automated patching, formalize and test an incident response plan.

## Files

- `Blue_Ridge_Risk_Assessment_Report.docx` — full report (executive summary, methodology, system characterization, threat/vulnerability identification, recommendations, conclusion)
- `Blue_Ridge_Risk_Register.xlsx` — scored risk register with conditional-formatting heat map and an auto-calculating 5x5 matrix tab

## Notes

This is a self-directed learning project built to practice GRC methodology, not a real client engagement. AI tools were used to help draft and structure the deliverables; the framework, scoring methodology, and content were reviewed and understood by me.
