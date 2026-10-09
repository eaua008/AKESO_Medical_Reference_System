"""Terms of Use and Privacy Notice shown in the app.

Written for a student project. Have them reviewed (by your adviser, or your
school's Data Protection Officer) before real users sign up. When you
change either text, bump TERMS_VERSION / PRIVACY_VERSION in
app/models/account.py: everyone is then asked to accept the new version at
their next sign-in, and the old acceptance stays on record.

document(kind) builds the page the app shows: a title block (version,
effective date, operator), a numbered table of contents and the numbered
sections, styled for the white document sheet (LegalDialog).
"""

from html import escape

EFFECTIVE_DATE = "10 October 2026"
OPERATOR = ("Eijkim Maulit (@eaua008), a student of Mapúa Malayan Colleges Mindanao, "
            "as a school project")
CONTACT = ("Eijkim Maulit (@eaua008), through Clinical Exchange or the contact details "
           "shared with testers")

TERMS_TITLE = "Akeso Terms of Use"
PRIVACY_TITLE = "Akeso Privacy Notice"

# ------------------------------------------------------------------ terms

TERMS_SUMMARY = ("These terms explain what Akeso is for, how it may be used, and what "
                 "is expected of everyone who uses it.")

TERMS_SECTIONS = [
    ("About Akeso",
     f"""<p>Akeso is a study and reference application for students of medicine and
     the health professions. It is built and operated by {OPERATOR}. In these terms,
     "Akeso", "we" and "us" mean the application and its operator; "you" means
     anyone who uses it.</p>"""),

    ("Accepting these terms",
     """<p>By creating an account or using Akeso you agree to these Terms of Use and
     to the Privacy Notice. If these terms change, you will be asked to accept the
     new version the next time you sign in. If you do not agree, do not use
     Akeso.</p>"""),

    ("Educational use only",
     """<p>Every part of Akeso (the disease, symptom and medicine references, the
     Symptom Checker, the Drug Interaction Checker, the Body System Explorer, the
     Emergency Guide and Clinical Exchange) is for <b>learning only</b>.</p>
     <ul>
     <li>It is not medical advice, a diagnosis, a treatment plan or a
     prescription.</li>
     <li>It must never replace the judgement of a licensed professional, or be
     used to care for a real patient.</li>
     <li>In an emergency, call <b>911</b> or go to the nearest hospital. The
     Emergency Guide is a first-aid study reference, not emergency help.</li>
     </ul>"""),

    ("Hypothetical cases only",
     """<p>Cases, notes and posts you create must be <b>hypothetical</b>. Do not enter
     a real person's name, record or case number, photograph, exact birth date,
     address or any other detail that could identify them. Ages are recorded as
     ranges for this reason.</p>"""),

    ("Your account",
     """<ul>
     <li>Keep your password private, and turn on two-factor sign-in if you can.</li>
     <li>Use <b>Remember me</b> only on a computer that is yours.</li>
     <li>You are responsible for what is done with your account.</li>
     <li>Do not try to read other people's data, overload the service, or get
     around its security.</li>
     </ul>"""),

    ("Clinical Exchange",
     """<p>Clinical Exchange is a shared space for discussing study cases.</p>
     <ul>
     <li>Be respectful. Harassment, hate, spam and deliberately false medical
     claims are not allowed.</li>
     <li>Post only hypothetical cases (section 4).</li>
     <li>Educators and administrators moderate the space: they may hide, lock or
     remove posts and replies, and members can report content.</li>
     </ul>"""),

    ("Content and sources",
     """<p>Reference content cites its sources. It may still contain errors or fall
     behind current practice, so always check the original source and current
     clinical guidelines before relying on any information. Third-party material
     (such as the BodyParts3D anatomy models, CC BY 4.0) stays under its own licence
     and is credited in the app's notices.</p>"""),

    ("Availability and updates",
     """<p>Akeso is a student project provided <b>as is</b>, without any warranty. It
     may change, contain mistakes, or be unavailable at times. New versions are
     offered in Settings &gt; Updates; installing them is up to you.</p>"""),

    ("Suspension and ending your account",
     """<p>You can delete your account at any time in Account Settings (section 7 of
     the Privacy Notice explains what happens). Administrators may suspend or remove
     an account that breaks these terms; a suspended account cannot sign in.</p>"""),

    ("Changes to these terms",
     """<p>These terms may be updated as Akeso develops. The version and effective
     date are shown at the top; you will be asked to accept any new version at your
     next sign-in.</p>"""),

    ("Contact",
     f"""<p>Questions about these terms: {CONTACT}.</p>"""),
]

