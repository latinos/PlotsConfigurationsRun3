
variables = {}

variables['events']  = {  
                          'name': '1',      
                          'range' : (1,0,2),
                          'xaxis' : 'events', 
                          'fold' : 0
                        }




variables['adnn_isVBF']  = {   
                            'name': 'adnns[0]',      
                            'range' : (100,0,1),
                            'xaxis' : 'adnn(isVBF)', 
                            'fold' : 0
                        }


variables['adnn_isGGH']  = {   
                            'name': 'adnns[1]',      
                            'range' : (100,0,1),
                            'xaxis' : 'adnn(isGGH)', 
                            'fold' : 0
                        }



bin_adnnisVBF = ['0.0', '0.04', '0.08', '0.12', '0.16', '0.2', '0.24', '0.28', '0.32', '0.36', '0.4', '0.44', '0.48', '0.52', '0.56', '0.6', '0.64', '0.68', '0.72', '0.76', '0.8', '0.84', '0.88', '0.92', '0.96', '1.0']
bin_adnnisGGH = ['0.0', '0.50', '0.80', '0.9', '1.0']
variables['adnn_VBFvsGGH'] = {
        'name': 'adnns_2D',
        'range': ((len(bin_adnnisVBF)-1)*(len(bin_adnnisGGH)-1), 1, (len(bin_adnnisVBF)-1)*(len(bin_adnnisGGH)-1)+1),
        'xaxis': 'adnn(isVBF):adnn(isGGH)',
        'fold' :0,
}


variables['dnn_isVBF']  = {   
                            'name': 'dnns[0]',      
                            'range' : (100,0,1),
                            'xaxis' : 'dnn(isVBF)', 
                            'fold' : 0
                        }

# variables['dnn_isGGH']  = {   
#                             'name': 'dnns[1]',      
#                             'range' : (100,0,1),
#                             'xaxis' : 'dnn(isGGH)', 
#                             'fold' : 0
#                         }

bin_dnnisVBF = ['0.0', '0.04', '0.08', '0.12', '0.16', '0.2', '0.24', '0.28', '0.32', '0.36', '0.4', '0.44', '0.48', '0.52', '0.56', '0.6', '0.64', '0.68', '0.72', '0.76', '0.8', '0.84', '0.88', '0.92', '0.96', '1.0']
bin_dnnisGGH = ['0.0', '0.50', '0.80', '0.9', '1.0']
variables['dnn_VBFvsGGH'] = {
        'name': 'dnns_2D',
        'range': ((len(bin_dnnisVBF)-1)*(len(bin_dnnisGGH)-1), 1, (len(bin_dnnisVBF)-1)*(len(bin_dnnisGGH)-1)+1),
        'xaxis': 'dnn(isVBF):dnn(isGGH)',
        'fold' :0,
}

