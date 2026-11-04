# AP Elections API integration — preparation

Status: **Prepared, not connected or live**. A licensed AP API key is required. AP results are NOT currently shown in the dashboard.

## Activate
1. Obtain AP Elections API access and written authorization for public display/caching at https://www.ap.org/elections/ or elections_api_info@ap.org.
2. In GitHub repo Settings > Secrets and variables > Actions > New repository secret, create **AP_ELECTIONS_API_KEY**. Do not paste the key in HTML, chat, a commit, or an email.
3. Actions > AP Elections API readiness check > Run workflow.
4. Inspect Actions logs. This check fetches authenticated JSON but deliberately does not publish AP data. The response schema, pagination/next-link handling, license attribution, permitted polling interval and data redistribution rights must be confirmed before activating the public adapter.
5. When approved, implement AP response normalization into the dashboard's existing race shape, plus incremental updates and authoritative call detection. Never interpret a leader as a called winner.

AP documentation: https://developer.ap.org/ap-elections-api/docs/Getting_Started.htm
AP query explorer: https://api.ap.org/v3/elections/xplor
AP elections request: https://developer.ap.org/ap-elections-api/docs/Elections_Request.htm

Security: x-api-key request header; Accept-Encoding: gzip; HTTPS. GitHub Pages is public, so browser-side calls would expose the key. Workflow intentionally never publishes the raw response.
