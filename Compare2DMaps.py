import sys 
import glob
import re
import os
from array import *
from ROOT import *
import time

hrfile = TFile(sys.argv[1])
print hrfile
bbfile = TFile(sys.argv[2])
print bbfile
#hr_h = hrfile.Get(sys.argv[2])
#print hr_h
#bb_h = bbfile.Get(sys.argv[4])
#print bb_h
outfile = TFile(sys.argv[3],'recreate')


#matches = TH2F('BB3vsHR','BB3vsHR',416,0,416,160,0,160)
#matches = TH2F('m','m',52,0,52,80,0,80)
onlyxray = 0
onlybb3 =0
both = 0
#for i in range(0,161):
    #for j in range(0,417):
#C = TDirectory()
outfile.mkdir('compare')
compare.cd()
summary = TH1F('BB','BB',3,0,3)
#summary = TH2F('BadBumps','BadBumps',16,0,16,3,0,2)
for n in range (0,16):
    #onlyxray = 0.0
    #onlybb3 = 0.0
    #both = 0.0
    matches = TH2F('BB3vsHR_C'+str(n)+'_V0','BB3vsHR_C'+str(n)+'_V0', 52,0,52,80,0,80)
    print matches
    for i in range (1,52):
        for j in range (1,80):
            hr_h = hrfile.Get('HighRate/hitMap_daqbbtest_C'+str(n)+'_V0')
            bb_h = bbfile.Get('BB3/rescaledThr_C'+str(n)+'_V0')
            bin = hr_h.GetBin(i,j)
            hits = hr_h.GetBinContent(bin)
            bb = bb_h.GetBinContent(bin)
            if (bb<5 and hits<1):
                print hits, bb
                matches.SetBinContent(bin,1)
                onlyxray +=1
            if (bb>5 and hits>1):
                matches.SetBinContent(bin,2)
                onlybb3 +=1
            if (bb>5 and hits<1):
                matches.SetBinContent(bin,3)
                both +=1
    #print onlyxray, onlybb3, both
    matches.Draw('COLZ')
    #summary.SetBinContent(n+1,1,onlyxray)
    #summary.GetXaxis().SetBinLabel(n+1,'C_'+str(n))
    #summary.GetYaxis().SetBinLabel(1,'XrayOnly')
    #summary.SetBinContent(n+1,2,onlybb3)
    #summary.GetXaxis().SetBinLabel(n+1,'C'_+str(n))
    #summary.GetYaxis().SetBinLabel(2,'BB3Only')
    #summary.SetBinContent(n+1,3,both)
    #summary.GetXaxis().SetBinLabel(n+1,'C'_+str(n))
    #summary.GetYaxis().SetBinLabel(3,'Both')
    #print both, onlybb3, float(both)/float(both+onlybb3)   
    summary.SetBinContent(1,onlyxray)
    summary.SetBinContent(2,onlybb3)
    summary.SetBinContent(3, both)   
    outfile.Write()
print onlyxray, onlybb3, both
xrayorbb3 = TH1F('Xray','Xray',2,0,2)
bb3andxray = TH1F('both','both',2,0,2)
hstak = THStack('hstack',' ')
xrayorbb3.SetBinContent(1,onlyxray)
xrayorbb3.SetBinContent(2,onlybb3)
xrayorbb3.SetFillColor(kBlue)
bb3andxray.SetBinContent(1,both)
bb3andxray.SetBinContent(2,both)
bb3andxray.SetFillColor(kRed)
clone1 = xrayorbb3.Clone()
clone2 = bb3andxray.Clone()
hstak.Add(clone1)
hstak.Add(clone2)
print hstak
hstak.Draw('A')
time.sleep(3)
hstak.GetStack().Draw()
outfile.WriteObject(hstak,'hstak')
outfile.Write()
outfile.Close()
 
         
