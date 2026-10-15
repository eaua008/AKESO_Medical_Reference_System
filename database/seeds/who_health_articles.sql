-- =====================================================================
-- Akeso: two Health Articles adapted from the World Health Organization
-- Run AFTER database/migrations/005_health_articles.sql
-- Supabase dashboard -> SQL Editor -> paste -> Run. Safe to run again
-- (it updates the two articles instead of duplicating them).
--
-- The text is a short summary written from the WHO pages below, not a copy.
-- Each article lists its WHO sources; in the app they show on the left of
-- the article and open in the built-in browser.
--
-- Sources checked 4 October 2026:
--   Dengue fact sheet (last updated 21 August 2025)
--     https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue
--   Stress, questions and answers (30 March 2026)
--     https://www.who.int/news-room/questions-and-answers/item/stress
-- Please read both against the WHO pages before you publish them to users.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- 1. The articles
-- ---------------------------------------------------------------------
insert into public.health_articles
    (id, name, kind, category, summary, body, url, source_name, author_name,
     reviewed_on, is_published)
values
(
    'art_who_dengue',
    'Dengue: Symptoms, Warning Signs and Prevention',
    'written',
    'Infectious disease',
    'Dengue is a mosquito-borne viral infection that puts about half of the world''s '
    || 'population at risk. Most cases are mild, but severe dengue can be fatal, so '
    || 'knowing the warning signs and preventing bites matter.',
$body$## Overview
Dengue is a viral infection spread to people through the bite of infected mosquitoes. It is found in tropical and subtropical climates worldwide, mostly in urban and semi-urban areas. About half of the world's population is now at risk, with an estimated 100–400 million infections each year.

Many infections cause no symptoms or only mild illness, and most people get better in 1–2 weeks. Some people develop severe dengue, which needs care in hospital and can be fatal.

## Symptoms
When symptoms occur, they usually start 4–10 days after the bite and last 2–7 days. Common symptoms include:
- High fever (40°C/104°F)
- Severe headache and pain behind the eyes
- Muscle and joint pains
- Nausea and vomiting
- Swollen glands
- Rash

People who get dengue a second time are at greater risk of severe dengue. Feeling tired can last for several weeks after recovery.

## Warning signs of severe dengue
Severe dengue often begins after the fever has gone away. Get medical care right away if any of these appear:
- Severe abdominal pain
- Vomiting that does not stop
- Fast breathing
- Bleeding gums or nose
- Extreme tiredness

## How dengue spreads
The virus is passed to people mainly by infected female Aedes aegypti mosquitoes. Once a mosquito is infectious, it can spread the virus for the rest of its life.

A mosquito can pick up the virus from an infected person from about 2 days before symptoms start until about 2 days after the fever ends, including from people who have no symptoms. Spread from mother to baby during pregnancy and through blood products or organ donation is possible but rare.

## Diagnosis and treatment
Dengue can be confirmed with laboratory tests such as nucleic acid amplification tests (NAATs), ELISAs and rapid diagnostic tests.

There is no specific treatment for dengue. Pain and fever can be managed with paracetamol (acetaminophen). Nonsteroidal anti-inflammatory drugs such as ibuprofen and aspirin are avoided because they can increase the risk of bleeding. Rest and plenty of fluids help, and severe dengue usually needs hospital care. Early detection and access to proper medical care greatly lower deaths from severe dengue.

## Prevention
Prevention depends on avoiding mosquito bites and controlling mosquitoes:
- Wear clothes that cover as much of the body as possible
- Use mosquito nets when sleeping during the day, ideally treated with insecticide
- Use window screens
- Use mosquito repellents containing DEET, Picaridin or IR3535
- Dispose of waste properly and remove things that collect water
- Empty, clean and cover water storage containers every week

One vaccine (QDenga) is licensed in some countries. WHO recommends it only for people aged 6–16 years in places with high transmission.

## The global picture
Reported cases rose from 505,430 in 2000 to 14.6 million in 2024. In 2024, more than 100 countries on every continent reported cases, with over 12,000 deaths.$body$,
    '',
    'World Health Organization',
    'Adapted from the World Health Organization',
    date '2026-10-04',
    true
),
(
    'art_who_stress',
    'Stress: What It Is and How to Manage It',
    'written',
    'Mental health',
    'Stress is a natural response to difficult situations. A little can help us get '
    || 'things done, but too much affects both mind and body. Here are the signs to '
    || 'look out for and practical ways to cope.',
$body$## What is stress?
WHO describes stress as a state of worry or mental tension caused by a difficult situation. It is a natural human response that pushes us to deal with the challenges and threats in our lives.

## How stress affects us
Stress affects both the mind and the body. A little stress can help us get through daily activities, but too much can cause problems. Learning ways to cope can help us feel less overwhelmed and support our wellbeing.

## Signs of stress
Stress can show up in many ways, such as:
- Finding it hard to relax or concentrate
- Feeling anxious or irritable
- Headaches or other pains in the body
- An upset stomach
- Trouble sleeping
- Eating much more or much less than usual

Long-term stress can make existing health problems worse and may lead to more use of alcohol, tobacco or other substances. It can also trigger or worsen anxiety and depression, which may need professional care.

## Everyone responds differently
There is no single way to react to stress: coping styles and symptoms vary from person to person.

Feeling stressed is normal in hard situations such as a job interview, exams, a heavy workload or a conflict with someone, and during larger events like economic hardship, disease outbreaks, natural disasters or war. For many people, stress eases as the situation improves or as they learn to cope with their emotions.

## Stress and daily life
Most people can keep working or studying while they manage stress. If it is becoming too much, talk to a health-care provider or someone you trust in your community.

## Ways to manage stress
- Learn stress-management skills, for example with WHO's illustrated guide "Doing What Matters in Times of Stress" and its audio exercises
- Keep a daily routine to help you manage your time and feel more in control
- Get enough sleep: go to bed at the same time each night, keep the room dark and limit screens before bed
- Stay connected and share your worries with people you trust
- Eat regular, balanced meals with fruits and vegetables
- Be physically active every day
- Limit the time you spend following the news and social media$body$,
    '',
    'World Health Organization',
    'Adapted from the World Health Organization',
    date '2026-10-04',
    true
)
on conflict (id) do update set
    name         = excluded.name,
    kind         = excluded.kind,
    category     = excluded.category,
    summary      = excluded.summary,
    body         = excluded.body,
    url          = excluded.url,
    source_name  = excluded.source_name,
    author_name  = excluded.author_name,
    reviewed_on  = excluded.reviewed_on,
    is_published = excluded.is_published,
    updated_at   = now();

