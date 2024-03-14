#!/bin/python3

import ROOT

f = ROOT.TFile("rootFiles__RDF_2016noHIPM_v9_2ADNN/mkShapes__RDF_2016noHIPM_v9_2ADNN.root")

dir="test_empty/events/"

ggh_thus = ['THU_ggH_Mu','THU_ggH_Res','THU_ggH_Mig01','THU_ggH_Mig12','THU_ggH_VBF2j','THU_ggH_VBF3j','THU_ggH_PT60','THU_ggH_PT120','THU_ggH_qmtop','PS_ISR','PS_FSR']
qqh_thus = ["THU_qqH_YIELD","THU_qqH_PTH200","THU_qqH_Mjj60","THU_qqH_Mjj120","THU_qqH_Mjj350","THU_qqH_Mjj700","THU_qqH_Mjj1000","THU_qqH_Mjj1500","THU_qqH_PTH25","THU_qqH_JET01","THU_qqH_EWK","PS_ISR","PS_FSR"]

ggh_thu_normfact = {}
ggh_sample_list = [f'histo_ggH_hww_GenDeltaPhijj_{num}{tag}' for num in range(4) for tag in ['fid','nonfid']]
ggh_thu_normfact['info'] = '[nominal/up, nominal/down]'

for n in ggh_thus:
    print('-------')
    print(n)
    ggh_thu_normfact[n] = {}
    for s in ggh_sample_list: 
        up = f.Get(dir+s+'_'+n+'Up').Integral()
        do = f.Get(dir+s+'_'+n+'Down').Integral()
        nom = f.Get(dir+s).Integral()
        print('###',s)

        print("nom = ", nom," nom/up = ", nom/up, " nom/down = ", nom/do) 
        ggh_thu_normfact[n][s.replace('histo_','')] = [nom/up, nom/do]


qqh_thu_normfact = {}
qqh_sample_list = [f'histo_qqH_hww_GenDeltaPhijj_{num}{tag}' for num in range(4) for tag in ['fid','nonfid']]
qqh_thu_normfact['info'] = '[nominal/up, nominal/down]'

for n in qqh_thus:
    print('-------')
    print(n)
    qqh_thu_normfact[n] = {}
    for s in qqh_sample_list:
        up = f.Get(dir+s+'_'+n+'Up').Integral()
        do = f.Get(dir+s+'_'+n+'Down').Integral()
        nom = f.Get(dir+s).Integral()
        print('###',s)

        print("nom = ", nom," nom/up = ", nom/up, " nom/down = ", nom/do)
 
        qqh_thu_normfact[n][s.replace('histo_','')] = [nom/up, nom/do]


import json

thu_normfact = qqh_thu_normfact.copy()
thu_normfact.update(ggh_thu_normfact)
thu_normfact['PS_ISR'].update(qqh_thu_normfact['PS_ISR'])
thu_normfact['PS_FSR'].update(qqh_thu_normfact['PS_FSR'])

with open("HiggsTHUNormFactors.json", "w") as outfile:
    json.dump(thu_normfact, outfile)
