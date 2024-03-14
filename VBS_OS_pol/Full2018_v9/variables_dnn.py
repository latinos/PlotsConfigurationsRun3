import math

_mergedCuts = []
for cut in list(cuts.keys()):
    __cutExpr = ''
    if type(cuts[cut]) == dict:
        __cutExpr = cuts[cut]['expr']
        for cat in list(cuts[cut]['categories'].keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts

variables       = {}
particles = ['Lepton_', 'CleanJet_']
observables = ['pt', 'eta', 'phi']

for particle in particles:
        for observable in observables:
                for i in range(2):
                        var = particle + observable + str(i+1)
                        variables[var]     = {}
                        if observable == 'pt':
                                variables[var]['range']    = (30, 0, 300)
                                if 'Lepton' in particle:
                                        variables[var]['xaxis']     = 'p_{T}^{l_{' + str(i+1) + '}} [GeV]'
                                else:
                                        variables[var]['xaxis']     = 'p_{T}^{j_{' + str(i+1) + '}} [GeV]'
                        elif observable == 'eta' and 'Lepton' in particle:
                                variables[var]['range']    = (25, -2.5, 2.5)
                                variables[var]['xaxis']     = '#eta ^{l_{' + str(i+1) + '}}'
                        elif observable == 'eta' and 'Jet' in particle:
                                variables[var]['range']    = (25, -5, 5)
                                variables[var]['xaxis']     = '#eta ^{j_{' + str(i+1) + '}}'
                        elif observable == 'phi':
                                variables[var]['range']    = (20, -math.pi, math.pi)
                                if 'Lepton' in particle:
                                        variables[var]['xaxis']     = '#phi ^{l_{' + str(i+1) + '}}'
                                else:
                                        variables[var]['xaxis']     = '#phi ^{j_{' + str(i+1) + '}}'
                        else:
                                pass
                        variables[var]['name']     = particle + observable + '[' + str(i) + ']'
                        variables[var]['fold']     = 0
                        variables[var]['blind']    = dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])

variables['ptmiss']  = {
        'name'          : 'PuppiMET_pt',      
        'range'         : (30,0,300),
        'xaxis'         : 'p_{T}^{miss} [GeV]', 
        'fold'          : 0,
        'blind'         : dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

variables['phimiss']  = {
        'name'          : 'PuppiMET_phi',      
        'range'         : (20, -math.pi, math.pi),
        'xaxis'         : '#phi ^{miss}', 
        'fold'          : 0,
        'blind'         : dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

observables = [ 'mjj', 'detajj', 'Rpt', 'Zepp_l1', 'Zepp_l2', 'Zepp_ll', 'ptll', 'mll', 'drll', 'yll', 'mtw1', 'mtw2',
                'dphillmet', 'dphilmet1', 'dphilmet2', 'dphill', 'dphilep1jet1', 'dphilep1jet2', 'dphilep2jet1',
                'dphilep2jet2', 'dphilep1jj', 'dphilep2jj', 'dphilljet', 'dphijj', 'dphilljetjet', 'detall',
                'mT2', 'mTi', 'mcoll', 'mcollWW', 'ht', 'm2ljj30', 'recoil']

for observable in observables:
        var = '_' + observable
        variables[var] = {}
        xaxis = observable
        xaxis = xaxis.replace('lep1', 'l_{1}')
        xaxis = xaxis.replace('lep2', 'l_{2}')
        xaxis = xaxis.replace('jet1', 'j_{1}')
        xaxis = xaxis.replace('jet2', 'j_{2}')
        xaxis = xaxis.replace('jet', 'j')
        xaxis = xaxis.replace('l1', 'l_{1}')
        xaxis = xaxis.replace('l2', 'l_{2}')
        xaxis = xaxis.replace('_l1', ' _{l_{1}}')
        xaxis = xaxis.replace('_l2', ' _{l_{2}}')
        xaxis = xaxis.replace('lmet1', 'l_{1}MET')
        xaxis = xaxis.replace('lmet2', 'l_{2}MET')
        xaxis = xaxis.replace('met', 'MET')
        if 'dphi' in observable:
                variables[var]['range']    = (20, 0, math.pi)
                variables[var]['xaxis']    = xaxis.replace('dphi','#Delta#phi _{') + '}'
        elif 'dr' in observable:
                #xaxis = observable.replace('dr','#Delta R _{') + '}'
                variables[var]['range']    = (20, 0, 8)
                variables[var]['xaxis']    = xaxis.replace('dr','#Delta R _{') + '}'
        elif observable.startswith('m'):
                if 'j' in observable:
                        variables[var]['range']    = (30, 0, 3000)
                        if observable == 'mjj':
                                variables[var]['xaxis']     = 'm_{jj} [GeV]'
                        elif observable == 'm2ljj30':
                                variables[var]['xaxis']     = 'm_{ljj} [GeV]'
                        else:
                                #variables[var]['xaxis']     = observable + '} [GeV]'
                                variables[var]['xaxis']     = xaxis + '} [GeV]'
                else:
                        xaxis = observable.replace('m', 'm_{')
                        xaxis = xaxis.replace('t', 'T}')
                        xaxis = xaxis.replace('w1', '^{W_{1}')
                        xaxis = xaxis.replace('w2', '^{W_{2}')
                        variables[var]['range']    = (20, 0, 1000)
                        variables[var]['xaxis']     = xaxis + '} [GeV]'
                #variables[var]['xaxis']     = observable + ' [GeV]'
        elif 'deta' in observable:
                variables[var]['range']    = (20, 0, 10)
                variables[var]['xaxis']     = observable.replace('deta', '#Delta#eta _{') + '}'
        elif 'Zepp' in observable and 'll' not in observable:
                variables[var]['range']    = (20, -5, 5)
                variables[var]['xaxis']     = xaxis
        elif observable == 'Zepp_ll':
                variables[var]['range']    = (20, 0, 5)
                variables[var]['xaxis']     = 'Zepp_{ll}'
        elif observable == 'Rpt':
                variables[var]['range']    = (20, 0, 20)
                variables[var]['xaxis']     = 'R_{p_{T}}'
        elif observable == 'ptll':
                variables[var]['range']    = (20, 0, 500)
                variables[var]['xaxis']     = 'p_{T}^{ll} [GeV]'
        elif observable == 'yll':
                variables[var]['range']    = (20, -2.5, 2.5)
                variables[var]['xaxis']     = 'y_{ll}'
        else:
                variables[var]['range']    = (20, 0, 1000)
                variables[var]['xaxis']     = observable + ' [GeV]'
        variables[var]['name']     = observable
        variables[var]['fold']     = 0
        variables[var]['blind']    = dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])

