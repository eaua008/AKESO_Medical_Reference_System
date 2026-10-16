-- 039_loperamide_gastroenteritis.sql  -  tester feedback (Kirce Rimando, Clinical Exchange)
-- Loperamide was linked to acute gastroenteritis as 'caution' with the note
-- "Acceptable for acute watery diarrhea in immunocompetent adults", while the
-- cholera link already says the Philippine CPG does not recommend loperamide
-- in adults with acute infectious diarrhea and advises against it in children.
-- This brings the gastroenteritis link in line with the cholera one.
--
-- REVIEW BEFORE RUNNING: confirm against the current Philippine CPG on acute
-- infectious diarrhea (PSMID/PhilHealth Circular 2022-0026 and the PSPGHAN
-- 2026 guideline already cited on med_ors). Not yet applied to the database.
-- Racecadotril (the alternative Kirce mentions) has no medicine entry yet;
-- add it through the content editor once its monograph is researched.
-- Safe to run twice.

begin;

update public.disease_medicines
set safety = 'avoid'::public.condition_safety,
    note = 'The Philippine CPG does not recommend loperamide for acute infectious diarrhea in adults and advises against it in children; it does not replace fluid loss. Never use it with fever, bloody stools or when a surgical abdomen (such as appendicitis) has not been ruled out. Oral rehydration (with zinc in children) is the mainstay.'
where disease_id = 'acute_gastroenteritis'
  and medicine_id = 'med_loperamide';

commit;
