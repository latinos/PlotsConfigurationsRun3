from HiggsAnalysis.CombinedLimit.PhysicsModel import *

##-------------------------------------
##--------- Higgs HELCITY -------------
##-------------------------------------


class Higgshelicity(PhysicsModel):
    def __init__(self):
        self.isFraction = False
        self.isXsec = False
        self.isInt = False
        self.isIntXsec = False        
        self.includeWW = False
        self.includeWWSig = False
        self.doFullPolarization = False
        self.doOnlyPolarization = False
        self.doOnlySignal = False

        self.poiMap = []
        self.pois = {}
        self.verbose = False
        self.xsec= 1.0 

    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self,modelBuilder)
        self.modelBuilder.doModelBOnly = False
 
    def getYieldScale(self,bin,process):
        if process == "ggH_HWLWL": 
            return "ggH_LL_func"
        elif process == "ggH_HWTWT": 
            return "ggH_TT_func"
        elif process == "ggH_hww": 
            return "ggH_sbi_func"
        elif process == "ggH_HWW_Int": 
            return "ggH_Int_func"
        elif process == "ggWW": 
            return "ggToWW_bkg_func"
        elif process == "ggToWW": 
            return "ggToWW_sbi_func"
        elif process == "qqH_HWLWL": 
            return "ggH_LL_func"
        elif process == "qqH_HWTWT": 
            return "ggH_TT_func"
        elif process == "qqH_hww": 
            return "ggH_sbi_func"
        elif process =="WWewk": 
            return "ggToWW_bkg_func"
        elif process =="qqToWW": 
            return "ggToWW_sbi_func"

        #elif process in ["ggH","qqH","ttH","WH","ZH","VH"]: return "CMS_zz4l_mu"
        else:
            return 1
            

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po == "doFullPolarization":
                print("Will consider cards in [S1+S2+Int]+B+Int style with constraint in the xsec. Normalization!")
                self.doFullPolarization = True
            if po == "doOnlyPolarization":
                print("Will consider cards in [S1+S2+Int]+B+Int style with constraint in the xsec. Not normalization!")
                self.doOnlyPolarization = True
            if po == "doOnlySignal":
                print("Will consider cards in S+B+Int style with constraint in the xsec")
                self.doOnlySignal = True
                

    def setXsec(self):
        self.xsec = 1.32200
        self.xsec_LL = 1.3200  * 0.42967
        self.xsec_TT = 1.3200  * 0.3809
        self.xsec_Int = 1.3200 * 0.1893
        

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        if self.doFullPolarization:
            
            self.setXsec()

            self.modelBuilder.doVar("r[%s,%s,%s]" % (1.0, 0.05, 4.0))
            self.modelBuilder.doVar("r_LL[%s,%s,%s]" % (1.0, 0.05, 3.0))
            self.modelBuilder.doVar("r_TT[%s,%s,%s]" % (1.0, 0.05, 3.0))
            
            #self.modelBuilder.factory_( "expr::ggToWW_sbi_func(\"sqrt(@0)\", r)")
            #self.modelBuilder.factory_( "expr::ggH_sbi_func(\"(sqrt(@1*@2)*(@0-sqrt(@0)))\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggH_LL_func(\"(@0-sqrt(@0))*(@1-sqrt(@1*@2))\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggH_TT_func(\"(@0-sqrt(@0))*(@2-sqrt(@1*@2))\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggToWW_bkg_func(\"(1-sqrt(@0))\", r)")
            
            #self.modelBuilder.factory_( "expr::ggToWW_sbi_func(\"sqrt(@0)\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggH_sbi_func(\"(@0-sqrt(@0)*sqrt(@1*@2))\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggH_LL_func(\"(@1-sqrt(@1*@2))\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggH_TT_func(\"(@2-sqrt(@1*@2))\", r,r_LL,r_TT)")
            #self.modelBuilder.factory_( "expr::ggToWW_bkg_func(\"(1-sqrt(@0))\", r)")
            
            self.modelBuilder.factory_( "expr::ggToWW_sbi_func(\"sqrt(@0)\", r,r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_sbi_func(\"0.0*(@0-sqrt(@0)*sqrt(@1*@2))\", r,r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_LL_func(\"(@0-sqrt(@0))*(@1-sqrt(@1*@2))\", r,r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"(@0-sqrt(@0))*(@2-sqrt(@1*@2))\", r,r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggToWW_bkg_func(\"(1-sqrt(@0))\", r)")

            poi = "r,r_LL,r_TT"

        if self.doOnlyPolarization:

            self.setXsec()

            self.modelBuilder.doVar("r_LL[%s,%s,%s]" % (1.0, 0, 10.0))
            self.modelBuilder.doVar("r_TT[%s,%s,%s]" % (1.0, 0, 10.0))

            self.modelBuilder.factory_( "expr::ggToWW_sbi_func(\"sqrt(@1*@0)\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_sbi_func(\"0.0\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_LL_func(\"(@0-sqrt(@1*@0))\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"(@1-sqrt(@1*@0))\", r_LL,r_TT)")
            self.modelBuilder.factory_( "expr::ggToWW_bkg_func(\"(1-sqrt(@1*@0))\", r_LL,r_TT)")

            poi = "r_LL,r_TT"

        if self.doOnlySignal:
            
            self.setXsec()

            self.modelBuilder.doVar("r[%s,%s,%s]" % (1.0, 0.1, 2.0))

            self.modelBuilder.factory_( "expr::ggToWW_sbi_func(\"sqrt(@0)\", r)")
            self.modelBuilder.factory_( "expr::ggH_sbi_func(\"(@0-sqrt(@0))\", r)")
            self.modelBuilder.factory_( "expr::ggH_LL_func(\"0.0\", r)")
            self.modelBuilder.factory_( "expr::ggH_TT_func(\"0.0\", r)")
            self.modelBuilder.factory_( "expr::ggToWW_bkg_func(\"(1-sqrt(@0))\", r)")

            poi = "r"
        
            
        self.modelBuilder.doSet("POI",poi)
        

higgshelicity = Higgshelicity()
