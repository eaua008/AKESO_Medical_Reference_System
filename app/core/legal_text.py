"""Terms of Use and Privacy Notice shown in the app.

Plain-language drafts written for a school project. Have them reviewed
(by your adviser, or your school's Data Protection Officer) before real
users sign up. When you change either text, bump TERMS_VERSION /
PRIVACY_VERSION in app/models/account.py: everyone is then asked to accept
the new version at their next sign-in, and the old acceptance stays on
record.
"""

TERMS_TITLE = "Akeso Terms of Use"
TERMS_HTML = """
<h3>What Akeso is</h3>
<p>Akeso is a study and reference tool for students of medicine and the
health professions. Its disease, symptom and medicine entries, the Symptom
Checker and the Drug Interaction Checker are for <b>learning only</b>.
They are not medical advice, a diagnosis or a prescription, and must never
replace a licensed professional's judgement or be used for real patient
care.</p>

<h3>Cases and notes</h3>
<p>Cases you build or save must be <b>hypothetical</b>. Do not enter real
patients' names, record numbers, photos, exact birth dates or anything else
that could identify a real person. Ages are recorded as ranges for this
reason.</p>

<h3>Your account</h3>
<ul>
<li>Keep your password to yourself, and turn on two-factor sign-in if you
can.</li>
<li>You are responsible for what is done with your account.</li>
<li>Do not try to read other people's data, overload the service, or get
around its security.</li>
</ul>

<h3>Sources</h3>
<p>Reference content cites its sources. Always check the original source and
current guidelines before relying on any information.</p>

<h3>Changes</h3>
<p>If these terms change, Akeso will ask you to accept the new version the
next time you sign in.</p>
"""

PRIVACY_TITLE = "Akeso Privacy Notice"
PRIVACY_HTML = """
<p>This notice explains what Akeso keeps about you, following the principles
of the Philippine Data Privacy Act of 2012 (Republic Act No. 10173):
transparency, legitimate purpose and proportionality.</p>

<h3>What is stored on Akeso's server (Supabase)</h3>
<ul>
<li><b>Sign-in:</b> your email, and a one-way hash of your password (Akeso
itself never sees or stores your password). If you use Google, the name
Google shares.</li>
<li><b>Profile:</b> the name, photo, handle, bio, program, school, year
level and interests you choose to add.</li>
<li><b>Verified student badge:</b> only the <i>domain</i> of your school
email (for example school.edu.ph), never the full address.</li>
<li><b>Security:</b> the computers you sign in from (their name and system
version), and a log of sign-ins and account changes, kept so you can spot
activity that was not you.</li>
<li><b>Study activity:</b> daily counts (pages viewed, checker runs), only
while the switch in Privacy &amp; data is on.</li>
<li><b>Consents:</b> which version of these documents you accepted, and
when.</li>
<li><b>Study Notebook:</b> your notes, saved cases, subjects and the
pictures you put in them, so they appear on every computer you sign in on.
A copy also stays on each computer, so the notebook works offline.</li>
</ul>

<h3>What stays on your computer</h3>
<p>Bookmarks, search history, medications and your settings are stored only
on the computer you use. Downloaded reference entries are kept there too,
so Akeso works offline.</p>

<h3>Who can see it</h3>
<p>Only you. The database only returns an account's own rows. Other students
can see your profile only if you make it public, and then only the parts your
switches allow. Akeso does not sell or share your data, and shows no
ads.</p>

<h3>Your rights</h3>
<ul>
<li><b>Access and portability:</b> Account &gt; Privacy &amp; data &gt;
Export downloads everything in one file.</li>
<li><b>Correction:</b> edit your profile at any time.</li>
<li><b>Erasure:</b> Delete account removes everything after a 30-day window
in which you can change your mind by signing in.</li>
<li><b>Objection:</b> switch study-activity tracking off at any time.</li>
</ul>
"""
