-- 033_medicines_review_01.sql  -  medicine review b01: med_aciclovir, med_allopurinol, med_aluminium_magnesium_hydroxide, med_amlodipine, med_amoxicillin, med_artemether_lumefantrine, med_aspirin, med_atorvastatin, med_azithromycin, med_benzathine_penicillin
-- Adds only: longer descriptions, new facts, references, disease links, and dosage
-- tables (for medicines that have none yet). Nothing is deleted or reworded.
-- Needs 030_medicine_doses.sql first. Safe to run twice (every insert is guarded).

begin;

-- ================================================ med_aciclovir  (Aciclovir)
update public.medicines set description = 'Aciclovir is a synthetic purine (guanosine) nucleoside analogue that is phosphorylated by viral and host cellular enzymes to aciclovir triphosphate, which inhibits herpesvirus DNA polymerase and terminates viral DNA chain elongation. Its selectivity for infected cells makes it active against herpes simplex virus types 1 and 2 and varicella-zoster virus. It is used for genital and mucocutaneous herpes, herpes zoster, varicella and, intravenously, herpes simplex encephalitis. Oral bioavailability is only 10–20%, and the drug is excreted mainly unchanged by the kidneys with a half-life of about 3 hours that lengthens to about 19.5 hours in chronic renal failure, which explains the frequent oral dosing and the need for renal dose reduction. Cerebrospinal fluid levels reach about 50% of plasma levels. In the Philippines, aciclovir is on the PNF Essential Medicines List as tablets, oral suspension and an injection for IV infusion.', updated_at = now()
where id = 'med_aciclovir' and description = 'Aciclovir is a synthetic purine (guanosine) nucleoside analogue that is phosphorylated by viral and host cellular enzymes to aciclovir triphosphate, which inhibits herpesvirus DNA polymerase and terminates viral DNA chain elongation. Its selectivity for infected cells makes it active against herpes simplex virus types 1 and 2 and varicella-zoster virus. It is used for genital and mucocutaneous herpes, herpes zoster, varicella and, intravenously, herpes simplex encephalitis.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Philippine National Formulary (PNF EML); CDC STI Treatment Guidelines' else source_attribution || '; UK SmPC (emc); Philippine National Formulary (PNF EML); CDC STI Treatment Guidelines' end
where id = 'med_aciclovir' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'indication', 'Prophylaxis of herpes simplex infections in immunocompromised patients', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'indication' and content = 'Prophylaxis of herpes simplex infections in immunocompromised patients');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'indication', 'Herpes simplex in people with HIV: episodic treatment and long-term suppression', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'indication' and content = 'Herpes simplex in people with HIV: episodic treatment and long-term suppression');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'adverse', 'Pruritus and rash, including photosensitivity', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse' and content = 'Pruritus and rash, including photosensitivity');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'adverse', 'Dizziness, abdominal pain, fatigue and fever', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse' and content = 'Dizziness, abdominal pain, fatigue and fever');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'adverse', 'Urticaria and accelerated diffuse hair loss (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse' and content = 'Urticaria and accelerated diffuse hair loss (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'adverse', 'Anaphylaxis, angioedema and dyspnoea (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse' and content = 'Anaphylaxis, angioedema and dyspnoea (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'adverse', 'Reversible rises in bilirubin and liver enzymes; very rarely hepatitis and jaundice', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse' and content = 'Reversible rises in bilirubin and liver enzymes; very rarely hepatitis and jaundice');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'adverse', 'Anaemia, leukopenia and thrombocytopenia (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'adverse' and content = 'Anaemia, leukopenia and thrombocytopenia (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'contraindication', 'Elderly patients: higher risk of neurological adverse effects; monitor closely (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'contraindication' and content = 'Elderly patients: higher risk of neurological adverse effects; monitor closely (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'contraindication', 'Breastfeeding: excreted in breast milk at 0.6–4.1 times plasma levels; use with caution (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'contraindication' and content = 'Breastfeeding: excreted in breast milk at 0.6–4.1 times plasma levels; use with caution (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'contraindication', 'Repeated or prolonged courses in severely immunocompromised patients may select less sensitive virus strains (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'contraindication' and content = 'Repeated or prolonged courses in severely immunocompromised patients may select less sensitive virus strains (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'interaction', 'Cimetidine: increases aciclovir AUC by reducing its renal clearance.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'interaction' and content = 'Cimetidine: increases aciclovir AUC by reducing its renal clearance.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'interaction', 'Mycophenolate mofetil: increases the AUC of aciclovir and of its inactive metabolite; no dose adjustment needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'interaction' and content = 'Mycophenolate mofetil: increases the AUC of aciclovir and of its inactive metabolite; no dose adjustment needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aciclovir', 'interaction', 'Theophylline: AUC increased by about 50%; measure theophylline levels during co-therapy.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aciclovir' and kind = 'interaction' and content = 'Theophylline: AUC increased by about 50%; measure theophylline levels during co-therapy.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aciclovir', 'UK SmPC (emc)', 'Aciclovir 200 mg Tablets – Summary of Product Characteristics. Milpharm Limited (PL 16363/0556). Electronic Medicines Compendium (emc), medicines.org.uk.', 'https://products.mhra.gov.uk/search/?search=aciclovir#emc-11673', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aciclovir'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aciclovir' and url = 'https://products.mhra.gov.uk/search/?search=aciclovir#emc-11673');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aciclovir', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aciclovir'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aciclovir' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aciclovir', 'CDC STI Treatment Guidelines', 'Centers for Disease Control and Prevention. Genital Herpes. Sexually Transmitted Infections Treatment Guidelines, 2021.', 'https://www.cdc.gov/std/treatment-guidelines/herpes.htm', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aciclovir'), 0)
where exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aciclovir' and url = 'https://www.cdc.gov/std/treatment-guidelines/herpes.htm');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_aciclovir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'safe'::condition_safety, 'CDC 2021 STI guideline gives aciclovir regimens for episodic and suppressive HSV therapy in people with HIV'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_aciclovir');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_aciclovir', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Renally excreted (half-life about 19.5 h in chronic renal failure); dose reduction needed and higher risk of neurotoxicity'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_aciclovir')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_aciclovir');

-- ================================================ med_allopurinol  (Allopurinol)
update public.medicines set description = 'Allopurinol and its active metabolite oxypurinol inhibit xanthine oxidase, reducing production of uric acid. Lowering serum urate below 6 mg/dL dissolves urate crystals over time, preventing flares, tophi and joint damage. It is the preferred first-line urate-lowering drug in gout, including in chronic kidney disease, started at a low dose and increased gradually. Allopurinol is not a treatment for an acute gout attack and plain asymptomatic hyperuricaemia is generally not an indication for it; it is also used to prevent uric acid build-up during cancer chemotherapy and for rare 2,8-dihydroxyadenine stones. In the Philippines it is listed in the PNF Essential Medicines List as 100 mg and 300 mg tablets.', updated_at = now()
where id = 'med_allopurinol' and description = 'Allopurinol and its active metabolite oxypurinol inhibit xanthine oxidase, reducing production of uric acid. Lowering serum urate below 6 mg/dL dissolves urate crystals over time, preventing flares, tophi and joint damage. It is the preferred first-line urate-lowering drug in gout, including in chronic kidney disease, started at a low dose and increased gradually.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine National Formulary – Essential Medicines List; UK SmPC – Allopurinol Tablets BP 100mg; DailyMed – Zyloprim (allopurinol) tablet label; Merck Manual Professional – Gout; FDA Philippines Advisory No. 2018-190' else source_attribution || '; Philippine National Formulary – Essential Medicines List; UK SmPC – Allopurinol Tablets BP 100mg; DailyMed – Zyloprim (allopurinol) tablet label; Merck Manual Professional – Gout; FDA Philippines Advisory No. 2018-190' end
where id = 'med_allopurinol' and position('Philippine National Formulary – Essential Medicines List' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'indication', '2,8-dihydroxyadenine (2,8-DHA) kidney stones in adenine phosphoribosyltransferase (APRT) deficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'indication' and content = '2,8-dihydroxyadenine (2,8-DHA) kidney stones in adenine phosphoribosyltransferase (APRT) deficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'adverse', 'Raised TSH (thyroid-stimulating hormone) on long-term treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse' and content = 'Raised TSH (thyroid-stimulating hormone) on long-term treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'adverse', 'Drowsiness', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse' and content = 'Drowsiness');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'adverse', 'Hepatitis (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse' and content = 'Hepatitis (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'adverse', 'Blood disorders: agranulocytosis, aplastic anaemia, thrombocytopenia, bone marrow depression (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'adverse' and content = 'Blood disorders: agranulocytosis, aplastic anaemia, thrombocytopenia, bone marrow depression (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Didanosine: allopurinol roughly doubles didanosine exposure; combination generally not recommended.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Didanosine: allopurinol roughly doubles didanosine exposure; combination generally not recommended.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Ciclosporin: ciclosporin levels may rise; watch for toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Ciclosporin: ciclosporin levels may rise; watch for toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Theophylline: metabolism inhibited; check theophylline levels when starting or increasing allopurinol.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Theophylline: metabolism inhibited; check theophylline levels when starting or increasing allopurinol.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Chlorpropamide: risk of prolonged hypoglycaemia, especially with poor kidney function.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Chlorpropamide: risk of prolonged hypoglycaemia, especially with poor kidney function.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Cytotoxics (e.g., cyclophosphamide, doxorubicin): blood dyscrasias more frequent; monitor blood counts.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Cytotoxics (e.g., cyclophosphamide, doxorubicin): blood dyscrasias more frequent; monitor blood counts.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'ACE inhibitors: higher risk of hypersensitivity reactions, especially in kidney impairment.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'ACE inhibitors: higher risk of hypersensitivity reactions, especially in kidney impairment.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Salicylates and uricosurics (e.g., probenecid): may speed oxipurinol excretion and reduce allopurinol''s effect.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Salicylates and uricosurics (e.g., probenecid): may speed oxipurinol excretion and reduce allopurinol''s effect.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Aluminium hydroxide antacids: may reduce allopurinol''s effect; separate doses by at least 3 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Aluminium hydroxide antacids: may reduce allopurinol''s effect; separate doses by at least 3 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'interaction', 'Vidarabine: half-life of vidarabine increased; watch for toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'interaction' and content = 'Vidarabine: half-life of vidarabine increased; watch for toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'brand_ph', 'Allujen', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'brand_ph'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'brand_ph' and content = 'Allujen');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_allopurinol', 'brand_intl', 'Zyloric', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'brand_intl'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_allopurinol' and kind = 'brand_intl' and content = 'Zyloric');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_allopurinol', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_allopurinol'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_allopurinol' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_allopurinol', 'UK SmPC – Allopurinol Tablets BP 100mg', 'Milpharm Ltd. Allopurinol Tablets BP 100mg – Summary of Product Characteristics. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=allopurinol#emc-7004', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_allopurinol'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_allopurinol' and url = 'https://products.mhra.gov.uk/search/?search=allopurinol#emc-7004');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_allopurinol', 'DailyMed – Zyloprim (allopurinol) tablet label', 'ZYLOPRIM (allopurinol) tablet – prescribing information. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=342832b5-1a32-4bea-bc49-ab0fd152154e', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_allopurinol'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_allopurinol' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=342832b5-1a32-4bea-bc49-ab0fd152154e');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_allopurinol', 'Merck Manual Professional – Gout', 'Merck Manual Professional Version. Gout. Musculoskeletal and Connective Tissue Disorders: Crystal-Induced Arthritides.', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_allopurinol'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_allopurinol' and url = 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_allopurinol', 'FDA Philippines Advisory No. 2018-190', 'Food and Drug Administration Philippines. FDA Advisory No. 2018-190: recall of one lot of Allopurinol 300 mg tablet (Allujen).', 'https://www.fda.gov.ph/?p=1608', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_allopurinol'), 0)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_allopurinol' and url = 'https://www.fda.gov.ph/?p=1608');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_allopurinol', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Kidney impairment raises adverse-effect risk; start low (e.g., 50 mg) and cap the dose by creatinine clearance.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_allopurinol');
-- med_allopurinol
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_allopurinol', 'adult', 0, 'Gout (starting dose)', 'PO', '100 mg', 'Once a day', 'Long-term', '—', 'Label · US DailyMed', 'Increase by 100 mg weekly until serum urate ≤ 6 mg/dL'),
    ('med_allopurinol', 'adult', 1, 'Gout, mild (maintenance)', 'PO', '200–300 mg/day', 'Once a day', 'Long-term', '800 mg/day', 'Label · US DailyMed', 'Doses above 300 mg/day given in divided doses'),
    ('med_allopurinol', 'adult', 2, 'Gout, moderately severe tophaceous', 'PO', '400–600 mg/day', 'Divided doses', 'Long-term', '800 mg/day', 'Label · US DailyMed', ''),
    ('med_allopurinol', 'adult', 3, 'Prevention of tumour lysis (cancer therapy)', 'PO', '600–800 mg/day', 'Divided doses', '2–3 days', '800 mg/day', 'Label · US DailyMed', 'With high fluid intake'),
    ('med_allopurinol', 'adult', 4, 'Recurrent calcium oxalate stones', 'PO', '200–300 mg/day', 'Once a day or divided', 'Long-term', '—', 'Label · US DailyMed', ''),
    ('med_allopurinol', 'adult', 5, 'Haemodialysis (2–3× a week)', 'PO', '300–400 mg', 'After each dialysis', 'Long-term', '—', 'Label · UK SmPC', 'None in between dialysis sessions'),
    ('med_allopurinol', 'child', 6, 'Cancer therapy / hyperuricaemic states (under 15 y)', 'PO', '10–20 mg/kg/day', 'Once a day', 'As needed', '400 mg/day', 'Label · UK SmPC', 'Use in children is rarely indicated'),
    ('med_allopurinol', 'child', 7, 'Cancer therapy, 6–10 years', 'PO', '300 mg/day', 'Once a day', 'As needed', '—', 'Label · US DailyMed', ''),
    ('med_allopurinol', 'child', 8, 'Cancer therapy, under 6 years', 'PO', '150 mg/day', 'Once a day', 'As needed', '—', 'Label · US DailyMed', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_allopurinol');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_allopurinol', 'renal', 0, 'CrCl 10–20', '200 mg a day is suitable.', 'Label · US DailyMed'),
    ('med_allopurinol', 'renal', 1, 'CrCl < 10', 'Do not exceed 100 mg a day.', 'Label · US DailyMed'),
    ('med_allopurinol', 'renal', 2, 'CrCl < 3', 'The dosing interval may also need to be lengthened.', 'Label · US DailyMed'),
    ('med_allopurinol', 'renal', 3, 'CrCl < 60', 'Some clinicians start at 50 mg once a day; supporting data are limited.', 'Merck Manual'),
    ('med_allopurinol', 'hepatic', 4, '', 'Use reduced doses in hepatic impairment; do periodic liver function tests early in treatment.', 'Label · UK SmPC'),
    ('med_allopurinol', 'elderly', 5, '', 'Use the lowest dose that gives satisfactory urate reduction.', 'Label · UK SmPC'),
    ('med_allopurinol', 'pregnancy', 6, '', 'Inadequate evidence of safety in human pregnancy; use only when no safer alternative exists. Use during breastfeeding is not recommended (allopurinol and oxipurinol pass into breast milk).', 'Label · UK SmPC'),
    ('med_allopurinol', 'administration', 7, '', 'Take once daily after a meal; split the dose if over 300 mg/day causes stomach upset. Drink enough fluid for at least 2 L of urine a day.', 'Label · UK SmPC'),
    ('med_allopurinol', 'administration', 8, '', 'The UK label advises waiting until an acute attack has fully subsided before starting; Merck notes it can be started during a flare if anti-inflammatory cover is given.', 'Merck Manual'),
    ('med_allopurinol', 'forms_ph', 9, '', 'Oral: 100 mg and 300 mg tablet.', 'PNF'),
    ('med_allopurinol', 'monitor', 10, '', 'Serum urate to guide dose titration; liver function tests in the early months; BUN and serum creatinine in kidney impairment; blood counts with cytotoxics or azathioprine; TSH on long-term use; stop at the first sign of rash.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_allopurinol');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_allopurinol', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_allopurinol', 'Label · US DailyMed', 'DailyMed – Zyloprim (allopurinol) tablet label', 'ZYLOPRIM (allopurinol) tablet – prescribing information. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=342832b5-1a32-4bea-bc49-ab0fd152154e', 1),
    ('med_allopurinol', 'Label · UK SmPC', 'UK SmPC – Allopurinol Tablets BP 100mg', 'Milpharm Ltd. Allopurinol Tablets BP 100mg – Summary of Product Characteristics. emc.', 'https://products.mhra.gov.uk/search/?search=allopurinol#emc-7004', 2),
    ('med_allopurinol', 'Merck Manual', 'Merck Manual Professional – Gout', 'Merck Manual Professional Version. Gout.', 'https://www.merckmanuals.com/professional/musculoskeletal-and-connective-tissue-disorders/crystal-induced-arthritides/gout', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_allopurinol')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_allopurinol');


-- ================================================ med_aluminium_magnesium_hydroxide  (Aluminium hydroxide + Magnesium hydroxide)
update public.medicines set description = 'A combination antacid that neutralizes gastric acid already secreted, giving fast but short-lived relief of heartburn and dyspepsia. Aluminium hydroxide also inhibits pepsin and tends to constipate, while magnesium hydroxide tends to loosen the stool, so combining them balances the effect on bowel habit. Antacids are suited to mild, intermittent reflux symptoms. It is a local, non-absorbed treatment for symptoms and does not heal ulcers or treat their cause, so persistent symptoms beyond about 2 weeks call for medical review. Its main practical problem is binding many other oral drugs in the gut, which reduces their absorption. In the Philippines it is on the PNF Essential Medicines List as a suspension (225 mg + 200 mg per 5 mL) and a tablet (200 mg + 100 mg).', updated_at = now()
where id = 'med_aluminium_magnesium_hydroxide' and description = 'A combination antacid that neutralizes gastric acid already secreted, giving fast but short-lived relief of heartburn and dyspepsia. Aluminium hydroxide also inhibits pepsin and tends to constipate, while magnesium hydroxide tends to loosen the stool, so combining them balances the effect on bowel habit. Antacids are suited to mild, intermittent reflux symptoms.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Philippine National Formulary – Essential Medicines List; UK SmPC – Mucogel Suspension; MSF Essential Drugs – Aluminium hydroxide/Magnesium hydroxide oral; DailyMed – Kesin Mag-Al suspension (OTC label)' else source_attribution || '; Philippine National Formulary – Essential Medicines List; UK SmPC – Mucogel Suspension; MSF Essential Drugs – Aluminium hydroxide/Magnesium hydroxide oral; DailyMed – Kesin Mag-Al suspension (OTC label)' end
where id = 'med_aluminium_magnesium_hydroxide' and position('Philippine National Formulary – Essential Medicines List' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'indication', 'Gastritis and gastric hyperacidity', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'indication' and content = 'Gastritis and gastric hyperacidity');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'adverse', 'Abdominal pain', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'adverse' and content = 'Abdominal pain');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'adverse', 'Hypermagnesaemia in young children, especially with kidney impairment or dehydration', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'adverse' and content = 'Hypermagnesaemia in young children, especially with kidney impairment or dehydration');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'contraindication', 'Severely debilitated patients', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'contraindication' and content = 'Severely debilitated patients');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'contraindication', 'Hereditary fructose intolerance (sorbitol-containing suspensions)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'contraindication' and content = 'Hereditary fructose intolerance (sorbitol-containing suspensions)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'interaction', 'Chloroquine, digoxin, gabapentin, itraconazole and atazanavir: reduced absorption; separate by at least 2 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction' and content = 'Chloroquine, digoxin, gabapentin, itraconazole and atazanavir: reduced absorption; separate by at least 2 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'interaction', 'Velpatasvir: reduced absorption; separate by 4 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction' and content = 'Velpatasvir: reduced absorption; separate by 4 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'interaction', 'Allopurinol: aluminium hydroxide may reduce its effect; separate by at least 3 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction' and content = 'Allopurinol: aluminium hydroxide may reduce its effect; separate by at least 3 hours.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'interaction', 'Salicylates: urine alkalinisation by magnesium hydroxide increases salicylate excretion.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction' and content = 'Salicylates: urine alkalinisation by magnesium hydroxide increases salicylate excretion.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'interaction', 'Vitamins: absorption reduced; do not take at the same time.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'interaction' and content = 'Vitamins: absorption reduced; do not take at the same time.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aluminium_magnesium_hydroxide', 'brand_intl', 'Mucogel', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'brand_intl'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aluminium_magnesium_hydroxide' and kind = 'brand_intl' and content = 'Mucogel');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aluminium_magnesium_hydroxide', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aluminium_magnesium_hydroxide', 'UK SmPC – Mucogel Suspension', 'Rosemont Pharmaceuticals Ltd. Mucogel Suspension – Summary of Product Characteristics. electronic medicines compendium (emc); updated 01-Mar-2022.', 'https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-13356', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide' and url = 'https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-13356');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aluminium_magnesium_hydroxide', 'MSF Essential Drugs – Aluminium hydroxide/Magnesium hydroxide oral', 'Médecins Sans Frontières. Essential drugs – practical guidelines: Aluminium hydroxide/Magnesium hydroxide, oral.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/aluminium-hydroxide-magnesium-hydroxide-oral-16685025.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/aluminium-hydroxide-magnesium-hydroxide-oral-16685025.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aluminium_magnesium_hydroxide', 'DailyMed – Kesin Mag-Al suspension (OTC label)', 'KESIN MAG-AL (aluminum and magnesium hydroxide suspension) – OTC drug label. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42df2198-14dc-da1c-e063-6394a90a1ae6', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide'), 0)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aluminium_magnesium_hydroxide' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42df2198-14dc-da1c-e063-6394a90a1ae6');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'peptic_ulcer_disease', 'med_aluminium_magnesium_hydroxide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease'), 0), 'safe'::condition_safety, 'Symptomatic relief of ulcer and gastritis pain (adjunct; does not heal the ulcer).'
where exists (select 1 from public.diseases where id = 'peptic_ulcer_disease')
  and exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'peptic_ulcer_disease' and medicine_id = 'med_aluminium_magnesium_hydroxide');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_aluminium_magnesium_hydroxide', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Reduces absorption of dolutegravir and atazanavir; time doses apart.'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_aluminium_magnesium_hydroxide');
