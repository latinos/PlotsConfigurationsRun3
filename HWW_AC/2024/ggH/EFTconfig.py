
ana    = "anaGGF"
Build  = 1
MakeDC = 1
Check  = 0

####### Categories and Variables  ##############

tag    = "ggF_EFT"
cat    = ["hww_sr_01j", "topcr_01j", "dyttcr_01j"]
var    = [["mllVSmth2"], ["events"], ["events"]]  

######## EFT signals #############################
# Full EFT signal model built for SR only. Just H1 in CR (renamed T1 for sig model)
# Shape syst built just for H1(SM) and copied to other hypotheses 

prod    = ["ggF"]
pwg     = ["ggH_hww"]
hyps_mc = [["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05"]] 
rwgt    = ["4C1V"]

SF      = [1.17] # nomralistion SF 1.17?
scorr   = [0]    # SM JHU->PWG shape correction
BL      = [[]]   # Black list for reweighting e.g [("H0PH",4)]

sys     = ["CMS_res_j_2024", "CMS_scale_met_2024", "CMS_lepscale_2024", "CMS_lepres_2024", "CMS_btagSFbc_2024", "CMS_btagSFlight_2024", "CMS_btagSFbc_correlated", "CMS_btagSFlight_correlated", "CMS_eff_hwwtrigger_2024", "CMS_eff_e_2024", "CMS_eff_m_2024", "ps_isr", "ps_fsr", "QCDscale_ggH"]
jes     = "CMS_scale_j_"
sys    += [jes+"Absolute", jes+"Absolute_2024", jes+"BBEC1", jes+"BBEC1_2024", jes+"EC2", jes+"EC2_2024", jes+"FlavorQCD", jes+"HF", jes+"HF_2024", jes+"RelativeBal", jes+"RelativeSample_2024"]

sys_eft  = [sys]
sys_type = 1 # 0 (no EFT sys), 1 (SM only), 2 (All hyps)

###### Minor Signals (+ their systematics) to include  ####################
# Add and change name to T1 -> SM scaling in signal model

minorsig = ["qqH_hww", "WH_hww", "ZH_hww", "ggZH_hww" ]

##### Other processes (+ their systematics) to include ####################

other = ["DATA", "top", "DY", "WW", "ggWW", "VZ", "Vg", "VgS", "VVV", "Fake", "ggH_htt"]

####### configure Signal Check #################

pairs = [[["a2","a3"]]]
minS = 80 
maxS = 110 
maxN = 5000




 
 


