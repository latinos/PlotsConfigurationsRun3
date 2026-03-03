


# cuts['Sig_mllZ'] = {
    # }


cuts['Sig'] = {
    'expr' : 'Alt(Lepton_pt,2,0) < 15 && (abs(Lepton_pdgId[0])==abs(Lepton_pdgId[1])) && Alt(CleanJet_pt,2,0) < 30 && Alt(CleanJet_pt,1,0) > 30',
    'categories' : {
        'mllZ'               : 'mll>60 && mll< 120',
        # 'two'                : 'mll>60 && mll< 120',
      }
    }



# cuts['single'] = 'mll>60 && mll< 120'