-- med_aluminium_magnesium_hydroxide
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_aluminium_magnesium_hydroxide', 'adult', 0, 'Dyspepsia, heartburn, ulcer/gastritis pain (suspension ~220 mg + 195 mg/5 mL)', 'PO', '10–20 mL', '3× a day + at bedtime', 'As needed', '—', 'Label · UK SmPC', '20 min–1 h after meals, or as required; also for ages 12+'),
    ('med_aluminium_magnesium_hydroxide', 'adult', 1, 'Acid indigestion, heartburn (suspension 200 mg + 200 mg/5 mL)', 'PO', '10–20 mL', '4× a day', '≤ 2 weeks at max dose', '80 mL/day', 'Label · US DailyMed', 'Also for ages 12+'),
    ('med_aluminium_magnesium_hydroxide', 'adult', 2, 'Gastritis / peptic ulcer pain (chewable tablet 400 mg + 400 mg)', 'PO', '1–2 tablets', '3× a day', 'By clinical response', '—', 'MSF', 'Or 1 tablet during painful episodes'),
    ('med_aluminium_magnesium_hydroxide', 'child', 3, 'Gastritis / peptic ulcer pain, over 5 years (tablet 400 mg + 400 mg)', 'PO', '½ tablet', '3× a day', 'By clinical response', '—', 'MSF', 'Rarely indicated')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_aluminium_magnesium_hydroxide');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_aluminium_magnesium_hydroxide', 'renal', 0, '', 'Ask a doctor before use with kidney disease or a magnesium-restricted diet.', 'Label · US DailyMed'),
    ('med_aluminium_magnesium_hydroxide', 'elderly', 1, '', 'Same dose as adults.', 'Label · UK SmPC'),
    ('med_aluminium_magnesium_hydroxide', 'pregnancy', 2, '', 'MSF lists no contraindication in pregnancy or breastfeeding; the UK label notes no clinical data for its product and advises caution in pregnancy.', 'MSF'),
    ('med_aluminium_magnesium_hydroxide', 'administration', 3, '', 'Shake suspension well; chew tablets thoroughly. Strengths differ between products, so dose by the product''s own label.', 'MSF'),
    ('med_aluminium_magnesium_hydroxide', 'administration', 4, '', 'Children under 12: not recommended for some suspensions (UK label) or only on a doctor''s advice (US OTC label).', 'Label · UK SmPC'),
    ('med_aluminium_magnesium_hydroxide', 'forms_ph', 5, '', 'Oral: 225 mg aluminium hydroxide + 200 mg magnesium hydroxide per 5 mL suspension (60 mL, 120 mL); 200 mg aluminium hydroxide + 100 mg magnesium hydroxide tablet.', 'PNF'),
    ('med_aluminium_magnesium_hydroxide', 'monitor', 6, '', 'Symptom relief; refer if symptoms last more than 2 weeks. Check the timing of other oral medicines (antibiotics, iron, antiretrovirals, levothyroxine).', 'Label · US DailyMed')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_aluminium_magnesium_hydroxide');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_aluminium_magnesium_hydroxide', 'PNF', 'Philippine National Formulary – Essential Medicines List', 'Department of Health / PhilHealth. Philippine National Formulary (PNF) Essential Medicines List. 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 0),
    ('med_aluminium_magnesium_hydroxide', 'Label · UK SmPC', 'UK SmPC – Mucogel Suspension', 'Rosemont Pharmaceuticals Ltd. Mucogel Suspension (220 mg dried aluminium hydroxide + 195 mg magnesium hydroxide per 5 mL) – SmPC. emc.', 'https://products.mhra.gov.uk/search/?search=aluminium+hydroxide#emc-13356', 1),
    ('med_aluminium_magnesium_hydroxide', 'MSF', 'MSF Essential Drugs – Aluminium hydroxide/Magnesium hydroxide oral', 'Médecins Sans Frontières. Essential drugs – practical guidelines: Aluminium hydroxide/Magnesium hydroxide, oral (400 mg + 400 mg chewable tablet).', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/aluminium-hydroxide-magnesium-hydroxide-oral-16685025.html', 2),
    ('med_aluminium_magnesium_hydroxide', 'Label · US DailyMed', 'DailyMed – Kesin Mag-Al suspension (OTC label)', 'KESIN MAG-AL (200 mg aluminum hydroxide + 200 mg magnesium hydroxide per 5 mL) – OTC drug label. DailyMed.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42df2198-14dc-da1c-e063-6394a90a1ae6', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_aluminium_magnesium_hydroxide')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_aluminium_magnesium_hydroxide');


-- ================================================ med_amlodipine  (Amlodipine)
update public.medicines set description = 'Amlodipine is a long-acting dihydropyridine calcium channel blocker that inhibits L-type calcium channels in vascular smooth muscle, causing arterial vasodilation and a fall in peripheral resistance and blood pressure. Its long half-life allows once-daily dosing. It is a first-line antihypertensive and is also used for chronic stable and vasospastic angina. In the Philippines it is listed in the PNF Essential Medicines List (5 mg and 10 mg tablets) and is the first drug in the national primary-care hypertension protocol, with losartan added if blood pressure stays above target. Amlodipine is not removed by dialysis, and the usual dose is used in renal impairment.', updated_at = now()
where id = 'med_amlodipine' and description = 'Amlodipine is a long-acting dihydropyridine calcium channel blocker that inhibits L-type calcium channels in vascular smooth muscle, causing arterial vasodilation and a fall in peripheral resistance and blood pressure. Its long half-life allows once-daily dosing. It is a first-line antihypertensive and is also used for chronic stable and vasospastic angina.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Philippine National Formulary (PhilHealth); National Protocol for Hypertension Management (Philippines)' else source_attribution || '; UK SmPC (emc); Philippine National Formulary (PhilHealth); National Protocol for Hypertension Management (Philippines)' end
where id = 'med_amlodipine' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'adverse', 'Abdominal pain and nausea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse' and content = 'Abdominal pain and nausea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'adverse', 'Gingival hyperplasia (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse' and content = 'Gingival hyperplasia (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'adverse', 'Hepatitis, jaundice and raised liver enzymes, mostly cholestatic (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse' and content = 'Hepatitis, jaundice and raised liver enzymes, mostly cholestatic (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'adverse', 'Extrapyramidal disorder (exceptional reports)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse' and content = 'Extrapyramidal disorder (exceptional reports)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'adverse', 'Angioedema, Stevens-Johnson syndrome and erythema multiforme (very rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse' and content = 'Angioedema, Stevens-Johnson syndrome and erythema multiforme (very rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'adverse', 'Overdose: marked prolonged hypotension and non-cardiogenic pulmonary oedema (may appear 24–48 h after ingestion)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'adverse' and content = 'Overdose: marked prolonged hypotension and non-cardiogenic pulmonary oedema (may appear 24–48 h after ingestion)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'contraindication', 'Hypersensitivity to other dihydropyridines', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication' and content = 'Hypersensitivity to other dihydropyridines');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'contraindication', 'Severe hypotension', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication' and content = 'Severe hypotension');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'contraindication', 'Shock, including cardiogenic shock', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication' and content = 'Shock, including cardiogenic shock');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'contraindication', 'Left ventricular outflow obstruction (e.g., high-grade aortic stenosis)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication' and content = 'Left ventricular outflow obstruction (e.g., high-grade aortic stenosis)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'contraindication', 'Haemodynamically unstable heart failure after acute myocardial infarction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'contraindication' and content = 'Haemodynamically unstable heart failure after acute myocardial infarction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'interaction', 'Diltiazem and verapamil (CYP3A4 inhibitors): increased amlodipine exposure and hypotension risk, especially in the elderly.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction' and content = 'Diltiazem and verapamil (CYP3A4 inhibitors): increased amlodipine exposure and hypotension risk, especially in the elderly.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'interaction', 'CYP3A4 inducers (rifampicin, St John''s wort): may alter amlodipine levels; monitor blood pressure during and after co-administration.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction' and content = 'CYP3A4 inducers (rifampicin, St John''s wort): may alter amlodipine levels; monitor blood pressure during and after co-administration.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'interaction', 'Grapefruit or grapefruit juice: not recommended (may increase blood-pressure lowering).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction' and content = 'Grapefruit or grapefruit juice: not recommended (may increase blood-pressure lowering).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'interaction', 'IV dantrolene: avoid calcium channel blockers in patients susceptible to or treated for malignant hyperthermia (hyperkalaemia risk).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction' and content = 'IV dantrolene: avoid calcium channel blockers in patients susceptible to or treated for malignant hyperthermia (hyperkalaemia risk).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amlodipine', 'interaction', 'mTOR inhibitors (sirolimus, temsirolimus, everolimus): amlodipine may increase their exposure.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amlodipine' and kind = 'interaction' and content = 'mTOR inhibitors (sirolimus, temsirolimus, everolimus): amlodipine may increase their exposure.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amlodipine', 'UK SmPC (emc)', 'Amlodipine 5 mg Tablets. Summary of Product Characteristics. Generics UK Ltd t/a Mylan (Viatris). electronic medicines compendium (emc); text revised 07/2022.', 'https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amlodipine'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amlodipine' and url = 'https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amlodipine', 'Philippine National Formulary (PhilHealth)', 'Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amlodipine'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amlodipine' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amlodipine', 'National Protocol for Hypertension Management (Philippines)', 'National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives; 2021 (rev. 2023).', 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amlodipine'), 0)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amlodipine' and url = 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_amlodipine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Use with caution: more pulmonary oedema in NYHA III–IV trial; contraindicated in unstable heart failure after acute MI.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_amlodipine');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'acute_coronary_syndrome', 'med_amlodipine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome'), 0), 'caution'::condition_safety, 'Contraindicated in haemodynamically unstable heart failure after acute MI and in cardiogenic shock.'
where exists (select 1 from public.diseases where id = 'acute_coronary_syndrome')
  and exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'acute_coronary_syndrome' and medicine_id = 'med_amlodipine');
