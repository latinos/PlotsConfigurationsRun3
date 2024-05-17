# cuts

cuts = {}

# MinIf$( WH3l_mOSll[], WH3l_mOSll[Iteration$] > 0) > 12
# Alt(WH3l_mOSll,0,9999) > 12 && Alt(WH3l_mOSll,1,9999) > 12 && Alt(WH3l_mOSll,2,9999) > 12 \

preselections = '(nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
             && Alt(Lepton_pt,0,0)>25 \
             && Alt(Lepton_pt,1,0)>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && Alt(Lepton_pt,2,0)>10 \
             && (WH3l_mOSll[0] < 0 || WH3l_mOSll[0] > 12) \
             && (WH3l_mOSll[1] < 0 || WH3l_mOSll[1] > 12) \
             && (WH3l_mOSll[2] < 0 || WH3l_mOSll[2] > 12) \
             && abs(WH3l_chlll) == 1 \
             && bVeto \
             '

## WZ control region

# CR 0jet - WH3l
cuts['wh3l_wz_13TeV'] = 'WH3l_flagOSSF == 1 \
                         && PuppiMET_pt > 45 \
                         && WH3l_ZVeto < 20 \
                         && WH3l_mlll > 100 \
                         && Alt(CleanJet_pt,0,0) < 30 \
                         '

# 11 = e
# 13 = mu
# 15 = tau
