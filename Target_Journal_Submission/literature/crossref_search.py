"""Query Crossref for literature records (verified DOIs/metadata). Usage: python crossref_search.py "query" [issn] [from_year] [rows]"""
import sys, json, urllib.parse, urllib.request
q=sys.argv[1]; issn=sys.argv[2] if len(sys.argv)>2 and sys.argv[2]!='-' else None
fy=sys.argv[3] if len(sys.argv)>3 else '2015'; rows=int(sys.argv[4]) if len(sys.argv)>4 else 15
flt=f"from-pub-date:{fy}-01-01,type:journal-article"
if issn: flt+=f",issn:{issn}"
url="https://api.crossref.org/works?"+urllib.parse.urlencode({"query.bibliographic":q,"filter":flt,"rows":rows,"select":"DOI,title,author,container-title,issued,is-referenced-by-count"})
req=urllib.request.Request(url,headers={"User-Agent":"lit-audit/1.0 (mailto:research@example.org)"})
import time
for _t in range(5):
    try:
        d=json.load(urllib.request.urlopen(req,timeout=60)); break
    except Exception as e:
        time.sleep(3*(_t+1))
for it in d["message"]["items"]:
    au=", ".join((a.get("family","")) for a in it.get("author",[])[:4])
    print(f'{it["issued"]["date-parts"][0][0]} | {(it.get("title") or [""])[0][:110]} | {au} | {(it.get("container-title") or [""])[0]} | {it["DOI"]} | cites={it.get("is-referenced-by-count")}')
