import ROOT
import CombineHarvester.CombineTools.ch as ch
import argparse
import os

def matching_proc(p,s):
  return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal()) 
         and (p.analysis()==s.analysis()) and  (p.era()==s.era()) 
         and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))
  
def drop_onesided_systs(syst):
  #same_yield = abs(syst.value_u() - 1)<0.05 and abs(syst.value_d() - 1)<0.05 and (syst.value_u()-1.)*(syst.value_d()-1.)>0 and syst.type() in 'shape'
  same_yield = (syst.value_u()-1.)*(syst.value_d()-1.)>0 and (syst.type() in 'shape' or syst.type() in 'lnN')
  if(same_yield):
    print ('Dropping one-sided systematic with small normalisation effect',syst.name(),' for region ', syst.bin(), ', process ', syst.process(), '. Up norm is ', syst.value_u() , ' and down norm is ', syst.value_d())
  return same_yield

#
def drop_zero_systs(syst):
  null_yield = abs(syst.value_u()-1)<1e-3 and abs(syst.value_d()-1)<1e-3 #5e-3
  if(null_yield):
    print ('Dropping systematic ',syst.name(),' for region ', syst.bin(), ', process ', syst.process(), '. Up norm is ', syst.value_u() , ' and down norm is ', syst.value_d())
  return null_yield

def drop_pdf_top(syst):
  drop = False
  if syst.name() in ["CMS_hww_pdf_top"]:
    print ('!!!!! Dropping CMS_hww_pdf_top systematic ',syst.name(),' for region ', syst.bin(), ', process ', syst.process(), '. Up norm is ', syst.value_u() , ' and down norm is ', syst.value_d())
    drop = True
  return drop

#
def small_shape_effect(histo_nom, syst, limit):
  #if (syst.process() in ['top', 'dytt'] or syst.signal()) and syst.type() in 'shape':
  small = False
  if syst.type() in 'shape':
    histo_u   = syst.shape_u()
    histo_d   = syst.shape_d()
    up_diff   = 0.
    down_diff = 0.
    for i in range(histo_nom.GetNbinsX()):
      if (abs(histo_u.GetBinContent(i+1) + histo_nom.GetBinContent(i+1))) > 0:
        up_diff += 2*(abs(histo_u.GetBinContent(i+1) - histo_nom.GetBinContent(i+1)))/(abs(histo_u.GetBinContent(i+1) + histo_nom.GetBinContent(i+1)))
      if (abs(histo_d.GetBinContent(i+1) + histo_nom.GetBinContent(i+1))) > 0:
        down_diff += 2*(abs(histo_d.GetBinContent(i+1) - histo_nom.GetBinContent(i+1)))/(abs(histo_d.GetBinContent(i+1) + histo_nom.GetBinContent(i+1)))
    if (up_diff < limit and down_diff < limit):
      small = True
      print ('Dropping systematic ',syst.name(),' with small shape effect for region ', syst.bin(), ', process ', syst.process(), '. Up diff is ', up_diff , ' and down diff is ', down_diff)
  return small
# 
def drop_small_shape_effect(chob, proc, limit):
  histo_n = proc.ShapeAsTH1F()
  # print(histo_n.Integral())
  # for i in range(histo_n.GetNbinsX()):
  #   print(histo_n.GetBinContent(i+1))
  if (histo_n.Integral()!=0):
    histo_n.Scale(1/histo_n.Integral())
  chob.FilterSysts(lambda x: small_shape_effect(histo_n, x, limit))