# ---------------------------------------------------------------- privacy

PRIVACY_SUMMARY = ("This notice explains what information Akeso keeps about you, why, "
                   "where it is stored, who can see it, and the rights you have under the "
                   "Philippine Data Privacy Act of 2012 (Republic Act No. 10173).")

_ROW = "<tr><td class='k'>{}</td><td>{}</td><td class='w'>{}</td></tr>"
_COLLECTED = "".join(_ROW.format(*row) for row in [
    ("Account", "Email address; a one-way hash of your password (Akeso never sees "
     "your password); the name Google shares if you sign in with Google.",
     "Server"),
    ("Profile", "The name, photo, handle, bio, program, school, year level and "
     "interests you choose to add.", "Server"),
    ("Student badge", "Only the <i>domain</i> of a verified school email (for example "
     "school.edu.ph), never the full address.", "Server"),
    ("Security", "The computers you sign in from (name, system and Akeso version) and "
     "a log of sign-ins and account changes.", "Server"),
    ("Study activity", "Daily counts such as pages viewed and checker runs, only while "
     "tracking is switched on in Privacy &amp; data.", "Server"),
    ("Study Notebook", "Your notes, saved cases, subjects and the pictures in them, so "
     "they follow you to every computer.", "Server + this computer"),
    ("Clinical Exchange", "Posts, replies, votes, follows and reports you make, and "
     "the notifications they create.", "Server"),
    ("Announcements", "Which announcements you have opened, so they stop showing as "
     "unread.", "Server"),
    ("Consents", "Which version of these documents you accepted, and when.", "Server"),
])

PRIVACY_SECTIONS = [
    ("Who is responsible",
     f"""<p>Akeso is operated by {OPERATOR}, who decides how the information
     described here is used. This notice follows the principles of the Data
     Privacy Act: transparency, legitimate purpose and proportionality.</p>"""),

    ("Information we keep and why",
     f"""<p>Akeso keeps only what it needs to run your account and the features you
     use. "Server" means Akeso's database (Supabase); "this computer" means the
     computer you use Akeso on.</p>
     <table class='data' cellspacing='0' cellpadding='8' width='100%'>
     <tr><th class='k'>Information</th><th>What exactly</th><th class='w'>Where</th></tr>
     {_COLLECTED}
     </table>"""),

    ("What stays on your computer",
     """<p>Bookmarks, search history, your settings, downloaded reference entries
     (so Akeso works offline) and a crash log are stored only on the computer you
     use. If you tick <b>Remember me</b>, your saved sign-in is kept there too,
     encrypted with your Windows account; signing out removes it.</p>"""),

    ("Who can see your information",
     """<ul>
     <li><b>You</b> can see all of it. The database only returns an account's own
     records.</li>
     <li><b>Other members</b> see your profile only if you make it public, and then
     only the parts your switches allow. Your Clinical Exchange posts and replies are
     visible to other members.</li>
     <li><b>Educators and administrators</b> can moderate Clinical Exchange content.
     Administrators can see account details (name, email, role, sign-up and sign-in
     times, status) to manage accounts, but not your notebook, saved cases or study
     data.</li>
     </ul>
     <p>Akeso does not sell or rent your information, and shows no ads.</p>"""),

    ("Service providers",
     """<ul>
     <li><b>Supabase</b> hosts the database, sign-in and file storage.</li>
     <li><b>Google</b>, only if you choose to sign in with Google.</li>
     <li><b>Gmail</b> sends the verification codes for school emails.</li>
     <li><b>GitHub</b> hosts Akeso's updates; checking for an update contacts GitHub,
     which can see your computer's internet address.</li>
     </ul>"""),

    ("How it is protected",
     """<p>Connections to Akeso's server are encrypted. Row-level security in the
     database lets each account read only its own records. Passwords are stored only
     as one-way hashes by Supabase. Two-factor sign-in and a sign-in log in Account
     Settings help you spot activity that was not you.</p>"""),

    ("How long it is kept",
     """<p>Server information is kept while your account exists. When you delete
     your account it is removed after a 30-day window, during which signing in
     cancels the deletion. Information on your computer stays until you delete it
     or remove Akeso and its data folder. A record of consents is kept as history.</p>"""),

    ("Your rights",
     """<ul>
     <li><b>Access and portability:</b> Account Settings &gt; Privacy &amp; data &gt;
     Export downloads your information in one file.</li>
     <li><b>Correction:</b> edit your profile at any time.</li>
     <li><b>Erasure:</b> delete your account (section 7).</li>
     <li><b>Objection:</b> switch study-activity tracking off at any time.</li>
     <li><b>Complaint:</b> you may contact the operator (section 10), or the
     National Privacy Commission of the Philippines.</li>
     </ul>"""),

    ("Changes to this notice",
     """<p>This notice may be updated as Akeso develops. The version and effective
     date are shown at the top; you will be asked to accept any new version at your
     next sign-in.</p>"""),

    ("Contact",
     f"""<p>Questions or requests about your information: {CONTACT}.</p>"""),
]

