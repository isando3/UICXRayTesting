from ROOT import *
from sys import argv

inputpath=argv[1]
moduleName=argv[2]
date=argv[3]

f=TFile(inputpath+"/highrate.root","OPEN") 

##########################Highrate##################################

f1=TFile(inputpath+"/dc05_"+moduleName+"_"+date+".root","RECREATE")  
#f1= TFile(inputpath+"/hrData_40.root","RECREATE")
d1=f1.mkdir("Xray")
d1.cd()
for i in range(16):
  i==0
  hr1=f.Get("Xray/hMap_DCLowRate_C"+str(i)+"_V0").Clone()
  hr1.Write()
  hr2=f.Get("Xray/q_DCLowRate_C"+str(i)+"_V0").Clone()
  hr2.Write()
  hr3=f.Get("Xray/ph_DCLowRate_C"+str(i)+"_V0").Clone()
  hr3.Write()
  hr4=f.Get("Xray/hitsVsEvents_DCLowRate_C"+str(i)+"_V0").Clone()
  hr4.Write()
  hr5=f.Get("Xray/hitsVsColumn_DCLowRate_C"+str(i)+"_V0").Clone()
  hr5.Write()
  hr6=f.Get("Xray/hitsVsEvtCol_DCLowRate_C"+str(i)+"_V0").Clone()
  hr6.Write()
  hr7=f.Get("Xray/qMap_DCLowRate_C"+str(i)+"_V0").Clone()
  hr7.Write()
  hr8=f.Get("Xray/phMap_DCLowRate_C"+str(i)+"_V0").Clone()
  hr8.Write()
hr9=f.Get("Xray/ntrig_DCLowRate_V0").Clone()
hr9.Write()

f1.Write()
f1.Close()



