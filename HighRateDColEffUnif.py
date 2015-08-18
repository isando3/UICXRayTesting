import sys
import glob
import re
import os
import string
from array import *
from ROOT import *
import time

hrflux1 = TFile(sys.argv[1])
hrflux2 = TFile(sys.argv[2])
logflux1 =  open(sys.argv[3],'r')
logflux2 = open(sys.argv[4],'r')
outfile = TFile(sys.argv[5],'recreate')
lineflux1 = logflux1.readlines()
lineflux2 = logflux2.readlines()
fluxstring = 'INFO: X-ray hit rate [MHz/cm2]:'
flux1values = []
flux2values = []
for l in range(0,len(lineflux1)):
    if fluxstring in lineflux1[l]:
        #print lineflux1
        fluxwords = string.rsplit(lineflux1[l].strip(),' ',16)
        del fluxwords[0]
        for fluxvalue in fluxwords:
            flux1values.append(float(fluxvalue))
for l in range(0,len(lineflux2)):
    if fluxstring in lineflux2[l]:
        fluxwords2 = string.rsplit(lineflux2[l].strip(),' ',16)
        del fluxwords2[0]
        for fluxvalue in fluxwords2:
            flux2values.append(float(fluxvalue))
print flux1values, flux2values
###
dbcolvcaltot =2.*78*50
flux1 = TH1F('Flux1', 'Flux1', 16,0,16)
flux2 = TH1F('Flux2','Flux2', 16,0,16)


for n in range  (0,16):
    dcoleff1 = TH1F('DCEff_Flux1_C'+str(n),'DCEff_Flux1_C'+str(n),24,0,24)
    dcoleff2 = TH1F('DCEff_Flux2_C'+str(n),'DCEff_Flux2_C'+str(n),24,0,24)
    dcolunif1 = TH1F('DCUnif_Flux1_C'+str(n),'DCUnif_Flux1_C'+str(n),24,0,24)
    dcolunif2 = TH1F('DCUnif_Flux2_C'+str(n),'DCUnif_Flux2_C'+str(n),24,0,24)
    dcolunifratio = TH1F('DCUnif_Ratio_C'+str(n),'DCUnif_Ratio_C'+str(n),24,0,24)
    dcoleffratio = TH1F('DCEff_Ratio_C'+str(n),'DCEff_Ratio_C'+str(n),24,0,24)
    f1_eff = hrflux1.Get('HighRate/highRate_C'+str(n)+'_V0')
    f2_eff = hrflux2.Get('HighRate/highRate_C'+str(n)+'_V0')
    f1_unif = hrflux1.Get('HighRate/highRate_xraymap_C'+str(n)+'_V0')
    f2_unif = hrflux2.Get('HighRate/highRate_xraymap_C'+str(n)+'_V0')
    #print f1_eff, f2_eff, f1_unif, f2_unif
    index =1
    for i in xrange (2,50,2):
        dbcolvcal_1 =0.
        dbcolvcal_2 =0.
        dbcolhits_1 = 0.
        dbcolhits_2 =0. 
        for j in range (1,79):
            #print i, j
            bin= f1_eff.GetBin(i,j)
            bin2 = f1_eff.GetBin(i+1,j)
            dbcolvcal_1 += f1_eff.GetBinContent(bin)
            dbcolvcal_1 += f1_eff.GetBinContent(bin2)
            dbcolvcal_2 += f2_eff.GetBinContent(bin)
            dbcolvcal_2 += f2_eff.GetBinContent(bin2)
            dbcolhits_1 += f1_unif.GetBinContent(bin)
            dbcolhits_1 += f1_unif.GetBinContent(bin2)
            dbcolhits_2 += f2_unif.GetBinContent(bin)
            dbcolhits_2+= f2_unif.GetBinContent(bin2)
        eff1 = dbcolvcal_1/dbcolvcaltot
        eff2 = dbcolvcal_2/dbcolvcaltot       
        dcoleff1.SetBinContent(index,eff1)
        dcoleff2.SetBinContent(index,eff2)
        dcolunif1.SetBinContent(index,dbcolhits_1)
        dcolunif2.SetBinContent(index,dbcolhits_2)
        dcoleff1.GetYaxis().SetRangeUser(0.,1.1)
        dcoleff2.GetYaxis().SetRangeUser(0.,1.1)
        if(dbcolhits_1>0 and dbcolhits_2>0):
            dcolunifratio.SetBinContent(index,dbcolhits_2/dbcolhits_1)
        elif (dcolhits_1==0. or dcolhits_2==0.):
            dcolunifratio.SetBinContent(index,0.)
        if (eff1>0 and eff2>0):
            dcoleffratio.SetBinContent(index,eff1/eff2)
        elif (eff1==0. or eff2==0.):
            dcolunifratio.SetBinContent(index,0.)
        dcolunifratio.GetYaxis().SetRangeUser(1.5,2.5)
        dcoleffratio.GetYaxis().SetRangeUser(0.5,1.5)
        index+=1
        #print index
    outfile.Write()

for n in range (0,16):
    flux1.SetBinContent(n+1,flux1values[n])
    flux2.SetBinContent(n+1,flux2values[n])
outfile.Write()
outfile.Close()
      

            
