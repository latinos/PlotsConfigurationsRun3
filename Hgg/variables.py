variables = {}

# variables['ttree_variable'] = {
#         'tree': {'LeptonPt1': 'Lepton_pt[0]'},
#         'cuts': ['sr']
#         }

variables['ptj1'] = {
        'name': 'CleanJet_pt[0]',
        'range': (100, 30, 500),
        'xaxis': 'p_{T} 1st jet',
        'fold' :3
}

variables['ptj2'] = {
        'name': 'CleanJet_pt[1]',
        'range': (100, 30, 500),
        'xaxis': 'p_{T} 2nd jet',
        'fold' :3
}

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
                        'range' : (70, 30, 600),
                        'xaxis' : 'p_{T}^{ll} [GeV]',
                        'fold' : 3
                        }

variables['mll']  = {   'name': 'mll',
                        'range' : (100, 66,107),
                        'xaxis' : 'm_{ll} [GeV]',
                        'fold' : 3
                        }


variables['ptl1']  = {   'name': 'Lepton_pt[0]',
                        'range' : (60,30,300),
                        'xaxis' : 'p_{T} 1st lep',
                        'fold'  : 3
                        }

variables['ptl2']  = {   'name': 'Lepton_pt[1]',
                        'range' : (60,20,300),
                        'xaxis' : 'p_{T} 2nd lep',
                        'fold'  : 3
                        }


variables['puppimet']  = {
                        'name': 'PuppiMET_pt',
                        'range' : (20,0,200),
                        'xaxis' : 'puppimet [GeV]',
                        'fold'  : 3
                        }

variables['detajj']  = {  'name': 'newDetajj',
                        'range' : (50, 0.0, 9.0),
                        'xaxis' : '#Delta#eta_{jj}',
                        'fold'  : 3
                        }

variables['dphijj']  = {  'name': 'dphijj',
                        'range' : (20, 0, 3.15),
                        'xaxis' : '#Delta#phi_{jj}',
                        'fold'  : 3
                        }

