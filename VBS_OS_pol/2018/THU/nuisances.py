mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
mcSteps = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
#limitFiles = -1

def makeMCDirectory(var=''):
    if var== '':
        return os.path.join(treeBaseDir, mcProduction, mcSteps)
    else:
        return os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var)


# merge cuts
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

nuisances = {}

##### PS

nuisances['PS_ISR']  = {
    'name'    : 'PS_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['PS_FSR']  = {
    'name'    : 'PS_FSR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
    'AsLnN'   : '0',
}

###### pdf uncertainties

# info at https://lhapdfsets.web.cern.ch/current/NNPDF31_nnlo_as_0118_mc_hessian_pdfas/NNPDF31_nnlo_as_0118_mc_hessian_pdfas.info
# LHEPdfWeight[0] is the average on replicas        (mem = 0)
# LHEPdfWeight[100] is the nominal weight           (mem = 101)
# LHEPdfWeight[101] is computed at aS(MZ) = 0.116   (mem = 102)
# LHEPdfWeight[102] is computed at aS(MZ) = 0.120   (mem = 103)

for pdf in range(1,100):
    pdf_variations = ['LHEPdfWeight[' + str(pdf) + ']', 'LHEPdfWeight[' + str(pdf) + ']']
    nuisances['pdf_WWewk_' + str(pdf)] = {
        'name': 'pdf_WWewk_' + str(pdf),
        'kind': 'weight',
        'type': 'shape',
        'samples' : dict((skey, pdf_variations) for skey in mc),
    }

##### Renormalization & factorization scales

## Shape nuisance due to QCD scale variations
# LHE scale variation weights (w_var / w_nominal)

## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
#variations = ['LHEScaleWeight[0]', 'LHEScaleWeight[1]', 'LHEScaleWeight[3]', 'LHEScaleWeight[Length$(LHEScaleWeight)-4]', 'LHEScaleWeight[Length$(LHEScaleWeight)-2]', 'LHEScaleWeight[Length$(LHEScaleWeight)-1]']

VBSvariations = ['LHEScaleWeight[2]', 'LHEScaleWeight[0]'] # LO samples include only variations on muF scale [2]: mu_R = 2.0, [0]: mu_R = 0.5

nuisances['QCDscale_WWewk'] = {
    'name': 'QCDscale_WWewk',
    'kind': 'weight',
    'type': 'shape',
    'samples' : dict((skey, VBSvariations) for skey in mc),
}

