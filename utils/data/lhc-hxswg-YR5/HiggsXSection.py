#!/usr/bin/env python
import sys, re, os, os.path, string
import ROOT
#from ROOT import *
from array import array 

class HiggsXSection:

    def file2map(self, x):
        ret = {}
        headers = []
        if not os.path.exists(x):
            print(f"Warning: File not found: {x}")
            return ret
        for line in open(x, "r"):
            cols = line.split()
            if len(cols) < 2: 
                continue
            if "mH" in line:
                headers = [i.strip() for i in cols[1:]]
            else:
                fields = [float(i) for i in cols]
                ret[fields[0]] = dict(zip(headers, fields[1:]))
        return ret

    def __init__(self):
        self._YR = {}       
        
        # Load only YR5 data (13p6TeV)
        self.readYR()
        self._UseggZH = True

        self._br = {}
        self._br['W2lv'] = 0.108 * 3.0
        self._br['W2QQ'] = 0.676
        self._br['Z2ll'] = 0.033658 * 3.0

    def readYR(self, model='sm'):
        
        # Create Structure
        if not model in self._YR: 
            self._YR[model] = {}
        if not 'xs' in self._YR[model]: 
            self._YR[model]['xs'] = {}
        if not 'br' in self._YR[model]: 
            self._YR[model]['br'] = {}
       

        # Add x-sections
        # ... SM
        if model == 'sm': 
            
            xs_dir = f'{model}/xs/13p6TeV-'
            self._YR[model]['xs']['ggH'] = self.file2map(f'{xs_dir}ggH.txt') 
            self._YR[model]['xs']['vbfH'] = self.file2map(f'{xs_dir}vbfH.txt') 
            self._YR[model]['xs']['WH'] = self.file2map(f'{xs_dir}WH.txt') 
            self._YR[model]['xs']['ZH'] = self.file2map(f'{xs_dir}ZH.txt') 
            self._YR[model]['xs']['ggZH'] = self.file2map(f'{xs_dir}ggZH.txt') 
            self._YR[model]['xs']['ttH'] = self.file2map(f'{xs_dir}ttH.txt') 
            
            br_dir = f'{model}/br/'
            self._YR[model]['br']['VV'] = self.file2map(f'{br_dir}BR4.txt')
            self._YR[model]['br']['ff'] = self.file2map(f'{br_dir}BR4.txt')

        else:
            print("Model Not Found")

    def printYR(self):
        print(self._YR)

    def GetYR(self):
        return self._YR

    def GetYRVal(self, YRDic, mh, Key):
        iMass = float(mh)
        if iMass in YRDic:
            if not Key in YRDic[iMass]: 
                return 0.
            return YRDic[iMass][Key]
        else:
            n = len(YRDic.keys())
            if n == 0: 
                return 0.
            x = []
            y = []
            for jMass in sorted(YRDic.keys()):
                if Key in YRDic[jMass]:
                    x.append(jMass)
                    y.append(YRDic[jMass][Key])
            if not x or iMass < x[0] or iMass > x[-1]: 
                return 0.
            gr = TGraph(len(x), array('f', x), array('f', y))
            sp = TSpline3("YR", gr)
            return sp.Eval(iMass)
        return 0.

    def GetHiggsProdXS(self, proc, mh, model='sm'):
        if not model in self._YR: 
            return 0
        if not 'xs' in self._YR[model]: 
            return 0
        if proc in ['HWplus', 'HWminus', 'HW']:
            if not 'WH' in self._YR[model]['xs']: 
                return 0 
        else:
            if not proc in self._YR[model]['xs']: 
                return 0 
     
        if proc == 'ZH':
            xs_ZH = self.GetYRVal(self._YR[model]['xs'][proc], mh, 'XS_pb')
            if self._UseggZH and not model == 'bsm':
                xs_ggZH = self.GetYRVal(self._YR[model]['xs']['ggZH'], mh, 'XS_pb')
            else:
                xs_ggZH = 0.
            return xs_ZH - xs_ggZH
        elif proc == 'HWplus':
            return self.GetYRVal(self._YR[model]['xs']['WH'], mh, 'XS_W_plus_pb')
        elif proc == 'HWminus':
            return self.GetYRVal(self._YR[model]['xs']['WH'], mh, 'XS_W_minus_pb')
        elif proc == 'HW':
            return self.GetYRVal(self._YR[model]['xs']['WH'], mh, 'XS_W_plus_pb') + self.GetYRVal(self._YR[model]['xs']['WH'], mh, 'XS_W_minus_pb')
        else:
            return self.GetYRVal(self._YR[model]['xs'][proc], mh, 'XS_pb')

    def GetHiggsProdXSNP(self, proc, mh, np='scale', model='sm'):
        if not np in ['scale', 'pdf']: 
            return '1.0'
        if not model in self._YR: 
            return '1.0'
        if not 'xs' in self._YR[model]: 
            return '1.0'
        if proc in ['HWplus', 'HWminus']:
            if not 'WH' in self._YR[model]['xs']: 
                return '1.0'
        else:
            if not proc in self._YR[model]['xs']: 
                return '1.0'
         
        if np == 'scale':
            if proc == 'ZH' and abs(float(mh) - 125.0) < 5 and model == 'sm':
                return str(1.0 + self.GetYRVal(self._YR[model]['xs']['qqZH125'], '125.0', 'Scale_neg') / 100.) + '/' + str(1.0 + self.GetYRVal(self._YR[model]['xs']['qqZH125'], '125.0', 'Scale_pos') / 100.)
            elif proc == 'ggZH' and abs(float(mh) - 125.0) < 5 and model == 'sm':
                return str(1.0 + self.GetYRVal(self._YR[model]['xs']['ggZH125'], '125.0', 'Scale_neg') / 100.) + '/' + str(1.0 + self.GetYRVal(self._YR[model]['xs']['ggZH125'], '125.0', 'Scale_pos') / 100.)
            elif proc == 'ggZH':
                return '1.37'  # Run-I CMS/ATLAS combination
            else:
                return str(1.0 + self.GetYRVal(self._YR[model]['xs'][proc], mh, 'Scale_neg') / 100.) + '/' + str(1.0 + self.GetYRVal(self._YR[model]['xs'][proc], mh, 'Scale_pos') / 100.)

        elif np == 'pdf':
            if proc == 'ZH' and abs(float(mh) - 125.0) < 5 and model == 'sm':
                return str(1.0 + self.GetYRVal(self._YR[model]['xs']['qqZH125'], '125.0', 'PDF_plus_alpha_s') / 100.)
            elif proc == 'ggZH' and abs(float(mh) - 125.0) < 5 and model == 'sm':
                return str(1.0 + self.GetYRVal(self._YR[model]['xs']['ggZH125'], '125.0', 'PDF_plus_alpha_s') / 100.)
            elif proc == 'ggZH':
                return '1.15'  # Run-I CMS/ATLAS combination
            else:  
                return str(1.0 + self.GetYRVal(self._YR[model]['xs'][proc], mh, 'PDF_plus_alpha_s') / 100.)

    def YR4dec(self, decay):
        decay_map = {
            'H_bb': 'hbb', 'H_tautau': 'htt', 'H_mumu': 'hmm',
            'H_ssbar': 'hss', 'H_ccbar': 'hcc', 'H_ttbar': 'htoptop',
            'H_gg': 'hgluglu', 'H_gamgam': 'hgg', 'H_Zgam': 'hzg',
            'H_WW': 'hww', 'H_ZZ': 'hzz'
        }
        return decay_map.get(decay, decay)

    def GetHiggsBR(self, decay, mh, model='sm'):
        if not model in self._YR: 
            return 0
        if not 'br' in self._YR[model]: 
            return 0
        if decay in ['H_bb', 'H_tautau', 'H_mumu', 'H_ssbar', 'H_ccbar', 'H_ttbar']: 
            return self.GetYRVal(self._YR[model]['br']['ff'], mh, self.YR4dec(decay))
        elif decay in ['H_gg', 'H_gamgam', 'H_Zgam', 'H_WW', 'H_ZZ', 'Total_Width_GeV']: 
            return self.GetYRVal(self._YR[model]['br']['VV'], mh, self.YR4dec(decay))
        return 0

    def GetHiggsXS4Sample(self, SampleName):
        HiggsXS = {}
        HiggsXS['Sample'] = SampleName
        
        # ... Higgs production mechanism
        HiggsProdXS = 0.
        ProdMode = 'unknown'
        if 'Mlarge' in SampleName: 
            ProdMode = 'unknown'
        elif 'GluGluH' in SampleName: 
            ProdMode = 'ggH'
        elif 'VBFH' in SampleName: 
            ProdMode = 'vbfH'
        elif 'HZJ' in SampleName: 
            ProdMode = 'ZH'
        elif 'ggZH' in SampleName or 'GluGluZH' in SampleName: 
            ProdMode = 'ggZH'
        elif 'HWplusJ' in SampleName: 
            ProdMode = 'HWplus'
        elif 'HWminusJ' in SampleName: 
            ProdMode = 'HWminus'
        elif 'ttH' in SampleName: 
            ProdMode = 'ttH'  
        elif 'VBF_H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            ProdMode = 'vbfH'  
        elif 'WH_H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            ProdMode = 'HW'
        elif 'ZH_H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            ProdMode = 'ZH' 
        elif 'ttH_H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            ProdMode = 'ttH'
        elif 'H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            ProdMode = 'ggH'  

        HiggsMass = 0.
        if 'Mlarge' in SampleName: 
            HiggsMass = '0.0'
        elif '_M' in SampleName: 
            HiggsMass = SampleName.split('_M')[1]
        if '_' in str(HiggsMass): 
            HiggsMass = HiggsMass.split('_')[0]
        if 'H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            HiggsMass = 125.0

        if not ProdMode == 'unknown':
            if float(HiggsMass) <= 130 and float(HiggsMass) >= 120:
                HiggsProdXS = self.GetHiggsProdXS(ProdMode, HiggsMass)
            else:
                HiggsProdXS = self.GetHiggsProdXS(ProdMode, HiggsMass, 'bsm')
      
        HiggsXS['ProdMode'] = ProdMode
        HiggsXS['HiggsMass'] = HiggsMass
        HiggsXS['ProdXS'] = HiggsProdXS

        # ... Higgs decay
        HiggsBR = 0.
        DecayMode = 'unknown'
        if 'HToWW' in SampleName: 
            DecayMode = 'H_WW'
        if 'HToZZ' in SampleName: 
            DecayMode = 'H_ZZ'
        if 'HToTauTau' in SampleName: 
            DecayMode = 'H_tautau'
        if 'HJetTobb' in SampleName or 'HJetToNonbb' in SampleName: 
            DecayMode = 'H_bb'
        if 'H0' in SampleName and '_ToWWTo2L2Nu' in SampleName: 
            DecayMode = 'H_WW'

        if not DecayMode == 'unknown':
            if float(HiggsMass) <= 130 and float(HiggsMass) >= 120:
                HiggsBR = self.GetHiggsBR(DecayMode, HiggsMass)
            else:
                HiggsBR = self.GetHiggsBR(DecayMode, HiggsMass, 'bsm')    
            if 'HJetToNonbb' in SampleName: 
                HiggsBR = 1.0 - HiggsBR

        HiggsXS['DecayMode'] = DecayMode
        HiggsXS['HiggsBR'] = HiggsBR
      
        # ... Final states
        FinalState = 'unknown'
        FinalStateBR = 1.

        if 'WWTo2L2Nu' in SampleName:  
            FinalState = 'WW->2l2v'
            FinalStateBR = self._br['W2lv'] * self._br['W2lv']
        if 'WWToLNuQQ' in SampleName or 'WWToNuQQ' in SampleName:  
            FinalState = 'WW->lvQQ'
            FinalStateBR = self._br['W2lv'] * self._br['W2QQ']
        if 'ZZTo4L' in SampleName:  
            FinalState = 'ZZ->4l'
            FinalStateBR = self._br['Z2ll'] * self._br['Z2ll']

        # ...... WH with W decays BR 
        if ProdMode == 'HWplus' or ProdMode == 'HWminus':
            if '_WToLNu_' in SampleName or '_LNu_' in SampleName: 
                FinalState += ' + W->lv'
                FinalStateBR *= self._br['W2lv']
            elif '_WToQQ_' in SampleName:  
                FinalState += ' + W->QQ'
                FinalStateBR *= self._br['W2QQ']
        # ...... ZH with Z decays BR
        if ProdMode == 'ZH' or ProdMode == 'ggZH':
            if '_ZTo2L_' in SampleName:
                FinalState += ' + Z->ll'
                FinalStateBR *= self._br['Z2ll'] 

        HiggsXS['FinalState'] = FinalState
        HiggsXS['FinalStateBR'] = FinalStateBR
        HiggsXS['xs'] = HiggsProdXS * HiggsBR * FinalStateBR    
        
        print(HiggsXS)
        return HiggsXS