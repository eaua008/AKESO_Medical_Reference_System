-- =====================================================================
-- Akeso: five starter cases for Clinical Exchange
-- =====================================================================
-- Run AFTER migrations 003-013, in the Supabase SQL Editor. Safe to run
-- more than once (it skips cases that already exist).
--
-- Five HYPOTHETICAL cases (no real patients) with a differential poll
-- each, so participants have something to vote on and argue about from
-- day one. They are posted under the first admin account (you), not
-- anonymously, and the polls are left OPEN: nobody sees the intended
-- answer until you reveal it in the app (open the case > Reveal answer).
-- The answer key, with a short explanation to paste when revealing, is
-- at the bottom of this file. Students never see this file.
--
-- Each case is built so two or three choices are genuinely defensible;
-- the clue that decides it is in the vignette.
-- =====================================================================

do $$
declare
    me uuid;
begin
    select r.user_id into me
    from public.user_roles r join auth.users u on u.id = r.user_id
    where r.role = 'admin' order by u.created_at limit 1;
    if me is null then
        raise exception 'No admin account found. Give your account the admin role first.';
    end if;

    -- ----------------------------------------------------------- 1
    insert into public.exchange_posts (id, author_id, kind, title, body, question,
        age_range, sex, setting, vitals, has_poll, created_at, last_activity_at)
    values ('a0e50000-0000-4000-8000-000000000001', me, 'case',
        'Fever, red eyes and aching calves after a typhoon week',
        'A man in his late 20s, a delivery rider, comes in on day 4 of a high-grade fever with '
        || 'chills and a severe frontal headache. He says his legs hurt so much he can barely '
        || 'walk; the pain is worst in both calves, which are tender to squeeze.' || chr(10) || chr(10)
        || 'Ten days ago he spent two days riding through knee-deep floodwater after a typhoon. '
        || 'Several neighbours have been admitted for dengue this month.' || chr(10) || chr(10)
        || 'On examination both eyes are red but there is no discharge and no itch. No rash, no '
        || 'bleeding gums, no petechiae. Mild right upper quadrant tenderness. He has passed '
        || 'less urine than usual since yesterday.' || chr(10) || chr(10)
        || 'Initial labs: platelets 128,000/uL, WBC 13,500/uL with neutrophilia, creatinine '
        || 'slightly above normal, total bilirubin mildly raised.',
        'What is your leading diagnosis, and which single finding tipped it for you?',
        '25–34', 'male', 'Emergency department',
        '{"temperature": 39.2, "heart_rate": 108, "bp_systolic": 112, "bp_diastolic": 70, "resp_rate": 20, "spo2": 98}',
        true, now() - interval '50 minutes', now() - interval '50 minutes')
    on conflict (id) do nothing;

    -- ----------------------------------------------------------- 2
    insert into public.exchange_posts (id, author_id, kind, title, body, question,
        age_range, sex, setting, vitals, has_poll, created_at, last_activity_at)
    values ('a0e50000-0000-4000-8000-000000000002', me, 'case',
        'Sudden fever with joint pain so bad she cannot hold a cup',
        'A woman in her early 40s has had fever for 2 days that began abruptly. Her main '
        || 'complaint is pain and stiffness in both wrists, the small joints of both hands and '
        || 'both ankles; she cannot grip a cup or button her blouse, and walks slowly because '
        || 'of her ankles.' || chr(10) || chr(10)
        || 'Since this morning she has a faint red maculopapular rash over the trunk and arms. '
        || 'Two people on her street were diagnosed with dengue last week.' || chr(10) || chr(10)
        || 'On examination the wrists and ankles are swollen and tender, with pain on movement. '
        || 'No conjunctival redness, no lymph nodes, no bleeding, tourniquet test negative. '
        || 'No cough or runny nose.' || chr(10) || chr(10)
        || 'Initial labs: platelets 190,000/uL, WBC 4,200/uL with lymphopenia, hematocrit '
        || 'normal.',
        'Dengue is all over the barangay. Is this dengue, or something else? Defend your pick.',
        '35–44', 'female', 'Outpatient clinic',
        '{"temperature": 39.0, "heart_rate": 96, "bp_systolic": 118, "bp_diastolic": 76, "resp_rate": 18, "spo2": 99}',
        true, now() - interval '40 minutes', now() - interval '40 minutes')
    on conflict (id) do nothing;

    -- ----------------------------------------------------------- 3
    insert into public.exchange_posts (id, author_id, kind, title, body, question,
        age_range, sex, setting, vitals, has_poll, created_at, last_activity_at)
    values ('a0e50000-0000-4000-8000-000000000003', me, 'case',
        'Nine days of fever that keeps climbing, and a pulse that does not',
        'A college student in his early 20s has had fever for 9 days. It started low and has '
        || 'risen a little higher each evening; this week it reaches 39-40 C. He has a dull '
        || 'headache, poor appetite and vague abdominal discomfort. He was constipated for the '
        || 'first few days and now has loose stools 2-3 times a day.' || chr(10) || chr(10)
        || 'He often eats from street stalls near campus and drinks from a refilling station of '
        || 'uncertain quality. He has not travelled outside the city.' || chr(10) || chr(10)
        || 'On examination he looks tired and apathetic. His tongue is coated. The abdomen is '
        || 'soft with mild diffuse tenderness and a palpable spleen tip. A few faint pink spots '
        || 'are seen on the upper abdomen. Note the pulse against the temperature.' || chr(10) || chr(10)
        || 'Initial labs: WBC 4,000/uL, platelets 150,000/uL, mildly raised liver enzymes.',
        'What is the most likely diagnosis, and what is the best first test to confirm it?',
        '18–24', 'male', 'Outpatient clinic',
        '{"temperature": 39.6, "heart_rate": 84, "bp_systolic": 110, "bp_diastolic": 70, "resp_rate": 18, "spo2": 98}',
        true, now() - interval '30 minutes', now() - interval '30 minutes')
    on conflict (id) do nothing;

    -- ----------------------------------------------------------- 4
    insert into public.exchange_posts (id, author_id, kind, title, body, question,
        age_range, sex, setting, vitals, has_poll, created_at, last_activity_at)
    values ('a0e50000-0000-4000-8000-000000000004', me, 'case',
        '"Just hyperacidity": burning stomach after a heavy dinner',
        'A man in his late 50s comes in at 10 PM with a burning pain in the upper abdomen that '
        || 'started about an hour after a heavy, oily dinner. He calls it "hyperacidity like '
        || 'before" and took an antacid at home, with no relief. He is nauseated, sweaty and '
        || 'feels short of breath. The pain does not change when he presses on his stomach.'
        || chr(10) || chr(10)
        || 'History: type 2 diabetes for 12 years, hypertension, smokes half a pack a day. He '
        || 'has had similar but milder "acid" episodes on climbing stairs over the past month, '
        || 'each settling with rest.' || chr(10) || chr(10)
        || 'On examination he is pale and clammy. The epigastrium is only mildly tender. Lungs '
        || 'clear, no murmurs.',
        'Is this the stomach or the heart? What is the first thing you would do in the next '
        || '10 minutes?',
        '55–64', 'male', 'Emergency department',
        '{"temperature": 36.8, "heart_rate": 102, "bp_systolic": 150, "bp_diastolic": 92, "resp_rate": 22, "spo2": 95}',
        true, now() - interval '20 minutes', now() - interval '20 minutes')
    on conflict (id) do nothing;

    -- ----------------------------------------------------------- 5
    insert into public.exchange_posts (id, author_id, kind, title, body, question,
        age_range, sex, setting, vitals, has_poll, created_at, last_activity_at)
    values ('a0e50000-0000-4000-8000-000000000005', me, 'case',
        'A smoker''s cough that will not go away, plus night sweats',
        'A jeepney driver in his late 40s has had a productive cough for 5 weeks. A week of '
        || 'amoxicillin from a pharmacy did not help. Over the past two weeks he noticed streaks '
        || 'of blood in his sputum twice. He wakes up drenched in sweat, feels feverish in the '
        || 'late afternoons, and has lost about 5 kg without trying.' || chr(10) || chr(10)
        || 'He has smoked a pack a day for 25 years. He lives with six relatives in a small '
        || 'house; an uncle who used to live with them was treated for a lung illness two years '
        || 'ago but did not finish his medicines.' || chr(10) || chr(10)
        || 'On examination he is thin. There are crackles over the right upper chest. No '
        || 'clubbing, no lymph nodes in the neck.' || chr(10) || chr(10)
        || 'Chest X-ray: patchy opacities in the right upper lobe with a small cavity.',
        'TB or lung cancer in a heavy smoker? What would you send first, and why?',
        '45–54', 'male', 'Outpatient clinic',
        '{"temperature": 37.8, "heart_rate": 92, "bp_systolic": 124, "bp_diastolic": 78, "resp_rate": 20, "spo2": 96}',
        true, now() - interval '10 minutes', now() - interval '10 minutes')
    on conflict (id) do nothing;

    -- ------------------------------------------------- poll choices
    -- disease_id links a choice to its Disease Encyclopedia entry; a
    -- choice with no entry (GERD, lung cancer) is plain text.
    insert into public.exchange_poll_options (id, post_id, disease_id, label, suggested_by, by_author, created_at)
    values
        ('a0e50001-0000-4000-8000-000000000011', 'a0e50000-0000-4000-8000-000000000001', 'dengue', 'Dengue', me, true, now() - interval '50 minutes'),
        ('a0e50001-0000-4000-8000-000000000012', 'a0e50000-0000-4000-8000-000000000001', 'leptospirosis', 'Leptospirosis', me, true, now() - interval '50 minutes'),
        ('a0e50001-0000-4000-8000-000000000013', 'a0e50000-0000-4000-8000-000000000001', 'typhoid_fever', 'Typhoid Fever', me, true, now() - interval '50 minutes'),
        ('a0e50001-0000-4000-8000-000000000014', 'a0e50000-0000-4000-8000-000000000001', 'influenza', 'Influenza', me, true, now() - interval '50 minutes'),

        ('a0e50001-0000-4000-8000-000000000021', 'a0e50000-0000-4000-8000-000000000002', 'dengue', 'Dengue', me, true, now() - interval '40 minutes'),
        ('a0e50001-0000-4000-8000-000000000022', 'a0e50000-0000-4000-8000-000000000002', 'chikungunya', 'Chikungunya', me, true, now() - interval '40 minutes'),
        ('a0e50001-0000-4000-8000-000000000023', 'a0e50000-0000-4000-8000-000000000002', 'measles', 'Measles', me, true, now() - interval '40 minutes'),
        ('a0e50001-0000-4000-8000-000000000024', 'a0e50000-0000-4000-8000-000000000002', 'leptospirosis', 'Leptospirosis', me, true, now() - interval '40 minutes'),

        ('a0e50001-0000-4000-8000-000000000031', 'a0e50000-0000-4000-8000-000000000003', 'typhoid_fever', 'Typhoid Fever', me, true, now() - interval '30 minutes'),
        ('a0e50001-0000-4000-8000-000000000032', 'a0e50000-0000-4000-8000-000000000003', 'dengue', 'Dengue', me, true, now() - interval '30 minutes'),
        ('a0e50001-0000-4000-8000-000000000033', 'a0e50000-0000-4000-8000-000000000003', 'hepatitis_a', 'Hepatitis A', me, true, now() - interval '30 minutes'),
        ('a0e50001-0000-4000-8000-000000000034', 'a0e50000-0000-4000-8000-000000000003', 'acute_gastroenteritis', 'Acute Gastroenteritis', me, true, now() - interval '30 minutes'),

        ('a0e50001-0000-4000-8000-000000000041', 'a0e50000-0000-4000-8000-000000000004', 'peptic_ulcer_disease', 'Peptic Ulcer Disease', me, true, now() - interval '20 minutes'),
        ('a0e50001-0000-4000-8000-000000000042', 'a0e50000-0000-4000-8000-000000000004', 'acute_coronary_syndrome', 'Acute Coronary Syndrome', me, true, now() - interval '20 minutes'),
        ('a0e50001-0000-4000-8000-000000000043', 'a0e50000-0000-4000-8000-000000000004', null, 'GERD (acid reflux)', me, true, now() - interval '20 minutes'),
        ('a0e50001-0000-4000-8000-000000000044', 'a0e50000-0000-4000-8000-000000000004', 'acute_gastroenteritis', 'Acute Gastroenteritis', me, true, now() - interval '20 minutes'),

        ('a0e50001-0000-4000-8000-000000000051', 'a0e50000-0000-4000-8000-000000000005', 'tuberculosis', 'Pulmonary Tuberculosis', me, true, now() - interval '10 minutes'),
        ('a0e50001-0000-4000-8000-000000000052', 'a0e50000-0000-4000-8000-000000000005', null, 'Lung cancer', me, true, now() - interval '10 minutes'),
        ('a0e50001-0000-4000-8000-000000000053', 'a0e50000-0000-4000-8000-000000000005', 'community_acquired_pneumonia', 'Community-Acquired Pneumonia', me, true, now() - interval '10 minutes'),
        ('a0e50001-0000-4000-8000-000000000054', 'a0e50000-0000-4000-8000-000000000005', 'copd', 'COPD exacerbation', me, true, now() - interval '10 minutes')
    on conflict do nothing;

    -- ------------------------------------------------------- tags
    -- Symptoms and body systems only: a disease tag would give the
    -- answer away.
    insert into public.exchange_post_tags (post_id, kind, ref_id, label) values
        ('a0e50000-0000-4000-8000-000000000001', 'symptom', 'sym_fever', 'Fever'),
        ('a0e50000-0000-4000-8000-000000000001', 'symptom', 'sym_calf_pain', 'Calf muscle pain / tenderness'),
        ('a0e50000-0000-4000-8000-000000000001', 'symptom', 'sym_conjunctivitis', 'Red eyes'),
        ('a0e50000-0000-4000-8000-000000000001', 'body_system', 'bs_multisystem', 'Multisystem (Systemic Infection)'),

        ('a0e50000-0000-4000-8000-000000000002', 'symptom', 'sym_fever', 'Fever'),
        ('a0e50000-0000-4000-8000-000000000002', 'symptom', 'sym_arthralgia', 'Joint pain (arthralgia)'),
        ('a0e50000-0000-4000-8000-000000000002', 'symptom', 'sym_joint_swelling', 'Joint swelling'),
        ('a0e50000-0000-4000-8000-000000000002', 'symptom', 'sym_rash', 'Rash'),
        ('a0e50000-0000-4000-8000-000000000002', 'body_system', 'bs_multisystem', 'Multisystem (Systemic Infection)'),

        ('a0e50000-0000-4000-8000-000000000003', 'symptom', 'sym_fever', 'Fever'),
        ('a0e50000-0000-4000-8000-000000000003', 'symptom', 'sym_abdominal_pain', 'Abdominal pain'),
        ('a0e50000-0000-4000-8000-000000000003', 'symptom', 'sym_constipation', 'Constipation'),
        ('a0e50000-0000-4000-8000-000000000003', 'body_system', 'bs_digestive', 'Digestive System'),

        ('a0e50000-0000-4000-8000-000000000004', 'symptom', 'sym_epigastric_pain', 'Epigastric pain'),
        ('a0e50000-0000-4000-8000-000000000004', 'symptom', 'sym_diaphoresis', 'Sweating (diaphoresis)'),
        ('a0e50000-0000-4000-8000-000000000004', 'symptom', 'sym_nausea_vomiting', 'Nausea / vomiting'),
        ('a0e50000-0000-4000-8000-000000000004', 'body_system', 'bs_cardiovascular', 'Cardiovascular System'),
        ('a0e50000-0000-4000-8000-000000000004', 'body_system', 'bs_digestive', 'Digestive System'),

        ('a0e50000-0000-4000-8000-000000000005', 'symptom', 'sym_cough', 'Cough'),
        ('a0e50000-0000-4000-8000-000000000005', 'symptom', 'sym_hemoptysis', 'Coughing up blood (hemoptysis)'),
        ('a0e50000-0000-4000-8000-000000000005', 'symptom', 'sym_night_sweats', 'Night sweats'),
        ('a0e50000-0000-4000-8000-000000000005', 'symptom', 'sym_weight_loss', 'Weight loss'),
        ('a0e50000-0000-4000-8000-000000000005', 'body_system', 'bs_respiratory', 'Respiratory System')
    on conflict do nothing;

    -- The author follows their own cases (as the app does for new posts),
    -- so replies show up in your notifications.
    insert into public.exchange_follows (user_id, post_id)
    select me, p.id from public.exchange_posts p
    where p.id::text like 'a0e50000-0000-4000-8000-00000000000_'
    on conflict do nothing;
