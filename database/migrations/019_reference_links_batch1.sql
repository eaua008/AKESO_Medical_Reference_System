-- =====================================================================
-- 019_reference_links_batch1.sql  -  open links for the guideline references
-- added in 018 (GERD, appendicitis, iron-deficiency anemia, CKD, rheumatic
-- fever). Textbooks (Harrison's, Schwartz's, Bates', Goodman & Gilman's)
-- stay without a link, like the existing entries.
-- Only fills a link that is still empty. Safe to run more than once.
-- =====================================================================
begin;

update public.clinical_references set url = 'https://doi.org/10.1186/s13017-020-00306-3' where source_name = 'WSES Jerusalem guidelines - Acute appendicitis (2020)' and coalesce(url, '') = '';
update public.symptom_references set url = 'https://doi.org/10.1186/s13017-020-00306-3' where source_name = 'WSES Jerusalem guidelines - Acute appendicitis (2020)' and coalesce(url, '') = '';
update public.medicine_references set url = 'https://doi.org/10.1186/s13017-020-00306-3' where source_name = 'WSES Jerusalem guidelines - Acute appendicitis (2020)' and coalesce(url, '') = '';
update public.clinical_references set url = 'https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf' where source_name = 'KDIGO 2024 Clinical Practice Guideline - Chronic Kidney Disease' and coalesce(url, '') = '';
update public.symptom_references set url = 'https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf' where source_name = 'KDIGO 2024 Clinical Practice Guideline - Chronic Kidney Disease' and coalesce(url, '') = '';
update public.medicine_references set url = 'https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf' where source_name = 'KDIGO 2024 Clinical Practice Guideline - Chronic Kidney Disease' and coalesce(url, '') = '';
update public.clinical_references set url = 'https://pubmed.ncbi.nlm.nih.gov/34807007/' where source_name = 'ACG Clinical Guideline - Diagnosis and Management of GERD (2022)' and coalesce(url, '') = '';
update public.symptom_references set url = 'https://pubmed.ncbi.nlm.nih.gov/34807007/' where source_name = 'ACG Clinical Guideline - Diagnosis and Management of GERD (2022)' and coalesce(url, '') = '';
update public.medicine_references set url = 'https://pubmed.ncbi.nlm.nih.gov/34807007/' where source_name = 'ACG Clinical Guideline - Diagnosis and Management of GERD (2022)' and coalesce(url, '') = '';
update public.clinical_references set url = 'https://www.who.int/publications/i/item/9789240088542' where source_name = 'WHO Guideline - Haemoglobin cutoffs to define anaemia (2024)' and coalesce(url, '') = '';
update public.symptom_references set url = 'https://www.who.int/publications/i/item/9789240088542' where source_name = 'WHO Guideline - Haemoglobin cutoffs to define anaemia (2024)' and coalesce(url, '') = '';
update public.medicine_references set url = 'https://www.who.int/publications/i/item/9789240088542' where source_name = 'WHO Guideline - Haemoglobin cutoffs to define anaemia (2024)' and coalesce(url, '') = '';
update public.clinical_references set url = 'https://professional.heart.org/en/science-news/revised-jones-criteria-for-the-diagnosis-of-acute-rheumatic-fever/top-things-to-know' where source_name = 'AHA Scientific Statement - Revision of the Jones Criteria (2015)' and coalesce(url, '') = '';
update public.symptom_references set url = 'https://professional.heart.org/en/science-news/revised-jones-criteria-for-the-diagnosis-of-acute-rheumatic-fever/top-things-to-know' where source_name = 'AHA Scientific Statement - Revision of the Jones Criteria (2015)' and coalesce(url, '') = '';
update public.medicine_references set url = 'https://professional.heart.org/en/science-news/revised-jones-criteria-for-the-diagnosis-of-acute-rheumatic-fever/top-things-to-know' where source_name = 'AHA Scientific Statement - Revision of the Jones Criteria (2015)' and coalesce(url, '') = '';
update public.clinical_references set url = 'https://pubmed.ncbi.nlm.nih.gov/19246689/' where source_name = 'AHA Scientific Statement - Prevention of Rheumatic Fever (2009)' and coalesce(url, '') = '';
update public.symptom_references set url = 'https://pubmed.ncbi.nlm.nih.gov/19246689/' where source_name = 'AHA Scientific Statement - Prevention of Rheumatic Fever (2009)' and coalesce(url, '') = '';
update public.medicine_references set url = 'https://pubmed.ncbi.nlm.nih.gov/19246689/' where source_name = 'AHA Scientific Statement - Prevention of Rheumatic Fever (2009)' and coalesce(url, '') = '';

update public.content_version set version = version + 1, updated_at = now() where id = 1;
commit;
