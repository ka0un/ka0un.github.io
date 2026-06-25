# Structured Project Data

Common structure for each project: Title, Background & Problem, Solution, Result,
Technologies Used, Tags. Source: projects.txt. The four SUNDEVS products
(SunLicense, SunGuard, SunLinks, SunPaste) appear both in the Products section
and as full projects (Products group below).

---

## CLIENT WORK (SoftSora)

### 1. CTN Buyer Registration Platform
- **Year:** 2024 (June) · SoftSora · Client: CTN Co., Ltd. (Osaka, Japan)
- **Background & problem:**
  - CTN runs a car bulk-appraisal service connecting vehicle sellers with buyers across Japan.
  - Buyer registration was handled entirely by hand with Excel sheets and email.
  - Slow, error-prone, and not scalable as the buyer base grew.
- **Solution:**
  - Built a web app to automate and streamline buyer onboarding.
  - User registration with personal and contact details.
  - Car-matching condition registration (make, model, year, price range, etc.).
  - Personalized dashboard to view preferences, track seller interactions, manage the account.
  - Automated notifications about new listings matching a buyer's criteria.
- **Result:**
  - 1,000+ buyers registered and onboarded on the platform.
  - Replaced manual Excel/email work with a self-service flow.
  - Ongoing project with continuous improvements.
- **Technologies:** Java, Spring Boot, React, AWS EC2, AWS RDS (PostgreSQL), CloudFront (CDN), AWS SNS, AWS SES
- **Tags:** Full-Stack, Backend, AWS, Web Application, Automation

### 2. CTN Dynamic Vehicle Data Platform
- **Year:** 2024 (October) · SoftSora · Client: CTN Co., Ltd.
- **Background & problem:**
  - The existing system used static JSON files embedded directly in the frontend.
  - Adding or updating vehicle data was difficult and required manual code changes.
  - Publishing new data took 1-2 days.
- **Solution:**
  - Introduced a dynamic vehicle-data model using JSON files on S3 served via CloudFront.
  - A separate microservice on EC2 to create, update, and remove vehicle data.
  - Kept the static, pre-loaded delivery model so reads stay extremely fast.
- **Result:**
  - Cut data publishing time from 1-2 days to a few hours.
  - Sub-1ms data access after initial load - faster than typical API-based systems.
  - More scalable and far easier to maintain.
- **Technologies:** AWS S3, AWS CloudFront, AWS EC2, Microservices, JSON
- **Tags:** Cloud Architecture, Microservices, AWS, Performance

### 3. Automated Business Analysis & Sales Research Pipeline
- **Year:** 2025 (February) · SoftSora
- **Background & problem:**
  - Before every sales meeting, reps had to manually research each prospect: company, online presence, Google Maps profile, background.
  - Doing this by hand was slow, inconsistent, and often skipped when busy.
- **Solution:**
  - Built an automated pipeline triggered the moment an appointment is confirmed.
  - Researches the company and its market, analyses the prospect's website, audits the Google Maps presence.
  - Generates three ready-to-read reports, files them automatically, and notifies the sales team.
- **Result:**
  - Reps walk into every meeting fully prepared with zero extra effort.
  - Research that took time per prospect now happens instantly and consistently.
  - Handles large batches at once and self-corrects on errors.
- **Technologies:** Workflow Automation, Web Scraping/Analysis, Google Maps data, Report Generation
- **Tags:** Automation, Sales Enablement, Pipeline, AI/Research

### 4. Finding Hidden Sales Leads on Autopilot
- **Year:** 2026 (January) · SoftSora · Client: Japanese enterprise (TSR)
- **Background & problem:**
  - A sales team relied on a large internal company database to find new business.
  - Someone manually visited job-posting sites, copied company names, and checked each against the database.
  - Person-dependent, inconsistent, and Japanese company names vary widely (abbreviations, spellings) making matching hard. An earlier automation attempt hit tool time-limits.
- **Solution:**
  - Built a daily, fully automated system that visits major job sites, gathers company names, and normalizes spelling variations into one entity.
  - Checks each company against the internal database; genuinely new ones are added as fresh leads with a summary to the sales team.
  - Delivered in two stages: first a reviewable spreadsheet to build trust, then full integration into the client's tools.
- **Result:**
  - Moved from a fragile, person-dependent routine to a dependable daily lead engine.
  - More thorough coverage; the messy company-name problem handled automatically.
  - Designed to grow - new sources can be added without a rebuild.
