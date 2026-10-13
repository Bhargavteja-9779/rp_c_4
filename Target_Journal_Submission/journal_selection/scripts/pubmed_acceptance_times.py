"""Measure submission(received)->acceptance intervals from PubMed history dates.

Primary-source verification of journal acceptance timelines. For each journal we
sample recent research articles (publication date window below), read the
PubMed <History> 'received' and 'accepted' dates deposited by the publisher,
and report n, median, IQR and the share accepted within 30/60/72 days.
Usage: python pubmed_acceptance_times.py out.csv
"""
import csv, sys, time, statistics, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import date

EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
WINDOW = "2025/07/01:2026/09/30[dp]"
JOURNALS = {  # display name -> PubMed journal query
 # Oxford University Press
 "Bioinformatics (OUP)": '"Bioinformatics"[ta]',
 "Briefings in Bioinformatics (OUP)": '"Brief Bioinform"[ta]',
 "NAR Genomics and Bioinformatics (OUP)": '"NAR Genom Bioinform"[ta]',
 "Bioinformatics Advances (OUP)": '"Bioinform Adv"[ta]',
 "GigaScience (OUP)": '"Gigascience"[ta]',
 "JAMIA (OUP)": '"J Am Med Inform Assoc"[ta]',
 "Nucleic Acids Research (OUP)": '"Nucleic Acids Res"[ta]',
 "European Heart Journal Digital Health (OUP)": '"Eur Heart J Digit Health"[ta]',
 "PNAS Nexus (OUP)": '"PNAS Nexus"[ta]',
 "Brain Communications (OUP)": '"Brain Commun"[ta]',
 # ACS / RSC
 "J Chem Inf Model (ACS)": '"J Chem Inf Model"[ta]',
 "J Chem Theory Comput (ACS)": '"J Chem Theory Comput"[ta]',
 "ACS Omega (ACS)": '"ACS Omega"[ta]',
 "Digital Discovery (RSC)": '"Digit Discov"[ta]',
 # Elsevier / Cell Press
 "Computers in Biology and Medicine (Elsevier)": '"Comput Biol Med"[ta]',
 "Comput Methods Programs Biomed (Elsevier)": '"Comput Methods Programs Biomed"[ta]',
 "J Biomedical Informatics (Elsevier)": '"J Biomed Inform"[ta]',
 "Artificial Intelligence in Medicine (Elsevier)": '"Artif Intell Med"[ta]',
 "Neural Networks (Elsevier)": '"Neural Netw"[ta]',
 "Medical Image Analysis (Elsevier)": '"Med Image Anal"[ta]',
 "Comput Struct Biotechnol J (Elsevier)": '"Comput Struct Biotechnol J"[ta]',
 "Journal of Advanced Research (Elsevier)": '"J Adv Res"[ta]',
 "Science of the Total Environment (Elsevier)": '"Sci Total Environ"[ta]',
 "J Hazardous Materials (Elsevier)": '"J Hazard Mater"[ta]',
 "Ecotoxicol Environ Saf (Elsevier)": '"Ecotoxicol Environ Saf"[ta]',
 "Environmental Research (Elsevier)": '"Environ Res"[ta]',
 "Water Research (Elsevier)": '"Water Res"[ta]',
 "J Environmental Management (Elsevier)": '"J Environ Manage"[ta]',
 "Patterns (Cell Press)": '"Patterns (N Y)"[ta]',
 "iScience (Cell Press)": '"iScience"[ta]',
 # Springer Nature / BMC
 "Scientific Reports (Nature)": '"Sci Rep"[ta]',
 "npj Digital Medicine (Nature)": '"NPJ Digit Med"[ta]',
 "Communications Biology (Nature)": '"Commun Biol"[ta]',
 "BMC Bioinformatics (BMC)": '"BMC Bioinformatics"[ta]',
 "BMC Med Inform Decis Mak (BMC)": '"BMC Med Inform Decis Mak"[ta]',
 "Journal of Cheminformatics (Springer)": '"J Cheminform"[ta]',
 "Brain Informatics (Springer)": '"Brain Inform"[ta]',
 # IEEE / Wiley / others
 "IEEE J Biomed Health Inform (IEEE)": '"IEEE J Biomed Health Inform"[ta]',
 "IEEE Trans Neural Netw Learn Syst (IEEE)": '"IEEE Trans Neural Netw Learn Syst"[ta]',
 "IEEE Trans Med Imaging (IEEE)": '"IEEE Trans Med Imaging"[ta]',
 "Advanced Science (Wiley)": '"Adv Sci (Weinh)"[ta]',
 "Medical Physics (Wiley)": '"Med Phys"[ta]',
 "PLOS Computational Biology (PLOS)": '"PLoS Comput Biol"[ta]',
 "Frontiers in Plant Science (Frontiers)": '"Front Plant Sci"[ta]',
 "Physiological Measurement (IOP)": '"Physiol Meas"[ta]',
 "J Neural Engineering (IOP)": '"J Neural Eng"[ta]',
 "Physics in Medicine & Biology (IOP)": '"Phys Med Biol"[ta]',
}

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:  # network/429: back off
            time.sleep(2 ** (i + 1))
    raise RuntimeError(url)

def pdate(node):
    try:
        return date(int(node.findtext("Year")), int(node.findtext("Month")), int(node.findtext("Day")))
    except Exception:
        return None

def measure(q, retmax=300):
    term = f"{q} AND {WINDOW} AND journal article[pt] NOT review[pt] NOT editorial[pt]"
    url = EU + "esearch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": retmax, "sort": "pub_date", "retmode": "json"})
    import json
    ids = json.loads(get(url))["esearchresult"]["idlist"]
    days = []
    for k in range(0, len(ids), 150):
        time.sleep(0.4)
        x = get(EU + "efetch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids[k:k + 150]), "retmode": "xml"}))
        for art in ET.fromstring(x).iter("PubmedArticle"):
            rec = acc = None
            for d in art.iter("PubMedPubDate"):
                if d.get("PubStatus") == "received": rec = pdate(d)
                if d.get("PubStatus") == "accepted": acc = pdate(d)
            if rec and acc and acc >= rec:
                days.append((acc - rec).days)
    return len(ids), days

if __name__ == "__main__":
    out = sys.argv[1]
    rows = []
    for name, q in JOURNALS.items():
        n_ids, d = measure(q)
        if len(d) >= 20:
            qs = statistics.quantiles(d, n=4)
            row = dict(journal=name, sampled=n_ids, n_with_dates=len(d), median_days=statistics.median(d),
                       q1=qs[0], q3=qs[2], pct_le30=round(100*sum(v <= 30 for v in d)/len(d), 1),
                       pct_le60=round(100*sum(v <= 60 for v in d)/len(d), 1), pct_le72=round(100*sum(v <= 72 for v in d)/len(d), 1))
        else:
            row = dict(journal=name, sampled=n_ids, n_with_dates=len(d))
        print(row, flush=True); rows.append(row)
    keys = ["journal", "sampled", "n_with_dates", "median_days", "q1", "q3", "pct_le30", "pct_le60", "pct_le72"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