-- med_amlodipine
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_amlodipine', 'adult', 0, 'Hypertension', 'PO', '5 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · UK SmPC', 'Increase by response'),
    ('med_amlodipine', 'adult', 1, 'Chronic stable or vasospastic angina', 'PO', '5 mg', 'Once a day', 'Long-term', '10 mg/day', 'Label · UK SmPC', ''),
    ('med_amlodipine', 'adult', 2, 'Hypertension (PH primary care)', 'PO', '5 mg, then 10 mg', 'Once a day', 'Long-term', '10 mg/day', 'PH HTN protocol', 'Step 1: 5 mg; step 2: add losartan 50 mg; step 3: amlodipine 10 mg + losartan 100 mg (1-month intervals)'),
    ('med_amlodipine', 'child', 3, 'Hypertension (6–17 years)', 'PO', '2.5 mg', 'Once a day', 'Long-term', '5 mg/day', 'Label · UK SmPC', 'May increase to 5 mg after 4 weeks; no data under 6 years')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_amlodipine');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_amlodipine', 'renal', 0, '', 'Usual dose. Amlodipine is not removed by dialysis.', 'Label · UK SmPC'),
    ('med_amlodipine', 'hepatic', 1, '', 'Mild–moderate impairment: start at the low end of the dose range. Severe impairment: start at the lowest dose and titrate slowly (prolonged half-life, higher AUC).', 'Label · UK SmPC'),
    ('med_amlodipine', 'elderly', 2, '', 'Usual doses apply; increase the dose with care.', 'Label · UK SmPC'),
    ('med_amlodipine', 'pregnancy', 3, '', 'Safety in pregnancy not established; use only when there is no safer alternative. Excreted in breast milk (infant dose about 3–7% of maternal dose, max 15%).', 'Label · UK SmPC'),
    ('med_amlodipine', 'administration', 4, '', 'Can be combined with thiazide diuretics, beta-blockers, alpha-blockers or ACE inhibitors. In the PH protocol, amlodipine and losartan are taken together; confirm adherence before stepping up.', 'PH HTN protocol'),
    ('med_amlodipine', 'forms_ph', 5, '', 'Amlodipine (as besilate/camsylate) 5 mg and 10 mg oral tablets.', 'PNF'),
    ('med_amlodipine', 'monitor', 6, '', 'Blood pressure and symptoms of hypotension; ankle/peripheral oedema; heart-failure symptoms; slow titration with close monitoring in hepatic impairment.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_amlodipine');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_amlodipine', 'Label · UK SmPC', 'UK SmPC (emc)', 'Amlodipine 5 mg Tablets SmPC, Generics UK Ltd t/a Mylan; text revised 07/2022.', 'https://products.mhra.gov.uk/search/?search=amlodipine#emc-2743', 0),
    ('med_amlodipine', 'PNF', 'Philippine National Formulary (PhilHealth)', 'PNF Essential Medicines List, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 1),
    ('med_amlodipine', 'PH HTN protocol', 'National Protocol for Hypertension Management (Philippines)', 'National Protocol for Hypertension Management in Primary Health Care Settings (Philippines). Resolve to Save Lives.', 'https://resolvetosavelives.org/wp-content/uploads/2023/09/htn-protocol-philippines_0721_rev-a_v1.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_amlodipine')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_amlodipine');


-- ================================================ med_amoxicillin  (Amoxicillin)
update public.medicines set description = 'Amoxicillin is a bactericidal beta-lactam that binds penicillin-binding proteins and inhibits transpeptidation in bacterial cell-wall synthesis, leading to cell lysis. It is a first-line agent for many respiratory, ENT, skin and urinary infections and a component of H. pylori eradication regimens. Oral bioavailability is about 70% and is not affected by food; the half-life is about 1 hour with mainly renal excretion, and the time the drug level stays above the MIC is the main driver of efficacy. CDC names penicillin or amoxicillin as the antibiotic of choice for group A streptococcal pharyngitis. In the Philippines, amoxicillin is on the PNF Essential Medicines List as 250 mg and 500 mg capsules, paediatric drops and oral suspension.', updated_at = now()
where id = 'med_amoxicillin' and description = 'Amoxicillin is a bactericidal beta-lactam that binds penicillin-binding proteins and inhibits transpeptidation in bacterial cell-wall synthesis, leading to cell lysis. It is a first-line agent for many respiratory, ENT, skin and urinary infections and a component of H. pylori eradication regimens.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Philippine National Formulary (PNF EML); CDC; Merck Manual Professional' else source_attribution || '; UK SmPC (emc); Philippine National Formulary (PNF EML); CDC; Merck Manual Professional' end
where id = 'med_amoxicillin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'indication', 'Typhoid and paratyphoid fevers', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication' and content = 'Typhoid and paratyphoid fevers');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'indication', 'Acute pyelonephritis and asymptomatic bacteriuria in pregnancy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication' and content = 'Acute pyelonephritis and asymptomatic bacteriuria in pregnancy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'indication', 'Dental abscess with spreading cellulitis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication' and content = 'Dental abscess with spreading cellulitis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'indication', 'Lyme disease', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication' and content = 'Lyme disease');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'indication', 'Prosthetic joint infections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication' and content = 'Prosthetic joint infections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'indication', 'Prophylaxis of endocarditis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'indication' and content = 'Prophylaxis of endocarditis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Mucocutaneous candidiasis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Mucocutaneous candidiasis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Blood disorders (very rare): reversible leucopenia, neutropenia, agranulocytosis, thrombocytopenia, haemolytic anaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Blood disorders (very rare): reversible leucopenia, neutropenia, agranulocytosis, thrombocytopenia, haemolytic anaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Convulsions, more likely with renal impairment, high doses or a seizure history', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Convulsions, more likely with renal impairment, high doses or a seizure history');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Crystalluria with acute kidney injury (mainly high-dose parenteral use)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Crystalluria with acute kidney injury (mainly high-dose parenteral use)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Jarisch-Herxheimer reaction during Lyme disease treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Jarisch-Herxheimer reaction during Lyme disease treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Kounis syndrome and drug-induced enterocolitis syndrome (mainly in children)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Kounis syndrome and drug-induced enterocolitis syndrome (mainly in children)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'adverse', 'Black hairy tongue', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'adverse' and content = 'Black hairy tongue');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'contraindication', 'Suspected infectious mononucleosis: avoid because of the high risk of rash (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'contraindication' and content = 'Suspected infectious mononucleosis: avoid because of the high risk of rash (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'contraindication', 'Previous acute generalised exanthematous pustulosis (AGEP) with amoxicillin: do not re-administer', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'contraindication' and content = 'Previous acute generalised exanthematous pustulosis (AGEP) with amoxicillin: do not re-administer');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'contraindication', 'Renal impairment: dose adjustment required (precaution)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'contraindication' and content = 'Renal impairment: dose adjustment required (precaution)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'interaction', 'Methotrexate: penicillins may reduce methotrexate excretion and increase its toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'interaction' and content = 'Methotrexate: penicillins may reduce methotrexate excretion and increase its toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_amoxicillin', 'interaction', 'Urine glucose tests: false-positive results with chemical methods; use enzymatic glucose oxidase tests.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_amoxicillin' and kind = 'interaction' and content = 'Urine glucose tests: false-positive results with chemical methods; use enzymatic glucose oxidase tests.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amoxicillin', 'UK SmPC (emc)', 'Amoxicillin 500 mg Capsules – Summary of Product Characteristics. Milpharm Limited (PL 16363/0045). Electronic Medicines Compendium (emc), medicines.org.uk; last updated April 2025.', 'https://products.mhra.gov.uk/search/?search=amoxicillin#emc-526', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amoxicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amoxicillin' and url = 'https://products.mhra.gov.uk/search/?search=amoxicillin#emc-526');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amoxicillin', 'Philippine National Formulary (PNF EML)', 'Philippine National Formulary Essential Medicines List, Volume I, 8th Edition (2019), as of November 02, 2022. PhilHealth / Department of Health.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amoxicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amoxicillin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amoxicillin', 'CDC', 'Centers for Disease Control and Prevention. Clinical Guidance for Group A Streptococcal Pharyngitis. Updated November 18, 2025.', 'https://www.cdc.gov/group-a-strep/hcp/clinical-guidance/strep-throat.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amoxicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amoxicillin' and url = 'https://www.cdc.gov/group-a-strep/hcp/clinical-guidance/strep-throat.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_amoxicillin', 'Merck Manual Professional', 'Werth BJ. Penicillins. Merck Manual Professional Edition. Reviewed May 2024.', 'https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/penicillins', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_amoxicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_amoxicillin' and url = 'https://www.merckmanuals.com/professional/infectious-diseases/bacteria-and-antibacterial-medications/penicillins');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'typhoid_fever', 'med_amoxicillin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'typhoid_fever'), 0), 'safe'::condition_safety, 'UK SmPC lists typhoid and paratyphoid fevers as an approved indication (use where the organism is susceptible)'
where exists (select 1 from public.diseases where id = 'typhoid_fever')
  and exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'typhoid_fever' and medicine_id = 'med_amoxicillin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_amoxicillin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Mainly renally excreted; dose reduction needed and seizure/crystalluria risk is higher with impaired renal function'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_amoxicillin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_amoxicillin');

