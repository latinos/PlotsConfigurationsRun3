
variables = {}

variables['events']  = {  
                          'name': '1',      
                          'range' : (1,0,2),
                          'xaxis' : 'events', 
                          'fold' : 0
                        }

variables['adnn_isVBF']  = {   
                            'name': 'adnn[0]',      
                            'range' : ([0.0, 0.405, 0.655, 0.78, 0.855, 0.9, 0.93, 0.9500000000000001, 0.965, 0.98, 0.99, 1.0],),
                            'xaxis' : 'adnn(isVBF)', 
                            'fold' : 0
                        }


# variables['Tree'] = {
#         'tree': {
#             'adnn_isVBF' : 'adnn[0]' ,
#             },
#         'cuts': ['hww2l2v_13TeV_of2j_dphijj_4bins']
#         }
