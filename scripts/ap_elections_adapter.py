#!/usr/bin/env python3
"""Licensed AP Elections API adapter. Never publish raw AP data without license approval."""
import os,json,urllib.request,datetime,pathlib,sys
KEY=os.getenv("AP_ELECTIONS_API_KEY","")
if not KEY:
    print("AP_ELECTIONS_API_KEY missing: no AP request made")
    sys.exit(0)
url="https://api.ap.org/v3/elections/2026-11-03?format=json&level=state&officeID=H,S&raceType=G"
req=urllib.request.Request(url,headers={"x-api-key":KEY,"Accept-Encoding":"gzip","Accept":"application/json","User-Agent":"ElectionDashboard/1.0"})
with urllib.request.urlopen(req,timeout=40) as response:
    raw=response.read()
    if response.headers.get("Content-Encoding","").lower()=="gzip":
        import gzip
        raw=gzip.decompress(raw)
    payload=json.loads(raw)
# Intentional fail-closed boundary: AP response structure and publication rights must be confirmed
# before any candidate, vote or call information is exported to the public site.
pathlib.Path("ap-integration-status.json").write_text(json.dumps({"source":"Associated Press Elections API","configured":True,"connected":True,"published":False,"message":"Authenticated API response received. Mapping and publication approval pending.","checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
print("AP authentication and JSON retrieval succeeded; no licensed data published.")
