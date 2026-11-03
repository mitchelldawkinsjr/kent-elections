#!/usr/bin/env python3
"""Add Inkster City Ward 1 Precinct 1 (ZIP 48141) and its November 3, 2026 contests.

Source: Michigan Voter Information Center public sample ballot for
Wayne County · Inkster City · Ward 1, Precinct 1. Address check for
29475 Carlysle St, Inkster MI 48141 maps to that precinct (Floyd B. Simmons
Center) and Romulus Community Schools.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BALLOT = ROOT / "data" / "ballot.json"
PRECINCTS = ROOT / "data" / "precincts.json"
INDEX = ROOT / "index.html"

MVIC = "https://mvic.sos.state.mi.us/"
MVIC_BALLOT = "https://mvic.sos.state.mi.us/PublicBallot/Index"
GIST = "https://thegist.vote/mi/wayne-county/inkster"
INKSTER_POLL = "https://www.cityofinkstermi.gov/607/Polling-Location"
WAYNE_ELECTION = (
    "https://www.waynecountymi.gov/Government/Elected-Officials/Clerk/"
    "Elections/Election-Results-Candidates/November-3rd-2026-General-Election"
)

SRC_MVIC = {"label": "Michigan Voter Information Center sample ballot", "url": MVIC_BALLOT}
SRC_WAYNE = {"label": "Wayne County November 3, 2026 election page", "url": WAYNE_ELECTION}
SRC_GIST = {"label": "The Gist: City of Inkster 2026", "url": GIST}
SRC_POLL = {"label": "City of Inkster polling places", "url": INKSTER_POLL}


def cand(name, party, status="Ballot-listed", **extra):
    out = {
        "name": name,
        "party": party,
        "status": status,
        "filing": "Inkster City Ward 1 Precinct 1 sample ballot, Michigan Voter Information Center, November 3, 2026.",
        "links": [SRC_MVIC, SRC_GIST],
    }
    out.update(extra)
    return out


def office(**kwargs):
    base = {
        "type": "Office",
        "candidates": [],
        "sources": [SRC_MVIC, SRC_WAYNE, SRC_GIST],
        "note": "Candidates and the vote limit are from the Inkster City Ward 1 Precinct 1 sample ballot on the Michigan Voter Information Center for November 3, 2026.",
    }
    base.update(kwargs)
    return base


def proposal(**kwargs):
    base = {
        "section": "Ballot proposals",
        "term": "See official wording",
        "voteLimit": 1,
        "type": "Proposal",
        "candidates": [],
        "sources": [SRC_MVIC, SRC_WAYNE, SRC_GIST],
    }
    base.update(kwargs)
    return base


NEW_RACES = [
    office(
        id="race-100",
        section="Congress",
        title="Representative in Congress - 12th District",
        jurisdiction="12th District",
        term="2 Year Term",
        voteLimit=1,
        scope="congress-12",
        candidates=[
            cand("Rashida Tlaib", "Democratic", "Incumbent", note="Incumbent U.S. representative for Michigan’s 12th District."),
            cand("James D. Hooper", "Republican"),
            cand("Marc Joseph Sosnowski", "U.S. Taxpayers"),
            cand("Brenda K. Sanders", "Green"),
            cand("Gary Walkowicz", "Working Class"),
        ],
    ),
    office(
        id="race-101",
        section="Legislature",
        title="State Senator - 5th District",
        jurisdiction="5th District",
        term="4 Year Term",
        voteLimit=1,
        scope="senate-5",
        candidates=[
            cand("Matt Koleszar", "Democratic"),
            cand("Estelle Oliansky", "Republican"),
        ],
    ),
    office(
        id="race-102",
        section="Legislature",
        title="State Representative - 26th District",
        jurisdiction="26th District",
        term="2 Year Term",
        voteLimit=1,
        scope="house-26",
        candidates=[
            cand("Dylan Wegela", "Democratic"),
            cand("Chris Dobis", "Republican"),
        ],
    ),
    office(
        id="race-103",
        section="County",
        title="Wayne County Executive",
        jurisdiction="Wayne County",
        term="4 Year Term",
        voteLimit=1,
        scope="wayne",
        candidates=[
            cand("Warren C. Evans", "Democratic", "Incumbent"),
            cand("Michael A. Evans", "Republican"),
            cand("John Olumba", "No Party Affiliation"),
        ],
    ),
    office(
        id="race-104",
        section="Judicial",
        title="Judge of Court of Appeals - 1st District - Incumbent",
        jurisdiction="Michigan",
        term="6 Year Term",
        voteLimit=3,
        scope="appeals-1",
        note="Nonpartisan. The sample ballot lists three incumbents for three seats on the 1st District Court of Appeals.",
        candidates=[
            cand("Mariam Saad Bazzi", "Nonpartisan", "Incumbent"),
            cand("Anica Letica", "Nonpartisan", "Incumbent"),
            cand("Christopher M. Murray", "Nonpartisan", "Incumbent"),
        ],
    ),
    office(
        id="race-105",
        section="Judicial",
        title="Judge of Court of Appeals - 1st District - Incumbent — partial term ending 01/01/2031",
        jurisdiction="Michigan",
        term="Partial Term Ending 01/01/2031",
        voteLimit=1,
        scope="appeals-1",
        note="Nonpartisan. Partial term for the 1st District Court of Appeals.",
        candidates=[
            cand("Andrew J. Lievense", "Nonpartisan", "Incumbent"),
        ],
    ),
    office(
        id="race-106",
        section="Judicial",
        title="Judge of Circuit Court - 3rd Circuit - Incumbent",
        jurisdiction="Wayne County",
        term="6 Year Term",
        voteLimit=16,
        scope="wayne",
        note="Nonpartisan. The sample ballot lists sixteen incumbents for sixteen seats on the 3rd Circuit Court.",
        candidates=[
            cand("David J. Allen", "Nonpartisan", "Incumbent"),
            cand("Chandra W. Baker-Robinson", "Nonpartisan", "Incumbent"),
            cand("Christopher M. Blount", "Nonpartisan", "Incumbent"),
            cand("Nicole L. Castka", "Nonpartisan", "Incumbent"),
            cand("Bradley L. Cobb", "Nonpartisan", "Incumbent"),
            cand("Chris Dingell", "Nonpartisan", "Incumbent"),
            cand("Charlene M. Elder", "Nonpartisan", "Incumbent"),
            cand("Helal A. Farhat", "Nonpartisan", "Incumbent"),
            cand("Nicole N. Goodson", "Nonpartisan", "Incumbent"),
            cand("Edward J. Joseph", "Nonpartisan", "Incumbent"),
            cand("Mary Beth Kelly", "Nonpartisan", "Incumbent"),
            cand("Don Knapp", "Nonpartisan", "Incumbent"),
            cand("Cylenthia LaToye Miller", "Nonpartisan", "Incumbent"),
            cand("Carla G. Testani", "Nonpartisan", "Incumbent"),
            cand("Margaret M. Van Houten", "Nonpartisan", "Incumbent"),
            cand("Shannon Nicol Walker", "Nonpartisan", "Incumbent"),
        ],
    ),
    office(
        id="race-107",
        section="Judicial",
        title="Judge of Circuit Court - 3rd Circuit - Incumbent — partial term ending 01/01/2031",
        jurisdiction="Wayne County",
        term="Partial Term Ending 01/01/2031",
        voteLimit=1,
        scope="wayne",
        note="Nonpartisan. Partial term for the 3rd Circuit Court.",
        candidates=[
            cand("Aliyah S. Sabree", "Nonpartisan", "Incumbent"),
        ],
    ),
    office(
        id="race-108",
        section="Judicial",
        title="Judge of Circuit Court - 3rd Circuit - Non-incumbent",
        jurisdiction="Wayne County",
        term="6 Year Term",
        voteLimit=1,
        scope="wayne",
        note="Nonpartisan. Non-incumbent seat on the 3rd Circuit Court.",
        candidates=[
            cand("Shakira Lynn Hawkins", "Nonpartisan"),
        ],
    ),
    office(
        id="race-109",
        section="Judicial",
        title="Judge of Probate Court - Wayne - Non-incumbent",
        jurisdiction="Wayne County",
        term="See official ballot",
        voteLimit=3,
        scope="wayne",
        note="Nonpartisan. The sample ballot lists three candidates for three non-incumbent probate seats.",
        candidates=[
            cand("Sarah Colegrove", "Nonpartisan"),
            cand("Suzanne Fanning", "Nonpartisan"),
            cand("Vanessa M. Moss", "Nonpartisan"),
        ],
    ),
    office(
        id="race-110",
        section="School boards",
        title="Board Member Romulus Community Schools",
        jurisdiction="Romulus Community Schools",
        term="4 Year Term",
        voteLimit=4,
        scope="school-romulus",
        candidates=[
            cand("Darcel C. Davis", "Nonpartisan"),
            cand("Antoine D. Jackson", "Nonpartisan"),
            cand("Porsche A. Laster", "Nonpartisan"),
            cand("Ursula L. Rogers", "Nonpartisan"),
            cand("Nychole Smith", "Nonpartisan"),
        ],
    ),
    proposal(
        id="proposal-5",
        title="Wayne County Zoological Authority millage",
        jurisdiction="Wayne County",
        officialText=(
            "In 2008 and 2016, pursuant to Public Act 49 of 2008, Wayne County voters renewed a "
            "10-year property tax millage to fund zoological services through the Wayne County "
            "Zoological Authority, supporting animal care for more than 2,000 animals and 200 "
            "species, educational and senior programs, and facility maintenance at the Detroit Zoo. "
            "To continue providing these services, the Authority seeks to renew and restore the "
            "millage to the original voter-approved rate of 0.10 mill (10 cents per $1,000 of "
            "taxable value). This proposal would renew the millage at 0.0982 mill and restore the "
            "remaining 0.0018 mill that was reduced due to required rollback, for a total "
            "authorized rate of 0.10 mill on taxable real and personal property for ten (10) years. "
            "If approved, the millage rate would be unchanged from those approved by voters in "
            "2008 and 2016. Funds will be disbursed to the Authority and transferred to the Detroit "
            "Zoo as permitted by law. All funds are subject to annual independent audits. It is "
            "estimated that $6,145,462 will be collected in the first year. Ballot Question: Do you "
            "approve the renewal and restoration of the levy of 0.10 mill on all taxable property "
            "in Wayne County for a period of ten (10) years, from 2028 through 2037?"
        ),
        plainEnglish=[
            "This asks Wayne County voters to renew the Detroit Zoo millage through the Wayne County Zoological Authority.",
            "The rate would be restored to 0.10 mill, which is $0.10 for every $1,000 of taxable value, each year from 2028 through 2037.",
            "The money supports animal care, educational and senior programs, and facility maintenance at the Detroit Zoo.",
            "The Authority estimates about $6,145,462 in the first year.",
        ],
        summary=(
            "Wayne County asks voters to renew and restore 0.10 mill for the Detroit Zoo from "
            "2028 through 2037. The dollar lines above follow the taxable value entered on this page."
        ),
        taxImpact={
            "kicker": "From your taxable value",
            "detail": [
                "A yes vote renews the zoo millage at up to 0.10 mill for 2028 through 2037. A no vote rejects the renewal."
            ],
        },
        levy={
            "kind": "renewal",
            "name": "Wayne County Zoological Authority",
            "proposedMills": 0.10,
            "baselineMills": 0.0982,
            "proposedSpan": "each year from 2028 through 2037",
            "baselineSpan": "the current rolled-back rate before restoration",
        },
        scope="wayne",
    ),
    proposal(
        id="proposal-6",
        title="Southeast Michigan Public Historical Museum Authority millage",
        jurisdiction="Wayne County",
        officialText=(
            "The Southeast Michigan Public Historical Museum Authority (“Authority”) is a joint "
            "authority established by Wayne and Oakland Counties (“Counties”) pursuant to Michigan "
            "Public Act 321 of the Public Acts of 2000, as amended, and was formed to support the "
            "Charles H. Wright Museum of African American History, Detroit Historical Museum, "
            "Dossin Great Lakes Museum, and other public historical museums located in Wayne and "
            "Oakland Counties (“Historical Museums”) that provide historical museum services for "
            "students, residents and visitors of the Counties. The law allows the Authority to seek "
            "authorization from the electors in each of the Counties to levy a tax of 0.2 mill "
            "(20 cents per $1,000 of taxable value) on taxable property to provide revenue for "
            "Historical Museums. It is estimated that if approved and levied on taxable property "
            "located within Wayne County, this new millage would generate approximately $12,219,200 "
            "in 2026. In addition to supporting the Charles H. Wright Museum of African American "
            "History, Detroit Historical Museum, and Dossin Great Lakes Museum, 15% of revenues "
            "received by the Authority from taxable property in Wayne County, after Authority "
            "administrative expenses, will be disbursed to the County of Wayne for the purposes of "
            "supporting Historical Museums in Wayne County. Shall a 0.2 mill tax on all taxable "
            "property located within Wayne County be imposed by the Authority for a period of ten "
            "(10) years, being years 2026 through 2035, inclusive, to provide historical museum "
            "services for the benefit of the residents of the Counties?"
        ),
        plainEnglish=[
            "This asks Wayne County voters to approve a new property tax for historical museums.",
            "The tax would be 0.2 mill, which is $0.20 for every $1,000 of taxable value, each year from 2026 through 2035.",
            "Money would support the Charles H. Wright Museum of African American History, the Detroit Historical Museum, the Dossin Great Lakes Museum, and other local historical museums. After administrative costs, 15% of Wayne County revenue would go to Wayne County for other historical museums in the county.",
            "The Authority estimates about $12,219,200 from Wayne County property in 2026.",
        ],
        summary=(
            "Wayne County asks voters to levy a new 0.2 mill for historical museum services from "
            "2026 through 2035. The dollar lines above follow the taxable value entered on this page."
        ),
        taxImpact={
            "kicker": "From your taxable value",
            "detail": [
                "A yes vote adds a new 0.2 mill tax for 2026 through 2035. A no vote rejects the new tax."
            ],
        },
        levy={
            "kind": "new",
            "name": "Historical museums",
            "proposedMills": 0.2,
            "baselineMills": 0,
            "proposedSpan": "each year from 2026 through 2035",
            "baselineSpan": "no current levy under this proposal",
        },
        scope="wayne",
    ),
    proposal(
        id="proposal-7",
        title="Inkster parks and recreation millage",
        jurisdiction="City of Inkster",
        officialText=(
            "Shall the City of Inkster, Wayne County, Michigan be authorized and empowered to levy "
            "a general valorem property tax which in any one year shall not exceed 2.0 mills "
            "(2.0 mills per $1,000.00 of State Equalized Valuation for ten (10) years, 2027 to 2036? "
            "The continuation of the dedicated Millage for Parks and Recreation Operations, which "
            "include Youth and Senior Programs, is up to 2.0 mills. It has been determined that up "
            "to 2.0 mills is necessary to operate these programs and to continue the current level "
            "of service. General Fund dollars are not available to support these programs. The "
            "average cost to a homeowner is estimated to be $54 and would generate an estimated "
            "$580,000 if the maximum allowable millage is levied."
        ),
        plainEnglish=[
            "This asks Inkster voters to renew a dedicated parks and recreation millage, including youth and senior programs.",
            "The rate would be up to 2.0 mills for ten years, 2027 through 2036. The printed wording measures the millage against State Equalized Valuation; the dollar estimate on the ballot is about $54 for an average homeowner.",
            "The city estimates about $580,000 a year if the full millage is levied. City notes say general-fund dollars are not available to keep these programs at the current level without the millage.",
        ],
        summary=(
            "Inkster asks voters to renew up to 2.0 mills for parks and recreation, including youth "
            "and senior programs, for 2027 through 2036. The official wording uses State Equalized "
            "Valuation; the calculator on this page still prices mills against the taxable value you enter."
        ),
        taxImpact={
            "kicker": "From your taxable value",
            "detail": [
                "The official ballot measures this millage against State Equalized Valuation. The estimate printed on the ballot is about $54 for an average homeowner."
            ],
        },
        levy={
            "kind": "renewal",
            "name": "Inkster parks and recreation",
            "proposedMills": 2.0,
            "baselineMills": 2.0,
            "proposedSpan": "each year from 2027 through 2036",
            "baselineSpan": "the current parks and recreation millage",
        },
        scope="inkster",
    ),
    proposal(
        id="proposal-8",
        title="Inkster senior services millage",
        jurisdiction="City of Inkster",
        officialText=(
            "Shall the City of Inkster, Wayne County, Michigan be authorized and empowered to levy "
            "a general valorem property tax which in any one year shall not exceed 1.0 mills "
            "(1.0 mills per $1,000.00 of State Equalized Valuation for ten (10) years, 2027 to 2036? "
            "The continuation of the dedicated Millage for Senior Services Operations is up to "
            "1.0 mills. It has been determined that up to 1.0 mills is necessary to operate this "
            "program and to continue the current level of service. General Fund dollars are not "
            "available to support these programs. The average cost to a homeowner is estimated to "
            "be $27 and would generate an estimated $290,000 if the maximum allowable amount is "
            "levied in any year."
        ),
        plainEnglish=[
            "This asks Inkster voters to renew a dedicated senior-services millage.",
            "The rate would be up to 1.0 mill for ten years, 2027 through 2036. The printed wording measures the millage against State Equalized Valuation; the dollar estimate on the ballot is about $27 for an average homeowner.",
            "The city estimates about $290,000 a year if the full millage is levied.",
        ],
        summary=(
            "Inkster asks voters to renew up to 1.0 mill for senior services for 2027 through 2036. "
            "The official wording uses State Equalized Valuation; the calculator on this page still "
            "prices mills against the taxable value you enter."
        ),
        taxImpact={
            "kicker": "From your taxable value",
            "detail": [
                "The official ballot measures this millage against State Equalized Valuation. The estimate printed on the ballot is about $27 for an average homeowner."
            ],
        },
        levy={
            "kind": "renewal",
            "name": "Inkster senior services",
            "proposedMills": 1.0,
            "baselineMills": 1.0,
            "proposedSpan": "each year from 2027 through 2036",
            "baselineSpan": "the current senior services millage",
        },
        scope="inkster",
    ),
    proposal(
        id="proposal-9",
        title="Romulus Community Schools operating millage renewal",
        jurisdiction="Romulus Community Schools",
        officialText=(
            "This proposal will allow the school district to levy millage previously authorized to "
            "be levied on all property, except property exempted by law and renews hold harmless "
            "millage that expired with the 2026 tax levy. Shall the total limitation on the hold "
            "harmless mills used for operating purposes which may be assessed against all property, "
            "except property exempted by law, in Romulus Community Schools, Wayne County, Michigan, "
            "be increased by 2.5 mills ($2.50 on each $1,000 of taxable valuation) for a period of "
            "10 years, 2027 to 2036, inclusive; the estimate of the revenue the school district "
            "will collect from hold harmless taxes authorized herein if the millage is approved "
            "and levied in 2027 is approximately $745,254 (this is a renewal of previously "
            "authorized millage that expired with the 2026 tax levy)?"
        ),
        plainEnglish=[
            "This asks Romulus Community Schools voters to renew a hold-harmless operating millage.",
            "The rate would be 2.5 mills, which is $2.50 for every $1,000 of taxable value, each year from 2027 through 2036, on property that is not exempted by law.",
            "The district estimates about $745,254 in 2027 if the millage is approved and levied. The ballot says this renews millage that expired with the 2026 tax levy.",
        ],
        summary=(
            "Romulus Community Schools asks voters to renew 2.5 mills of hold-harmless operating "
            "millage for 2027 through 2036. The dollar lines above follow the taxable value entered "
            "on this page."
        ),
        taxImpact={
            "kicker": "From your taxable value",
            "detail": [
                "A yes vote renews 2.5 mills for 2027 through 2036. A no vote rejects the renewal."
            ],
        },
        levy={
            "kind": "renewal",
            "name": "Romulus hold-harmless operating",
            "proposedMills": 2.5,
            "baselineMills": 0,
            "proposedSpan": "each year from 2027 through 2036",
            "baselineSpan": "expired with the 2026 tax levy",
        },
        scope="school-romulus",
    ),
]

INKSTER_PRECINCT = {
    "id": "inkster-city-ward-1-precinct-1",
    "name": "Inkster City, Ward 1, Precinct 1",
    "municipality": "Inkster City",
    "zips": ["48141"],
    "scopes": [
        "statewide",
        "wayne",
        "appeals-1",
        "congress-12",
        "senate-5",
        "house-26",
        "school-romulus",
        "inkster",
    ],
    "school": "Romulus Community Schools",
    "explained": ["district-"],
    "notices": [
        "Polling place for this precinct: Floyd B. Simmons Center, 29150 Carlysle St, Inkster. "
        "No 22nd District Court judge appears on the November 3, 2026 sample ballot for this precinct."
    ],
    "districts": [
        ["County", "Wayne County"],
        ["Jurisdiction", "Inkster City"],
        ["Ward", "1"],
        ["Precinct", "1"],
        ["U.S. Congress", "12th District"],
        ["Court of appeals", "1st District"],
        ["Circuit court", "3rd Circuit"],
        ["Probate court", "Wayne County Probate Court"],
        ["District court", "22nd District"],
        ["State house", "26th District"],
        ["State senate", "5th District"],
        ["School", "Romulus Community Schools"],
        ["Polling place", "Floyd B. Simmons Center, 29150 Carlysle St"],
    ],
}


def embed_json(html: str, script_id: str, payload) -> str:
    start_tag = f'<script type="application/json" id="{script_id}">'
    start = html.find(start_tag)
    if start == -1:
        raise SystemExit(f"index.html has no {script_id}")
    start_inner = start + len(start_tag)
    end = html.find("</script>", start_inner)
    if end == -1:
        raise SystemExit(f"{script_id} script is not closed")
    body = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return html[:start_inner] + "\n" + body + "\n" + html[end:]


def main():
    ballot = json.loads(BALLOT.read_text())
    precincts = json.loads(PRECINCTS.read_text())

    existing_ids = {item["id"] for item in ballot}
    for race in NEW_RACES:
        if race["id"] in existing_ids:
            ballot = [item for item in ballot if item["id"] != race["id"]]
        ballot.append(race)

    precincts = [p for p in precincts if p["id"] != INKSTER_PRECINCT["id"]]
    precincts.append(INKSTER_PRECINCT)
    precincts.sort(key=lambda p: (p["municipality"], p["name"]))

    BALLOT.write_text(json.dumps(ballot, indent=2, ensure_ascii=False) + "\n")
    PRECINCTS.write_text(json.dumps(precincts, indent=2, ensure_ascii=False) + "\n")

    html = INDEX.read_text()
    html = embed_json(html, "ballot-data", ballot)
    html = embed_json(html, "precinct-data", precincts)
    INDEX.write_text(html)

    scopes = set(INKSTER_PRECINCT["scopes"])
    shown = [r for r in ballot if r.get("scope") in scopes]
    print(f"Wrote {len(NEW_RACES)} Inkster/Wayne contests")
    print(f"Precincts: {len(precincts)}")
    print(f"Contests for Inkster Ward 1 Precinct 1: {len(shown)}")
    for race in shown:
        print(f"  {race['id']}: {race['title']} [{race['scope']}]")


if __name__ == "__main__":
    main()
