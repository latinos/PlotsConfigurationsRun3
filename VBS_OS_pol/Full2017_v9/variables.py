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

variables = {}
variables['events']  = {  
                          'name': '1',      
                          'range' : (1,0,2),
                          'xaxis' : 'events', 
                          'fold' : 0,
                          'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
                        }

variables['dnn_isVBS']  = {   
                            'name': 'dnn_SigVsBkg[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'dnn(isVBS)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])

                        }

variables['dnn_isLL']  = {   
                            'name': 'dnn_LLVsOther[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'dnn(isLL)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
                        }

variables['dnn_isTT']  = {   
                            'name': 'dnn_TTVsOther[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'dnn(isTT)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
                        }

bin_dnnTT = ['0.', '0.1', '0.2', '0.4', '0.6', '0.8', '0.9', '1.']
bin_dnnLL = ['0.', '0.1', '0.2', '0.4', '0.6', '0.8', '0.9', '1.']
variables['dnn_TTvsLL_49'] = {
        'name': 'dnn2D_49',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

bin_dnnTT = ['0.', '0.15', '0.3', '0.5', '0.7', '0.85', '1.']
bin_dnnLL = ['0.', '0.15', '0.3', '0.5', '0.7', '0.85', '1.']
variables['dnn_TTvsLL_36'] = {
        'name': 'dnn2D_36',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

bin_dnnTT = ['0.', '0.15', '0.3', '0.7', '0.85', '1.']
bin_dnnLL = ['0.', '0.15', '0.3', '0.7', '0.85', '1.']
variables['dnn_TTvsLL_25'] = {
        'name': 'dnn2D_25',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

bin_dnnTT = ['0.', '0.2', '0.5', '0.8', '1.']
bin_dnnLL = ['0.', '0.2', '0.5', '0.8', '1.']
variables['dnn_TTvsLL_16'] = {
        'name': 'dnn2D_16',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}
'''
variables['new_dnn_TTvsLL_16'] = {
        'name': 'dnn_isTT:dnn_isLL',
        'range': ([0., 0.2, 0.5, 0.8, 1.],[0., 0.2, 0.5, 0.8, 1.]),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}
'''
bin_dnnTT = ['0.', '0.25', '0.5', '0.75', '1.']
bin_dnnLL = ['0.', '0.25', '0.5', '0.75', '1.']
variables['dnn_TTvsLL_16v2'] = {
        'name': 'dnn2D_16v2',
        'range': ((len(bin_dnnTT)-1)*(len(bin_dnnLL)-1), 1, (len(bin_dnnTT)-1)*(len(bin_dnnLL)-1)+1),
        'xaxis': 'dnnTT:dnnLL',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mjj'] = {   
                    'name': 'mjj',            #   variable name    
                    'range' : ([300., 500., 750., 1000., 1500., 2000., 4000.],),    #   variable range
                    'xaxis' : 'm_{jj} [GeV]',  #   x axis name
                    'fold' :3,
                    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
                  }

print(variables)
