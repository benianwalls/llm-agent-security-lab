# LLM Agent Security Evaluation Lab

A sandboxed security lab for evaluating common risks in LLM-powered agents.

This project uses fake tools, fake customer data, fake email, and deterministic model behavior to demonstrate how LLM agents can fail under prompt injection and excessive agency conditions.

No real systems are attacked.

## What This Tests

- Prompt injection
- Mock data exfiltration
- Excessive agency
- Tool misuse
- Improper output handling
- System prompt leakage

## Why This Exists

LLM agents are different from normal chatbots because they can use tools.

If an agent can read untrusted content and then call tools, malicious text can influence the agent into taking actions the user did not intend.

This lab demonstrates that problem safely.

## Architecture

```text
User prompt
   ↓
Fake LLM
   ↓
Agent loop
   ↓
Security policy
   ↓
Fake tools
   ↓
Output guard
   ↓
Structured logs

Modes:

agentsec-demo --mode vulnerable "Summarize the vendor note." --json

agentsec-demo --mode defended "Summarize the vendor note." --json