-- ================================================ med_artemether_lumefantrine  (Artemether + Lumefantrine)
update public.medicines set description = 'Artemether (and its metabolite dihydroartemisinin) rapidly reduces parasite biomass, while the long-acting lumefantrine eliminates residual parasites; both are thought to interfere with parasite heme detoxification and nucleic acid/protein synthesis. This fixed-dose artemisinin-based combination therapy is a WHO-recommended first-line treatment for uncomplicated P. falciparum malaria. In the Philippines, DOH Administrative Order No. 2009-0001 made artemether-lumefantrine the first-line medicine for confirmed P. falciparum malaria, replacing chloroquine plus sulfadoxine-pyrimethamine, and allows an ACT for all Plasmodium species and mixed infections. It acts on the blood stages of P. vivax but not on the liver hypnozoites, so vivax and ovale infections still need an anti-relapse drug (primaquine or tafenoquine, after G6PD testing).', updated_at = now()
where id = 'med_artemether_lumefantrine' and description = 'Artemether (and its metabolite dihydroartemisinin) rapidly reduces parasite biomass, while the long-acting lumefantrine eliminates residual parasites; both are thought to interfere with parasite heme detoxification and nucleic acid/protein synthesis. This fixed-dose artemisinin-based combination therapy is a WHO-recommended first-line treatment for uncomplicated P. falciparum malaria.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc) - Riamet; WHO Prequalification - WHOPAR MA026; CDC - Malaria treatment tables; WHO guidelines for malaria; DOH AO 2009-0001; WHO Prequalification - WHOPAR MA026 (Riamet SmPC); Philippine National Formulary - Essential Medicines List; DOH Administrative Order No. 2009-0001' else source_attribution || '; UK SmPC (emc) - Riamet; WHO Prequalification - WHOPAR MA026; CDC - Malaria treatment tables; WHO guidelines for malaria; DOH AO 2009-0001; WHO Prequalification - WHOPAR MA026 (Riamet SmPC); Philippine National Formulary - Essential Medicines List; DOH Administrative Order No. 2009-0001' end
where id = 'med_artemether_lumefantrine' and position('UK SmPC (emc) - Riamet' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'indication', 'Uncomplicated P. malariae and P. knowlesi malaria (CDC treatment tables)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'indication' and content = 'Uncomplicated P. malariae and P. knowlesi malaria (CDC treatment tables)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'indication', 'Oral follow-on course after IV artesunate for severe malaria, once the patient can take oral medicines (CDC)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'indication' and content = 'Oral follow-on course after IV artesunate for severe malaria, once the patient can take oral medicines (CDC)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'adverse', 'Palpitations and sleep disorders', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse' and content = 'Palpitations and sleep disorders');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'adverse', 'Rash and pruritus', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse' and content = 'Rash and pruritus');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'adverse', 'Cough (very common in children)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse' and content = 'Cough (very common in children)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'adverse', 'Raised liver function tests (children)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse' and content = 'Raised liver function tests (children)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'adverse', 'Delayed haemolytic anaemia, reported up to a few weeks after treatment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'adverse' and content = 'Delayed haemolytic anaemia, reported up to a few weeks after treatment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'contraindication', 'Severe malaria (WHO definition), including cerebral malaria: not evaluated', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication' and content = 'Severe malaria (WHO definition), including cerebral malaria: not evaluated');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'contraindication', 'Family history of sudden death or congenital QTc prolongation, or other conditions known to prolong QTc', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication' and content = 'Family history of sudden death or congenital QTc prolongation, or other conditions known to prolong QTc');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'contraindication', 'Symptomatic arrhythmia, clinically relevant bradycardia or heart failure with reduced ejection fraction', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication' and content = 'Symptomatic arrhythmia, clinically relevant bradycardia or heart failure with reduced ejection fraction');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'contraindication', 'Electrolyte disturbances such as hypokalaemia or hypomagnesaemia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication' and content = 'Electrolyte disturbances such as hypokalaemia or hypomagnesaemia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'contraindication', 'Use with drugs metabolised by CYP2D6 (e.g., metoprolol, imipramine, amitriptyline, clomipramine)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'contraindication' and content = 'Use with drugs metabolised by CYP2D6 (e.g., metoprolol, imipramine, amitriptyline, clomipramine)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'interaction', 'CYP2D6 substrates (e.g., flecainide, metoprolol, imipramine, amitriptyline): contraindicated with artemether-lumefantrine.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction' and content = 'CYP2D6 substrates (e.g., flecainide, metoprolol, imipramine, amitriptyline): contraindicated with artemether-lumefantrine.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'interaction', 'Lopinavir/ritonavir: raises lumefantrine exposure about 2.3-fold.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction' and content = 'Lopinavir/ritonavir: raises lumefantrine exposure about 2.3-fold.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'interaction', 'Nevirapine and efavirenz: markedly reduce artemether exposure; use cautiously with antiretrovirals.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction' and content = 'Nevirapine and efavirenz: markedly reduce artemether exposure; use cautiously with antiretrovirals.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_artemether_lumefantrine', 'interaction', 'Other antimalarials: should not be given concurrently unless no other option exists.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_artemether_lumefantrine' and kind = 'interaction' and content = 'Other antimalarials: should not be given concurrently unless no other option exists.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_artemether_lumefantrine', 'UK SmPC (emc) - Riamet', 'Riamet 20 mg/120 mg tablets - Summary of Product Characteristics. Novartis Pharmaceuticals UK Ltd. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=artemether#emc-1628', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine' and url = 'https://products.mhra.gov.uk/search/?search=artemether#emc-1628');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_artemether_lumefantrine', 'WHO Prequalification - WHOPAR MA026', 'Riamet (artemether/lumefantrine 20 mg/120 mg tablets), Novartis Pharma Schweiz AG. WHO Public Assessment Report, Part 4: Summary of Product Characteristics. World Health Organization Prequalification Unit.', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/MA026part4v3.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine' and url = 'https://extranet.who.int/prequal/sites/default/files/whopar_files/MA026part4v3.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_artemether_lumefantrine', 'CDC - Malaria treatment tables', 'Centers for Disease Control and Prevention. Appendix A: Malaria in the United States - Treatment Tables. Clinical guidance for healthcare providers.', 'https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine' and url = 'https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_artemether_lumefantrine', 'WHO guidelines for malaria', 'World Health Organization. WHO guidelines for malaria. Geneva: WHO; latest version 10 September 2026.', 'https://www.who.int/publications/i/item/guidelines-for-malaria', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine' and url = 'https://www.who.int/publications/i/item/guidelines-for-malaria');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_artemether_lumefantrine', 'DOH AO 2009-0001', 'Department of Health (Philippines). Administrative Order No. 2009-0001: Revised Policy and Guidelines on the Diagnosis and Treatment for Malaria. 13 January 2009.', 'https://dev.lawyerly.ph/laws/46597', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine'), 0)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_artemether_lumefantrine' and url = 'https://dev.lawyerly.ph/laws/46597');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hiv_infection', 'med_artemether_lumefantrine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hiv_infection'), 0), 'caution'::condition_safety, 'Antiretrovirals change exposure (lopinavir/ritonavir raises lumefantrine; nevirapine/efavirenz lower artemether); may reduce efficacy.'
where exists (select 1 from public.diseases where id = 'hiv_infection')
  and exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hiv_infection' and medicine_id = 'med_artemether_lumefantrine');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'tuberculosis', 'med_artemether_lumefantrine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'tuberculosis'), 0), 'avoid'::condition_safety, 'Rifampicin (strong CYP3A4 inducer) sharply lowers artemether/lumefantrine levels; combination is contraindicated.'
where exists (select 1 from public.diseases where id = 'tuberculosis')
  and exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'tuberculosis' and medicine_id = 'med_artemether_lumefantrine');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_artemether_lumefantrine', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'avoid'::condition_safety, 'Contraindicated in heart failure with reduced ejection fraction because of QT/arrhythmia risk.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_artemether_lumefantrine');