- **Technologies:** n8n (self-hosted workflow automation), client database API integration, automated notifications
- **Tags:** Automation, n8n, Lead Generation, Data Matching

### 5. AI-Powered Sales Proposal Engine
- **Year:** 2026 (March) · SoftSora · Client: SMB sales/marketing org, Japan (FileMaker)
- **Background & problem:**
  - The sales team manually researched every prospect (site speed, reviews, social media, renewal timing) before pitching.
  - Slow, inconsistent, and dependent on whoever was working; good leads went cold.
  - No single place combining known customer data with real-world signals.
- **Solution:**
  - Built an AI engine that researches and reasons, then hands over a ready-to-use proposal.
  - Layer 1: reads the client's own records (contracts, plans, payment history) to spot renewal windows, service gaps, and consolidation opportunities.
  - Layer 2: reads public signals (slow/insecure sites, stale footers, quiet social accounts, recurring review complaints, competitor ranking, hiring, seasonal timing) and turns them into plain-language insights.
  - Tunes each suggestion to local context and industry language.
- **Result:**
  - Hour-long research now happens in seconds, the same way every time.
  - Consistent proposal quality regardless of who's at the desk.
  - Renewal windows and openings surfaced automatically instead of missed.
- **Technologies:** AI/decision layer, internal data integration, public-signal analysis (Google, business listings, review platforms), FileMaker
- **Tags:** AI, Sales Enablement, Data Integration, Automation

### 6. Automated Weekly Deal Summaries
- **Year:** 2026 (April) · SoftSora · Client: Japan-based enterprise sales team (HubSpot)
- **Background & problem:**
  - All deal data lived in HubSpot, but their plan had no automation features.
  - Staying on top of closing deals meant logging in and pulling numbers by hand weekly.
  - Information lived in HubSpot while the team communicated in Google Chat - no bridge between them.
- **Solution:**
  - Built an automated weekly digest connecting HubSpot and Google Chat.
  - Every Monday 9:00 AM it checks the pipeline, finds deals closing that week, and posts a tidy summary (name, stage, amount, close date) into the team's Google Chat space.
  - Used a separate automation platform as the bridge - no HubSpot upgrade needed.
  - Prototyped in a test environment first, then moved to production.
- **Result:**
  - The team starts each week knowing exactly where to focus, with zero manual effort.
  - Fewer missed deals; a manual chore became fully hands-off.
- **Technologies:** HubSpot, Google Chat, n8n
- **Tags:** Automation, CRM Integration, n8n, Workflow

### 7. CRM Unification & AI Data Enrichment (KOBUSHI)
- **Year:** 2026 (May) · SoftSora · Client: KOBUSHI Marketing (B2B, Japan)
- **Background & problem:**
  - Contacts were split across three tools: CRM, a business-card app, and Excel files - never joined up.
  - Thousands of older records lacked business details; no way to tell decision-makers from junior staff.
  - The job-title field was a mess - one role written 79 different ways (typos, formatting, garbled characters).
- **Solution:**
  - Built one unified pipeline so business-card contacts import the same clean way as event contacts, with duplicate merging by email.
  - Full clean-up and enrichment - auto-filled missing details (website, company info) across ~6,000 contacts.
  - Automatic decision-maker sorting: normalized 79 title variations into standard categories and split contacts into decision-makers vs. others.
- **Result:**
  - One source of truth across all channels.
  - 3,000+ genuine decision-makers cleanly identified out of ~6,700 contacts.
  - Targeting in seconds; enrichment of ~6,000 records engineered to cost only a few dollars to run.
- **Technologies:** Zoho CRM, Google Sheets, n8n, Gemini API
- **Tags:** CRM, AI Enrichment, Data Engineering, Automation

### 8. HAG - Human Approval Gateway
- **Year:** 2026 (May) · SoftSora
- **Background & problem:**
  - Getting human approval for sensitive operations (production deploys, high-value transactions, important actions) was a bottleneck.
  - Approvals were lost across emails, Slack, and ticketing systems - fragmented, slow, error-prone.
- **Solution:**
  - Built HAG, a self-hosted gateway between systems that need approval and the people who give it.
  - Listens for approval requests from any system, posts interactive Approve/Reject messages to Slack DMs/channels, applies the rule (first-response-wins or all-must-agree), and notifies the originating system.
  - Works with any system that can make an HTTP request.
