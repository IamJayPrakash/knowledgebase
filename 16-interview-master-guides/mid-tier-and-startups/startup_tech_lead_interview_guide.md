# Startup Tech Lead / Staff SDE Interview Guide (Series A to Unicorn)

---

## 🚀 1. What Startups Look For
In high-growth startups (Series A-C), interviewers do not ask trivia. They evaluate:
1. **Speed vs Quality Tradeoffs**: When to build a quick monolithic MVP vs when to decouple into microservices.
2. **Cost & Cloud Economics**: Designing architectures that minimize AWS/GCP bills (e.g. S3 intelligent tiering, spot instances).
3. **Ownership & Zero-to-One Delivery**: Ability to debug obscure production crashes across the entire stack without documentation.
4. **Pragmatic Technology Choices**: Picking boring, reliable technology (PostgreSQL, Redis, Next.js) over unproven hype.

---

## 🎯 2. Archetypal Startup Architectural Scenarios
- **Scenario 1**: "Our AWS bill jumped by $15,000 this month due to RDS egress and DynamoDB read capacity. How do you audit and reduce costs in 48 hours?"
- **Scenario 2**: "We need to ingest 50,000 IoT events per second with an engineering team of 4 people. Design a low-maintenance pipeline." (Solution: Managed Cloud PubSub/Kinesis ➔ ClickHouse / Snowflake ➔ Grafana).
