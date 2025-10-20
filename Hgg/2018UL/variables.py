# variables

# 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
    
variables = {}

# variables['ttree_variable'] = {
#         'tree': {'LeptonPt1': 'Lepton_pt[0]'},
#         'cuts': ['sr']
#         }

variables['ptj1'] = {
        'name': 'Alt(CleanJet_pt,0,0)',
        'range': (100, 30, 500),
        'xaxis': 'p_{T} 1st jet',
        'fold' :3
}

variables['ptj2'] = {
        'name': 'Alt(CleanJet_pt,1,0)',
        'range': (100, 30, 500),
        'xaxis': 'p_{T} 2nd jet',
        'fold' :3
}

variables['qglj1'] = {
        'name': 'Alt(Jet_qgl,CleanJet_jetIdx[0],2)',
        'range': (100, -1, 1),
        'xaxis': 'QGL 1st jet',
        'fold' :3
}


variables['qglj1morebins'] = {
        'name': 'Alt(Jet_qgl,CleanJet_jetIdx[0],2)',
        'range': (20, -0.01, 0.3),
        'xaxis': 'QGL 1st jet',
        'fold' :3
}

variables['qglj2'] = {
        'name': 'Alt(Jet_qgl,CleanJet_jetIdx[1],2)',
        'range': (100, -1, 1),
        'xaxis': 'QGL 2nd jet',
        'fold' :3
}


variables['etaj1'] = {
        'name': 'Alt(CleanJet_eta,0,0)',
        'range': (100, -5, 5),
        'xaxis': '#eta 1st jet',
        'fold' :3
}

variables['etaj2'] = {
        'name': 'Alt(CleanJet_eta,1,0)',
        'range': (100, -5, 5),
        'xaxis': '#eta 2nd jet',
        'fold' :3
}



variables['btagDeepBj1'] = {
        'name': 'Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)',
        'range': (100, -1, 1),
        'xaxis': 'btagDeepB 1st jet',
        'fold' :3
}

variables['btagDeepBj2'] = {
        'name': 'Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2)',
        'range': (100, -1, 1),
        'xaxis': 'btagDeepB 2nd jet',
        'fold' :3
}


variables['btagCSVV2j1'] = {
        'name': 'Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)',
        'range': (100, -1, 1),
        'xaxis': 'btagCSVV2 1st jet',
        'fold' :3
}

variables['btagCSVV2j2'] = {
        'name': 'Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2)',
        'range': (100, -1, 1),
        'xaxis': 'btagCSVV2 2nd jet',
        'fold' :3
}



#Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0)
#Jet_btagDeepFlavB[CleanJet_jetIdx[0]]
#Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 1, -99) -999.99*(CleanJet_pt[1]<20)
#
#Take(Jet_btagDeepFlavB, CleanJet_jetIdx)[0]
#Jet_btagDeepFlavB[CleanJet_jetIdx[0]]
#

variables['mjj']      = {   'name': 'mjj',            #   variable name    
                            'range' : (20, 0, 200),    #   variable range
                            'xaxis' : 'm_{jj} [GeV]',  #   x axis name
                            'fold' :3
                        }

variables['mjjbins']      = {   'name': 'mjj',            #   variable name    
                            'range' : (100, 0, 200),    #   variable range
                            'xaxis' : 'm_{jj} [GeV]',  #   x axis name
                            'fold' :3
                        }

variables['ptll']  = {   'name': 'ptll',
                        'range' : (100, 0, 600),
                        'xaxis' : 'p_{T}^{ll} [GeV]',
                        'fold' : 3
                        }

variables['mll']  = {   'name': 'mll',
                        'range' : (100, 0,200),
                        'xaxis' : 'm_{ll} [GeV]',
                        'fold' : 3
                        }


variables['ptl1']  = {   'name': 'Lepton_pt[0]',
                        'range' : (60,0,300),
                        'xaxis' : 'p_{T} 1st lep',
                        'fold'  : 3
                        }


variables['ptl1lessbins']  = {   'name': 'Lepton_pt[0]',
                        'range' : (20,0,300),
                        'xaxis' : 'p_{T} 1st lep',
                        'fold'  : 3
                        }

variables['ptl2']  = {   'name': 'Lepton_pt[1]',
                        'range' : (60,0,300),
                        'xaxis' : 'p_{T} 2nd lep',
                        'fold'  : 3
                        }


variables['puppimet']  = {
                        'name': 'PuppiMET_pt',
                        'range' : (100,0,200),
                        'xaxis' : 'puppimet [GeV]',
                        'fold'  : 3
                        }

variables['detajj']  = {  'name': 'detajj',
                        'range' : (100, 0.0, 9.0),
                        'xaxis' : '#Delta#eta_{jj}',
                        'fold'  : 3
                        }

variables['dphijj']  = {  'name': 'dphijj',
                        'range' : (100, -3.15, 3.15),
                        'xaxis' : '#Delta#phi_{jj}',
                        'fold'  : 3
                        }


#variables['drjj']  = {  'name': 'drjj',
                        #'range' : (100, 0.0, 9.0),
                        #'xaxis' : '#DeltaR_{jj}',
                        #'fold'  : 3
                        #}

#
# ll jetjet
#

variables['dphilljet']  = {  'name': 'dphilljet',
                        'range' : (100, -3.15, 3.15),
                        'xaxis' : '#Delta#phi_{ll,j}',
                        'fold'  : 3
                        }

variables['dphilljetjet']  = {  'name': 'dphilljetjet',
                        'range' : (100, -3.15, 3.15),
                        'xaxis' : '#Delta#phi_{ll,jj}',
                        'fold'  : 3
                        }






