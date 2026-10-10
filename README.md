# CYBERNEXA — Clarity before you click

A complete standalone React + Python + SQLite security analysis application, built from the provided cybersecurity requirements. This is a **new project**, not an extension or rebrand of SkillSync. No SkillSync marketplace code is used.

Four functional tools, authenticated reports/history, a live sample lab and a premium responsive dark/cyan interface. Basic operation uses no cloud services, no threat-intelligence API keys and no third-party Python dependencies.

## Fastest startup — Windows / VS Code

**Prerequisite:** Python 3.11 or newer, installed with the Python launcher (`py`).

1. Extract this archive.
2. In VS Code, open the `cybernexa` folder.
3. Open the integrated PowerShell terminal and run:

```powershell
py -3 run.py
```

4. Open **http://127.0.0.1:8000** in your browser.
5. Choose **Get started**, create your own account, then enter the workspace.

The precompiled frontend is included, so Node/npm is **not necessary** just to run the supplied application. Alternatively double-click `start_windows.bat`.

There is **no default account or shared demo password**. Registration initializes your personal workspace. Use a unique account passphrase of 15–128 characters, and do not reuse a real password from another service.

The database is created automatically at `backend/data/cybernexa.sqlite3` on first startup. Accounts and saved reports persist after you stop/restart the Python server. Stop with Ctrl+C.

If `py` is unavailable but Python is on PATH:

```powershell
python run.py
```

On macOS/Linux:

```bash
python3 run.py
```

Run from the project root. The default host is loopback only, port 8000.

## Frontend development — two terminals

**Prerequisites:** Python 3.11+ and Node.js 20.19+ (or a newer supported Node LTS). Internet is needed to download npm dependencies. Runtime uses local assets and system fonts only.

Terminal 1, project root:

```powershell
py -3 run.py
```

Terminal 2:

```powershell
cd frontend
npm ci
npm run dev
```

Open **http://localhost:5173**. Vite proxies `/api` to `127.0.0.1:8000`. Keep both terminals running. Browser requests use same-origin cookies and the proxy; there is no permissive CORS configuration.

After editing the frontend:

```powershell
cd frontend
npm run build
```

Restart/refresh the Python-hosted application on port 8000 to use the new compiled assets. Hash routing (`/#/dashboard/url`, etc.) works with the built server without SPA rewrite configuration.

`npm run preview` uses port 4173 with the same API proxy and still requires the Python backend. It is for local previews, not commercial deployment.

## Tools implemented

### URL Safety Checker

- Absolute HTTP/HTTPS validation, hostname/port parsing and malformed input handling.
- Indicators for HTTP, IP/non-public destinations, user-info tricks, nested/brand subdomains, limited lookalike patterns, internationalized/punycode hostnames, shorteners, confusing encoding, unusual ports, long links and executable/archive/sensitive-action paths.
- Explainable points, grouped contributions, classification, findings, next actions and explicit limitations.
- URL credentials, query values and fragments are removed from reports. Paths/domains are retained and may still reveal information.
- The server **never requests the submitted URL**, resolves its DNS, follows redirects or downloads files. Displayed extracted links are inert text, not clickable navigation.

### Email Phishing Analyzer

- Separate sender, reply-to, subject, body and optional header inputs.
- Optional full-email paste parsing with the Python standard email parser. Explicit fields override parsed fields.
- Sender/reply-to domain mismatch, limited sender lookalikes, pressure language, sensitive-data requests, account verification, payment/reward lures, risky attachment references and extracted URL findings.
- HTML link display/destination hostname mismatch detection. HTML is parsed as text, never rendered or executed.
- Authentication-Results evidence labeled **supplied and unverified**. No claim of independent SPF/DKIM/DMARC verification.
- Highlighted input is held on the current page only. Full raw email, subject, address local parts and headers are not saved in reports. Some indicator excerpts and link paths still remain.

### Message Scam Detector

- User-entered SMS/chat/social message text and optional sender context.
- Delivery-fee, prize, account-secret, personal-data, bank/security identity, urgency, investment and gift-card patterns; URL extraction and explanation.
- Scam and ordinary samples use the same engine. Highlighted excerpts remain in the current page only.

### Password Strength

- Real-time browser-only length/common-list/repetition/keyboard-sequence checks.
- Weak / Fair / Good / Strong heuristic labels and improvement advice.
- Password generation using browser `crypto.getRandomValues` with rejection sampling.
- Show/hide, clear and opt-in clipboard copy.
- **No password-checker request, logging, history or browser storage.** Input clears on navigation or after five minutes without editing.
- Account sign-in passwords are distinct: they are transmitted to your local server for authentication and stored as salted hashes. The checker should be used with samples, not real existing credentials.

### Live Security Lab

Five interactive scenarios: suspicious-looking URL, phishing email, ordinary email, delivery-fee message and local password strength. Synthetic examples use reserved example domains. Every Analyze action invokes the same engine as the real tools.

The sequence shows actual confirmed completion only after the engine returns. External reputation is explicitly marked skipped. It does not simulate a fake threat-intelligence scan.

### Workspace, history and reports

