from ROOT import *
from sys import argv

inputpath=argv[1]
moduleName=argv[2]
date=argv[3]

f=TFile(inputpath+"/highrate.root","OPEN") 

##########################Highrate##################################

f1=TFile(inputpath+"/dc15_"+moduleName+"_"+date+".root","RECREATE")  
#f1= TFile(inputpath+"/hrData_120.root","RECREATE")
d1=f1.mkdir("Xray")
d1.cd()
for i in range(16):
  i==0
  hr1=f.Get("Xray/hMap_DCHighRate_C"+str(i)+"_V0").Clone()
  hr1.Write()
  hr2=f.Get("Xray/q_DCHighRate_C"+str(i)+"_V0").Clone()
  hr2.Write()
  hr3=f.Get("Xray/ph_DCHighRate_C"+str(i)+"_V0").Clone()
  hr3.Write()
  hr4=f.Get("Xray/hitsVsEvents_DCHighRate_C"+str(i)+"_V0").Clone()
  hr4.Write()
  hr5=f.Get("Xray/hitsVsColumn_DCHighRate_C"+str(i)+"_V0").Clone()
  hr5.Write()
  hr6=f.Get("Xray/hitsVsEvtCol_DCHighRate_C"+str(i)+"_V0").Clone()
  hr6.Write()
  hr7=f.Get("Xray/qMap_DCHighRate_C"+str(i)+"_V0").Clone()
  hr7.Write()
  hr8=f.Get("Xray/phMap_DCHighRate_C"+str(i)+"_V0").Clone()
  hr8.Write()
hr9=f.Get("Xray/ntrig_DCHighRate_V0").Clone()
hr9.Write()

f1.Write()
f1.Close()

