"""Write 032_amoxicillin_dose_source_fix.sql (python database/medicine_review/gen_032.py).

The first amoxicillin rows (031) cited the FDA Philippines insert PDF, whose
link now gives 404. The rows are now from the UK SmPC (emc 14145, verified).
For databases where the old 031 already ran: replace amoxicillin's rows only if
they are still exactly the old sample (every row tagged 'Label · FDA PH' and the
old PDF link present). If an admin has edited them, only the dead link is
updated. Fresh databases (new 031) are not touched. Safe to run twice.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_doses import ROOT, block  # noqa: E402

from app.services import dose_samples as ds  # noqa: E402

OLD_URL = "https://verification.fda.gov.ph/files/DRP-10727_PI_01.pdf"
MID = "med_amoxicillin"
rows, notes = ds.SAMPLES[MID]
src = ds.SOURCES[MID]
new_ph = next(s for s in src if s.tag == ds.FDAPH)

text = f"""-- 032_amoxicillin_dose_source_fix.sql  -  amoxicillin dosage rows from a working, verified source
-- Needs 030 (and 031). The old FDA PH PDF link gave 404, so amoxicillin's rows now
-- follow the UK SmPC (medicines.org.uk/emc/product/14145, section 4.2).
-- Replaces the rows only while they are still the untouched old sample; otherwise
-- only the dead link is fixed. Safe to run twice.

begin;

create temporary table _amox_old on commit drop as
select exists (select 1 from public.medicine_dose_sources
               where medicine_id = '{MID}' and url = '{OLD_URL}')
   and not exists (select 1 from public.medicine_doses
                   where medicine_id = '{MID}' and source <> 'Label · FDA PH') as untouched;

delete from public.medicine_doses      where medicine_id = '{MID}' and (select untouched from _amox_old);
delete from public.medicine_dose_notes where medicine_id = '{MID}' and (select untouched from _amox_old);
delete from public.medicine_dose_sources where medicine_id = '{MID}' and (select untouched from _amox_old);

-- Edited by an admin: keep their rows, just fix the dead link.
update public.medicine_dose_sources
   set url = '{new_ph.url}', source_name = '{new_ph.source_name.replace("'", "''")}', updated_at = now()
 where medicine_id = '{MID}' and url = '{OLD_URL}';

"""
text += block(MID, rows, notes, src)
text += "update public.content_version set version = version + 1, updated_at = now() where id = 1;\n\ncommit;\n"
path = os.path.join(ROOT, "database", "migrations", "032_amoxicillin_dose_source_fix.sql")
open(path, "w", encoding="utf-8").write(text)
print("wrote", path)