-- med_artemether_lumefantrine
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_artemether_lumefantrine', 'adult', 0, 'Uncomplicated malaria (≥35 kg or ≥12 y)', 'PO', '4 tablets (80/480 mg)', 'At 0 h and 8 h, then 2× a day', '3 days (6 doses)', '24 tablets/course', 'WHO PQ', 'Take with food or a milky drink'),
    ('med_artemether_lumefantrine', 'child', 1, 'Uncomplicated malaria, 5 to <15 kg', 'PO', '1 tablet (20/120 mg)', 'At 0 h and 8 h, then 2× a day', '3 days (6 doses)', '6 tablets/course', 'WHO PQ', 'Tablet may be crushed'),
    ('med_artemether_lumefantrine', 'child', 2, 'Uncomplicated malaria, 15 to <25 kg', 'PO', '2 tablets (40/240 mg)', 'At 0 h and 8 h, then 2× a day', '3 days (6 doses)', '12 tablets/course', 'WHO PQ', ''),
    ('med_artemether_lumefantrine', 'child', 3, 'Uncomplicated malaria, 25 to <35 kg', 'PO', '3 tablets (60/360 mg)', 'At 0 h and 8 h, then 2× a day', '3 days (6 doses)', '18 tablets/course', 'WHO PQ', ''),
    ('med_artemether_lumefantrine', 'child', 4, 'Uncomplicated malaria, ≥35 kg', 'PO', '4 tablets (80/480 mg)', 'At 0 h and 8 h, then 2× a day', '3 days (6 doses)', '24 tablets/course', 'WHO PQ', 'Same as adult dose')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_artemether_lumefantrine');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_artemether_lumefantrine', 'renal', 0, '', 'No dose adjustment recommended; in severe renal impairment use with caution and monitor ECG and blood potassium.', 'Label · UK SmPC'),
    ('med_artemether_lumefantrine', 'hepatic', 1, '', 'No dose adjustment in mild to moderate hepatic impairment; in severe impairment use with caution and monitor ECG and blood potassium.', 'Label · UK SmPC'),
    ('med_artemether_lumefantrine', 'elderly', 2, '', 'No information suggesting the dose should differ in patients over 65 years.', 'Label · UK SmPC'),
    ('med_artemether_lumefantrine', 'pregnancy', 3, '', 'CDC states artemether-lumefantrine can be used in all trimesters of pregnancy, per WHO evidence review and policy (older labels still advise against first-trimester use if alternatives exist). Primaquine and tafenoquine must not be given in pregnancy.', 'CDC'),
    ('med_artemether_lumefantrine', 'pregnancy', 4, '', 'Breastfeeding: the UK label advises not breastfeeding during treatment and for at least one week after the last dose; CDC advises against use in women breastfeeding infants <5 kg.', 'Label · UK SmPC'),
    ('med_artemether_lumefantrine', 'administration', 5, '', 'Tablets may be crushed for infants and children; dispersible tablets exist for paediatric use and are not recommended for adults.', 'WHO PQ'),
    ('med_artemether_lumefantrine', 'administration', 6, '<5 kg', 'Infants <5 kg: the standard tablet is not established below 5 kg; the September 2026 WHO malaria guidelines add a new artemether-lumefantrine formulation for children under 5 kg.', 'WHO 2026'),
    ('med_artemether_lumefantrine', 'administration', 7, 'Radical cure', 'P. vivax / P. ovale: after the blood-stage course, give primaquine 0.5 mg/kg base (adults 30 mg base) once a day for 14 days, or tafenoquine 300 mg once (≥16 y), only after quantitative G6PD testing shows normal activity.', 'CDC'),
    ('med_artemether_lumefantrine', 'administration', 8, '', 'Philippine policy: antimalarials used must be WHO-prequalified or GMP-certified; quinine plus tetracycline, doxycycline or clindamycin for 7 days is the second-line option if AL fails or is unavailable.', 'DOH AO 2009-0001'),
    ('med_artemether_lumefantrine', 'forms_ph', 9, '', 'Oral tablet, 20 mg artemether + 120 mg lumefantrine. Listed as a List B medicine (needs in vivo bioequivalence studies).', 'PNF'),
    ('med_artemether_lumefantrine', 'monitor', 10, '', 'Watch for QT prolongation: check ECG and correct potassium/magnesium if the patient deteriorates, has severe hepatic or renal impairment, or takes other QT-prolonging drugs.', 'Label · UK SmPC'),
    ('med_artemether_lumefantrine', 'monitor', 11, '', 'Check haemoglobin if the patient becomes pale or tired in the weeks after treatment (delayed haemolytic anaemia has been reported).', 'Label · UK SmPC'),
    ('med_artemether_lumefantrine', 'monitor', 12, '', 'Overdose: symptomatic and supportive care with ECG and blood potassium monitoring.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_artemether_lumefantrine');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_artemether_lumefantrine', 'WHO PQ', 'WHO Prequalification - WHOPAR MA026 (Riamet SmPC)', 'Riamet (artemether/lumefantrine 20 mg/120 mg tablets). WHO Public Assessment Report, Part 4: Summary of Product Characteristics. WHO Prequalification Unit.', 'https://extranet.who.int/prequal/sites/default/files/whopar_files/MA026part4v3.pdf', 0),
    ('med_artemether_lumefantrine', 'Label · UK SmPC', 'UK SmPC (emc) - Riamet', 'Riamet 20 mg/120 mg tablets - Summary of Product Characteristics. Novartis Pharmaceuticals UK Ltd. emc.', 'https://products.mhra.gov.uk/search/?search=artemether#emc-1628', 1),
    ('med_artemether_lumefantrine', 'CDC', 'CDC - Malaria treatment tables', 'Centers for Disease Control and Prevention. Appendix A: Malaria in the United States - Treatment Tables.', 'https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html', 2),
    ('med_artemether_lumefantrine', 'WHO 2026', 'WHO guidelines for malaria', 'World Health Organization. WHO guidelines for malaria. Geneva: WHO; 10 September 2026.', 'https://www.who.int/publications/i/item/guidelines-for-malaria', 3),
    ('med_artemether_lumefantrine', 'PNF', 'Philippine National Formulary - Essential Medicines List', 'Philippine National Formulary Essential Medicines List. PhilHealth / Department of Health; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4),
    ('med_artemether_lumefantrine', 'DOH AO 2009-0001', 'DOH Administrative Order No. 2009-0001', 'Department of Health (Philippines). Revised Policy and Guidelines on the Diagnosis and Treatment for Malaria. 13 January 2009.', 'https://dev.lawyerly.ph/laws/46597', 5)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_artemether_lumefantrine')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_artemether_lumefantrine');


-- ================================================ med_aspirin  (Aspirin (low-dose))
update public.medicines set description = 'Aspirin irreversibly acetylates platelet cyclooxygenase-1, blocking thromboxane A2 synthesis for the life of the platelet and thereby inhibiting platelet aggregation. At low doses it is used for acute coronary syndromes and secondary prevention of cardiovascular and cerebrovascular events. In the Philippines, the DOH dengue case-management guidelines tell patients not to take aspirin, mefenamic acid or other NSAIDs during dengue and to use paracetamol instead, because these drugs raise bleeding risk. It is not recommended for children and adolescents under 16 except on medical advice (Reye''s syndrome), and low-dose aspirin is not used as an analgesic, antipyretic or anti-inflammatory.', updated_at = now()
where id = 'med_aspirin' and description = 'Aspirin irreversibly acetylates platelet cyclooxygenase-1, blocking thromboxane A2 synthesis for the life of the platelet and thereby inhibiting platelet aggregation. At low doses it is used for acute coronary syndromes and secondary prevention of cardiovascular and cerebrovascular events.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Philippine National Formulary (PhilHealth); Department of Health (Philippines); World Health Organization' else source_attribution || '; UK SmPC (emc); Philippine National Formulary (PhilHealth); Department of Health (Philippines); World Health Organization' end
where id = 'med_aspirin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'indication', 'Stable angina and history of unstable angina (prevention of cardiovascular events)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'indication' and content = 'Stable angina and history of unstable angina (prevention of cardiovascular events)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'indication', 'Prevention of graft occlusion after coronary artery bypass grafting', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'indication' and content = 'Prevention of graft occlusion after coronary artery bypass grafting');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'indication', 'Coronary angioplasty (outside the acute phase)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'indication' and content = 'Coronary angioplasty (outside the acute phase)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Tinnitus and reduced hearing', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Tinnitus and reduced hearing');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Hyperuricaemia (low doses reduce uric acid excretion; may trigger gout)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Hyperuricaemia (low doses reduce uric acid excretion; may trigger gout)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Kounis syndrome (allergic acute coronary syndrome)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Kounis syndrome (allergic acute coronary syndrome)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Thrombocytopenia, agranulocytosis, aplastic anaemia (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Thrombocytopenia, agranulocytosis, aplastic anaemia (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Severe skin reactions: Stevens-Johnson syndrome, Lyell''s syndrome (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Severe skin reactions: Stevens-Johnson syndrome, Lyell''s syndrome (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Renal impairment and acute renal failure', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Renal impairment and acute renal failure');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'adverse', 'Menorrhagia', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'adverse' and content = 'Menorrhagia');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'contraindication', 'Acute or recurrent peptic ulcer, or history of NSAID-related GI bleeding/perforation', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication' and content = 'Acute or recurrent peptic ulcer, or history of NSAID-related GI bleeding/perforation');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'contraindication', 'Severe hepatic, renal or cardiac insufficiency', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication' and content = 'Severe hepatic, renal or cardiac insufficiency');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'contraindication', 'Doses above 100 mg/day in the third trimester of pregnancy', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication' and content = 'Doses above 100 mg/day in the third trimester of pregnancy');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'contraindication', 'Methotrexate above 15 mg/week', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication' and content = 'Methotrexate above 15 mg/week');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'contraindication', 'Suspected or confirmed dengue (DOH/WHO: avoid aspirin and NSAIDs; use paracetamol)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'contraindication' and content = 'Suspected or confirmed dengue (DOH/WHO: avoid aspirin and NSAIDs; use paracetamol)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Alteplase: do not start aspirin within 24 h after thrombolysis for acute stroke.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Alteplase: do not start aspirin within 24 h after thrombolysis for acute stroke.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Probenecid and sulfinpyrazone: salicylates reverse their uricosuric effect (not recommended).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Probenecid and sulfinpyrazone: salicylates reverse their uricosuric effect (not recommended).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Sulfonylureas and insulin: enhanced hypoglycaemic effect; dose adjustment may be needed.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Sulfonylureas and insulin: enhanced hypoglycaemic effect; dose adjustment may be needed.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Digoxin and lithium: reduced renal excretion; monitor plasma levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Digoxin and lithium: reduced renal excretion; monitor plasma levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Acetazolamide: severe acidosis and CNS toxicity.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Acetazolamide: severe acidosis and CNS toxicity.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Metamizole: may reduce the antiplatelet effect of aspirin.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Metamizole: may reduce the antiplatelet effect of aspirin.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_aspirin', 'interaction', 'Valproate and phenytoin: altered protein binding and free drug levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_aspirin' and kind = 'interaction' and content = 'Valproate and phenytoin: altered protein binding and free drug levels.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aspirin', 'UK SmPC (emc)', 'Aspirin 75 mg Tablets. Summary of Product Characteristics. G.L. Pharma GmbH. electronic medicines compendium (emc); revised 03/08/2026.', 'https://products.mhra.gov.uk/search/?search=aspirin#emc-107619', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aspirin'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aspirin' and url = 'https://products.mhra.gov.uk/search/?search=aspirin#emc-107619');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aspirin', 'Philippine National Formulary (PhilHealth)', 'Philippine National Formulary Essential Medicines List (PNF-EML), 2022. Department of Health / PhilHealth.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aspirin'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aspirin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aspirin', 'Department of Health (Philippines)', 'Department of Health. Administrative Order: Revised Dengue Clinical Case Management Guidelines 2011. Manila: DOH; 2012.', 'https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aspirin'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aspirin' and url = 'https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_aspirin', 'World Health Organization', 'World Health Organization. Dengue and severe dengue. Fact sheet; 21 August 2025.', 'https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_aspirin'), 0)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_aspirin' and url = 'https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_aspirin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'Contraindicated in severe cardiac insufficiency.'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_aspirin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'chronic_kidney_disease', 'med_aspirin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease'), 0), 'caution'::condition_safety, 'Contraindicated in severe renal insufficiency; caution in moderate impairment and with diuretics/ACE inhibitors.'
where exists (select 1 from public.diseases where id = 'chronic_kidney_disease')
  and exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'chronic_kidney_disease' and medicine_id = 'med_aspirin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hypertension', 'med_aspirin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hypertension'), 0), 'caution'::condition_safety, 'Caution in uncontrolled hypertension; may reduce the effect of antihypertensives.'
where exists (select 1 from public.diseases where id = 'hypertension')
  and exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hypertension' and medicine_id = 'med_aspirin');
