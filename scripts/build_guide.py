#!/usr/bin/env python3
"""Deepen candidate notes on the Precinct 7 ballot.

Reads data/ballot.json, replaces thin notes with sourced biographies, and
writes that file plus the copy embedded in index.html.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVE = Path("/tmp/byron-ballot-serve/index.html")
OUT = ROOT / "index.html"
BALLOT_OUT = ROOT / "data" / "ballot.json"

WIKI = {
    "benson": "https://en.wikipedia.org/wiki/Jocelyn_Benson",
    "brinks": "https://en.wikipedia.org/wiki/Winnie_Brinks",
    "james": "https://en.wikipedia.org/wiki/John_James_(Michigan_politician)",
    "deboyer": "https://en.wikipedia.org/wiki/Jay_DeBoyer",
    "gilchrist": "https://en.wikipedia.org/wiki/Garlin_Gilchrist",
    "forlini": "https://en.wikipedia.org/wiki/Anthony_Forlini",
    "savit": "https://en.wikipedia.org/wiki/Eli_Savit",
    "elsayed": "https://en.wikipedia.org/wiki/Abdul_El-Sayed",
    "rogers": "https://en.wikipedia.org/wiki/Mike_Rogers_(Michigan_politician)",
    "scholten": "https://en.wikipedia.org/wiki/Hillary_Scholten",
    "rigas": "https://en.wikipedia.org/wiki/Angela_Rigas",
    "victory": "https://en.wikipedia.org/wiki/Roger_Victory",
    "hood": "https://en.wikipedia.org/wiki/Noah_Hood",
}
SBE_NEWS = "https://www.bridgedetroit.com/michigan-state-board-of-education-candidates-what-to-know/"
SBE_GUIDE = "https://michwomen.com/blog/michigan-state-board-of-education-2026-voter-guide"
UM_NEWS = "https://www.michiganpublic.org/politics-government/2026-10-09/meet-the-candidates-running-for-the-u-m-board-of-regents"
MSU_NEWS = "https://www.michiganpublic.org/politics-government/2026-10-23/meet-the-democratic-and-republican-candidates-for-the-msu-board-of-trustees"
UNIV = "https://michwomen.com/blog/u-m-regents-msu-trustees-wsu-governors-2026-voter-guide"
WSU = "https://www.mlive.com/news/detroit/2026/10/10-candidates-seek-2-seats-on-wayne-state-university-board.html"
MSC = "https://www.michiganpublic.org/politics-government/2026-10-09/michigan-supreme-court-candidates-2026"
BRIDGE = "https://bridgemi.com/michigan-government/whos-running-for-michigan-supreme-court-6-candidates-compete-for-2-seats/"
HOUSE = "https://www.mlive.com/news/grand-rapids/2026/10/republican-incumbent-faces-former-researcher-for-state-house-district-79-seat.html"
DEBOER = "https://www.mlive.com/news/grand-rapids/2026/08/familiar-face-uphill-race-terri-deboer-faces-difficult-path-against-hillary-scholten.html"
LLOYD = "https://www.michiganpublic.org/politics-government/2026-10-22/doug-lloyd-michigan-attorney-general-candidate"
LLOYD_BIO = "https://www.eatoncounty.org/m/directory/employee?eid=7"
SENATE = "https://www.abc57.com/news/candidates-for-michigan-state-senate-district-20-race-speak-out"
GRCC = "https://www.ottawanewsnetwork.org/heres-everyone-running-for-office-in-ottawa-county-for-the-2026-november-general-election/"
MANUAL = "https://www.legislature.mi.gov/documents/2025-2026/michiganmanual/2025-MM-P0442-p0448.pdf"
WEAREBC = "https://wearebc.substack.com/p/your-vote-your-schools-board-of-education"
MIKA = "https://www.mikameyers.com/attorneys/jeffrey-m-black/"


def L(*pairs):
    return [{"label": a, "url": b} for a, b in pairs]


# Richer public biographies. Filing lines on each card are left as they are.
NOTES = {
    "race-1|Jocelyn Benson / Winnie Brinks": (
        "Wikipedia: Jocelyn Benson has been Michigan secretary of state since 2019 and was previously dean of Wayne State University Law School. Winnie Brinks is majority leader of the Michigan Senate, the first woman in that job, and a senator since 2019 after six years in the state House.",
        L(("Wikipedia — Jocelyn Benson", WIKI["benson"]), ("Wikipedia — Winnie Brinks", WIKI["brinks"])),
    ),
    "race-1|John James / Jay DeBoyer": (
        "Wikipedia: John James is the U.S. representative for Michigan’s 10th District, a businessman, and a former military officer. He was the Republican nominee for U.S. Senate in 2018 and 2020. Jay DeBoyer is a state representative and a former St. Clair County clerk.",
        L(("Wikipedia — John James", WIKI["james"]), ("Wikipedia — Jay DeBoyer", WIKI["deboyer"])),
    ),
    "race-1|Donna Brandenburg / Robert Donald Cowper II": (
        "U.S. Taxpayers ticket. The state’s official candidate list gives this ticket a Byron Center mailing address. The street address is not shown here. No separate biography was found.",
        [],
    ),
    "race-2|Garlin Gilchrist II": (
        "Wikipedia: Garlin Gilchrist II has been lieutenant governor of Michigan since 2019. He is an engineer. He sought the Democratic nomination for governor before becoming the nominee for secretary of state.",
        L(("Wikipedia", WIKI["gilchrist"])),
    ),
    "race-2|Anthony G. Forlini": (
        "Wikipedia: Anthony Forlini has been Macomb County clerk since 2021. He served in the Michigan House from 2011 through 2016 and was Harrison Township supervisor from 2004 to 2011.",
        L(("Wikipedia", WIKI["forlini"])),
    ),
    "race-3|Eli Savit": (
        "Wikipedia: Eli Savit has been Washtenaw County prosecuting attorney since 2021. He was senior legal counsel to Detroit Mayor Mike Duggan, clerked for U.S. Supreme Court Justices Sandra Day O’Connor and Ruth Bader Ginsburg, and teaches at the University of Michigan Law School.",
        L(("Wikipedia", WIKI["savit"])),
    ),
    "race-3|Doug Lloyd": (
        "Michigan Public: Doug Lloyd is the Eaton County prosecuting attorney and the Republican nominee. He was appointed in 2013 after earlier work as a prosecutor in Eaton and Jackson counties, and he is a former president of the Prosecuting Attorneys Association of Michigan. This is not the former football player of the same name.",
        L(("Michigan Public interview", LLOYD), ("Eaton County biography", LLOYD_BIO)),
    ),
    "race-4|Abdul El-Sayed": (
        "Wikipedia: Abdul El-Sayed is a physician and epidemiologist. He led the Detroit Health Department from 2015 to 2017 and the Wayne County health department from 2023 to 2025. He is a University of Michigan graduate and a Rhodes Scholar, and he won the 2026 Democratic primary.",
        L(("Wikipedia", WIKI["elsayed"])),
    ),
    "race-4|Mike Rogers": (
        "Wikipedia: Mike Rogers represented Michigan’s 8th Congressional District from 2001 to 2015 and chaired the House Intelligence Committee. He is a former FBI agent. He was the Republican nominee for U.S. Senate in 2024 and is the nominee again.",
        L(("Wikipedia", WIKI["rogers"])),
    ),
    "race-6|Hillary Scholten": (
        "Wikipedia: Hillary Scholten has represented Michigan’s 3rd Congressional District since 2023. She is an attorney who previously worked at the U.S. Department of Justice and in private practice.",
        L(("Wikipedia", WIKI["scholten"])),
    ),
    "race-6|Terri DeBoer": (
        "MLive: Terri DeBoer is a West Michigan meteorologist who worked in local television for more than 30 years, including at WOOD-TV, and lives in Byron Center. She left broadcasting to run and won the August 2026 Republican primary.",
        L(("MLive profile", DEBOER), ("Ballotpedia", "https://ballotpedia.org/Terri_DeBoer")),
    ),
    "race-8|Dale Murney": (
        "Ballotpedia: Dale Murney is the Democratic nominee and was unopposed in the August 4, 2026 primary. ABC57 reports the seat is open because Senator Aric Nesbitt is term-limited. No occupation was found.",
        L(("ABC57 primary coverage", SENATE)),
    ),
    "race-8|Chris Moraitis": (
        "ABC57: Chris Moraitis, the Republican nominee, has served as president of the Van Buren Bar Association and has been involved with the Paw Paw Downtown Development Authority and the Van Buren County Republican Party. He won a three-way primary.",
        L(("ABC57 primary coverage", SENATE), ("Ballotpedia", "https://ballotpedia.org/Chris_Moraitis")),
    ),
    "race-13|Zach Abbott": (
        "MLive: Zach Abbott, the Democratic nominee, served six years in the U.S. Air Force, graduated from Calvin University with a history degree, and worked as a researcher at The Right Place in Grand Rapids. He lives in Caledonia Township.",
        L(("MLive profile", HOUSE)),
    ),
    "race-13|Angela Rigas": (
        "MLive: Angela Rigas, the Republican incumbent since 2023, is a Hastings High School graduate and a small-business owner in the salon industry. She was unopposed in the August 2026 primary.",
        L(("MLive profile", HOUSE), ("Wikipedia", WIKI["rigas"])),
    ),
    "race-22|Judith Pritchett": (
        "Bridge Michigan: Judith Pritchett is an incumbent Democrat first elected to the State Board of Education in 2018. The same report describes her as an education consultant and retired public-school administrator from Macomb County.",
        L(("Bridge Michigan", SBE_NEWS), ("Longer candidate guide", SBE_GUIDE)),
    ),
    "race-22|Tiffany Tilley": (
        "Bridge Michigan: Tiffany Tilley is an incumbent Democrat first elected in 2018. The same report describes her as an adjunct professor and realtor from West Bloomfield.",
        L(("Bridge Michigan", SBE_NEWS), ("Longer candidate guide", SBE_GUIDE)),
    ),
    "race-22|Terence Collins": (
        "Bridge Michigan: Terence Collins, the Republican nominee, is a senior financial analyst at General Motors. A compiled voter guide says he was appointed to the Grosse Pointe Public Schools board in 2023 and lost a bid for a full term in 2024.",
        L(("Bridge Michigan", SBE_NEWS), ("Campaign site", "https://collins4misboe.com")),
    ),
    "race-22|Bree Moeggenberg": (
        "Bridge Michigan: Bree Moeggenberg, the Republican nominee, is a recruiter for a canvassing company and a licensed child-care provider from Mt. Pleasant.",
        L(("Bridge Michigan", SBE_NEWS), ("Campaign site", "https://www.bree4misboe.com")),
    ),
    "race-22|Charles Essner": (
        "A compiled voter guide describes Libertarian nominee Charles Essner as managing partner of a machining shop in Oxford and a former manufacturing engineer. No campaign site was found.",
        L(("Candidate guide", SBE_GUIDE)),
    ),
    "race-22|William Mohr II": (
        "A compiled voter guide lists U.S. Taxpayers nominee William Mohr II in Kent City and reports earlier campaigns for the Wayne State board, the Kent City school board, and Tyrone Township trustee. No 2026 campaign site was found.",
        L(("Candidate guide", SBE_GUIDE)),
    ),
    "race-22|Christine C. Schwartz": (
        "A compiled voter guide says U.S. Taxpayers nominee Christine C. Schwartz served four terms on the Hopkins Public Schools board and has been the party’s nominee for statewide education offices before.",
        L(("Candidate guide", SBE_GUIDE)),
    ),
    "race-22|Wissam Charafeddine": (
        "A compiled voter guide describes Green nominee Wissam Charafeddine as a family-engagement liaison at Hamadeh Educational Services.",
        L(("Campaign site", "https://charafeddine2026.com"), ("Candidate guide", SBE_GUIDE)),
    ),
    "race-22|Mary Anne Hering": (
        "A compiled voter guide describes Working Class nominee Mary Anne Hering as a retired social-sciences instructor who taught for decades at Henry Ford College, and as the party’s nominee for this board in several recent elections.",
        L(("Working Class Party", "https://workingclassfight.com"), ("Candidate guide", SBE_GUIDE)),
    ),
    "race-23|Paul Brown": (
        "Michigan Public: Paul Brown is an incumbent University of Michigan regent and a Democratic nominee. A compiled voter guide lists him as managing partner of eLab Ventures.",
        L(("Michigan Public", UM_NEWS), ("Campaign site", "https://gobluevotebrown.com")),
    ),
    "race-23|Amir Makled": (
        "Michigan Public: Amir Makled is a civil-rights attorney and a Democratic nominee. He defeated incumbent regent Jordan Acker for the nomination. Acker is not on this ballot.",
        L(("Michigan Public", UM_NEWS), ("Campaign site", "https://amirmakled.com")),
    ),
    "race-23|Lena Epstein": (
        "Michigan Public: Lena Epstein, a Republican nominee, is co-owner of Vesco Oil Corporation. She was the Republican nominee for this board in 2022 and the 2018 Republican nominee for Congress in Michigan’s 11th District.",
        L(("Michigan Public", UM_NEWS), ("Campaign site", "https://lenaforuofm.com/")),
    ),
    "race-23|Michael Schostak": (
        "Michigan Public: Michael Schostak, a Republican nominee, is treasurer of Bloomfield Township and a former finance lecturer at Wayne State. A compiled voter guide says he leads Schostak Capital Advisors.",
        L(("Michigan Public", UM_NEWS), ("Campaign site", "https://michaelschostak.com")),
    ),
    "race-23|Andrew Chadderdon": (
        "A compiled voter guide says Libertarian nominee Andrew Chadderdon was also the party’s nominee for this board in 2024. No campaign platform was found.",
        L(("Candidate guide", UNIV)),
    ),
    "race-23|Kyle Maas": (
        "A compiled voter guide lists U.S. Taxpayers nominee Kyle Maas in Byron Center and says he took part in a University of Michigan faculty-senate forum. No campaign site was found.",
        L(("Candidate guide", UNIV)),
    ),
    "race-24|Brianna Scott": (
        "Michigan Public: Brianna Scott is chair of the MSU Board of Trustees and a Democratic nominee seeking another term. She is a Muskegon attorney and an MSU alumna.",
        L(("Michigan Public", MSU_NEWS), ("Campaign site", "https://brianna4msu.com")),
    ),
    "race-24|Kelly Tebay Zemke": (
        "Michigan Public: Kelly Tebay Zemke is an incumbent MSU trustee and director of government and external relations at The Henry Ford in Dearborn. She is a Democratic nominee. Ballotpedia shortens her name to Kelly Tebay.",
        L(("Michigan Public", MSU_NEWS), ("Campaign site", "https://kellyformsu.com")),
    ),
    "race-24|Julie Maday": (
        "Michigan Public: Julie Maday, a Republican nominee, is a former Novi City Council member. She ran for this board in 2024 and lost by fewer than 5,000 votes.",
        L(("Michigan Public", MSU_NEWS), ("Campaign site", "https://juliemadayformsu.org")),
    ),
    "race-24|Roger Victory": (
        "Michigan Public: Roger Victory is a Republican state senator from Hudsonville and owner of Victory Farms. He is term-limited in the Senate at the end of 2026 and is a Republican nominee for this board.",
        L(("Michigan Public", MSU_NEWS), ("Wikipedia", WIKI["victory"])),
    ),
    "race-24|Will Tyler White": (
        "Libertarian nominee Will Tyler White’s campaign site describes him as an MSU student and emphasizes budget management, affordability, and online courses.",
        L(("Campaign site", "https://willtylerwhite.org")),
    ),
    "race-24|John Sanger": (
        "A compiled voter guide says U.S. Taxpayers nominee John Sanger, of Litchfield, has run for this board several times. No 2026 campaign platform was found.",
        L(("Candidate guide", UNIV)),
    ),
    "race-24|John Anthony La Pietra": (
        "A compiled voter guide describes Green nominee John Anthony La Pietra as an attorney from Marshall who has run for this board and other offices before.",
        L(("Candidate guide", UNIV)),
    ),
    "race-25|Shereef Akeel": (
        "MLive: Shereef Akeel, a Democratic nominee, is a civil-rights attorney, a certified public accountant, and a Wayne State alumnus.",
        L(("MLive", WSU), ("Campaign site", "https://akeelforwsu.com")),
    ),
    "race-25|Richard Mack": (
        "MLive: Richard Mack, a Democratic nominee, is a union-side labor and employment attorney and a Wayne State law graduate.",
        L(("MLive", WSU), ("Campaign site", "https://richardmackforwsu.com")),
    ),
    "race-25|Andy Anuzis": (
        "A compiled voter guide says Republican nominee Andy Anuzis is principal of Lincoln-King High School. It also says he previously led Cornerstone Schools in Detroit.",
        L(("Candidate guide", UNIV), ("Campaign site", "https://andyforwaynestate.com")),
    ),
    "race-25|Christa Murphy": (
        "MLive: Christa Murphy, a Republican nominee, is a technology executive. A compiled voter guide describes work at Meta, Samsung, and General Motors, and an earlier run for this board in 2022.",
        L(("MLive", WSU), ("Campaign site", "https://murphyforwaynestate.com")),
    ),
    "race-25|Jami Van Alstine": (
        "A compiled voter guide says Libertarian nominee Jami Van Alstine listed the occupation of system administrator in a prior local campaign. No 2026 campaign platform was found.",
        L(("Candidate guide", UNIV)),
    ),
    "race-25|Suzanne Roehrig": (
        "MLive: Suzanne Roehrig, the Working Class nominee, is a retired teacher and librarian with three degrees from Wayne State.",
        L(("MLive", WSU), ("Working Class Party", "https://workingclassfight.com")),
    ),
    "race-25|Kathleen Oakford": (
        "A compiled voter guide says Natural Law nominee Kathleen Oakford ran for this board in 2024 and for University of Michigan regent in 2022. No 2026 campaign platform was found.",
        L(("Candidate guide", UNIV)),
    ),
    "race-31|Megan Kathleen Cavanagh": (
        "Michigan Public: Megan Cavanagh is chief justice, a justice since 2019, and the Democratic nominee. Before the court she was an appellate attorney in private practice. The Michigan Manual says she became chief justice in 2025.",
        L(("Michigan Public", MSC), ("Michigan Manual", MANUAL)),
    ),
    "race-31|Noah P. Hood": (
        "Michigan Public: Noah Hood was appointed to the Supreme Court in May 2025 by Governor Gretchen Whitmer and is the Democratic nominee for a full term. He previously was a Court of Appeals judge, a Wayne County circuit judge, and a federal prosecutor.",
        L(("Michigan Public", MSC), ("Wikipedia", WIKI["hood"])),
    ),
    "race-31|Thomas W. Howe": (
        "Bridge Michigan: Thomas Howe, the U.S. Taxpayers nominee, is a retired engineer and does not have a law degree. The Michigan Constitution requires a justice to be a licensed lawyer with at least five years of practice. News outlets report he can appear on the ballot but could not take office if elected.",
        L(("Bridge Michigan", BRIDGE), ("Michigan Public", MSC)),
    ),
    "race-31|Casandra Morse-Bills": (
        "Michigan Public: Casandra Morse-Bills is the presiding judge of the 23rd Circuit Court, elected in 2018 and re-elected in 2024, and a former prosecutor. She is a Republican nominee. No party is printed on the ballot.",
        L(("Michigan Public", MSC)),
    ),
    "race-31|Michael Warren": (
        "Michigan Public: Michael Warren has been an Oakland County circuit judge since 2002 and is the Republican nominee. He has taught constitutional law and served on the State Board of Education from 1999 to 2002. He said the Libertarian Party endorsed him but could not nominate him, because Michigan does not allow two parties to nominate the same candidate.",
        L(("Michigan Public", MSC), ("Bridge Michigan", BRIDGE)),
    ),
    "race-31|Jody White": (
        "Bridge Michigan: Jody White, the U.S. Taxpayers nominee, is a real-estate broker and does not have a law degree. As with Thomas Howe, news outlets report she can appear on the ballot but could not take office if elected.",
        L(("Bridge Michigan", BRIDGE), ("Michigan Public", MSC)),
    ),
    "race-32|Mark T. Boonstra": (
        "Incumbent judge of the Michigan Court of Appeals, 3rd District. The county list shows no challenger for this seat. A current biography was not copied into this guide; the court’s judge directory is the place to confirm the official bio.",
        L(("Court of Appeals judges", "https://www.courts.michigan.gov/courts/court-of-appeals/judges/")),
    ),
    "race-32|Daniel S. Korobkin": (
        "Incumbent judge of the Michigan Court of Appeals, 3rd District. The county list shows no challenger for this seat. A current biography was not copied into this guide; the court’s judge directory is the place to confirm the official bio.",
        L(("Court of Appeals judges", "https://www.courts.michigan.gov/courts/court-of-appeals/judges/")),
    ),
    "race-33|Maureen A. Gottlieb": (
        "A professional biography: Maureen Gottlieb has been a 17th Circuit Court judge in the Family Division since January 2021. Her earlier career was in family law, mostly at Legal Aid of Western Michigan, and she was a circuit-court referee before joining the bench.",
        L(("Professional biography", "https://www.icle.org/modules/directories/contributors/bio.aspx?Pnumber=P71673")),
    ),
    "race-33|Scott A. Noto": (
        "Kent County: Scott Noto was elected in November 2020. He practiced civil and criminal law and has been an Army judge advocate since 2009. He earned a B.A. from the University of Chicago and a law degree from Loyola University Chicago.",
        L(("Kent County biography", "https://www.kentcountymi.gov/m/directory/employee?eid=40")),
    ),
    "race-33|Clay M. West": (
        "Kent County: Clay West joined the 17th Circuit Court in April 2023. He was a federal prosecutor and an Army judge advocate, and he clerked for federal and California appellate judges. He earned degrees from Harvard, Cambridge, and Yale Law School.",
        L(("Kent County biography", "https://www.kentcountymi.gov/m/directory/employee?eid=34")),
    ),
    "race-34|David M. Murkowski": (
        "Kent County: David Murkowski is the incumbent probate judge. The county biography says he grew up in Milwaukee, graduated from Marquette University and Cooley Law School, and practiced law in Grand Rapids.",
        L(("Kent County biography", "https://www.kentcountymi.gov/1432/Judges")),
    ),
    "race-38|Jeffrey J. O'Hara": (
        "Kent County: Jeffrey O’Hara is chief judge of the 63rd District Court. He graduated from Michigan State University, earned his law degree from Cooley Law School in 1985, practiced as a trial attorney, and was elected in 2014.",
        L(("Kent County biography", "https://www.kentcountymi.gov/1436/Judges")),
    ),
    "race-39|Kirsten L. Holz": (
        "Kent County: Kirsten Holz was appointed to the 63rd District Court by Governor Gretchen Whitmer in 2024. This race is the rest of a term ending January 1, 2029. She earned degrees from Cornell and a law degree from American University in 2007.",
        L(("Kent County biography", "https://www.kentcountymi.gov/m/directory/employee?eid=575")),
    ),
    "race-40|Jamie Gordon": (
        "Ottawa News Network: Jamie Gordon was appointed to the GRCC board in May 2026 for a term ending December 31, 2026, and is running for a full term. She is executive director of human resources for Kentwood Public Schools and previously spent 23 years at Grand Rapids Public Schools.",
        L(("Ottawa News Network", GRCC), ("GRCC directory", "https://www.grcc.edu/faculty-staff/directory/jamie-gordon")),
    ),
    "race-40|Brandy Lovelady Mitchell": (
        "Ottawa News Network: Brandy Lovelady Mitchell was elected to the GRCC board in 2020 for a term ending December 31, 2026. She is a deputy superintendent at Grand Rapids Public Schools and earlier worked at what is now Network 180.",
        L(("Ottawa News Network", GRCC), ("GRCC directory", "https://www.grcc.edu/faculty-staff/directory/brandy-lovelady-mitchell")),
    ),
    "race-40|Tim Russ": (
        "Ottawa News Network: Tim Russ is a Michigan Education Association representative and community organizer, and second vice chair of the Grand Rapids Township Democrats. He is not described as a current trustee.",
        L(("Ottawa News Network", GRCC)),
    ),
    "race-41|Adriana Almanza": (
        "Ottawa News Network: Adriana Almanza is the only candidate listed for the partial term ending December 31, 2030. She has worked about 16 years in education and human resources, including about 12 years in K–12 and higher education. Little else was published.",
        L(("Ottawa News Network", GRCC)),
    ),
    "race-71|Jeff Black": (
        "Byron Center Public Schools questionnaire: Jeff Black is an estate-planning, probate, and business attorney at Mika Meyers and a Byron Center parent. His firm biography says he previously clerked for the Kent County Circuit Court. He is not on the current board roster.",
        L(("Mika Meyers biography", MIKA)),
    ),
    "race-71|Shannon Smith": (
        "Byron Center Public Schools questionnaire: Shannon Smith is a licensed professional counselor and certified rehabilitation counselor who owns a counseling practice. She is a Byron Center parent and is not on the current board roster.",
        [],
    ),
    "race-71|Amber Swift": (
        "The district roster lists Amber Swift as board vice president. In the district questionnaire she describes herself as a former business owner who worked as a chief financial officer and human-resources manager, and as a parent seeking another term.",
        L(("Community Q&A", WEAREBC)),
    ),
    "race-71|Thalia Tilma": (
        "The district roster lists Thalia Tilma as board secretary. In the questionnaire she says she is a current member, that her husband’s family has long roots in Byron Center, and that her priorities include academics, parent involvement, and spending.",
        [],
    ),
    "race-71|Ashley Upchurch": (
        "Byron Center Public Schools questionnaire: Ashley Upchurch works in marketing and is a Byron Center parent of elementary students. She is not on the current board roster. She says her priorities are family-school partnerships, keeping educators, and preparing students for different paths after graduation.",
        [],
    ),
    "race-71|Brad Wiechertjes": (
        "The district roster lists Brad Wiechertjes as treasurer. In the questionnaire he says his family has lived in Byron Center for more than 20 years and that he directs advancement for a nonprofit serving Deaf communities. His wife is a special-education teacher.",
        L(("Community Q&A", WEAREBC)),
    ),
}


def merge_links(existing, extra):
    seen = {item["url"] for item in existing}
    for item in extra:
        if item["url"] not in seen:
            existing.append(item)
            seen.add(item["url"])
    return existing


def embed_ballot(ballot):
    if not OUT.exists():
        return
    html = OUT.read_text()
    start_tag = '<script type="application/json" id="ballot-data">'
    start = html.find(start_tag)
    if start == -1:
        print("index.html has no embedded ballot; left the page unchanged")
        return
    start_inner = start + len(start_tag)
    end = html.find("</script>", start_inner)
    if end == -1:
        raise SystemExit("ballot-data script is not closed")
    payload = json.dumps(ballot, ensure_ascii=False).replace("<", "\\u003c")
    OUT.write_text(html[:start_inner] + "\n" + payload + "\n" + html[end:])


def main():
    if not BALLOT_OUT.exists():
        raise SystemExit(f"Missing {BALLOT_OUT}")
    ballot = json.loads(BALLOT_OUT.read_text())
    applied = []
    missing = []
    for race in ballot:
        for cand in race.get("candidates") or []:
            key = f"{race['id']}|{cand['name']}"
            if key not in NOTES:
                continue
            note, links = NOTES[key]
            cand["note"] = note
            cand["links"] = merge_links(list(cand.get("links") or []), links)
            applied.append(key)
    known = {f"{r['id']}|{c['name']}" for r in ballot for c in r.get("candidates") or []}
    for key in NOTES:
        if key not in known:
            missing.append(key)
    if missing:
        raise SystemExit("Enrichment keys not on the ballot:\n" + "\n".join(missing))

    for race in ballot:
        if race["id"] == "race-31" and "law license" not in race.get("note", ""):
            race["note"] = (
                race.get("note", "").rstrip()
                + " Bridge Michigan reports that two U.S. Taxpayers nominees do not have law degrees. The state constitution requires a justice to be a licensed lawyer with at least five years of practice. They can appear on the ballot; news outlets report they could not take office if elected."
            )

    BALLOT_OUT.parent.mkdir(parents=True, exist_ok=True)
    BALLOT_OUT.write_text(json.dumps(ballot, indent=2, ensure_ascii=False) + "\n")
    embed_ballot(ballot)
    if SERVE.parent.exists():
        shutil.copyfile(OUT, SERVE)
    print(f"Updated {len(applied)} candidate profiles")
    print(f"Wrote {BALLOT_OUT}")


if __name__ == "__main__":
    main()
