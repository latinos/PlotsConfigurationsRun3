
variables = {}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,1),  
    'xaxis' : 'events', 
    'fold'  : 3,
}

variables['mllVSmth2'] = {
    'name'  : 'mll:mth',
    'range' : ([12, 25, 40, 50, 70, 90, 210],[60, 80, 90, 110, 130, 150, 200],),
    'xaxis' : 'm_{ll} : m_{T}^{H}',
    'fold'  : 0,
}

variables['mth']  = {  
    'name': 'mth',     
    'range' : (20, 60, 200),   
    'xaxis' : 'm_{T}^{H} [GeV]',
    'fold' : 0,
}

variables['mll'] = {
    'name': 'mll',    
    'range' : (20,0,200), 
    'xaxis' : 'm_{ll} [GeV]',
    'fold' : 0,
}

