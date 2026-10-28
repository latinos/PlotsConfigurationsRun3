
variables = {}

"""
variables['classvbf'] = { 
    'name': 'vbf_clf[0]',
    'range' : (750,0.25,1.),
    'xaxis' : 'DNN discriminant vbf',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['classtop'] = { 
    'name': 'vbf_clf[2]',
    'range' : (15,0.25,1.),
    'xaxis' : 'DNN discriminant top',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])

}

variables['classww'] = { 
    'name': 'vbf_clf[3]',
    'range' : (15,0.25,1.),
    'xaxis' : 'DNN discriminant ww',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['classggh'] = { 
    'name': 'vbf_clf[1]',
    #'range' : ([0.,0.485, 0.555, 0.615, 0.665, 0.715, 0.7750, 0.865, 1.],),
    'range' : (750,0.25,1.),
    'xaxis' : 'DNN discriminant ggh',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}
"""

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

 
DeclareKD4D('vbf','D_{VBF}','kd_vbf',[0.0,0.75,1],'kd_mixhm',[-1,0,1],'kd_mixhp',[-1,0.4,1],'kd_hp',[0,0.25,0.5,0.75,1],['hww_sr_2j'])

#DeclareKD4D('vbf2','D_{VBF}','kd_vbf',[0.25,0.75,1],'kd_mixhm',[-1,0,1],'kd_mixhp',[-1,0.4,1],'kd_hp',[0,0.25,0.5,0.75,1],['hww_sr_2j'])

#DeclareKD4D('vbf3','D_{VBF}','kd_vbf',[0.5,0.8,1],'kd_mixhm',[-1,0,1],'kd_mixhp',[-1,0.4,1],'kd_hp',[0,0.25,0.5,0.75,1],['hww_sr_2j']) 

"""
variables['kd2d_mix'] = {'name': 'kd_mixhm:kd_mixhp',
                         'range' : ([-1,0,1],[-1,0.4,1],),
                         'xaxis' : 'D_{0-:0+}',
                         'fold' : 0,
                        }
"""

variables['kd_vbf'] = { 'name'  : 'kd_vbf', 'range' : (10, 0., 1.), 'xaxis' : 'D_{VBF}', 'fold'  : 0}

variables['kd_hp']   = { 'name'  : 'kd_hp',   'range' : (10, 0., 1.), 'xaxis' : 'D_{0^{+}}',    'fold'  : 0 }
variables['kd_hm']   = { 'name'  : 'kd_hm',   'range' : (10, 0., 1.), 'xaxis' : 'D_{0^{-}}',    'fold'  : 0 }
variables['kd_hl']   = { 'name'  : 'kd_hl',   'range' : (10, 0., 1.), 'xaxis' : 'D_{#Lambda}',   'fold'  : 0 }
variables['kd_hpzg'] = { 'name'  : 'kd_hpzg', 'range' : (10, 0., 1.), 'xaxis' : 'D_{0_Zg^{+}}', 'fold'  : 0 }
variables['kd_hmzg'] = { 'name'  : 'kd_hmzg', 'range' : (10, 0., 1.), 'xaxis' : 'D_{0_Zg^{-}}', 'fold'  : 0 }
variables['kd_hpgg'] = { 'name'  : 'kd_hpgg', 'range' : (10, 0., 1.), 'xaxis' : 'D_{0_gg^{+}}', 'fold'  : 0 }
variables['kd_hmgg'] = { 'name'  : 'kd_hmgg', 'range' : (10, 0., 1.), 'xaxis' : 'D_{0_gg^{-}}', 'fold'  : 0 }

variables['kd_mixhp']   = { 'name'  : 'kd_mixhp',   'range' : (10, -1., 1.), 'xaxis' : 'D_{Int}',          'fold'  : 0 }
variables['kd_mixhm']   = { 'name'  : 'kd_mixhm',   'range' : (10, -1., 1.), 'xaxis' : 'D_{CP}',           'fold'  : 0 }
variables['kd_mixhl']   = { 'name'  : 'kd_mixhl',   'range' : (10, -1., 1.), 'xaxis' : 'D_{Int^{#Lambda}}','fold'  : 0 }
variables['kd_mixhpzg'] = { 'name'  : 'kd_mixhpzg', 'range' : (10, -1., 1.), 'xaxis' : 'D_{Int^{Zg}}',     'fold'  : 0 }
variables['kd_mixhmzg'] = { 'name'  : 'kd_mixhmzg', 'range' : (10, -1., 1.), 'xaxis' : 'D_{CP^{Zg}}',      'fold'  : 0 }
variables['kd_mixhpgg'] = { 'name'  : 'kd_mixhpgg', 'range' : (10, -1., 1.), 'xaxis' : 'D_{Int^{gg}}',     'fold'  : 0 }
variables['kd_mixhmgg'] = { 'name'  : 'kd_mixhmgg', 'range' : (10, -1., 1.), 'xaxis' : 'D_{CP^{gg}}',      'fold'  : 0 }


