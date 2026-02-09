# variables
variables = {}

variables['events'] = {
    'name'  : '1',
    'range' : (1,0,2),
    'xaxis' : 'events',
    'fold'  : 3
}

variables['nvtx'] = {
    'name'  : 'PV_npvsGood',
    'range' : (100, 0, 100),
    'xaxis' : 'number of vertices',
    'fold'  : 3
}

variables['mll'] = {
    'name': 'mll',
    'range' : (60,0,120),
    'xaxis' : 'm(\ell_1,\ell_2) [GeV]',
    'fold' : 3
}

variables['mllOneThree'] = {
    'name': 'mllOneThree',
    'range' : (60,0,120),
    'xaxis' : 'm(\ell_1,\ell_3) [GeV]',
    'fold' : 3
}

variables['mllTwoThree'] = {
    'name': 'mllTwoThree',
    'range' : (60,0,120),
    'xaxis' : 'm(\ell_2,\ell_3) [GeV]',
    'fold' : 3
}