# def symmetrize_binbybin(proc, histo_nom, syst, limit,):
#   if not matching_proc(proc,syst): 
#         return 
#   # if syst.type() in 'shape' and ("fake_e_2018" in syst.name()):
#   if syst.type() in 'shape' and ("fake_m_201" in syst.name() or "fake_e_201" in syst.name()):
#     histo_u   = syst.shape_u() #questi sono normalizzati
#     histo_d   = syst.shape_d()
#     print("-------------------------")
#     print(str(syst.name())+" "+ str(proc.process()) + " " + str(proc.bin()) + " rate is " + str(proc.rate()))
#     for i in range(histo_nom.GetNbinsX()):
#       print(f"Before anything: histo_u[{i+1}] = {histo_u.GetBinContent(i+1)}, histo_d[{i+1}] = {histo_d.GetBinContent(i+1)}")
#       if (i+1 == 6): break
#     for i in range(histo_nom.GetNbinsX()):
#         nom = histo_nom.GetBinContent(i+1)
#         print(histo_nom.GetBinContent(i+1), histo_u.GetBinContent(i+1), histo_d.GetBinContent(i+1))
#         if ((proc.rate()!=0 and nom < (1.5/proc.rate())) and nom!=0) : #se nom è normalizzato devo dividere per histo_nom.Integral() qui
#         # if (proc.rate()!=0 and nom!=0) : 
#             delta_up = (histo_u.GetBinContent(i+1)/histo_nom.GetBinContent(i+1))-1
#             delta_do = (histo_d.GetBinContent(i+1)/histo_nom.GetBinContent(i+1))-1
#             delta = 0
#             print("DeltaUp variation is " + str(delta_up)) 
#             print("DeltaDo variation is " + str(delta_do))
#             if (abs(abs(delta_up) - abs(delta_do)) > 0):
#                 print("bin " + str(i+1)+ " content is " + str(nom) + " in category " + proc.bin() + " for process " + proc.process() + " with rate "+ str(proc.rate()))
#                 print("Up/Do variation is " + str(abs(abs(delta_up) - abs(delta_do))) + " for syst " + syst.name())
#                 print("up is " + str(histo_u.GetBinContent(i+1)) )
#                 print("down is " + str(histo_d.GetBinContent(i+1)) )
#                 if abs(delta_up) >= abs(delta_do):
#                   delta = delta_up
#                   print("Delta is " + str(delta))
#                   print("Up is the biggest variation, setting Do to "+ str(histo_nom.GetBinContent(i+1)*(1-delta)))
#                   histo_d.SetBinContent(i+1, histo_nom.GetBinContent(i+1)*(1-delta))
#                   if (histo_nom.GetBinContent(i+1)*(1-delta) < 0): histo_d.SetBinContent(i+1, 0.0)
#                 else:
#                   delta = delta_do
#                   print("Delta is " + str(delta))
#                   print("Do is the biggest variation, setting Up to "+ str(histo_nom.GetBinContent(i+1)*(1-delta)))
#                   histo_u.SetBinContent(i+1, histo_nom.GetBinContent(i+1)*(1-delta))
#                   if (histo_nom.GetBinContent(i+1)*(1-delta)<0): histo_u.SetBinContent(i+1, 0.0)
#                 print( "up reset to " + str(histo_u.GetBinContent(i+1)) )
#                 print( "down reset to " + str(histo_d.GetBinContent(i+1)) )
#                 print( " ---------------------- ") 
#         else : 
#           print("nothing to change") 
#           # histo_d.SetBinContent(i+1, histo_d.GetBinContent(i+1))
#           # histo_u.SetBinContent(i+1, histo_u.GetBinContent(i+1))
#           print( " ---------------------- ") 

#     for i in range(histo_nom.GetNbinsX()):
#       print(f"Before set_shapes: histo_u[{i+1}] = {histo_u.GetBinContent(i+1)}, histo_d[{i+1}] = {histo_d.GetBinContent(i+1)}")
#       if (i+1 == 6): break