- Real registration/login/logout, cookie sessions, private user-scoped history and guarded frontend routes.
- Dashboard totals, type counts, high/very-high assessments and risk chart calculated from saved scans only. Empty accounts begin at zero.
- Save-to-history is explicit. Unsaved redacted reports are accessible for one hour. They become inaccessible after expiry and are physically purged on the next analysis or startup (not by an always-running cleanup job).
- Saved reports persist until deleted; ownership is required for reading, saving, downloading or deleting.
- History text/type/classification filtering, report details and JSON/text downloads.
- Maximum 1,000 saved reports shown in a list; pagination is not implemented.
- Account display name, compact spacing, reduced motion, account-password change (invalidates other sessions), and confirmed account deletion.
- Mobile sidebar and responsive layouts. Wide tables have an internal scrolling container rather than widening the page.

## Architecture

```text
cybernexa/
  run.py                       one-command launcher
  start_windows.bat            Windows launcher
  backend/
    server.py                  HTTP API, sessions/CSRF, rate/size limits, static hosting
    engine.py                  shared URL/email/message scoring rules
    storage.py                 SQLite, account hashing, session/report persistence
    requirements.txt           no third-party runtime packages
    tests/                     engine/API test suites
  frontend/
    src/
      components/              layout, reusable UI and report viewer
      pages/                   home, auth, overview, tools, lab, history, reports, settings
      lib/                     API/auth clients, samples, local password checker
      styles/                  shared responsive dark/cyan system
    tests/                     browser-only password logic tests
    public/                    favicon
    dist/                      runnable compiled application
    package.json
    package-lock.json
  docs/                        API, scoring, security, test results and implementation manifest
  previews/                    desktop/mobile screenshots from the tested application
```

## Tests — exact commands

From the project root:

```powershell
py -3 -m unittest discover -s backend/tests -v
```

Frontend:

```powershell
cd frontend
npm ci
npm test
npm run build
```

The provided results document **32 backend tests**, **8 password tests**, a successful production build and real browser smoke checks. Tests ran in Linux with Python/Node/headless Chromium. Windows instructions are cross-platform startup commands; native Windows execution was **not** tested in this environment.

## Optional configuration

No `.env` loader is used; `.env.example` is a reference only. Set environment variables in PowerShell before launching:

```powershell
$env:CYBERNEXA_DB = "C:\Users\YourName\cybernexa-data\cybernexa.sqlite3"
py -3 run.py
```

Use a local writable filesystem for SQLite. Do not commit the database or share it with this source archive. The database is not encrypted at rest; account isolation does not protect it from someone with filesystem access.

`CYBERNEXA_ORIGINS` can override the comma-separated allowed write origins. `CYBERNEXA_SECURE_COOKIE=1` adds the Secure cookie flag and must be used only behind correctly configured HTTPS.

Changing the backend port requires corresponding changes to the Vite proxy and allowed origins. Defaults are already aligned.

## Security boundaries and what is NOT implemented

This is a working **local analysis platform**, not a proof that links/content are safe or a production-certified service.

- No external VirusTotal, Google Safe Browsing, URLhaus, DNS, certificate or redirect lookup. No API-key integration is implemented. **No features require keys.** Reputation remains explicitly unavailable.
- No calibrated scam probabilities, comprehensive domain ownership/public-suffix verification, live threat feeds or malware detection.
- No actual attachment scanning, email delivery, recovery email, email verification or MFA. There is no administrator recovery UI. For a disposable installation, resetting the database removes all accounts/reports.
- No QR scanner, file hash tool, quiz, certificate/header lookup or PDF export; JSON and text reports are implemented.
- No cross-origin public API or production reverse proxy included.
- The Python standard-library HTTP server is designed here for loopback use. Before public deployment use a production-grade service stack and HTTPS, review session management, add operational monitoring, robust distributed rate limiting, backups, disk encryption and a security review. Do not expose it publicly by simply changing the host to `0.0.0.0`.
- Rate limiting is in-memory and per client IP, not distributed. There is no proxy trust configuration. Static assets are not rate-limited by the API limiter.
- A long random-looking input can score Strong without being unique or secret. The checker cannot detect reuse, breach exposure or meaning beyond its small ruleset.

See the included security and scoring notes for the exact boundaries and rule weights.

## Troubleshooting

- **Port 8000 already in use:** stop the other server/process; do not launch multiple copies. Keep the documented ports aligned.
- **Cannot reach backend:** start `py -3 run.py`; verify `/api/health` on port 8000.
- **403 security token:** refresh the page and sign in again. Use the exact documented origin; arbitrary ports are not allow-listed.
- **429 rate limit:** wait one minute. Default limits: 10 auth requests/minute/IP and 60 other API requests/minute/IP.
- **Expired unsaved report:** run the analysis again and save it promptly.
- **Database locked/read-only:** use a writable local folder, not an archive viewer or cloud-synchronized/network filesystem.
- **Cookie disappears:** keep the same browser profile/origin. Sessions expire after 24 hours.
- **Forgot account passphrase:** there is no email reset. Do not expect a decorative reset button to send mail. For a disposable local demo only, stop the server and delete `backend/data/cybernexa.sqlite3` to reset all local accounts and reports.
