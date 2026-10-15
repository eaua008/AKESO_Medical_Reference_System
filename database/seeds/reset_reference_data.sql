-- =====================================================================
-- OPTIONAL and DESTRUCTIVE: clears ALL reference content (diseases,
-- symptoms, medicines, their lists, links and references, and the drug
-- interaction data) so seed_reference_data.sql starts from a clean slate.
--
-- It does NOT touch users/auth, body_systems or patient_conditions.
-- Run it only if you want to remove the old data. Take a backup first
-- (Supabase: Database > Backups) if you might need the old rows.
-- =====================================================================

BEGIN;

DELETE FROM public.interaction_rule_members;
DELETE FROM public.interaction_rules;
DELETE FROM public.drug_interactions;
DELETE FROM public.medicine_condition_safety;

DELETE FROM public.disease_symptoms;
DELETE FROM public.disease_medicines;
DELETE FROM public.disease_related;
DELETE FROM public.disease_tags;
DELETE FROM public.disease_causes;
DELETE FROM public.disease_emergency_signs;
DELETE FROM public.disease_home_care;
DELETE FROM public.disease_recommended_tests;
DELETE FROM public.disease_risk_factors;
DELETE FROM public.disease_treatments;
DELETE FROM public.disease_prevention;
DELETE FROM public.disease_differentials;
DELETE FROM public.clinical_references;

DELETE FROM public.symptom_causes;
DELETE FROM public.symptom_red_flags;
DELETE FROM public.symptom_references;

DELETE FROM public.medicine_facts;
DELETE FROM public.medicine_references;
DELETE FROM public.medicine_brands;
DELETE FROM public.medicine_uses;
DELETE FROM public.medicine_side_effects;
DELETE FROM public.medicine_warnings;
DELETE FROM public.medicine_contraindications;
DELETE FROM public.medicine_interactions;

DELETE FROM public.diseases;
DELETE FROM public.symptoms;
DELETE FROM public.medicines;

UPDATE public.content_version SET version = version + 1, updated_at = now() WHERE id = 1;

COMMIT;
