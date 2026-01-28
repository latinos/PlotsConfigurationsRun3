cuts = {}

# Preselections - applied to all the cuts
preselections = 'Alt(Lepton_pt,0,0)>25 \
              && Alt(Lepton_pt,1,0)>10 \
              && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
              && Alt(Lepton_pt,2,0)>10 \
              && (nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
              && (WH3l_mOSll[0] < 0 || WH3l_mOSll[0] > 12) \
              && (WH3l_mOSll[1] < 0 || WH3l_mOSll[1] > 12) \
              && (WH3l_mOSll[2] < 0 || WH3l_mOSll[2] > 12) \
              && abs(WH3l_chlll) == 1 \
              && bVeto \
'

###########################################
###############   VgS CR   ###############
###########################################

# VgS_mee  (mu + e e)

cuts['VgS_mee'] = {
    'expr': 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 11 && abs(Lepton_pdgId[2]) == 11',
    'categories': {
        'mll': 'mll > 0 && mll < 100'
    }
}

# VgS_emm  (e + mu mu)

cuts['VgS_emm'] = {
    'expr': 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 13 && abs(Lepton_pdgId[2]) == 13',
    'categories': {
        'mll': 'mll > 0 && mll < 100'
    }
}

