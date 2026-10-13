"""Verify candidate references against Crossref (DOI -> authors/title/year/venue). Writes references_verified.json."""
import json, time, urllib.request, urllib.parse, sys
DOIS = {
 "barber2021": "10.1214/20-aos1965", "lei2018": "10.1080/01621459.2017.1307116", "vovk2005": "10.1007/b106715",
 "angelopoulos2023": "10.1561/2200000101", "papadopoulos2011": "10.1613/jair.3198", "fontana2023": "10.3150/21-BEJ1447",
 "wang1991": "10.1021/ac00023a016", "bouveresse1996": "10.1016/0169-7439(95)00074-7", "feudale2002": "10.1016/S0169-7439(02)00085-0",
 "workman2018": "10.1177/0003702817736064", "nikzad2018": "10.1021/acs.analchem.8b00498", "fonseca2022": "10.1016/j.aca.2022.340154",
 "xie2024": "10.1016/j.aca.2024.342404", "huang2026": "10.1016/j.aca.2026.346104", "fan2025": "10.1016/j.aca.2025.344151",
 "allegrini2016": "10.1016/j.aca.2015.11.028", "olivieri2006": "10.1351/pac200678030633", "bouckaert2011": "10.1016/j.chemolab.2011.08.008",
 "jovic2025": "10.1016/j.foodchem.2025.145387", "maxime2025": "10.1016/j.chemolab.2025.105532", "anderson2020": "10.1016/j.postharvbio.2020.111202",
 "walsh2024": "10.1016/j.saa.2024.124003", "mishra2022": "10.1016/j.trac.2022.116804", "kennard1969": "10.1080/00401706.1969.10490666",
 "wold2001": "10.1016/S0169-7439(01)00155-1", "savitzky1964": "10.1021/ac60214a047", "barnes1989": "10.1366/0003702894202201",
 "pasquini2018": "10.1016/j.aca.2018.04.004", "gneiting2007": "10.1198/016214506000001437", "booksh2025": "10.1002/cem.70017",
 "redd2024": "10.1002/cem.3639", "gu2019": "10.1177/0003702819831017", "norinder2014": "10.1021/ci5001168",
 "fonollosa2016": "10.1016/j.snb.2016.05.089", "mishra2020dipls": "10.1016/j.infrared.2020.103547", "anderson2021": "10.1016/j.postharvbio.2020.111358",
 "astm_e1655": "10.1520/E1655-17", "qian2024": "10.1016/j.chemolab.2024.105225", "guan2022": "10.1093/biomet/asac040",
 "faber1997": "10.1002/(SICI)1099-128X(199705)11:3<181::AID-CEM459>3.0.CO;2-7", "mango_data": "10.17632/46htwnp833.6",
}
out = {}
for k, doi in DOIS.items():
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    for t in range(4):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ref-audit/1.0 (mailto:research@example.org)"}), timeout=60))["message"]
            break
        except Exception as e:
            d = None; err = str(e); time.sleep(3 * (t + 1))
    if d is None:
        out[k] = dict(doi=doi, verified=False, error=err); print(k, "FAILED", err); continue
    au = [f'{a.get("family","")}, {a.get("given","")}'.strip(", ") for a in d.get("author", [])] or [a.get("name","") for a in d.get("editor", [])]
    yr = (d.get("published-print") or d.get("published-online") or d.get("issued"))["date-parts"][0][0]
    out[k] = dict(doi=doi, verified=True, authors=au, title=(d.get("title") or [""])[0], year=yr,
                  venue=(d.get("container-title") or [d.get("publisher", "")])[0] if d.get("container-title") else d.get("publisher", ""),
                  volume=d.get("volume"), issue=d.get("issue"), pages=d.get("page") or d.get("article-number"), type=d.get("type"))
    print(k, yr, "|", out[k]["title"][:90], "|", out[k]["venue"], "|", "; ".join(au[:3]))
    time.sleep(1.2)
json.dump(out, open("references_verified.json", "w"), indent=1)