particles       = ['l1j1', 'l1j2', 'l2j1', 'l2j2']
observables     = ['m_lj', 'dr_lj']
for i, particle in enumerate(particles):
        for observable in observables:
                var     = observable.strip('lj') + particle
                variables[var] = {
                        'name'  : observable + '[' + str(i) + ']',
                        'fold'  : 0,
                        'blind' : dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                }
                xaxis = var
                xaxis = xaxis.replace('l1', 'l_{1}')
                xaxis = xaxis.replace('l2', 'l_{2}')
                xaxis = xaxis.replace('j1', 'j_{1}')
                xaxis = xaxis.replace('j2', 'j_{2}')
                if 'dr' in observable:
                        xaxis = xaxis.replace('dr_','#Delta R_{')
                        #variables[var]['xaxis'] = var.replace('dr','#Delta R (') + ')'
                        variables[var]['xaxis'] = xaxis + '}'
                        variables[var]['range'] = (20, 0, 8)
                else:
                        xaxis = xaxis.replace('m_','m_{')
                        #variables[var]['xaxis'] = var.replace('m_','m_{') + '} [GeV]'
                        variables[var]['xaxis'] = xaxis + '} [GeV]'
                        variables[var]['range'] = (20, 0, 2000)

for i in range(2):
        variables['proxy_W' + str(i+1)]  = {  
                'name'  : 'proxyW['+ str(i) + ']',
                'range' : (20, 0, 500),
                'xaxis' : 'proxy_{W_{' + str(i+1) + '}} [GeV]',
                'fold'  : 0,
                'blind' :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
        }

variables['events']  = {  
                          'name': '1',      
                          'range' : (1,0,2),
                          'xaxis' : 'events', 
                          'fold' : 0,
                          'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                        }

variables['dnn_isVBS']  = {   
                            'name': 'dnn_SigVsBkg[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'dnn(isVBS)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])

                        }

variables['dnn_isLL']  = {   
                            'name': 'dnn_LLVsOther[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'dnn(isLL)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                        }

variables['dnn_isTT']  = {   
                            'name': 'dnn_TTVsOther[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'dnn(isTT)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                        }

variables['dnn_LLD']  = {   
                            'name': 'LLD',      
                            'range' : (5,0,2),
                            'xaxis' : 'dnn(isLL) / (1 - dnn(isTT))', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                        }

variables['dnn_TTD']  = {   
                            'name': 'TTD',      
                            'range' : (5,0,2),
                            'xaxis' : 'dnn(isTT) / (1 - dnn(isLL))', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                        }


bin_dnnTT = ['0.', '0.1', '0.2', '0.4', '0.6', '0.8', '0.9', '1.']
bin_dnnLL = ['0.', '0.1', '0.2', '0.4', '0.6', '0.8', '0.9', '1.']
variables['dnn_TTvsLL_49'] = {
        'name': 'dnn2D_49',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

bin_dnnTT = ['0.', '0.15', '0.3', '0.5', '0.7', '0.85', '1.']
bin_dnnLL = ['0.', '0.15', '0.3', '0.5', '0.7', '0.85', '1.']
variables['dnn_TTvsLL_36'] = {
        'name': 'dnn2D_36',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

bin_dnnTT = ['0.', '0.15', '0.3', '0.7', '0.85', '1.']
bin_dnnLL = ['0.', '0.15', '0.3', '0.7', '0.85', '1.']
variables['dnn_TTvsLL_25'] = {
        'name': 'dnn2D_25',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

bin_dnnTT = ['0.', '0.2', '0.5', '0.8', '1.']
bin_dnnLL = ['0.', '0.2', '0.5', '0.8', '1.']
variables['dnn_TTvsLL_16'] = {
        'name': 'dnn2D_16',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}
'''
variables['new_dnn_TTvsLL_16'] = {
        'name': 'dnn_isTT:dnn_isLL',
        'range': ([0., 0.2, 0.5, 0.8, 1.],[0., 0.2, 0.5, 0.8, 1.]),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}
'''
bin_dnnTT = ['0.', '0.25', '0.5', '0.75', '1.']
bin_dnnLL = ['0.', '0.25', '0.5', '0.75', '1.']
variables['dnn_TTvsLL_16v2'] = {
        'name': 'dnn2D_16v2',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

bin_dnnTT = ['0.', '0.5', '1.']
bin_dnnLL = ['0.', '0.5', '1.']
variables['dnn_TTvsLL_4'] = {
        'name': 'dnn2D_4',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
}

variables['mjj'] = {   
                    'name': 'mjj',            #   variable name    
                    'range' : ([300., 500., 750., 1000., 1500., 2000., 4000.],),    #   variable range
                    'xaxis' : 'm_{jj} [GeV]',  #   x axis name
                    'fold' :3,
                    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'VBS' in cut and 'BKG' not in cut])
                  }

print(variables)
