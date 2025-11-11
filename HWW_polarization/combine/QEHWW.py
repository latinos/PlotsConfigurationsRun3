from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.PhysicsModel import  CanTurnOffBkgModel, MultiSignalModel, PhysicsModelBase_NiceSubclasses


##-------------------------------------
##--------- Higgs QEHWW -------------
##-------------------------------------


class QEHWW(PhysicsModel):
    def __init__(self):
        self.poiMap = []
        self.pois = {}
        self.verbose = False
        self.xsec= 1.0
        self.fL = "0p6"
        self.fP = "0p0"
        self.txt = "fL_0p6_fPerp_0p0"

        self.doInterference = False
        self.txt_plus = ""
        self.txt_minus = ""
        
        # fL_0p6_fPerp_0p0
        # ggH_fL_1p0_fPerp_0p0
        
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self,modelBuilder)
        self.modelBuilder.doModelBOnly = False
 
    def getYieldScale(self,bin,process):
        
        if "ggH_fL" in process:
            if not self.doInterference:
                # One signal defined by self.txt
                if self.txt not in process:
                    return "dummy"
                else:
                    return "ggH_HYP"
            else:
                # Two signals needed -> [ +fL , -fL ]
                if self.txt_plus in process:
                    return "ggH_HYP_plus"
                elif self.txt_minus in process:
                    return "ggH_HYP_minus"
                
                
        if "qqH_fL" in process:
            if not self.doInterference:
                # One signal defined by self.txt
                if self.txt not in process:
                    return "dummy"
                else:
                    return "qqH_HYP"
            else:
                # Two signals needed -> [ +fL , -fL ]
                if self.txt_plus in process:
                    return "qqH_HYP_plus"
                elif self.txt_minus in process:
                    return "qqH_HYP_minus"
            
        
        if process == "ggH_hww":   return "ggH_0PM"
        elif process == "qqH_hww":   return "qqH_0PM"
        elif process == "ggH_HWLWL": return "dummy"
        elif process ==	"qqH_HWLWL": return "dummy"
        elif process ==	"ggH_HWTWT": return "dummy"
        elif process == "qqH_HWTWT": return "dummy"
        elif process == "ggH_perp": return "dummy"
        elif process == "qqH_perp": return "dummy"
        elif process == "ggToWW": return "dummy"
        elif process == "qqToWW": return "dummy"
        else:
            return 1


    def processPhysicsOptions(self, physOptions):
        processed = ["r"]
        processed += super(self).processPhysicsOptions(physOptions)
        return processed

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if "fL" in po:
                self.fL = po.split("fL_")[1]
            elif "fPerp" in po:
                self.fP = po.split("fPerp_")[1]

            if "doMatrix" in po:
                self.doInterference = True

        self.txt = f"fL_{self.fL}_fPerp_{self.fP}"
        
        # two signals needed
        # Assume self.txt has fL > 0
        if self.doInterference:
            print("[INTERFERENCE MODE] Scan over fL and Cll")            
            self.txt_plus = self.txt
            if self.fL == "0p0":
                self.txt_minus = f"fL_{self.fL}_fPerp_{self.fP}"
            else:
                self.txt_minus = f"fL_m{self.fL}_fPerp_{self.fP}"

            print(self.txt_plus)
            print(self.txt_minus)
        else:
            print(self.txt)
                
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        if not self.doInterference:
        
            self.modelBuilder.doVar("r[1.0, 0, 1]")
            # self.modelBuilder.out.var("r").setConstant(False)
            # self.modelBuilder.out.var("r").setAttribute("flatParam")
            
            # self.modelBuilder.doVar(f'expr::ggH_0PM("@0",fL)')
            # self.modelBuilder.doVar(f'expr::qqH_0PM("@0",fL)')
            #
            # self.modelBuilder.doVar(f'expr::ggH_HYP("(1 - @0)",fL)')
            # self.modelBuilder.doVar(f'expr::qqH_HYP("(1 - @0)",fL)')
            
            self.modelBuilder.doVar("mu[1.0, 0, 2]")
            self.modelBuilder.out.var("mu").setConstant(False)
            self.modelBuilder.out.var("mu").setAttribute("flatParam")        
            
            self.modelBuilder.doVar(f'expr::ggH_0PM("(@0)*@1",r,mu)')
            self.modelBuilder.doVar(f'expr::qqH_0PM("(@0)*@1",r,mu)')
            
            self.modelBuilder.doVar(f'expr::ggH_HYP("(1 - @0)*@1",r,mu)')
            self.modelBuilder.doVar(f'expr::qqH_HYP("(1 - @0)*@1",r,mu)')
            
            self.modelBuilder.doVar(f'expr::dummy("0.0",mu)')
            
            poi = "r"                        
            self.modelBuilder.doSet("POI",poi)
            
        else:

            self.modelBuilder.doVar("r[1.0, 0, 1]")
            self.modelBuilder.doVar("cll[0.91, -1, 1]")

            self.modelBuilder.doVar("mu[1.0, 0, 2]")
            self.modelBuilder.out.var("mu").setConstant(False)
            self.modelBuilder.out.var("mu").setAttribute("flatParam")

            self.modelBuilder.doVar(f'expr::ggH_0PM("(@0)*@1",r,mu)')
            self.modelBuilder.doVar(f'expr::qqH_0PM("(@0)*@1",r,mu)')

            self.modelBuilder.doVar(f'expr::ggH_HYP_plus("(1 - @0) * @1 * (abs(1+@2)/2.0)",r,mu,cll)')
            self.modelBuilder.doVar(f'expr::qqH_HYP_plus("(1 - @0) * @1 * (abs(1+@2)/2.0)",r,mu,cll)')

            self.modelBuilder.doVar(f'expr::ggH_HYP_minus("(1 - @0) * @1 * (abs(1-@2)/2.0)",r,mu,cll)')
            self.modelBuilder.doVar(f'expr::qqH_HYP_minus("(1 - @0) * @1 * (abs(1-@2)/2.0)",r,mu,cll)')

            self.modelBuilder.doVar(f'expr::dummy("0.0",mu)')

            poi = "r,cll"
            self.modelBuilder.doSet("POI",poi)
            
        

QEHWW = QEHWW()
