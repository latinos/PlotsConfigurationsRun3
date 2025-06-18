from HiggsAnalysis.CombinedLimit.PhysicsModel import *

##-------------------------------------
##--------- Higgs HELCITY -------------
##-------------------------------------


class HiggsHelicity(PhysicsModel):
    def __init__(self):
        self.doGGFxs = False
        self.doVBFxs = False
        self.doHWWxs = False
        self.doPolarization = False
        self.doFraction = False

        self.bkg_plus_int = False
        self.bkg_only = False
        
        self.poiMap = []
        self.pois = {}
        self.verbose = False
        self.xsec= 1.0 

    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self,modelBuilder)
        self.modelBuilder.doModelBOnly = False
 
    def getYieldScale(self,bin,process):
        
        if process == "ggH_HWLWL":   return "ggH_LL_func"      #### Gluon fusion processes 
        elif process == "ggH_HWTWT": return "ggH_TT_func"
        elif process == "ggH_hww":   return "ggH_sonly_func"
        elif process == "ggWW_si":
            self.bkg_plus_int = True
            return "ggH_bi_func"

        elif process == "ggWW":
            self.bkg_only = True
            return "ggH_bkg_func"

        elif process == "ggToWW":    return "ggH_sbi_func"

        elif process == "qqH_HWLWL":  return "qqH_LL_func"     ### Vector boson fusion   
        elif process == "qqH_HWTWT":  return "qqH_TT_func"
        elif process == "qqH_hww":    return "qqH_sonly_func"
        elif process == "WWewk_si":   return "qqH_bi_func"
        elif process == "WWewk":      return "qqH_bkg_func"
        elif process == "qqToWW":     return "qqH_sbi_func"

        else:
            return 1
            

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po == "mu_ggf":
                print ("Will consider ggF only and float the cross-section signal strength")
                self.doGGFxs = True
            if po == "mu_vbf":
                print ("Will consider VBF only and float the cross-section signal strength")
                self.doVBFxs = True
            if po == "mu_hww":
                print ("Will consider all the HWW only and float the cross-section signal strength")
                self.doHWWxs = True
            if po == "Polarization":
                print ("Will consider polarization and flot mu_LL and mu_TT")
                self.doPolarization = True
            if po == "Fraction":
                print ("Will consider polarization and float the fraction")
                self.doFraction = True
            

    def setXsec(self):
        self.xsec = 1.32200
        self.xsec_LL = 1.3200  * 0.42967
        self.xsec_TT = 1.3200  * 0.3809
        self.xsec_Int = 1.3200 * 0.1893
        

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        if self.doGGFxs:

            self.modelBuilder.doVar("mu[%s,%s,%s]" % (1.0, 0, 10.0))
            
            self.modelBuilder.factory_( "expr::ggH_sbi_func(\"sqrt(@0)\", mu)")
            self.modelBuilder.factory_( "expr::ggH_sonly_func(\"@0-sqrt(@0)\", mu)") 
            self.modelBuilder.factory_( "expr::ggH_bkg_func(\"(1-sqrt(@0))\", mu)")

            self.modelBuilder.factory_( "expr::ggH_LL_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::qqH_LL_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::qqH_TT_func(\"0.0\", mu)")

            if self.bkg_plus_int:
                self.modelBuilder.factory_( "expr::ggH_bi_func(\"0.0\", mu)")
                self.modelBuilder.factory_( "expr::qqH_bi_func(\"0.0\", mu)")

            self.modelBuilder.factory_( "expr::qqH_sonly_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::qqH_bkg_func(\"0.0\", mu)")

            poi = "mu"

        if self.doVBFxs:

            self.modelBuilder.doVar("mu[%s,%s,%s]" % (1.0, 0, 10.0))

            self.modelBuilder.factory_( "expr::qqH_sbi_func(\"sqrt(@0)\", mu)")
            self.modelBuilder.factory_( "expr::qqH_sonly_func(\"@0-sqrt(@0)\", mu)")
            self.modelBuilder.factory_( "expr::qqH_bkg_func(\"(1-sqrt(@0))\", mu)")

            self.modelBuilder.factory_( "expr::ggH_LL_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::qqH_LL_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::qqH_TT_func(\"0.0\", mu)")

            if self.bkg_plus_int:
                self.modelBuilder.factory_( "expr::ggH_bi_func(\"0.0\", mu)")
                self.modelBuilder.factory_( "expr::qqH_bi_func(\"0.0\", mu)")

            self.modelBuilder.factory_( "expr::ggH_sonly_func(\"0.0\", mu)")
            self.modelBuilder.factory_( "expr::ggH_bkg_func(\"0.0\", mu)")

            poi = "mu"
            
        if self.doPolarization:

            self.modelBuilder.doVar("r_LL[%s,%s,%s]" % (1.0, 0, 10.0))
            self.modelBuilder.doVar("r_TT[%s,%s,%s]" % (1.0, 0, 10.0))

            self.modelBuilder.factory_( "expr::ggH_sbi_func(\"sqrt(@1*@0)\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_LL_func(\"(@0-sqrt(@1*@0))\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"(@1-sqrt(@1*@0))\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_bi_func(\"(1-sqrt(@1*@0))\", r_LL,r_TT)")

            self.modelBuilder.factory_( "expr::qqH_sbi_func(\"sqrt(@1*@0)\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::qqH_LL_func(\"(@0-sqrt(@1*@0))\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::qqH_TT_func(\"(@1-sqrt(@1*@0))\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::qqH_bi_func(\"(1-sqrt(@1*@0))\", r_LL,r_TT)")

            self.modelBuilder.factory_( "expr::ggH_sonly_func(\"0.0\", r_LL,r_TT)")                ### Fix to zero
            self.modelBuilder.factory_( "expr::qqH_sonly_func(\"0.0\", r_LL,r_TT)")                ### Fix to zero 
            if self.bkg_only:
                self.modelBuilder.factory_( "expr::ggH_bkg_func(\"0.0\", r_LL)")
                self.modelBuilder.factory_( "expr::qqH_bkg_func(\"0.0\", r_LL)")

            poi = "r_LL,r_TT"

        
        if self.doFraction:
            
            self.modelBuilder.doVar("r[%s,%s,%s]" % (1.0, 0, 10.0))  ## sqrt(mu_ll / mu_tt)
            self.modelBuilder.doVar("mu[%s,%s,%s]" % (1.0, 0, 10.0)) ## auxiliary mu_TT

            self.modelBuilder.out.var("mu").setVal(1)
            self.modelBuilder.out.var("mu").setConstant(False)
            self.modelBuilder.out.var("mu").setAttribute("flatParam")

            #### r = SQRT(mu_ll/mu_tt)
            
            self.modelBuilder.factory_( "expr::ggH_sbi_func(\"@0*@1\",                r,mu)")
            self.modelBuilder.factory_( "expr::ggH_LL_func(\"(@0*@0*@1 - @0*@1)\",    r,mu)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"(@1 - @0*@1)\",          r,mu)")
            self.modelBuilder.factory_( "expr::ggH_bi_func(\"(1 - @0*@1)\",           r,mu)")
            #
            self.modelBuilder.factory_( "expr::qqH_sbi_func(\"@0*@1\",                r,mu)")
            self.modelBuilder.factory_( "expr::qqH_LL_func(\"(@0*@0*@1 - @0*@1)\",    r,mu)")
            self.modelBuilder.factory_( "expr::qqH_TT_func(\"(@1 - @0*@1)\",          r,mu)")
            self.modelBuilder.factory_( "expr::qqH_bi_func(\"(1 - @0*@1)\",           r,mu)")

            self.modelBuilder.factory_( "expr::ggH_sonly_func(\"0.0\",       r,mu)")                ### Fix to zero
            self.modelBuilder.factory_( "expr::qqH_sonly_func(\"0.0\",       r,mu)")                ### Fix to zero
            if self.bkg_only:
                self.modelBuilder.factory_( "expr::ggH_bkg_func(\"0.0\", mu)")
                self.modelBuilder.factory_( "expr::qqH_bkg_func(\"0.0\", mu)")

            poi = "r"
            
            
        self.modelBuilder.doSet("POI",poi)
        

higgshelicity = Higgshelicity()