-- med_aspirin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_aspirin', 'adult', 0, 'Secondary prevention of MI, stable angina, post-CABG', 'PO', '75–160 mg', 'Once a day', 'Long-term', '300 mg/day', 'Label · UK SmPC', ''),
    ('med_aspirin', 'adult', 1, 'Secondary prevention of TIA / ischaemic stroke', 'PO', '75–300 mg', 'Once a day', 'Long-term', '300 mg/day', 'Label · UK SmPC', 'Start only after intracerebral haemorrhage is excluded'),
    ('med_aspirin', 'adult', 2, 'Acute myocardial infarction', 'PO', '150–300 mg loading, then 75–160 mg', 'Once a day', 'Long-term', '300 mg/day', 'Label · UK SmPC', ''),
    ('med_aspirin', 'child', 3, 'Under 16 years', 'PO', 'Not recommended', '—', '—', '—', 'Label · UK SmPC', 'Reye''s syndrome risk; only on medical advice')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_aspirin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_aspirin', 'renal', 0, '', 'Contraindicated in severe renal insufficiency; use with caution in moderate impairment or dehydration.', 'Label · UK SmPC'),
    ('med_aspirin', 'hepatic', 1, '', 'Contraindicated in severe hepatic insufficiency; in mild–moderate impairment use with caution and check liver function regularly.', 'Label · UK SmPC'),
    ('med_aspirin', 'elderly', 2, '', 'More prone to adverse effects; usual adult dose if no severe renal or hepatic insufficiency; review treatment regularly.', 'Label · UK SmPC'),
    ('med_aspirin', 'pregnancy', 3, '', 'Up to 100 mg/day appears safe for restricted obstetric use under specialist monitoring; higher doses contraindicated in the third trimester. Breastfeeding: short-term use acceptable; stop with long-term or high-dose use.', 'Label · UK SmPC'),
    ('med_aspirin', 'administration', 4, '', 'Swallow with about half a glass of water. Bleeding risk persists 4–8 days after stopping; temporary withdrawal may be needed before surgery, including tooth extraction.', 'Label · UK SmPC'),
    ('med_aspirin', 'administration', 5, '', 'Dengue: patients should not take aspirin, mefenamic acid or other NSAIDs; use paracetamol (max 4 g/day in adults). Those already on these drugs should consult their doctor.', 'DOH 2012'),
    ('med_aspirin', 'forms_ph', 6, '', 'Aspirin oral tablets 80 mg, 100 mg, 300 mg and 325 mg.', 'PNF'),
    ('med_aspirin', 'monitor', 7, '', 'Signs of GI bleeding (black stools, haematemesis) and anaemia; gout flares; renal function when combined with diuretics, ACE inhibitors or ARBs; blood glucose with sulfonylureas or insulin.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_aspirin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_aspirin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Aspirin 75 mg Tablets SmPC, G.L. Pharma GmbH; revised 03/08/2026.', 'https://products.mhra.gov.uk/search/?search=aspirin#emc-107619', 0),
    ('med_aspirin', 'PNF', 'Philippine National Formulary (PhilHealth)', 'PNF Essential Medicines List, 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 1),
    ('med_aspirin', 'DOH 2012', 'Department of Health (Philippines)', 'Revised Dengue Clinical Case Management Guidelines 2011 (Administrative Order, 2012).', 'https://doh.gov.ph/wp-content/uploads/2023/08/ao2012-0026-1.pdf', 2)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_aspirin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_aspirin');


-- ================================================ med_atorvastatin  (Atorvastatin)
update public.medicines set description = 'Atorvastatin competitively inhibits HMG-CoA reductase, the rate-limiting enzyme of hepatic cholesterol synthesis, which up-regulates hepatic LDL receptors and lowers LDL-cholesterol. Moderate-intensity doses (10-20 mg) lower LDL-C by about 30-50% and high-intensity doses (40-80 mg) by more than 50%. It reduces the risk of MI, stroke and revascularization in primary and secondary prevention. The 2020 Philippine dyslipidemia guidelines recommend early, maximally tolerated high-intensity statin therapy after ACS, an LDL-C goal below 55 mg/dL in clinical ASCVD, and statins for CKD patients not on dialysis (lipid care of dialysis and transplant patients is referred to a nephrologist). In the Philippines it is listed in the PNF as 10, 20, 40 and 80 mg tablets.', updated_at = now()
where id = 'med_atorvastatin' and description = 'Atorvastatin competitively inhibits HMG-CoA reductase, the rate-limiting enzyme of hepatic cholesterol synthesis, which up-regulates hepatic LDL receptors and lowers LDL-cholesterol. Moderate-intensity doses (10-20 mg) lower LDL-C by about 30-50% and high-intensity doses (40-80 mg) by more than 50%. It reduces the risk of MI, stroke and revascularization in primary and secondary prevention.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); JAFES (Philippine CPG); DailyMed (FDA label); PhilHealth / DOH (PNF-EML); Philippine Dyslipidemia CPG 2020; Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); JAFES (Philippine CPG); DailyMed (FDA label); PhilHealth / DOH (PNF-EML); Philippine Dyslipidemia CPG 2020; Philippine National Formulary – EML' end
where id = 'med_atorvastatin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'indication', 'Heterozygous familial hypercholesterolaemia in children aged 10 years and over', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'indication' and content = 'Heterozygous familial hypercholesterolaemia in children aged 10 years and over');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'adverse', 'Constipation, flatulence, nausea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse' and content = 'Constipation, flatulence, nausea');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'adverse', 'Myalgia, muscle spasms, joint swelling, back pain', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse' and content = 'Myalgia, muscle spasms, joint swelling, back pain');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'adverse', 'Raised creatine kinase', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse' and content = 'Raised creatine kinase');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'adverse', 'Interstitial lung disease (rare)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse' and content = 'Interstitial lung disease (rare)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'adverse', 'Higher haemorrhagic stroke incidence with 80 mg in patients with recent stroke/TIA (SPARCL), especially prior haemorrhagic stroke or lacunar infarct', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'adverse' and content = 'Higher haemorrhagic stroke incidence with 80 mg in patients with recent stroke/TIA (SPARCL), especially prior haemorrhagic stroke or lacunar infarct');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'contraindication', 'Active liver disease or unexplained persistent transaminase elevation >3× ULN', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication' and content = 'Active liver disease or unexplained persistent transaminase elevation >3× ULN');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'contraindication', 'Pregnancy and breastfeeding', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication' and content = 'Pregnancy and breastfeeding');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'contraindication', 'Women of childbearing potential not using appropriate contraception', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication' and content = 'Women of childbearing potential not using appropriate contraception');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'contraindication', 'Concurrent glecaprevir/pibrentasvir', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'contraindication' and content = 'Concurrent glecaprevir/pibrentasvir');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'interaction', 'Systemic fusidic acid: must not be co-administered (fatal rhabdomyolysis reported); stop the statin and restart 7 days after the last fusidic acid dose.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction' and content = 'Systemic fusidic acid: must not be co-administered (fatal rhabdomyolysis reported); stop the statin and restart 7 days after the last fusidic acid dose.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'interaction', 'Elbasvir/grazoprevir or letermovir: do not exceed 20 mg daily; letermovir with ciclosporin is not recommended.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction' and content = 'Elbasvir/grazoprevir or letermovir: do not exceed 20 mg daily; letermovir with ciclosporin is not recommended.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'interaction', 'Rifampicin: give at the same time; delayed atorvastatin dosing markedly lowers its levels.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction' and content = 'Rifampicin: give at the same time; delayed atorvastatin dosing markedly lowers its levels.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_atorvastatin', 'interaction', 'Azithromycin: post-marketing rhabdomyolysis reported with statins; use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_atorvastatin' and kind = 'interaction' and content = 'Azithromycin: post-marketing rhabdomyolysis reported with statins; use with caution.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_atorvastatin', 'UK SmPC (emc)', 'Atorvastatin 20 mg Film-coated Tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; revised 2024. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_atorvastatin'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_atorvastatin' and url = 'https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_atorvastatin', 'JAFES (Philippine CPG)', 'Gonzalez-Santos LE, Oliva R, Jimeno C, et al. Executive Summary of the 2020 Clinical Practice Guidelines for the Management of Dyslipidemia in the Philippines. J ASEAN Fed Endocr Soc. 2021;36(1):5–11. doi:10.15605/jafes.036.01.01', 'https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_atorvastatin'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_atorvastatin' and url = 'https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_atorvastatin', 'DailyMed (FDA label)', 'LIPITOR (atorvastatin calcium) tablet, film coated. Prescribing information. Viatris Specialty LLC; updated April 2024. DailyMed, U.S. National Library of Medicine.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_atorvastatin'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_atorvastatin' and url = 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_atorvastatin', 'PhilHealth / DOH (PNF-EML)', 'Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_atorvastatin'), 0)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_atorvastatin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_a', 'med_atorvastatin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_a'), 0), 'avoid'::condition_safety, 'Active liver disease is a contraindication (UK SmPC).'
where exists (select 1 from public.diseases where id = 'hepatitis_a')
  and exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_a' and medicine_id = 'med_atorvastatin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'hepatitis_b', 'med_atorvastatin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'hepatitis_b'), 0), 'caution'::condition_safety, 'Use with caution in hepatic impairment; contraindicated if active liver disease or persistent transaminases >3× ULN.'
where exists (select 1 from public.diseases where id = 'hepatitis_b')
  and exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'hepatitis_b' and medicine_id = 'med_atorvastatin');
-- med_atorvastatin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_atorvastatin', 'adult', 0, 'Hypercholesterolaemia / mixed dyslipidaemia', 'PO', '10 mg', 'Once a day', 'Long-term', '80 mg/day', 'Label · UK SmPC', 'Adjust at intervals of ≥4 weeks'),
    ('med_atorvastatin', 'adult', 1, 'Moderate-intensity statin therapy', 'PO', '10–20 mg', 'Once a day', 'Long-term', '—', 'PH CPG 2020', 'Lowers LDL-C 30–50%'),
    ('med_atorvastatin', 'adult', 2, 'High-intensity therapy (ASCVD, ACS, FH)', 'PO', '40–80 mg', 'Once a day', 'Long-term', '80 mg/day', 'PH CPG 2020', 'Start early after ACS'),
    ('med_atorvastatin', 'adult', 3, 'With elbasvir/grazoprevir or letermovir', 'PO', '≤20 mg', 'Once a day', '—', '20 mg/day', 'Label · UK SmPC', ''),
    ('med_atorvastatin', 'child', 4, 'Heterozygous FH (≥10 y)', 'PO', '10 mg', 'Once a day', 'Long-term', '80 mg/day', 'Label · UK SmPC', 'US label range 10–20 mg; not indicated <10 y'),
    ('med_atorvastatin', 'child', 5, 'Homozygous FH (≥10 y)', 'PO', '10–20 mg', 'Once a day', 'Long-term', '80 mg/day', 'Label · US FDA', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_atorvastatin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_atorvastatin', 'renal', 0, '', 'No dose adjustment; monitor for myopathy.', 'Label · US FDA'),
    ('med_atorvastatin', 'renal', 1, 'Dialysis', 'Patients on dialysis or after kidney transplant: lipid management by a nephrologist (no statin recommendation made).', 'PH CPG 2020'),
    ('med_atorvastatin', 'hepatic', 2, '', 'Use with caution in hepatic impairment; contraindicated in active liver disease.', 'Label · UK SmPC'),
    ('med_atorvastatin', 'elderly', 3, '', 'Efficacy and safety in patients over 70 at recommended doses are similar to the general population.', 'Label · UK SmPC'),
    ('med_atorvastatin', 'pregnancy', 4, '', 'Contraindicated in pregnancy and breastfeeding; women of childbearing potential should use appropriate contraception.', 'Label · UK SmPC'),
    ('med_atorvastatin', 'administration', 5, '', 'Whole daily dose at once, any time of day, with or without food. Give at the same time as rifampicin.', 'Label · UK SmPC'),
    ('med_atorvastatin', 'forms_ph', 6, '', 'Tablet: 10 mg, 20 mg, 40 mg, 80 mg (as calcium).', 'PNF'),
    ('med_atorvastatin', 'monitor', 7, '', 'Liver function tests before starting and periodically thereafter.', 'Label · UK SmPC'),
    ('med_atorvastatin', 'monitor', 8, '', 'Lipid panel (LDL-C) as early as 4 weeks after starting or changing the dose.', 'Label · US FDA'),
    ('med_atorvastatin', 'monitor', 9, '', 'Ask about muscle pain/weakness; check CK if present; stop if CK >10× ULN or rhabdomyolysis suspected.', 'Label · UK SmPC')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_atorvastatin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_atorvastatin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Atorvastatin 20 mg Film-coated Tablets. Summary of Product Characteristics. Sun Pharma UK Ltd; revised 2024.', 'https://products.mhra.gov.uk/search/?search=atorvastatin#emc-4343', 0),
    ('med_atorvastatin', 'Label · US FDA', 'DailyMed (FDA label)', 'LIPITOR (atorvastatin calcium) tablets. Prescribing information. Viatris; updated April 2024.', 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a60cc18b-0631-4cf0-b021-9f52224ece65', 1),
    ('med_atorvastatin', 'PH CPG 2020', 'Philippine Dyslipidemia CPG 2020', 'Gonzalez-Santos LE, et al. Executive Summary of the 2020 Clinical Practice Guidelines for the Management of Dyslipidemia in the Philippines. J ASEAN Fed Endocr Soc. 2021;36(1):5–11.', 'https://www.asean-endocrinejournal.org/index.php/JAFES/article/view/927', 2),
    ('med_atorvastatin', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 3)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_atorvastatin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_atorvastatin');


-- ================================================ med_azithromycin  (Azithromycin)
update public.medicines set description = 'Azithromycin is an azalide macrolide that binds the 23S rRNA of the 50S ribosomal subunit and inhibits bacterial protein synthesis; it is mainly bacteriostatic. Its long tissue half-life allows short once-daily courses for respiratory infections, atypical pneumonia and sexually transmitted infections. In the Philippines it is listed in the PNF as capsules, tablets, oral suspension and a vial for IV infusion. Beyond respiratory and sexually transmitted infections, it is used as a single-dose treatment for cholera and trachoma and as a 7-day oral option for typhoid fever.', updated_at = now()
where id = 'med_azithromycin' and description = 'Azithromycin is an azalide macrolide that binds the 23S rRNA of the 50S ribosomal subunit and inhibits bacterial protein synthesis; it is mainly bacteriostatic. Its long tissue half-life allows short once-daily courses for respiratory infections, atypical pneumonia and sexually transmitted infections.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'UK SmPC (emc); Pfizer labeling (US); MSF Essential Drugs; PhilHealth / DOH (PNF-EML); Philippine National Formulary – EML' else source_attribution || '; UK SmPC (emc); Pfizer labeling (US); MSF Essential Drugs; PhilHealth / DOH (PNF-EML); Philippine National Formulary – EML' end
where id = 'med_azithromycin' and position('UK SmPC (emc)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Acute otitis media', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Acute otitis media');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Gonococcal urethritis/cervicitis (together with a second agent such as ceftriaxone)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Gonococcal urethritis/cervicitis (together with a second agent such as ceftriaxone)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Pelvic inflammatory disease (IV then oral)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Pelvic inflammatory disease (IV then oral)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Typhoid fever', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Typhoid fever');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Cholera (single dose, susceptible strains)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Cholera (single dose, susceptible strains)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Pertussis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Pertussis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Leptospirosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Leptospirosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Trachoma (single dose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Trachoma (single dose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Yaws (single dose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Yaws (single dose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'indication', 'Shigellosis (second-line)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'indication' and content = 'Shigellosis (second-line)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'adverse', 'Vomiting, headache', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse' and content = 'Vomiting, headache');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'adverse', 'Deafness and tinnitus (hearing disorders usually reversible)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse' and content = 'Deafness and tinnitus (hearing disorders usually reversible)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'adverse', 'Dizziness, drowsiness, convulsions', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse' and content = 'Dizziness, drowsiness, convulsions');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'adverse', 'Visual impairment (uncommon)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse' and content = 'Visual impairment (uncommon)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'adverse', 'Decreased lymphocytes and bicarbonate; increased eosinophils', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse' and content = 'Decreased lymphocytes and bicarbonate; increased eosinophils');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'adverse', 'Electrolyte disturbances', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'adverse' and content = 'Electrolyte disturbances');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'contraindication', 'Severe hepatic impairment', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'contraindication'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'contraindication' and content = 'Severe hepatic impairment');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'interaction', 'Ergot derivatives: do not co-administer (risk of ergotism).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction' and content = 'Ergot derivatives: do not co-administer (risk of ergotism).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'interaction', 'Ciclosporin: peak levels rise about 24%; monitor and adjust.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction' and content = 'Ciclosporin: peak levels rise about 24%; monitor and adjust.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'interaction', 'Statins (e.g., atorvastatin): rhabdomyolysis reported; use with caution.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction' and content = 'Statins (e.g., atorvastatin): rhabdomyolysis reported; use with caution.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'interaction', 'Dabigatran: possible increased bleeding risk.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction' and content = 'Dabigatran: possible increased bleeding risk.');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'interaction', 'Antimalarials with QT effect (artemether-lumefantrine, chloroquine, mefloquine, quinine), amiodarone, fluconazole, ondansetron: avoid combining (QT prolongation).', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction' and content = 'Antimalarials with QT effect (artemether-lumefantrine, chloroquine, mefloquine, quinine), amiodarone, fluconazole, ondansetron: avoid combining (QT prolongation).');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_azithromycin', 'interaction', 'Aluminium/magnesium hydroxide antacids: separate doses by 2 hours.', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_azithromycin' and kind = 'interaction' and content = 'Aluminium/magnesium hydroxide antacids: separate doses by 2 hours.');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_azithromycin', 'UK SmPC (emc)', 'Zithromax 250 mg Capsules. Summary of Product Characteristics. Pfizer Ltd; updated July 2026. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=azithromycin#emc-1073', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_azithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_azithromycin' and url = 'https://products.mhra.gov.uk/search/?search=azithromycin#emc-1073');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_azithromycin', 'UK SmPC (emc)', 'Zithromax 200 mg/5 ml Powder for Oral Suspension. Summary of Product Characteristics. Pfizer Ltd; updated July 2026. electronic medicines compendium (emc).', 'https://products.mhra.gov.uk/search/?search=azithromycin#emc-3006', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_azithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_azithromycin' and url = 'https://products.mhra.gov.uk/search/?search=azithromycin#emc-3006');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_azithromycin', 'Pfizer labeling (US)', 'ZITHROMAX (azithromycin dihydrate) injection, powder, lyophilized, for solution. Prescribing information. Pfizer Inc; revised 2026.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=1181', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_azithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_azithromycin' and url = 'https://labeling.pfizer.com/ShowLabeling.aspx?id=1181');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_azithromycin', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Azithromycin oral. MSF Medical Guidelines; updated June 2025.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/azithromycin-oral-16685286.html', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_azithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_azithromycin' and url = 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/azithromycin-oral-16685286.html');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_azithromycin', 'PhilHealth / DOH (PNF-EML)', 'Philippine National Formulary – Essential Medicines List. Department of Health / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_azithromycin'), 0)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_azithromycin' and url = 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'heart_failure', 'med_azithromycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'heart_failure'), 0), 'caution'::condition_safety, 'QT/arrhythmia risk; use with caution in severe cardiac insufficiency (UK SmPC).'
where exists (select 1 from public.diseases where id = 'heart_failure')
  and exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'heart_failure' and medicine_id = 'med_azithromycin');