#     # syst.set_shapes(histo_u, histo_d, histo_nom)

        
def symmetrize_binbybin(proc, histo_nom, syst, limit,):
  if not matching_proc(proc,syst): 
        return 
  # if syst.type() in 'shape' and ("fake_e_2018" in syst.name()):
  if syst.type() in 'shape' and ("fake_m_201" in syst.name() or "fake_e_201" in syst.name()):
    histo_u   = syst.shape_u() #questi sono normalizzati
    histo_d   = syst.shape_d()
    print("-------------------------")
    print(str(syst.name())+" "+ str(proc.process()) + " " + str(proc.bin()) + " rate is " + str(proc.rate()))
    for i in range(histo_nom.GetNbinsX()):
        nom = histo_nom.GetBinContent(i+1)
        print(histo_nom.GetBinContent(i+1), histo_u.GetBinContent(i+1), histo_d.GetBinContent(i+1))
        if (proc.rate()!=0 and nom!=0) : #se nom è normalizzato devo dividere per histo_nom.Integral() qui
        # if (proc.rate()!=0 and nom!=0) : 
            delta_up = ((histo_u.GetBinContent(i+1)*syst.value_u()*proc.rate())/(histo_nom.GetBinContent(i+1)*proc.rate()))-1
            delta_do = ((histo_d.GetBinContent(i+1)*syst.value_d()*proc.rate())/(histo_nom.GetBinContent(i+1)*proc.rate()))-1
            delta = 0
            print("DeltaUp variation is " + str(delta_up)) 
            print("DeltaDo variation is " + str(delta_do))
            if (abs(abs(delta_up) - abs(delta_do)) > 0):
                print("bin " + str(i+1)+ " content is " + str(nom*proc.rate()) + " in category " + proc.bin() + " for process " + proc.process() + " with rate "+ str(proc.rate()))
                print("Up/Do variation is " + str(abs(abs(delta_up) - abs(delta_do))) + " for syst " + syst.name())
                print("up is " + str(histo_u.GetBinContent(i+1)*syst.value_u()*proc.rate()) )
                print("down is " + str(histo_d.GetBinContent(i+1)*syst.value_d()*proc.rate()) )
                if abs(delta_up) >= abs(delta_do):
                  delta = delta_up
                  print("Delta is " + str(delta))
                  print("Up is the biggest variation, setting Do to "+ str((histo_nom.GetBinContent(i+1)*proc.rate())*(1-delta)))
                  histo_d.SetBinContent(i+1, (histo_nom.GetBinContent(i+1)*proc.rate())*(1-delta)/(syst.value_d()*proc.rate()))
                  if (histo_nom.GetBinContent(i+1)*(1-delta) < 0): histo_d.SetBinContent(i+1, 0.0)
                else:
                  delta = delta_do
                  print("Delta is " + str(delta))
                  print("Do is the biggest variation, setting Up to "+ str((histo_nom.GetBinContent(i+1)*proc.rate())*(1-delta)))
                  histo_u.SetBinContent(i+1, (histo_nom.GetBinContent(i+1)*proc.rate())*(1-delta)/(syst.value_u()*proc.rate()))
                  if (histo_nom.GetBinContent(i+1)*(1-delta)<0): histo_u.SetBinContent(i+1, 0.0)
                print( "up reset to " + str(histo_u.GetBinContent(i+1)) )
                print( "down reset to " + str(histo_d.GetBinContent(i+1)) )
                print( " ---------------------- ") 
        else : 
          print("nothing to change") 
          # histo_d.SetBinContent(i+1, histo_d.GetBinContent(i+1))
          # histo_u.SetBinContent(i+1, histo_u.GetBinContent(i+1))
          print( " ---------------------- ") 

    for i in range(histo_nom.GetNbinsX()):
      print(f"Before set_shapes: histo_u[{i+1}] = {histo_u.GetBinContent(i+1)}, histo_d[{i+1}] = {histo_d.GetBinContent(i+1)}")
      if (i+1 == 6): break


def symmetrize_small_stat_process(chob, proc, limit):
  histo_n = proc.ShapeAsTH1F()
  chob.ForEachSyst(lambda x: symmetrize_binbybin(proc, histo_n, x, limit))

# 
def drop_small_procs(chob,proc):
  null_yield = (proc.rate() < 0.01 and "_GenDeltaPhijj_" not in proc.process())
  if(null_yield):
    print('Dropping process ' + proc.process() + " in region "+ proc.bin() + ", yield is " + str(proc.rate()) )
    chob.FilterSysts(lambda sys: matching_proc(proc,sys))
  return null_yield

def transform_to_sym_lnN(syst):
    if syst.type() in 'lnN' and (abs(syst.value_u()-1)<1e-5 or abs(syst.value_d()-1)<1e-5 ):
        if (abs(syst.value_u()-1)>abs(syst.value_d()-1)):
            syst.set_asymm(False)
            if syst.value_u()>1:
                syst.set_value_u(syst.value_u())
                syst.set_value_d(syst.value_u())
            else:
                syst.set_value_u(1/syst.value_u())
                syst.set_value_d(1/syst.value_u())
        else:
            syst.set_asymm(False)
            if syst.value_d()>1:
                syst.set_value_u(syst.value_d())
                syst.set_value_d(syst.value_d())
            else:
                syst.set_value_u(1/syst.value_d())
                syst.set_value_d(1/syst.value_d())
        