- **Result:**
  - Approvals go from minutes (hunting people down) to seconds.
  - Every decision logged, audited, and visible; no more lost or missed approvals.
- **Technologies:** Java (self-hosted service), Slack interactive messages, HTTP/webhook integration
- **Tags:** Backend, Integration, Workflow, Self-Hosted

---

## PLATFORM (SunDevs)

### 9. SunDevs Dashboard
- **Year:** 2026 (June) · SunDevs
- **Link:** https://dashboard.sundevs.net
- **Background & problem:**
  - SunDevs customers had no centralized way to manage assets, track service requests, or get support.
  - Support teams were overwhelmed with repetitive questions; the experience was fragmented across systems.
- **Solution:**
  - Built a unified, web-based customer management platform - a single source of truth.
  - Unified dashboard with real-time licenses/servers/requests, interactive charts, light/dark themes.
  - Self-service asset management: license management, server monitoring, service requests, call scheduling.
  - Selection-based support chatbot (no typing) for purchases, docs, requests, scheduling - context-aware, with anti-duplicate and rate-limit safeguards.
  - Role-based access (Customer/Admin), Discord OAuth2, audit logging, email verification.
- **Result:**
  - Shifted customer experience from reactive (waiting for support) to proactive (24/7 self-service).
  - Dramatically reduced support workload; scales without proportional staffing.
  - 2,857+ lines of documentation; chatbot state machine with 20+ states and 11 conversation flows.
- **Technologies:** Java 17, Spring Boot 3.5, Spring Security, Vaadin Flow + TypeScript, H2/MongoDB, WebSocket (Vaadin Push), Maven
- **Tags:** Full-Stack, Enterprise, Vaadin, Spring Boot, SaaS

---

## OPEN-SOURCE PLUGINS

### 10. OPProtector
- **Year:** 2023 (July) · SunDevs
- **Link:** https://github.com/ka0un/OPProtector
- **Background & problem:**
  - Minecraft server admins faced unauthorized access to operator accounts - a single compromise grants full server control (griefing, data theft, destruction).
  - No automated way to detect operator abuse; admins relied on manual log parsing and reactive responses.
- **Solution:**
  - A security plugin that scans and monitors operator accounts in real time.
  - Continuous monitoring, automated detection of blacklisted permissions and unauthorized patterns, real-time admin alerts, and early preventive action.
- **Result:**
  - 19,000+ servers protected (and counting); adopted across thousands of servers.
  - 75+ GitHub stars; zero false positives via intelligent detection; immediate threat response.
- **Technologies:** Java, Bukkit/Spigot
- **Tags:** Open-Source, Security, Minecraft Plugin, Java

### 11. Discord Leaderboards
- **Year:** 2023 (April) · SunDevs
- **Link:** https://github.com/ka0un/DiscordLeaderboards
- **Background & problem:**
  - Server owners wanted to showcase top players in their Discord communities in real time.
  - No simple way to extract leaderboard data from servers and display it in Discord without building custom integrations.
- **Solution:**
  - A lightweight plugin connecting Minecraft server data directly to Discord.
  - Pulls rankings via PlaceholderAPI, posts via webhooks or DiscordSRV slash commands, updates on schedule (hourly/daily/weekly/monthly), works across MC 1.8.8-1.19.4, supports unlimited custom leaderboards.
- **Result:**
  - Adopted across hundreds of servers and thousands of players.
  - 40+ GitHub stars; released on SpigotMC, BuiltByBit, PolyMart; open-source (MIT) with a premium version.
  - First commercial product - the foundation for starting SunDevs.
- **Technologies:** Java, Bukkit/Spigot, PlaceholderAPI, DiscordSRV, Webhooks
- **Tags:** Open-Source, Discord Integration, Minecraft Plugin, Java

### 12. SummitEvents
- **Year:** 2023 (October) · Summit Realms
- **Background & problem:**
  - Server admins needed to run time-limited competitive events (mining/farming challenges) but coordinating them manually was tedious and error-prone.
  - No straightforward way to launch scheduled events, track rankings live, auto-reward winners, or show progress/time.
- **Solution:**
  - Built a comprehensive event management plugin.
  - Event creation/configuration, real-time leaderboards, automated broadcast messaging, boss-bar HUD (score, position, time remaining), automated reward commands, and flexible event types (block breaking, farming) with customizable materials.
- **Result:**
  - Made events easy to organize and more engaging with live progress tracking and automated recognition.
  - Config-driven design let the client launch diverse event types without code changes.