insert into public.disease_medicines (disease_id, medicine_id, position, safety, note)
select 'malaria', 'med_azithromycin', coalesce((select max(position) + 1 from public.disease_medicines where disease_id = 'malaria'), 0), 'caution'::condition_safety, 'Avoid combining with QT-prolonging antimalarials (artemether-lumefantrine, quinine, mefloquine, chloroquine).'
where exists (select 1 from public.diseases where id = 'malaria')
  and exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.disease_medicines where disease_id = 'malaria' and medicine_id = 'med_azithromycin');
-- med_azithromycin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_azithromycin', 'adult', 0, 'CAP, sinusitis, pharyngitis, skin infections', 'PO', '500 mg', 'Once a day', '3 days', '1.5 g/course', 'Label · UK SmPC', 'Or 500 mg day 1, then 250 mg days 2–5'),
    ('med_azithromycin', 'adult', 1, 'Chlamydial urethritis/cervicitis', 'PO', '1 g', 'Single dose', '1 day', '—', 'Label · UK SmPC', ''),
    ('med_azithromycin', 'adult', 2, 'Gonorrhoea (with ceftriaxone)', 'PO', '1–2 g', 'Single dose', '1 day', '—', 'Label · UK SmPC', 'Give with a second antibacterial'),
    ('med_azithromycin', 'adult', 3, 'CAP (hospitalised)', 'IV', '500 mg', 'Once a day', '≥2 days, then PO to 7–10 days', '—', 'Label · US IV', 'Switch to 500 mg PO once a day'),
    ('med_azithromycin', 'adult', 4, 'Pelvic inflammatory disease', 'IV', '500 mg', 'Once a day', '1–2 days, then PO to 7 days', '—', 'Label · US IV', 'Then 250 mg PO once a day'),
    ('med_azithromycin', 'adult', 5, 'Typhoid fever', 'PO', '500 mg–1 g', 'Once a day', '7 days', '1 g/day', 'MSF 2025', 'Or 1 g day 1, then 500 mg days 2–7'),
    ('med_azithromycin', 'adult', 6, 'Cholera', 'PO', '1 g', 'Single dose', '1 day', '—', 'MSF 2025', 'If strain susceptible'),
    ('med_azithromycin', 'adult', 7, 'Leptospirosis', 'PO', '1 g day 1, then 500 mg', 'Once a day', '3 days', '—', 'MSF 2025', ''),
    ('med_azithromycin', 'adult', 8, 'Trachoma', 'PO', '1 g', 'Single dose', '1 day', '—', 'MSF 2025', ''),
    ('med_azithromycin', 'child', 9, 'CAP, sinusitis, skin infections (≥6 mo)', 'PO', '10 mg/kg', 'Once a day', '3 days', '500 mg/day; 1.5 g/course', 'Label · UK SmPC susp', 'Or 10 mg/kg day 1, then 5 mg/kg days 2–5'),
    ('med_azithromycin', 'child', 10, 'Acute otitis media (≥6 mo)', 'PO', '30 mg/kg', 'Single dose', '1 day', '1.5 g', 'Label · UK SmPC susp', 'Or a 3- or 5-day regimen'),
    ('med_azithromycin', 'child', 11, 'Streptococcal pharyngitis (≥2 y)', 'PO', '20 mg/kg', 'Once a day', '3 days', '500 mg/day', 'Label · UK SmPC susp', 'Or 12 mg/kg once a day for 5 days'),
    ('med_azithromycin', 'child', 12, 'Typhoid fever', 'PO', '10–20 mg/kg', 'Once a day', '7 days', '1 g/day', 'MSF 2025', ''),
    ('med_azithromycin', 'child', 13, 'Cholera', 'PO', '20 mg/kg', 'Single dose', '1 day', '1 g', 'MSF 2025', 'If strain susceptible'),
    ('med_azithromycin', 'child', 14, 'Leptospirosis', 'PO', '10 mg/kg day 1, then 5 mg/kg', 'Once a day', '3 days', '500 mg day 1; 250 mg/day', 'MSF 2025', ''),
    ('med_azithromycin', 'child', 15, 'Pertussis (<6 mo)', 'PO', '10 mg/kg', 'Once a day', '5 days', '—', 'MSF 2025', 'Caution <6 weeks (pyloric stenosis)'),
    ('med_azithromycin', 'child', 16, 'Pertussis (≥6 mo)', 'PO', '10 mg/kg day 1, then 5 mg/kg', 'Once a day', '5 days', '500 mg day 1; 250 mg/day', 'MSF 2025', '')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_azithromycin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_azithromycin', 'renal', 0, 'GFR ≥10', 'No dose adjustment.', 'Label · UK SmPC'),
    ('med_azithromycin', 'renal', 1, 'GFR <10', 'Use with caution.', 'Label · UK SmPC'),
    ('med_azithromycin', 'hepatic', 2, '', 'No adjustment in mild–moderate impairment; use with caution in severe impairment (no data).', 'Label · UK SmPC'),
    ('med_azithromycin', 'elderly', 3, '', 'No dose adjustment, but extra caution because of arrhythmia/QT risk.', 'Label · UK SmPC'),
    ('med_azithromycin', 'pregnancy', 4, '', 'Use only if clinically needed; >7000 exposed pregnancies showed no clear rise in major malformations. Excreted substantially in breast milk.', 'Label · UK SmPC'),
    ('med_azithromycin', 'administration', 5, '', 'Capsules: swallow whole at least 1 h before or 2 h after a meal. Suspension: with or without food; shake before each dose.', 'Label · UK SmPC susp'),
    ('med_azithromycin', 'administration', 6, '', 'IV: infuse 1 mg/mL over 3 h or 2 mg/mL over 1 h; never as IV bolus or IM.', 'Label · US IV'),
    ('med_azithromycin', 'administration', 7, '', 'Missed dose: take if ≤12 h late, otherwise wait for the next scheduled dose.', 'Label · UK SmPC'),
    ('med_azithromycin', 'forms_ph', 8, '', 'Capsule 250 mg; tablet 250 mg, 500 mg; powder for suspension 200 mg/5 mL (15 mL, 60 mL); powder for IV infusion 500 mg vial.', 'PNF'),
    ('med_azithromycin', 'monitor', 9, '', 'Check ECG and K/Mg in patients with QT risk (bradycardia, arrhythmia, heart failure, QT-prolonging drugs).', 'Label · UK SmPC'),
    ('med_azithromycin', 'monitor', 10, '', 'Stop and check liver tests if jaundice, dark urine or other hepatitis symptoms appear.', 'Label · UK SmPC'),
    ('med_azithromycin', 'monitor', 11, '', 'Infants in the first 42 days: watch for projectile vomiting or feeding irritability (pyloric stenosis).', 'Label · UK SmPC susp')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_azithromycin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_azithromycin', 'Label · UK SmPC', 'UK SmPC (emc)', 'Zithromax 250 mg Capsules / 200 mg/5 ml Powder for Oral Suspension. Summary of Product Characteristics. Pfizer Ltd; July 2026.', 'https://products.mhra.gov.uk/search/?search=azithromycin#emc-1073', 0),
    ('med_azithromycin', 'Label · UK SmPC susp', 'UK SmPC (emc)', 'Zithromax 200 mg/5 ml Powder for Oral Suspension. Summary of Product Characteristics. Pfizer Ltd; July 2026.', 'https://products.mhra.gov.uk/search/?search=azithromycin#emc-3006', 1),
    ('med_azithromycin', 'Label · US IV', 'Pfizer labeling (US)', 'ZITHROMAX (azithromycin) for injection. Prescribing information. Pfizer Inc; 2026.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=1181', 2),
    ('med_azithromycin', 'MSF 2025', 'MSF Essential Drugs', 'Médecins Sans Frontières. Essential drugs – Azithromycin oral. Updated June 2025.', 'https://medicalguidelines.msf.org/en/viewport/EssDr/english/azithromycin-oral-16685286.html', 3),
    ('med_azithromycin', 'PNF', 'Philippine National Formulary – EML', 'Philippine National Formulary – Essential Medicines List. DOH / PhilHealth; 2022.', 'https://www.philhealth.gov.ph/partners/providers/pdf/PNF-EML_11022022.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_azithromycin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_azithromycin');


