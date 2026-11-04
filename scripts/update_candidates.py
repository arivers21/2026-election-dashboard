import csv, io, json, urllib.request, pathlib, datetime
url='https://deepsyte.app/data/candidates-2026.csv'
req=urllib.request.Request(url,headers={'User-Agent':'ElectionDashboard/1.0 (public civic data)'})
with urllib.request.urlopen(req,timeout=35) as response:
    raw=response.read().decode('utf-8-sig')
rows=list(csv.DictReader(io.StringIO(raw)))
if not rows: raise RuntimeError('No CSV candidate rows')
def get(r,*names):
    d={''.join(c for c in k.lower() if c.isalnum()):str(v or '').strip() for k,v in r.items() if k}
    return next((d[n] for n in names if d.get(n)), '')
roster={}
for r in rows:
    state=get(r,'state','statecode','stateabbreviation','stateabbr').upper()
    name=get(r,'name','candidatename','candidate','fullname') or (get(r,'firstname','first')+' '+get(r,'lastname','last')).strip()
    office=get(r,'office','chamber','race','officename').lower()
    party=get(r,'party','partyaffiliation','partyname') or 'Unknown'
    district=get(r,'district','districtnumber','congressionaldistrict')
    state_names={'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA','COLORADO':'CO','CONNECTICUT':'CT','DELAWARE':'DE','FLORIDA':'FL','GEORGIA':'GA','HAWAII':'HI','IDAHO':'ID','ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS','KENTUCKY':'KY','LOUISIANA':'LA','MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA','MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS','MISSOURI':'MO','MONTANA':'MT','NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ','NEW MEXICO':'NM','NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK','OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC','SOUTH DAKOTA':'SD','TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA','WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY','DISTRICT OF COLUMBIA':'DC'}
    state=state_names.get(state,state)
    if len(state)!=2 or not name: continue
    if 'senat' in office: race='U.S. Senate'
    elif 'house' in office or 'congress' in office or 'representative' in office: race='House District '+(district or 'unspecified')
    else: continue
    status=get(r,'ballotstatus','status','candidatestatus')
    group=roster.setdefault(state,{}).setdefault(race,[])
    if not any(x[0]==name for x in group):group.append([name,party,status])
if len(roster)<40: raise RuntimeError(f'Only {len(roster)} states parsed; check CSV schema: {list(rows[0])}')
out={'source':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'states':roster}
pathlib.Path('candidates-2026.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
print('Prepared',len(roster),'states',sum(len(v) for rs in roster.values() for v in rs.values()),'candidates')
