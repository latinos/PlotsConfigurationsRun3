import numpy as np
n_bins = 4

cuts = {}


preselections = '1.'



cuts['incl'] = '1.'

cuts['fid'] = 'isFID==1'
cuts['nonfid'] = 'isFID==0'

cuts['fid_bin'] =  {
  'expr' : 'isFID==1',
  'categories' : {
      '_0' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
      '_1' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
      '_2' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
      '_3' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
  }

}

cuts['nonfid_bin'] =  {
  'expr' : 'isFID==0',
  'categories' : {
      '_0' : '(isFID == 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
      '_1' : '(isFID == 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
      '_2' : '(isFID == 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
      '_3' : '(isFID == 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
  }

}