# ----------------------------------------------------------------- render

STYLE = """
body { color: #1F2937; font-size: 15px; }
h1 { color: #111827; font-size: 30px; font-weight: 600; margin: 0 0 6px 0; }
h2 { color: #111827; font-size: 19px; font-weight: 600; margin: 26px 0 8px 0; }
p, li { line-height: 135%; }
p { margin: 0 0 10px 0; }
ul { margin: 0 0 10px 0; }
li { margin-bottom: 4px; }
a { color: #4F46E5; text-decoration: none; }
.meta { color: #6B7280; font-size: 13px; margin: 0 0 14px 0; }
.summary { color: #374151; font-size: 16px; margin: 0 0 18px 0; }
.toc-title { color: #6B7280; font-size: 12px; font-weight: 700; margin: 0 0 6px 0; }
.toc { margin: 0 0 4px 0; }
.num { color: #9CA3AF; }
table.data { border-color: #E5E7EB; margin: 4px 0 10px 0; }
th { background-color: #F3F4F6; color: #374151; font-size: 13px; text-align: left;
     font-weight: 600; }
td { border-top: 1px solid #E5E7EB; vertical-align: top; font-size: 14px; }
td.k, th.k { font-weight: 600; color: #111827; }
td.w, th.w { color: #6B7280; }
.part { color: #6B7280; font-size: 12px; font-weight: 700; margin: 34px 0 4px 0; }
"""


def _document_body(prefix: str, title: str, version: str, summary: str,
                   sections: list[tuple[str, str]], show_title: bool = True) -> str:
    parts = []
    if show_title:
        parts.append(f"<h1>{escape(title)}</h1>")
    if version:
        parts.append(f"<p class='meta'>Version {escape(version)} &nbsp;·&nbsp; "
                     f"Effective {EFFECTIVE_DATE}</p>")
    parts.append(f"<p class='summary'>{summary}</p>")
    parts.append("<p class='toc-title'>CONTENTS</p>")
    for number, (heading, _html) in enumerate(sections, 1):
        parts.append(f"<p class='toc'><span class='num'>{number}.</span>&nbsp; "
                     f"<a href='#{prefix}{number}'>{escape(heading)}</a></p>")
    parts.append("<hr>")
    for number, (heading, html) in enumerate(sections, 1):
        parts.append(f"<h2><a name='{prefix}{number}'></a>"
                     f"<span class='num'>{number}.</span>&nbsp; {escape(heading)}</h2>")
        parts.append(html)
    return "\n".join(parts)


def document(kind: str, terms_version: str, privacy_version: str) -> str:
    """kind: "terms", "privacy" or "both" (the sign-in consent step)."""
    terms = _document_body("t", TERMS_TITLE, terms_version, TERMS_SUMMARY, TERMS_SECTIONS)
    privacy = _document_body("p", PRIVACY_TITLE, privacy_version, PRIVACY_SUMMARY,
                             PRIVACY_SECTIONS)
    if kind == "terms":
        body = terms
    elif kind == "privacy":
        body = privacy
    else:
        body = (f"<p class='part'>PART 1 OF 2</p>{terms}<br><hr>"
                f"<p class='part'>PART 2 OF 2</p>{privacy}")
    return f"<html><body>{body}</body></html>"


# Older code imported these names; kept so nothing breaks.
TERMS_HTML = _document_body("t", TERMS_TITLE, "", TERMS_SUMMARY, TERMS_SECTIONS, False)
PRIVACY_HTML = _document_body("p", PRIVACY_TITLE, "", PRIVACY_SUMMARY, PRIVACY_SECTIONS,
                              False)
