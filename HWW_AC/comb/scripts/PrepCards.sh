
cmsenv
ulimit -s unlimited

Ana_Dir=~/work/private/ACRun3/PlotsConfigurationsRun3/HWW_AC/2024

### categories

VBF=$Ana_Dir/VBF/anaVBF/datacards/hww_sr_2j/kd4d_vbf/datacard.txt
VH=$Ana_Dir/VH/anaVH/datacards/hww_sr_2jvh/kd3d_vh/datacard.txt 
DY2J=$Ana_Dir/VBF/anaVBF/datacards/dycr_2j/events/datacard.txt
Top2J=$Ana_Dir/VBF/anaVBF/datacards/topcr_2j/events/datacard.txt
WW2J=$Ana_Dir/VBF/anaVBF/datacards/wwcr_2j/events/datacard.txt

GGF=$Ana_Dir/ggH/anaGGF/datacards/hww_sr_01j/mllVSmth2/datacard.txt
DY01J=$Ana_Dir/ggH/anaGGF/datacards/dyttcr_01j/events/datacard.txt
Top01J=$Ana_Dir/ggH/anaGGF/datacards/topcr_01j/events/datacard.txt 

### combine categories

combineCards.py $VBF $VH $DY2J $Top2J $WW2J $GGF $DY01J $Top01J > cards/HVV.txt   

### workspace with CMSHistSum which constructs more optimised pdf to reduce memory + fitting time 

#text2workspace.py cards/HVV.txt -o cards/HVVciWB.root -P HiggsAnalysis.CombinedLimit.HWWSMEFTciWB:HWWSMEFTciWB --for-fits --no-wrappers --X-pack-asympows --optimize-simpdf-constraints=cms --use-histsum > cards/scalesWB.txt
text2workspace.py cards/HVV.txt -o cards/HVVciHB.root -P HiggsAnalysis.CombinedLimit.HWWSMEFTciHB:HWWSMEFTciHB --for-fits --no-wrappers --X-pack-asympows --optimize-simpdf-constraints=cms --use-histsum > cards/scalesHB.txt
text2workspace.py cards/HVV.txt -o cards/HVVFai.root -P HiggsAnalysis.CombinedLimit.HWWSMEFTFai:HWWSMEFTFai --for-fits --no-wrappers --X-pack-asympows --optimize-simpdf-constraints=cms --use-histsum > cards/scalesFai.txt


