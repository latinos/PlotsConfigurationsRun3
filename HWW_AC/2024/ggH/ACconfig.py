

####### Categories and Variables  ##############

tag    = "ggF_AC"
cat    = ["hww_sr_01j"] 
var    = [["mllVSmth2"]] 

######## EFT signals #############################
# Full EFT signal model built for SR only. Just H1 in CR 
# Shape syst built just for H1(SM) and copied to other hypotheses 

prod    = ["ggF"]
pwg     = ["ggH_hww"]
hyps_mc = [["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05"]] 
rwgt    = [["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05"]]

SF      = [1.17] # nomralistion SF
scorr   = [0] # SM JHU->PWG shape correction
BL      = [[]] # Black list for reweighting e.g [("H0PH",4)]

minorsig = [] 




 
 


