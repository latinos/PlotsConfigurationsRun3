# variables

# 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow

# variables = {}

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


