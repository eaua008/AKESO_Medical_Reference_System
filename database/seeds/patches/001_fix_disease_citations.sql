-- =====================================================================
-- Patch 001: citations on the wrong kind of entry
--
-- For a database already filled with seed_reference_data.sql. Small and
-- safe to run more than once. (A fresh seed already includes these fixes.)
--
-- 1. Five disease pages cited a drug's FDA label (DailyMed / prescribing
--    information): ibuprofen on Acute Coronary Syndrome and Heart Failure,
--    sumatriptan on Ischemic Stroke and Migraine, Paxlovid on COVID-19.
--    A drug label documents the drug, so it belongs on the medicine page,
--    where each of those three medicines already cites its own label.
--    The disease pages keep their guideline and StatPearls sources.
-- 2. Ten disease pages linked the Harrison's textbook citation to a
--    McGraw Hill press release. Textbook ("mother book") citations carry
--    no link, the same as on the symptom and medicine pages.
-- 3. Bumps content_version so every installed app downloads the change.
-- =====================================================================

BEGIN;

-- 1. Drug labels off disease pages
DELETE FROM public.clinical_references
WHERE disease_id IN ('acute_coronary_syndrome', 'heart_failure', 'ischemic_stroke',
                     'migraine', 'covid19')
  AND (source_name ILIKE '%dailymed%'
       OR source_name ILIKE '%prescribing information%'
       OR citation_text ILIKE '%dailymed%');

UPDATE public.diseases
SET source_attribution = replace(source_attribution,
                                 'FDA ibuprofen and sumatriptan labels (DailyMed); ', '')
WHERE id = 'acute_coronary_syndrome';

UPDATE public.diseases
SET source_attribution = replace(source_attribution, 'FDA ibuprofen label (DailyMed); ', '')
WHERE id = 'heart_failure';

UPDATE public.diseases
SET source_attribution = replace(source_attribution, 'FDA sumatriptan label (DailyMed); ', '')
WHERE id IN ('ischemic_stroke', 'migraine');

UPDATE public.diseases
SET source_attribution = replace(source_attribution, 'FDA PAXLOVID prescribing information; ', '')
WHERE id = 'covid19';

-- 2. No link on textbook citations
UPDATE public.clinical_references
SET url = NULL
WHERE is_mother_book AND url IS NOT NULL;

-- 3. Tell every installed app to re-download the reference data.
UPDATE public.content_version SET version = version + 1, updated_at = now() WHERE id = 1;

COMMIT;

-- Check (should return 0 rows):
-- SELECT disease_id, source_name FROM public.clinical_references
-- WHERE source_name ILIKE '%dailymed%' OR source_name ILIKE '%prescribing information%';
