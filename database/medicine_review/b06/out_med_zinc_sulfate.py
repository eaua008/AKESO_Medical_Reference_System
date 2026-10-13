JS_URL = "https://stg.nutritioncluster.net/sites/nutritioncluster.com/files/2019-12/WHO_FCH_CAH_04.71.pdf"
ELENA_URL = "https://www.who.int/tools/elena/bbc/zinc-diarrhoea"
SOL_URL = "https://extranet.who.int/prequal/sites/default/files/whopar_files/DI010part4v2.pdf"
DOH_URL = "https://elibrary.judiciary.gov.ph/thebookshelf/showdocsfriendly/10/52204"
MOST_URL = "https://cdn.who.int/media/docs/default-source/2021-dha-docs/pnadk428.pdf"

MED = {
  "id": "med_zinc_sulfate",
  "desc_add": "Besides shortening and easing the current episode, a 10–14 day zinc course lowers the incidence of diarrhoea in the following 2–3 months (WHO/UNICEF 2004). In the Philippines, DOH Administrative Order No. 2007-0045 (17 December 2007) adopted zinc supplementation together with reformulated ORS for the management of diarrhoea in children. WHO-prequalified products include 20 mg dispersible tablets and a 10 mg/5 mL oral solution.",
  "facts": {
    "indication": [
      "Bloody diarrhoea (dysentery) in children, given as for watery diarrhoea alongside antibiotics",
    ],
    "adverse": [
      "Headache, irritability and lethargy (frequency not known)",
      "Gastric irritation and gastritis",
    ],
    "contraindication": [
      "Copper deficiency",
      "Hereditary fructose intolerance with sorbitol-containing oral solutions",
    ],
    "interaction": [
      "Calcium salts, oral iron and trientine: mutual reduction in absorption; separate doses.",
      "Copper: zinc inhibits copper absorption.",
    ],
    "brand_ph": [],
    "brand_intl": [],
  },
  "refs": [
    ("WHO/UNICEF Joint Statement", "World Health Organization, UNICEF. Clinical Management of Acute Diarrhoea: WHO/UNICEF Joint Statement. WHO/FCH/CAH/04.7; May 2004.", JS_URL),
    ("WHO eLENA", "Khan WU, Sellen DW. Zinc supplementation in the management of diarrhoea: biological, behavioural and contextual rationale. WHO e-Library of Evidence for Nutrition Actions (eLENA); April 2011.", ELENA_URL),
    ("WHO Prequalification (WHOPAR product information)", "World Health Organization Prequalification Unit. Zinc (as sulfate monohydrate) 10 mg/5 mL oral solution, PharmEvo (DI010): Summary of Product Characteristics, WHOPAR part 4; revised June 2025.", SOL_URL),
    ("Department of Health (Philippines)", "Department of Health. Administrative Order No. 2007-0045: Zinc Supplementation and Reformulated Oral Rehydration Salt in the Management of Diarrhea Among Children. Adopted 17 December 2007. National Administrative Register Vol. 19 No. 1 (Jan–Mar 2008), Supreme Court E-Library.", DOH_URL),
    ("MOST / USAID", "MOST, the USAID Micronutrient Program. Diarrhoea Treatment Guidelines including new recommendations for the use of ORS and zinc supplementation for clinic-based healthcare workers. Arlington, VA; January 2005.", MOST_URL),
  ],
  "links": [
    ("acute_gastroenteritis", "safe", "Zinc with low-osmolarity ORS is recommended for all children with acute diarrhoea (WHO/UNICEF 2004)."),
    ("chronic_kidney_disease", "caution", "Zinc may accumulate in renal failure (WHO-prequalified product information)."),
  ],
  "sources": [
    ("WHO/UNICEF 2004", "WHO/UNICEF Joint Statement", "World Health Organization, UNICEF. Clinical Management of Acute Diarrhoea. WHO/FCH/CAH/04.7; 2004.", JS_URL),
    ("Label · WHO PQ", "WHO Prequalification (WHOPAR)", "Zinc (as sulfate monohydrate) 10 mg/5 mL oral solution (DI010), SmPC; June 2025.", SOL_URL),
    ("MOST 2005", "MOST / USAID", "Diarrhoea Treatment Guidelines including new recommendations for the use of ORS and zinc supplementation. MOST, USAID Micronutrient Program; 2005.", MOST_URL),
  ],
  "doses": [
    ("child", "Acute or persistent diarrhoea, <6 months", "PO", "10 mg elemental zinc", "Once a day", "10–14 days", "—", "WHO/UNICEF 2004", "= ½ × 20 mg tablet or 5 mL of 10 mg/5 mL solution"),
    ("child", "Acute or persistent diarrhoea, 6 months–5 y", "PO", "20 mg elemental zinc", "Once a day", "10–14 days", "—", "WHO/UNICEF 2004", "= 1 × 20 mg tablet or 10 mL of 10 mg/5 mL solution"),
    ("child", "Dysentery (bloody diarrhoea)", "PO", "Same as acute diarrhoea by age", "Once a day", "10–14 days", "—", "MOST 2005", "Give antibiotic for Shigella separately"),
  ],
  "notes": [
    ("renal", "Zinc may accumulate in renal failure.", "", "Label · WHO PQ"),
    ("pregnancy", "Limited human data; animal studies show no reproductive toxicity at the therapeutic dose. Zinc is present in breast milk.", "", "Label · WHO PQ"),
    ("administration", "Give between meals. If the child vomits within 30 minutes, repeat the dose. Missed dose: give as soon as possible unless the next is due within 6 hours.", "", "Label · WHO PQ"),
    ("administration", "Dispersible tablet: dissolve in about 5 mL of expressed breast milk, ORS or clean water on a small spoon for infants; older children may chew it. Finish all 10–14 days even after diarrhoea stops.", "", "MOST 2005"),
    ("administration", "Oral solution excipients: aspartame (avoid in phenylketonuria), sodium benzoate (may worsen newborn jaundice) and sorbitol (mild laxative effect). Discard 28 days after opening.", "", "Label · WHO PQ"),
    ("monitor", "Ask about vomiting after doses; if the child vomits ORS, food and fluids, bring to a health facility rather than continuing zinc at home.", "", "MOST 2005"),
  ],
  "checked": [
    (JS_URL, "WHO/UNICEF joint statement WHO/FCH/CAH/04.7 (May 2004): 20 mg/day zinc for 10–14 days, 10 mg/day under 6 months; reduces duration and severity and lowers incidence of diarrhoea in the following 2–3 months; low-osmolarity ORS composition."),
    (ELENA_URL, "WHO eLENA rationale page (Khan & Sellen, April 2011): 20 mg/day >6 months, 10 mg/day <6 months, 10–14 days; reduces duration/severity and later infections for 2–3 months."),
    (SOL_URL, "WHOPAR DI010 (PharmEvo 10 mg/5 mL oral solution, rev June 2025): <6 mo 5 mL (10 mg), 6 mo–5 y 10 mL (20 mg) once daily 10–14 days; between meals, repeat if vomit within 30 min, missed dose rule; 4.3 copper deficiency; 4.4 renal accumulation, aspartame, sodium benzoate, sorbitol/fructose intolerance; 4.5 calcium, iron, trientine, copper; 4.6 pregnancy/breast milk; 4.8 headache, irritability, lethargy, gastritis; discard 28 days after opening."),
    (DOH_URL, "Supreme Court E-Library, NAR Vol 19 No 1: DOH Administrative Order No. 2007-0045 'Zinc Supplementation and Reformulated Oral Rehydration Salt in the Management of Diarrhea Among Children', adopted 17 Dec 2007 (title and date only; full text not on page)."),
    (MOST_URL, "MOST/USAID 2005 diarrhoea treatment guidelines: <6 mo ½ tablet, ≥6 mo 1 tablet for 10/14 days; dissolve in ~5 mL breast milk/ORS/water; complete course; zinc for dysentery as for watery diarrhoea with separate Shigella antibiotic; vomiting ORS/food/fluids -> health facility."),
  ],
}
