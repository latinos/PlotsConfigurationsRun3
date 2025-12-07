

groupPlot = {}
plot = {}

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#



groupPlot['Fake']  = {
                  'nameHR' : 'nonprompt',
                  'isSignal' : 0,
                  'color': 921,    # kGray + 1
                  # 'samples'  : ['Fake_me', 'Fake_em']
                  'samples'  : ['Fake']
}



#plot = {}

# keys here must match keys in samples.py    
#  



plot['Fake']  = {
                  'color': 921,    # kGray + 1
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
              }



# additional options

legend = {}

legend['lumi'] = 'L = 41.5/fb'

legend['sqrt'] = '#sqrt{s} = 13 TeV'