-- ================================================ med_benzathine_penicillin  (Benzathine Penicillin G)
update public.medicines set description = 'Benzathine penicillin G is a depot form of penicillin G that is released slowly from the intramuscular injection site, giving low but prolonged blood levels for 3-4 weeks. Like other penicillins it inhibits bacterial cell-wall synthesis and is bactericidal. A single injection eradicates group A streptococcal pharyngitis, and repeated injections every 3-4 weeks are the most effective secondary prophylaxis against recurrent rheumatic fever. In the Philippines, the PhilHealth outpatient benefit package for rheumatic fever/rheumatic heart disease covers benzathine benzylpenicillin 1.2 million units IM every 28 days for rheumatic fever, and every 21 days once rheumatic heart disease is present, with injections tracked against the schedule. The American Heart Association calls injectable BPG secondary prophylaxis the cornerstone of RHD prevention and management, while noting that uptake has been sub-optimal.', updated_at = now()
where id = 'med_benzathine_penicillin' and description = 'Benzathine penicillin G is a depot form of penicillin G that is released slowly from the intramuscular injection site, giving low but prolonged blood levels for 3-4 weeks. Like other penicillins it inhibits bacterial cell-wall synthesis and is bactericidal. A single injection eradicates group A streptococcal pharyngitis, and repeated injections every 3-4 weeks are the most effective secondary prophylaxis against recurrent rheumatic fever.';
update public.medicines set source_attribution = case when coalesce(source_attribution, '') = '' then 'Bicillin L-A US prescribing information (Pfizer); AHA science news - BPG reactions in severe RHD; PhilHealth RF/RHD benefit package - Annex C1; WHO guideline on RF and RHD (2024); Merck Manual Professional - Rheumatic fever; Medsafe data sheet - Bicillin L-A; PhilHealth RF/RHD benefit package - Annex N' else source_attribution || '; Bicillin L-A US prescribing information (Pfizer); AHA science news - BPG reactions in severe RHD; PhilHealth RF/RHD benefit package - Annex C1; WHO guideline on RF and RHD (2024); Merck Manual Professional - Rheumatic fever; Medsafe data sheet - Bicillin L-A; PhilHealth RF/RHD benefit package - Annex N' end
where id = 'med_benzathine_penicillin' and position('Bicillin L-A US prescribing information (Pfizer)' in coalesce(source_attribution, '')) = 0;
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'indication', 'Prophylaxis of rheumatic chorea and of glomerulonephritis after an acute attack', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'indication' and content = 'Prophylaxis of rheumatic chorea and of glomerulonephritis after an acute attack');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'indication', 'Congenital syphilis (children under 2 years, weight-based dose)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'indication' and content = 'Congenital syphilis (children under 2 years, weight-based dose)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'indication', 'Late (tertiary) syphilis: three weekly injections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'indication'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'indication' and content = 'Late (tertiary) syphilis: three weekly injections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'adverse', 'Severe cutaneous reactions (Stevens-Johnson syndrome, DRESS): stop immediately', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse' and content = 'Severe cutaneous reactions (Stevens-Johnson syndrome, DRESS): stop immediately');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'adverse', 'Hoigne syndrome (agitation, confusion, hallucinations)', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse' and content = 'Hoigne syndrome (agitation, confusion, hallucinations)');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'adverse', 'Nicolau syndrome and injection-site necrosis', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse' and content = 'Nicolau syndrome and injection-site necrosis');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'adverse', 'Quadriceps fibrosis and atrophy after repeated anterolateral thigh injections', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse' and content = 'Quadriceps fibrosis and atrophy after repeated anterolateral thigh injections');
insert into public.medicine_facts (medicine_id, kind, content, position)
select 'med_benzathine_penicillin', 'adverse', 'Clostridioides difficile-associated diarrhoea', coalesce((select max(position) + 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_facts where medicine_id = 'med_benzathine_penicillin' and kind = 'adverse' and content = 'Clostridioides difficile-associated diarrhoea');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_benzathine_penicillin', 'Bicillin L-A US prescribing information (Pfizer)', 'BICILLIN L-A (penicillin G benzathine injectable suspension) - prescribing information. Pfizer Laboratories.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=691', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin' and url = 'https://labeling.pfizer.com/ShowLabeling.aspx?id=691');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_benzathine_penicillin', 'AHA science news - BPG reactions in severe RHD', 'American Heart Association. Penicillin reactions in patients with severe rheumatic heart disease (advisory in J Am Heart Assoc, doi:10.1161/JAHA.121.024517). Updated 20 Jan 2022.', 'https://professional.heart.org/en/science-news/penicillin-reactions-in-patients-with-severe-rheumatic-heart-disease', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin' and url = 'https://professional.heart.org/en/science-news/penicillin-reactions-in-patients-with-severe-rheumatic-heart-disease');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_benzathine_penicillin', 'PhilHealth RF/RHD benefit package - Annex C1', 'Philippine Health Insurance Corporation. Annex C1 - RF/RHD: Checklist of mandatory services (Tranche 1). January 2019.', 'https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexC1_MandatoryChecklist_010319.pdf', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin' and url = 'https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexC1_MandatoryChecklist_010319.pdf');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_benzathine_penicillin', 'WHO guideline on RF and RHD (2024)', 'World Health Organization. WHO guideline on the prevention and diagnosis of rheumatic fever and rheumatic heart disease. Geneva: WHO; 29 October 2024. ISBN 9789240100077.', 'https://www.who.int/publications/i/item/9789240100077', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin' and url = 'https://www.who.int/publications/i/item/9789240100077');
insert into public.medicine_references (medicine_id, source_name, citation_text, url, is_mother_book, position)
select 'med_benzathine_penicillin', 'Merck Manual Professional - Rheumatic fever', 'Rheumatic Fever. Merck Manual Professional Version. Merck & Co., Inc.', 'https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever', false, coalesce((select max(position) + 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin'), 0)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_references where medicine_id = 'med_benzathine_penicillin' and url = 'https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever');
-- med_benzathine_penicillin
insert into public.medicine_doses (medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
select * from (values
    ('med_benzathine_penicillin', 'adult', 0, 'Secondary prophylaxis: rheumatic fever', 'IM', '1.2 million units', 'Every 28 days', 'Long-term (see notes)', '—', 'PhilHealth', 'PhilHealth RF/RHD package'),
    ('med_benzathine_penicillin', 'adult', 1, 'Secondary prophylaxis: rheumatic heart disease', 'IM', '1.2 million units', 'Every 21 days', 'Long-term (see notes)', '—', 'PhilHealth', 'PhilHealth RF/RHD package'),
    ('med_benzathine_penicillin', 'adult', 2, 'Group A strep pharyngitis', 'IM', '1.2 million units', 'Once', 'Single dose', '—', 'Label · US', ''),
    ('med_benzathine_penicillin', 'adult', 3, 'Syphilis: primary, secondary, latent', 'IM', '2.4 million units', 'Once', 'Single dose', '—', 'Label · US', ''),
    ('med_benzathine_penicillin', 'adult', 4, 'Syphilis: late (tertiary)', 'IM', '2.4 million units', 'Every 7 days', '3 doses', '—', 'Label · US', ''),
    ('med_benzathine_penicillin', 'adult', 5, 'Yaws, bejel, pinta', 'IM', '1.2 million units', 'Once', 'Single dose', '—', 'Label · US', ''),
    ('med_benzathine_penicillin', 'child', 6, 'Secondary prophylaxis, ≥20 kg', 'IM', '1.2 million units', 'Every 4 weeks', 'Long-term (see notes)', '—', 'Label · NZ', 'Every 3 weeks if high risk'),
    ('med_benzathine_penicillin', 'child', 7, 'Secondary prophylaxis, <20 kg', 'IM', '600,000 units', 'Every 4 weeks', 'Long-term (see notes)', '—', 'Label · NZ', 'Every 3 weeks if high risk'),
    ('med_benzathine_penicillin', 'child', 8, 'Group A strep pharyngitis, older children', 'IM', '900,000 units', 'Once', 'Single dose', '—', 'Label · NZ', ''),
    ('med_benzathine_penicillin', 'child', 9, 'Group A strep pharyngitis, <27 kg', 'IM', '300,000–600,000 units', 'Once', 'Single dose', '—', 'Label · NZ', ''),
    ('med_benzathine_penicillin', 'child', 10, 'Congenital syphilis, <2 years', 'IM', '50,000 units/kg', '—', '—', '—', 'Label · US', 'Ages 2–12: adult schedule')
) v(medicine_id, population, position, indication, route, dose, frequency, duration, max_dose, source, note)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_doses where medicine_id = 'med_benzathine_penicillin');
insert into public.medicine_dose_notes (medicine_id, kind, position, label, content, source)
select * from (values
    ('med_benzathine_penicillin', 'forms_ph', 0, '', 'Benzathine benzylpenicillin (penicillin G benzathine) 1.2 million units, vial, for IM injection (PhilHealth RF/RHD package).', 'PhilHealth'),
    ('med_benzathine_penicillin', 'renal', 1, '', 'Substantially excreted by the kidney; toxic reactions may be more likely in impaired renal function. Select doses cautiously and consider monitoring renal function.', 'Label · US'),
    ('med_benzathine_penicillin', 'elderly', 2, '', 'Older patients more often have reduced renal function: choose the dose carefully and monitor renal function.', 'Label · US'),
    ('med_benzathine_penicillin', 'pregnancy', 3, '', 'No harm in animal studies but no adequate human studies; use if clearly needed. Penicillin G passes into breast milk, so use caution when breastfeeding.', 'Label · US'),
    ('med_benzathine_penicillin', 'administration', 4, 'Injection site', 'Give deep IM into the upper outer quadrant of the buttock or the ventrogluteal site; in neonates, infants and small children the midlateral thigh may be preferable. The anterolateral thigh is not recommended.', 'Label · US'),
    ('med_benzathine_penicillin', 'administration', 5, '', 'Inject at a slow, steady rate (the thick suspension can block the needle) and vary the site with repeat doses.', 'Label · US'),
    ('med_benzathine_penicillin', 'administration', 6, 'Duration', 'Duration of secondary prophylaxis: RF without carditis, 5 years or until age 21 (whichever is longer); carditis without residual heart disease, 10 years or until age 21; carditis with residual valve disease, more than 10 years (many experts: until age 40 or lifelong).', 'Merck'),
    ('med_benzathine_penicillin', 'administration', 7, 'Alternatives', 'If injections are refused or the patient is allergic: daily oral penicillin V (or sulfadiazine); if allergic to both penicillin and sulfa, daily oral erythromycin or azithromycin.', 'Merck'),
    ('med_benzathine_penicillin', 'monitor', 8, '', 'Keep epinephrine and resuscitation equipment ready: serious, sometimes fatal anaphylaxis can occur.', 'Label · US'),
    ('med_benzathine_penicillin', 'monitor', 9, '', 'Track adherence to the injection schedule (doses due every 21 or 28 days) and follow RHD patients with yearly 2D echo, ASO/ESR/CRP as needed, and dental clearance.', 'PhilHealth RF/RHD form')
) v(medicine_id, kind, position, label, content, source)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_dose_notes where medicine_id = 'med_benzathine_penicillin');
insert into public.medicine_dose_sources (medicine_id, tag, source_name, citation_text, url, position)
select * from (values
    ('med_benzathine_penicillin', 'PhilHealth', 'PhilHealth RF/RHD benefit package - Annex C1', 'Philippine Health Insurance Corporation. Annex C1 - RF/RHD: Checklist of mandatory services (Tranche 1). January 2019.', 'https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexC1_MandatoryChecklist_010319.pdf', 0),
    ('med_benzathine_penicillin', 'Label · US', 'Bicillin L-A US prescribing information (Pfizer)', 'BICILLIN L-A (penicillin G benzathine injectable suspension) - prescribing information. Pfizer Laboratories.', 'https://labeling.pfizer.com/ShowLabeling.aspx?id=691', 1),
    ('med_benzathine_penicillin', 'Label · NZ', 'Medsafe data sheet - Bicillin L-A', 'Bicillin L-A (benzathine benzylpenicillin) injection - New Zealand data sheet. Medsafe.', 'https://www.Medsafe.govt.nz/profs/Datasheet/b/BicillinLAinj.pdf', 2),
    ('med_benzathine_penicillin', 'Merck', 'Merck Manual Professional - Rheumatic fever', 'Rheumatic Fever. Merck Manual Professional Version. Merck & Co., Inc.', 'https://www.merckmanuals.com/professional/pediatrics/miscellaneous-bacterial-infections-in-infants-and-children/rheumatic-fever', 3),
    ('med_benzathine_penicillin', 'PhilHealth RF/RHD form', 'PhilHealth RF/RHD benefit package - Annex N', 'Philippine Health Insurance Corporation. Annex N - RF/RHD: Systematic clinical assessment and follow-up form. January 2019.', 'https://www.philhealth.gov.ph/downloads/rf-rhd/RF-RHD_AnnexN_OutpatientAssessmentForm_010319.pdf', 4)
) v(medicine_id, tag, source_name, citation_text, url, position)
where exists (select 1 from public.medicines where id = 'med_benzathine_penicillin')
  and not exists (select 1 from public.medicine_dose_sources where medicine_id = 'med_benzathine_penicillin');


update public.content_version set version = version + 1, updated_at = now() where id = 1;

commit;