-- ---------------------------------------------------------------------
-- 2. Sources and further reading (the links on the left of the article)
--    source_name = publisher, citation_text = the link's title
-- ---------------------------------------------------------------------
delete from public.health_article_references
 where article_id in ('art_who_dengue', 'art_who_stress');

insert into public.health_article_references
    (article_id, position, source_name, citation_text, url)
values
    ('art_who_dengue', 0, 'World Health Organization',
     'Dengue and severe dengue — fact sheet (updated 21 August 2025)',
     'https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue'),
    ('art_who_dengue', 1, 'World Health Organization',
     'Dengue and severe dengue — questions and answers',
     'https://www.who.int/news-room/questions-and-answers/item/dengue-and-severe-dengue'),
    ('art_who_dengue', 2, 'World Health Organization',
     'Dengue and severe dengue — health topic',
     'https://www.who.int/health-topics/dengue-and-severe-dengue'),
    ('art_who_dengue', 3, 'World Health Organization',
     'Global dengue surveillance dashboard',
     'https://worldhealthorg.shinyapps.io/dengue_global/'),
    ('art_who_dengue', 4, 'World Health Organization',
     'Laboratory testing for dengue virus: interim guidance (April 2025)',
     'https://www.who.int/publications/i/item/B09394'),

    ('art_who_stress', 0, 'World Health Organization',
     'Stress — questions and answers (30 March 2026)',
     'https://www.who.int/news-room/questions-and-answers/item/stress'),
    ('art_who_stress', 1, 'World Health Organization',
     'Doing What Matters in Times of Stress: an illustrated guide',
     'https://www.who.int/publications/i/item/9789240003927'),
    ('art_who_stress', 2, 'World Health Organization',
     'Mental health at work — fact sheet',
     'https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work'),
    ('art_who_stress', 3, 'World Health Organization',
     'Mental health: strengthening our response — fact sheet',
     'https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response');

-- ---------------------------------------------------------------------
-- 3. Linked entry: show the dengue article on the Dengue page
--    (only added if your diseases table has the id 'dengue')
-- ---------------------------------------------------------------------
insert into public.health_article_links (article_id, kind, ref_id)
select 'art_who_dengue', 'disease', 'dengue'
 where exists (select 1 from public.diseases where id = 'dengue')
on conflict do nothing;

commit;

-- Check:
-- select id, name, kind, category, is_published from public.health_articles order by id;
-- select article_id, position, citation_text from public.health_article_references order by 1, 2;
