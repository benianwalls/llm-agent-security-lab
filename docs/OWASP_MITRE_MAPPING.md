# OWASP GenAI and MITRE ATLAS Mapping

This lab evaluates a sandboxed LLM-style agent with fake tools and fake data.

No real systems are attacked. All email, calendar, and customer data are mock data.

## Mapping Table

| Case | Risk | OWASP GenAI Mapping | MITRE ATLAS Mapping | Defense |
|---|---|---|---|---|
| PI-001 | Indirect prompt injection from retrieved vendor note | LLM01 Prompt Injection, LLM06 Excessive Agency | AML.T0051.001 LLM Prompt Injection: Indirect | Treat retrieved content as untrusted data; block non-allowlisted tools |
| DE-001 | Mock private-data disclosure | LLM02 Sensitive Information Disclosure | Impact / Exfiltration-style behavior | Restrict private tools; redact sensitive fields |
| EA-001 | Agent takes action without user approval | LLM06 Excessive Agency | Agent/tool-abuse behavior | Human confirmation required for email and calendar actions |
| IO-001 | Raw unsafe HTML returned to downstream renderer | LLM05 Improper Output Handling | N/A | HTML escaping |
| SP-001 | System prompt leakage | LLM07 System Prompt Leakage, LLM01 Prompt Injection | AML.T0051.000 LLM Prompt Injection: Direct | Output guard; do not store real secrets in prompts |

## Key Lesson

The model is not the security boundary.

The application must enforce security with deterministic controls:

- tool allowlists
- least privilege
- confirmation gates
- output encoding
- sensitive-data redaction
- structured logging