from ROOT import *
from sys import argv

inputfile=argv[1]
moduleName=argv[2]
date=argv[3]


f=TFile(inputfile+"/highrate.root","OPEN") 
current=str()


############################highrate############################
for version in range(3):  
  version==0

  if version==0: current="0"+str(5)
  #if version==0: flux=str(40)
  elif version==1: current=str(10)
  #elif version==1: flux=str(80)
  else: current=str(15)
  #else: flux=str(120)
  #f1 = TFile('hrEff_'+flux.root)
  f1=TFile(inputfile+"hr"+str(current)+"ma_"+moduleName+"_"+date+".root","RECREATE")
  d1=f1.mkdir("HighRate")
  d1.cd()
  for i in range(16):
    i==0
    hr1=f.Get("HighRate/HR_Overall_Efficiency_C"+str(i)+"_V"+str(version))
    hr1.SetName("HR_Overall_Efficiency_C"+str(i)+"_V0")
    hr1.Write()
    hr2=f.Get("HighRate/HR_Fiducial_Efficiency_C"+str(i)+"_V"+str(version))
    hr2.SetName("HR_Fiducial_Efficiency_C"+str(i)+"_V0")
    hr2.Write()
    hr3=f.Get("HighRate/highRate_C"+str(i)+"_V"+str(version))
    hr3.SetName("highRate_C"+str(i)+"_V0")
    hr3.Write()
    hr4=f.Get("HighRate/highRate_xraymap_C"+str(i)+"_V"+str(version))
    hr4.SetName("highRate_xraymap_C"+str(i)+"_V0")
    hr4.Write()
  
                
  f1.Write()
  f1.Close()
f.Close()







