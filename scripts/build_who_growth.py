# Rebuilds data/who_growth.json. Needs the downloaded pygrowup and rcpchgrowth
# packages (pip download pygrowup rcpchgrowth --no-deps), paths below.
"""Builds data/who_growth.json from WHO's published LMS tables.
0-5 y: WHO Child Growth Standards 2006 (expanded monthly z-score tables, as in WHO's
igrowup files, via pygrowup's copies). 5-19 y: WHO Growth Reference 2007 (via RCPCH)."""
import json
T='/tmp/pkgs/p/pygrowup-0.8.2/pygrowup/tables/'
R=json.load(open('/tmp/pkgs/r/rcpchgrowth/data_tables/who/who_2007_children.json'))['measurement']
def lms(r): return [float(r['L']), float(r['M']), float(r['S'])]
def load(n): return json.load(open(T+n))
out={"source":{
 "standards_2006":"WHO Child Growth Standards (2006), 0-60 months, monthly LMS tables",
 "reference_2007":"WHO Growth Reference for school-aged children and adolescents (2007), 61-228 months"},
 "bfa":{}, "wfa":{}, "hfa":{}, "wfl":{}, "wfh":{}}
for sex,word in (('male','boys'),('female','girls')):
    b02=load(f'bmifa_{word}_0_2_zscores.json'); b25=load(f'bmifa_{word}_2_5_zscores.json')
    rows=[lms(r) for r in b02 if int(r['Month'])<24]+[lms(r) for r in b25]
    assert len(rows)==61
    r07=[lms(r) for r in R['bmi'][sex] if round(r['decimal_age']*12)>60]
    assert len(r07)==168, len(r07)
    out['bfa'][sex]=rows+r07
    w=[lms(r) for r in load(f'wfa_{word}_0_5_zscores.json')]; assert len(w)==61
    w07=[lms(r) for r in R['weight'][sex] if round(r['decimal_age']*12)>60]; assert len(w07)==60, len(w07)
    out['wfa'][sex]=w+w07
    h=load(f'lhfa_{word}_0_5_zscores.json')
    hrows=[]; seen24=0
    for r in h:
        m=int(r['Month'])
        if m==24:
            seen24+=1
            if seen24==1: continue            # the length row; from 24 months height is used
        hrows.append(lms(r))
    assert len(hrows)==61, len(hrows)
    h07=[lms(r) for r in R['height'][sex] if round(r['decimal_age']*12)>60]; assert len(h07)==168
    out['hfa'][sex]=hrows+h07
    wfl=load(f'wfl_{word}_0_2_zscores.json'); wfh=load(f'wfh_{word}_2_5_zscores.json')
    out['wfl'][sex]={"start":45.0,"step":0.5,"rows":[lms(r) for r in wfl]}
    out['wfh'][sex]={"start":65.0,"step":0.5,"rows":[lms(r) for r in wfh]}
    assert float(wfl[0]['Length'])==45 and float(wfh[0]['Height'])==65
    assert all(abs(float(r['Length'])-(45+0.5*i))<1e-6 for i,r in enumerate(wfl))
    assert all(abs(float(r['Height'])-(65+0.5*i))<1e-6 for i,r in enumerate(wfh))
json.dump(out,open('who_growth.json','w'),separators=(',',':'))
print({k:{s:(len(v[s]) if isinstance(v[s],list) else len(v[s]['rows'])) for s in v} for k,v in out.items() if k!='source'})