def transform_to_ln(syst):
    # if syst.type() in 'shape' and ('_TOP_' in syst.bin() or '_dytt_' in syst.bin()):
    if syst.type() in 'shape' and ('CR_' in syst.bin() or '_dytt_' in syst.bin() or '_top_' in syst.bin()):
        syst.set_type("lnN")
        print("Trasforming systematics " +syst.name() + "to ln: " )
        print(syst.value_u())
        print(syst.value_d())
        if (syst.value_u()==0 and syst.value_d() != 0) : 
            syst.set_value_u(1/syst.value_d())
        elif (syst.value_d()==0 and syst.value_u() != 0) : 
            syst.set_value_d(1/syst.value_u())
        else:
            syst.set_value_u(syst.value_u())
            syst.set_value_d(syst.value_d())
        print(syst.value_u())
        print(syst.value_d())

def transform_to_ln_fake(syst):
    if syst.type() in 'shape' and ('fake_e_201' in syst.name() or 'fake_m_201' in syst.name()):
        syst.set_type("lnN")
        print("FAKE::: Trasforming " + syst.name() + " systematics " +syst.name() + "to ln: " )
        print(syst.value_u())
        print(syst.value_d())
        if (syst.value_u()==0 and syst.value_d() != 0) : 
            syst.set_value_u(1/syst.value_d())
        elif (syst.value_d()==0 and syst.value_u() != 0) : 
            syst.set_value_d(1/syst.value_u())
        else:
            syst.set_value_u(syst.value_u())
            syst.set_value_d(syst.value_d())
        print(syst.value_u())
        print(syst.value_d())
        
def fixBug_shape_syst(syst, factor):
    # applies only for WW and top PDF uncrty 
    # if syst is shape or lnN it reduces variation by multiplicative factor
    for _syst in ["CMS_hww_pdf_WW","CMS_hww_pdf_top"]:
        if _syst in syst.name():
            if syst.type() in "shape": 
                print("Bugfix of "+syst.name()+" in region " + syst.bin() +": "+syst.type()+" "+str(syst.scale())+"-->"+str(syst.scale()/factor))
                syst.set_scale(syst.scale()/factor)
            elif syst.type() in "lnN":
                new_u = 1.+(syst.value_u()-1.)*factor
                new_d = 1.+(syst.value_d()-1.)*factor
                # new_d = 1./(1.+abs(syst.value_d()-1.)*factor)
                print("Bugfix of "+syst.name()+" in region " + syst.bin() +": "+syst.type()+" "+str(syst.value_u())+"/"+str(syst.value_d())+"-->"+str(new_u)+"/"+str(new_d))
                syst.set_value_u(new_u)
                syst.set_value_d(new_d)

def symmmetrize_onesided_for_small_processes(chob,syst,cut,cap):
    # only applies for small yields
    chob.ForEachProc(lambda x: symmmetrize_onesided(x, syst, cut, cap))

def symmmetrize_onesided(proc,syst,cut,cap):
    # if lnN normalization is onesided change it for symmetrized
 
    if not matching_proc(proc,syst): 
        return 0
    if syst.type() in 'lnN' and proc.rate() < cut:
        isOnesided = (syst.value_u()-1.)*(syst.value_d()-1.)>0 and syst.asymm()
        if isOnesided:
            new = 0.
            if (abs(syst.value_u()-1)>abs(syst.value_d()-1)):
                if syst.value_u()>1:
                    new = syst.value_u()
                else:
                    new = 1/syst.value_u()
            else:
                if syst.value_d()>1:
                    new = syst.value_d()
                else:
                    new = 1/syst.value_d()
            print("Symmetrize "+syst.name()+" for low-stat process "+syst.process()+"="+str(proc.rate())+" in bin "+proc.bin()+": "+syst.type()+" "+str(syst.value_u())+"/"+str(syst.value_d())+"-->"+str(new))
            syst.set_asymm(False)
            syst.set_value_u(new)
            syst.set_value_d(new)
    if syst.type() in 'lnN' and proc.rate() < cut*10. and cap is not None:
        if not syst.asymm() and (((abs(syst.value_u())>0) and (abs(syst.value_u()-1)>abs(cap-1))) or ((abs(syst.value_d())>0) and (abs(syst.value_d()-1)>abs(cap-1)))):
            new = cap
            print("WARNING "+syst.name()+" for low-stat process "+syst.process()+"="+str(proc.rate())+" in bin "+proc.bin()+": "+syst.type()+" detected with abnormal normalisation "+str(syst.value_u())+" "+str(syst.value_d())+" RESET to "+str(new))
            syst.set_asymm(False)
            syst.set_value_u(new)
            syst.set_value_d(new)

def cap_large_norm_for_all_processes(chob, syst, cut, cap):
    # cap variation for all processes for a given lnN systematic
    chob.ForEachProc(lambda x: cap_large_norm(x, syst, cut, cap))

