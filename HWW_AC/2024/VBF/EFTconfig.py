
ana    = "anaVBF"
Build  = 1
MakeDC = 1
Check  = 0

####### Categories and Variables  ##############

tag    = "VBF_EFT"
cat    = ["hww_sr_2j", "dycr_2j", "topcr_2j", "wwcr_2j"] 
var    = [["kd4d_vbf"],["events"],["events"],["events"]]

#["kd_vbf","kd_hp","kd_hm","kd_hl","kd_hpzg","kd_hmzg","kd_hpgg","kd_hmgg","kd_mixhp","kd_mixhm","kd_mixhl","kd_mixhpzg","kd_mixhmzg","kd_mixhpgg","kd_mixhmgg"]]

######## EFT signals #############################
# Full EFT signal model built for SR only. Just H1 in CR (renamed T1 for sig model)
# Shape syst built just for SM and copied to other hypotheses

prod    = ["VBF"]
pwg     = ["qqH_hww"]
hyps_mc = [["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05", "H0LZgf05", "H0PHZgf05", "H0MZgf05", "H0PHggf05", "H0Mggf05"]]
rwgt    = ["8C2V"]

SF      = [1.02] # nomralistion SF
scorr   = [1]    # SM JHU->PWG shape correction
BL      = [[]]   # Black list for reweighting (hopefully never needed)

sys     = ["CMS_res_j_2024", "CMS_scale_met_2024", "CMS_lepscale_2024", "CMS_lepres_2024", "CMS_btagSFbc_2024", "CMS_btagSFlight_2024", "CMS_btagSFbc_correlated", "CMS_btagSFlight_correlated", "CMS_eff_hwwtrigger_2024", "CMS_eff_e_2024", "CMS_eff_m_2024", "ps_isr", "ps_fsr", "QCDscale_qqH"]
jes     = "CMS_scale_j_"
sys    += [jes+"Absolute", jes+"Absolute_2024", jes+"BBEC1", jes+"BBEC1_2024", jes+"EC2", jes+"EC2_2024", jes+"FlavorQCD", jes+"HF", jes+"HF_2024", jes+"RelativeBal", jes+"RelativeSample_2024"]

sys_eft  = [sys]
sys_type = 1 # 0 (no EFT sys), 1 (SM only), 2 (All hyps)

##### Minor Signals (+ their systematics) to include  ####################
# Add and change name to T1 -> SM scaling in signal model

minorsig = [ "ggH_hww", "WH_hww", "ZH_hww", "ggZH_hww" ]

##### Other processes (+ their systematics) to include ####################

other = [ "DATA", "top", "DY", "WW", "ggWW", "VZ", "Vg", "VgS", "VVV", "Fake" ] # "qqH_htt"

####### configure Signal Check #################

pairs = [[["a2","a3"], ["g2","g3"], ["z2","z3"]]] #, ["a2","k1"], ["a3","k1"]]
minS = 0
maxS = 25
maxN = 200





 
 