end $$;

select title, created_at from public.exchange_posts
where id::text like 'a0e50000-0000-4000-8000-00000000000_' order by created_at;

-- =====================================================================
-- ANSWER KEY (for the admin only; paste the "Why" text when revealing)
-- =====================================================================
-- 1  Leptospirosis
--    Why: Floodwater exposure 1-2 weeks before (the usual incubation),
--    severe calf myalgia with tenderness, conjunctival suffusion (red eyes
--    without discharge), neutrophilic leukocytosis, and early kidney and
--    liver involvement (less urine, raised creatinine and bilirubin).
--    Dengue usually gives leukopenia, not neutrophilia. Start treatment
--    without waiting for confirmation; doxycycline prophylaxis is advised
--    after flood exposure.
--
-- 2  Chikungunya
--    Why: Abrupt fever with disabling, symmetric polyarthralgia and joint
--    swelling of the hands, wrists and ankles is the hallmark. Platelets
--    and hematocrit are normal and there is no bleeding tendency. Dengue
--    can cause aches but rarely true joint swelling; both are spread by
--    Aedes mosquitoes, so the outbreak clue fits both. Joint pain can
--    persist for weeks to months.
--
-- 3  Typhoid fever
--    Why: Stepwise rising fever over more than a week, relative
--    bradycardia (pulse 84 at 39.6 C), coated tongue, constipation then
--    diarrhea, splenomegaly, rose spots and leukopenia, with street food
--    and unsafe water exposure. Blood culture is the first test (highest
--    yield in the first week or two); serology like Widal is unreliable
--    on its own.
--
-- 4  Acute coronary syndrome
--    Why: Epigastric "burning" that does not respond to antacid, with
--    sweating, nausea and breathlessness, in a diabetic smoker with
--    hypertension and recent exertional episodes relieved by rest (unstable
--    pattern). Diabetics often present atypically. First 10 minutes: a
--    12-lead ECG, aspirin if not contraindicated, and cardiac troponin.
--    Never call it hyperacidity until the heart is ruled out.
--
-- 5  Pulmonary tuberculosis
--    Why: Cough over 2 weeks not responding to antibiotics, hemoptysis,
--    night sweats, afternoon fevers, weight loss, crowded household with an
--    untreated contact, and an upper-lobe cavity. Send sputum for a rapid
--    molecular test (Xpert MTB/RIF) first. Lung cancer remains on the list
--    in a heavy smoker: if TB tests are negative or he does not improve,
--    he needs further work-up (CT, bronchoscopy).
-- =====================================================================
