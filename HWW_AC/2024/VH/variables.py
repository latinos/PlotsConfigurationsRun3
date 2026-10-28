
variables = {}


variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

"""
variables['mjj']  = {
    'name': 'mjj',
    'range' : (20, 100,1100),
    'xaxis' : 'm_{jj}',
    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}
"""

def DeclareKD3D(KDName,Xaxis, mainvar,mainbinning,sub1var,sub1binning,sub2var,sub2binning, Cuts):

 nbins =  (len(sub2binning) - 1)*(len(sub1binning) - 1)*(len(mainbinning) - 1)

 name = ''
 sub2bin = ['1'] # folding underflow -> always 1
 for isub2 in range(1, len(sub2binning) - 1):
    sub2bin.append('('+sub2var+' >= %1.2f)' % sub2binning[isub2])
 name += '+'.join(sub2bin)
 name += ' + %d*(' % (len(sub2binning) - 1)
 sub1bin = [] # 1-1 for first bin
 for isub1 in range(1, len(sub1binning) - 1):
    sub1bin.append('('+sub1var+' >= %1.2f)' % sub1binning[isub1])
 name += '+'.join(sub1bin)
 name += ')'
 name += ' + %d*(' % ((len(sub2binning) - 1)*(len(sub1binning) - 1))
 mainbin = [] # 1-1 for first bin
 for imain in range(1, len(mainbinning) - 1):
    mainbin.append('('+mainvar+' >= %1.2f)' % mainbinning[imain])
 name += '+'.join(mainbin)
 name += ') - 0.5'

 variables['kd3d_'+KDName+''] = {
    'name': name,
    'range': (nbins, 0., nbins),
    'xaxis': Xaxis,
    'fold': 0,   
    'cuts' : Cuts
 }

def DeclareKD4D(KDName,Xaxis, mainvar,mainbinning,sub1var,sub1binning,sub2var,sub2binning,sub3var,sub3binning, Cuts):

 nbins =  (len(sub3binning) - 1)*(len(sub2binning) - 1)*(len(sub1binning) - 1)*(len(mainbinning) - 1)

 name = ''
 sub3bin = ['1'] # folding underflow -> always 1
 for isub3 in range(1, len(sub3binning) - 1):
    sub3bin.append('( '+sub3var+'>= %1.2f)' % sub3binning[isub3])
 name += '+'.join(sub3bin)
 name += ' + %d*(' % (len(sub3binning) - 1)
 sub2bin = [] # 1-1 for first bin
 for isub2 in range(1, len(sub2binning) - 1):
    sub2bin.append('('+sub2var+' >= %1.2f)' % sub2binning[isub2])
 name += '+'.join(sub2bin)
 name += ')'
 name += ' + %d*(' % ((len(sub3binning) - 1)*(len(sub2binning) - 1))
 sub1bin = [] # 1-1 for first bin
 for isub1 in range(1, len(sub1binning) - 1):
    sub1bin.append('('+sub1var+' >= %1.2f)' % sub1binning[isub1])
 name += '+'.join(sub1bin)
 name += ')'
 name += ' + %d*(' % ((len(sub3binning) - 1)*(len(sub2binning) - 1)*(len(sub1binning) - 1))
 mainbin = [] # 1-1 for first bin
 for imain in range(1, len(mainbinning) - 1):
    mainbin.append('('+mainvar+' >= %1.2f)' % mainbinning[imain])
 name += '+'.join(mainbin)
 name += ') - 0.5'

 variables['kd4d_'+KDName+''] = {
    'name': name,
    'range': (nbins, 0., nbins),
    'xaxis': Xaxis,
    'fold': 0,  
    'cuts' : Cuts
 }


DeclareKD3D('vh','D_{VH}','kd_mixhm',[-1,0,1],'kd_mixhp',[-1,-0.82,1],'kd_hp',[0,0.25,0.5,0.75,1],
['hww_sr_2jvh'])

variables['kd2d_mix'] = {'name': 'kd_mixhm:kd_mixhp',
                         'range' : ([-1,0,1],[-1,-0.82,1],),
                         'xaxis' : 'D_{0-:0+}',
                         'fold' : 3,
                        }
 
"""
variables['kd_hp'] = { 'name'  : 'kd_hp',
                       'range' : (10, 0., 1.),
                       'xaxis' : 'D_{0^{+}}',
                       'fold'  : 0
                   }
"""

variables['kd_hm'] = { 'name'  : 'kd_hm',
                       'range' : (10, 0., 1.),
                       'xaxis' : 'D_{0^{-}}',
                       'fold'  : 0
                   }

"""
variables['kd_mixhp'] = { 'name'  : 'kd_mixhp',
                          'range' : (10, -1., 1.),
                          'xaxis' : 'D_{Int}',
                          'fold'  : 0
                   }

"""

variables['kd_mixhm'] = { 'name'  : 'kd_mixhm',
                          'range' : (10, -1., 1.),
                          'xaxis' : 'D_{CP}',
                          'fold'  : 0
                   }


