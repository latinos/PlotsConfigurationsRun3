# _mergedCuts = []
# for cut in list(cuts.keys()):
#     __cutExpr = ''
#     if type(cuts[cut]) == dict:
#         __cutExpr = cuts[cut]['expr']
#         for cat in list(cuts[cut]['categories'].keys()):
#             _mergedCuts.append(cut + '_' + cat)
#     elif type(cuts[cut]) == str:
#         _mergedCuts.append(cut)

# cuts2j = _mergedCuts



variables = {}

variables['events']  = {  
                          'name': '1',      
                          'range' : (1,0,2),
                          'xaxis' : 'events', 
                          'fold' : 0
                        }
'''
variables['adnn_isVBF']={
                          'name' : 'adnns[0]',
                          'range': (10,0,1),
                          'xaxis':'events',
                          'fold':0
    }

'''
variables['adnn_isVBF']  = {   
                            'name': 'adnns[0]',      
                            'range' : ([0, 0.485, 0.695, 0.8, 0.86, 0.9, 0.93, 0.95, 0.965, 0.975, 0.985, 0.99, 0.995, 1.0],),
                            'xaxis' : 'adnn(isVBF)', 
                            'fold' : 0
                        }


variables['adnn_isGGH']  = {   
                            'name': 'adnns[1]',      
                            'range' : ([0.0, 0.50, 0.65, 0.80, 0.85, 0.9, 0.93, 0.95, 0.96, 0.98, 0.99, 1.0],),
                            'xaxis' : 'adnn(isGGH)', 
                            'fold' : 0
                        }


bin_adnnisVBF = ['0.0', '0.50', '0.65', '0.80', '0.85', '0.9', '0.93', '0.95', '0.96', '0.98', '0.99', '1.0']
bin_adnnisGGH = ['0.0', '0.50', '0.65', '0.80', '0.85', '0.9', '0.93', '0.95', '0.96', '0.98', '0.99', '1.0']
variables['adnn_VBFvsGGH'] = {
        'name': 'adnns_2D',
        'range': ((len(bin_adnnisVBF)-1)*(len(bin_adnnisGGH)-1), 1, (len(bin_adnnisVBF)-1)*(len(bin_adnnisGGH)-1)+1),
        'xaxis': 'adnn(isVBF):adnn(isGGH)',
        'fold' :0,
}





# variables['Tree'] = {
#         'tree': {
#             'adnn_isVBF' : 'adnns[0]' ,
#             'adnn_isGGH' : 'adnns[1]' ,
#             },
#         'cuts': ['hww2l2v_13TeV_of2j_dphijj_4bins']
#         }