def cap_large_norm(proc, syst, cut, cap):
    # cap variation for the selected lnN systematic
    if not matching_proc(proc,syst): 
        return 0
    if syst.type() in 'lnN' and proc.rate() < cut:
        up = syst.value_u()
        delta_up = abs(1-up)
        do = syst.value_d()
        delta_do = abs(1-do) 

        if (delta_up > cap and up != 0 ) :
            print("WARNING2 "+syst.name()+" for low-stat process "+syst.process()+"="+str(proc.rate())+" in bin "+proc.bin()+": "+syst.type()+" detected with abnormal normalisation "+str(up)+" RESET to "+str(1+cap)  + " UP " )
            syst.set_value_u(1+cap)
        if (delta_do > cap and do != 0):
            print("WARNING3 "+syst.name()+" for low-stat process "+syst.process()+"="+str(proc.rate())+" in bin "+proc.bin()+": "+syst.type()+" detected with abnormal normalisation "+str(do)+" RESET to "+str(1-cap)  + " DOWN")
            syst.set_value_d(1-cap)   

# def remove_illdefined_for_small_processes(chob,syst,cut,cap):
#     # only applies for small yields
#     chob.ForEachProc(lambda x: remove_illdefined(x, syst, cut, cap))

# def remove_illdefined(proc,syst,cut,cap):
#     # if normalization is abnormally large for the small stat process
    
#     if not matching_proc(proc,syst):
#         return 0
#     if syst.type() in 'lnN' and proc.rate() < cut*10.:
#         if not syst.asymm() and (((abs(syst.value_u())>0) and (abs(syst.value_u()-1)>0.2)) or ((abs(syst.value_d())>0) and (abs(syst.value_d()-1)>0.2))):
#             #new = cap
#             print("WARNING "+syst.name()+" for low-stat process "+syst.process()+"="+str(proc.rate())+" in bin "+proc.bin()+": "+syst.type()+" detected with abnormal normalisation "+str(syst.value_u())+" "+str(syst.value_d())+" RESET to "+str(new))
#             #syst.set_asymm(False)
#             #syst.set_value_u(new)
#             #syst.set_value_d(new)
#             return 1
#     return 0    

parser = argparse.ArgumentParser()

parser.add_argument('--inputFile', '-i', default='datacards.txt',
                    help='Specifies the name of the datacards to sanitize')

args = parser.parse_args()


ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit') 
cb = ch.CombineHarvester() 
cb.SetFlag('workspaces-use-clone', True) 
cb.SetFlag('filters-use-regex', True) 
cb.SetFlag("check-negative-bins-on-import",1) 
cb.SetFlag("zero-negative-bins-on-import", 1) 
cb.SetVerbosity(0)


cb.ParseDatacard(args.inputFile, analysis='benedetta')


cb.FilterProcs(lambda x: drop_small_procs(cb,x)) #1e-2 except for signal process
cb.cp().ForEachSyst(lambda x: transform_to_ln(x))
# cb.cp().ForEachSyst(lambda x: transform_to_ln_fake(x))  
cb.cp().ForEachSyst(lambda x: fixBug_shape_syst(x,10))
cb.FilterSysts(lambda x: drop_zero_systs(x)) #1e-3
cb.FilterSysts(lambda x: drop_pdf_top(x)) 
cb.ForEachProc(lambda x: drop_small_shape_effect(cb, x, 0.001))
cb.cp().ForEachSyst(lambda x: transform_to_sym_lnN(x)) # se una delle due variazioni è < 1e-5
cb.cp().ForEachSyst(lambda x: symmmetrize_onesided_for_small_processes(cb,x,0.015,1.1)) 
# cb.cp().ForEachSyst(lambda x: cap_large_norm_for_all_processes(cb, x, 0.7, 0.1) if ("CMS_scale_JESAbsolute_2017" in x.name()) else False)
cb.ForEachProc(lambda x: symmetrize_small_stat_process(cb, x, 0.12))


# cb.FilterSysts(lambda x: drop_onesided_systs(x)) #indipendentemente dalla grandezza

if not os.path.exists('shapes'):
    os.makedirs('shapes')


output_file = f'shapes/{args.inputFile}'.replace('.txt', '_sanitized.root')

outf = ROOT.TFile(output_file, 'recreate')
cb.WriteDatacard(f'{args.inputFile}'.replace('.txt', '_sanitized.txt'), outf)
outf.Close()

