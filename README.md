I build AI products end to end: the agent, the backend, the web and mobile apps, and the servers they run on. Open to new roles.

**Now:** [Quant AI](https://aiquant.io), an AI research assistant for markets, investing and quant trading. It runs on the web, on [iPhone, iPad and Mac](https://apps.apple.com/us/app/quant-ai-smart-agent/id6754956523), and on Android in closed testing. I have designed, built and run it on my own since April 2025.

What it took:

- **Agent**: a single LangChain/LangGraph agent that hands off between market capabilities (US stocks, A-shares, crypto, commodities) without breaking the prompt cache. Answers stream over Redis Streams and can be cancelled mid-run; state lives in Postgres checkpoints, with long-term memory per user and model fallback behind an LLM gateway.
- **Research**: the agent rates about 200 US stocks on seven dimensions. Each batch is scored against later excess returns, and the rating system counts as working only at t ≥ 2, corrected for overlapping holding periods. Batch jobs run on Temporal.
- **Backend**: Python, FastAPI, PostgreSQL, Redis, Supabase Auth, Stripe and RevenueCat billing, APNs and FCM push.
- **Web**: TypeScript, Nuxt 4 for the site and app, Vue 3 for the admin console; 16 languages, server-rendered for search.
- **iOS**: Swift and SwiftUI, one codebase for iPhone, iPad and Mac Catalyst, shipped through Xcode Cloud.
- **Android**: Kotlin, Jetpack Compose, Hilt, Navigation 3.
- **Infrastructure**: Docker Compose behind Traefik; Prometheus, Loki and Grafana; Cloudflare; tag-based releases on GitHub Actions.
- **How I work**: most changes start as a GitHub issue. Claude Code agents implement it, verify it on the real stack, pass an independent agent review, then merge and deploy. 70+ architecture decision records keep people and agents on the same rules.
