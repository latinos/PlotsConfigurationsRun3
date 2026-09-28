preselections = {}

# preselections['ALL'] = 'Lepton_pt[0][0]>25 \
#             && Lepton_pt[1][0]>20 \
#             && Lepton_pt[2][0]>15 \
#             && Lepton_pt[3][0]<10 \
#             && (WH3l_mOSll[0] < 0 || WH3l_mOSll[0] > 12) \
#             && (WH3l_mOSll[1] < 0 || WH3l_mOSll[1] > 12) \
#             && (WH3l_mOSll[2] < 0 || WH3l_mOSll[2] > 12) \
#             && abs(WH3l_chlll) == 1 \
#            '

preselections['ALL'] = 'Alt$( Lepton_pt[0], 0) > 25 \
            && Alt$( Lepton_pt[1], 0) > 20 \
            && Alt$( Lepton_pt[2], 0) > 15 \
            && Alt$( Lepton_pt[3], 0) < 10 \
            && (WH3l_mOSll[0] < 0 || WH3l_mOSll[0] > 12) \
            && (WH3l_mOSll[1] < 0 || WH3l_mOSll[1] > 12) \
            && (WH3l_mOSll[2] < 0 || WH3l_mOSll[2] > 12) \
            && abs(WH3l_chlll) == 1 \
           '