- **Technologies:** Java, Bukkit/Spigot, YAML configuration, asynchronous task scheduling
- **Tags:** Open-Source, Minecraft Plugin, Java, Event System

---

## PRODUCTS (SunDevs)

### 13. SunLicense - Software License Management Platform
- **Year:** 2025 (January) · SunDevs
- **Link:** https://store.sundevs.net/l/sunlicense
- **Background & problem:**
  - Managing software licenses across products, customers, and requests is complex and error-prone.
  - Companies juggled scattered spreadsheets, had no unified view, and faced security concerns around API access.
- **Solution:**
  - A web-based platform consolidating products, licenses, customers, and requests into one secure dashboard.
  - Admin dashboard with real-time visibility and analytics; create/assign/revoke licenses in seconds.
  - Customer self-service portal, secure token-based REST API (intent-based access control), blacklist management, and Discord integration.
- **Result:**
  - Replaced manual tracking with automated management; prevents revenue leakage.
  - Self-service reduces support load; scales to unlimited products, licenses, and customers.
- **Technologies:** Spring Boot 3.3.5, Spring Security, Vaadin 24.5, Discord OAuth2, REST API v2, H2, Playwright + TypeScript
- **Tags:** Product, Spring Boot, Vaadin, SaaS, REST API

### 14. SunGuard - Code Obfuscation Platform
- **Year:** 2025 (May) · SunDevs
- **Link:** https://store.sundevs.net/l/sunguard
- **Background & problem:**
  - Protecting code from theft and reverse engineering was a luxury reserved for enterprises.
  - Existing tools were too technical or prohibitively expensive for independent and small dev teams.
- **Solution:**
  - A developer-friendly obfuscation platform bringing enterprise-grade protection within reach.
  - Multi-engine support (ProGuard, yGuard, Skidfuscator), automated dependency management, flexible config, real-time progress, Java & JavaScript support.
  - Clean web interface (Spring Boot, Vaadin, TypeScript) usable from any browser.
- **Result:**
  - Democratized code obfuscation - upload a file and click "Obfuscate."
  - Removed the trade-off between security and simplicity.
- **Technologies:** Spring Boot, Vaadin, TypeScript, ProGuard, yGuard, Skidfuscator
- **Tags:** Product, Developer Tools, Security, Vaadin

### 15. SunLinks - Self-Hosted URL Management Platform
- **Year:** 2026 (March) · SunDevs
- **Link:** https://store.sundevs.net/l/sunlinks
- **Background & problem:**
  - Teams share links at scale but lack visibility into performance.
  - Services like Bitly/TinyURL require subscriptions, lock data into proprietary platforms, and limit customization.
- **Solution:**
  - A self-hosted URL shortener giving organizations full control over links and analytics.
  - Custom short codes with redirects, expiration, and password protection; real-time analytics (geography, device, browser, referrer); automatic QR codes; full REST API with rate limiting; zero-config single-executable deployment.
- **Result:**
  - Complete data ownership and advanced analytics with no per-click or subscription fees.
  - Scales from small teams to enterprises; integrates into broader automation via the API.
- **Technologies:** Spring Boot 3.3, Vaadin 24, H2, ApexCharts, REST API
- **Tags:** Product, Self-Hosted, Analytics, Vaadin, REST API

### 16. SunPaste - Self-Hosted Code & Text Sharing Platform
- **Year:** 2026 (June) · SunDevs
- **Link:** https://store.sundevs.net/l/sunpaste
- **Background & problem:**
  - Teams need to share code and sensitive snippets quickly, but public paste services expose content to the internet.
  - No middle ground between sacrificing privacy to a third party or building something complex from scratch.
- **Solution:**
  - A self-hosted paste platform for teams that need control without complexity.
  - Flexible sharing (public/unlisted/private), security features (password protection, self-destruct-after-view, expiration), REST API with keys, syntax highlighting, QR codes, Discord slash commands, and backup/restore.
  - Spring Boot backend with a Vaadin frontend; efficient filesystem overflow for large pastes, real-time language detection, responsive design.
- **Result:**
  - Eliminates the trade-off between security and convenience.
  - Complete data ownership with a polished, familiar experience and no vendor lock-in.
- **Technologies:** Spring Boot, Vaadin, REST API, Swagger / ReDoc
- **Tags:** Product, Self-Hosted, Developer Tools, Vaadin
