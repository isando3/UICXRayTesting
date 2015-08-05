#How to run it:  python Databasefile.py --outputfile=ModuleName_XRaySummary.root --FLinputfile =


from optparse import OptionParser
parser = OptionParser()

from ROOT import *
import numpy as npy
import re
import glob
import os
import string


parser.add_option('--outputfile', type='string', action='store',
                  default='DB_file.root',
                  dest='outputfile',
                  help='Set first part of the name of outputfile: Usually DB_MXXYYY')
parser.add_option('--FLinputfile', type='string', action='store',
                  default='SummaryDistributionTable.txt',
                  dest='FLinputfile',
                  help='Name of the txt file to be used for the Fluorescence summary, usually SummaryDistributionTable_MXXYYY.txt generated through XRayAnalysistool.py')
parser.add_option('--HRinputfile', type='string', action='store',
                  default='HR_module.root',
                  dest='HRinputfile',
                  help='Name of the log  file to be used for the HighRate summary, use the log file after you run the HR tests')
parser.add_option('--badrocs', type='string', action='store',
                  default='17',
                  dest='badrocs',
                  help='List of bad rocs, for example [2,4,5]')
(options, args) = parser.parse_args()
argv = []

###Fluorescence  Summary

rocs = range(0,16)
Badrocs = options.badrocs
badrocs = Badrocs.split(',')
print badrocs[0] 
if badrocs[0] == '17':
    print 'no bad rocs'
else:
    badrocs = [int(x) for x in badrocs]   
    for x in badrocs:
        rocs.remove(x)
print 'Analyzing rocs:', rocs
f = TFile(options.outputfile, 'recreate')
slope_hist = TH1F('Ele/Vcal', 'Ele/Vcal', 16,0,16)
offset_hist = TH1F('Offset','Offset', 16,0,16)
means_hist = TH2F('Means','Means',16,0,16,5,0,5)
qfile = open(options.FLinputfile,'r')
line = qfile.readlines()
for l in range(0,len(line)):
    values = re.split('\t',line[l])
    slope = float(values[0])
    offset = float(values[1].strip('\n'))
    slope_hist.SetBinContent(l+1,slope)
    slope_hist.GetXaxis().SetBinLabel(l+1,'ROC'+str(l))
    offset_hist.SetBinContent(l+1,offset)
    offset_hist.GetXaxis().SetBinLabel(l+1,'ROC'+str(l))
slope_hist.Draw()
#f.Write()
offset_hist.Draw()
#f.Write()
for i in rocs:
    print 'Analyzing Roc:', i
    cumeans = []
    for file in  glob.glob('*'+'C_'+str(i)+'_stats.txt'):
        name = os.path.splitext(file)[0]
        print 'Opening:', name
        if ('MoC' in name):
            stat_file = open(file, 'r')
            stat_line = stat_file.readlines()
            for j in  range(0,len(stat_line)-1):
                print j, stat_line[j]
                if ('Mean_Mo' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meanmo = words[1].strip('\n')
                    means_hist.SetBinContent(i+1,2,float(meanmo))
                    means_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
                    means_hist.GetYaxis().SetBinLabel(2,'Mo')
                elif ('Mean_Cu' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meancu = words[1].strip('\n')
                    cumeans.append(float(meancu))
                print cumeans
        elif ('AgC' in name):
            stat_file = open(file, 'r')
            stat_line = stat_file.readlines()
            for j in range (0,len(stat_line)-1):
                if ('Mean_Ag' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meanag = words[1].strip('\n')
                    means_hist.SetBinContent(i+1,3,float(meanag))
                    means_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
                    means_hist.GetYaxis().SetBinLabel(3,'Ag')
                elif ('Mean_Cu' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meancu = words[1].strip('\n')
                    cumeans.append(float(meancu))
                print cumeans
        elif ('InC' in name):
            stat_file = open(file, 'r')
            stat_line = stat_file.readlines()
            for j in range (0,len(stat_line)-1):
                if ('Mean_In' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meanin = words[1].strip('\n')
                    means_hist.SetBinContent(i+1,4,float(meanin))
                    means_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
                    means_hist.GetYaxis().SetBinLabel(4,'In')
                elif ('Mean_Cu' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meancu = words[1].strip('\n')
                    cumeans.append(float(meancu))
        elif ('SnC' in name):
            stat_file = open(file, 'r')
            stat_line = stat_file.readlines()
            for j in range (0,len(stat_line)-1):
                if ('Mean_Sn' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meansn = words[1].strip('\n')
                    means_hist.SetBinContent(i+1,5,float(meansn))
                    means_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
                    means_hist.GetYaxis().SetBinLabel(5,'Sn')
                elif ('Mean_Cu' in stat_line[j]):
                    words =  re.split(':\t',stat_line[j])
                    meancu = words[1].strip('\n')
                    cumeans.append(float(meancu))
        print cumeans
        cu = sum(cumeans)/len(cumeans)
        means_hist.SetBinContent(i+1,1,cu)
        means_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
        means_hist.GetYaxis().SetBinLabel(1,'Cu')
means_hist.Draw('lego2')

#High Rate Summary

effstring = 'INFO: Vcal hit overall efficiency (%):'
fluxstring = 'INFO: X-ray hit rate [MHz/cm2]:'
bbstring = 'Pixels without X-ray hits (per ROC):'

ineffvalues=[]
fluxvalues=[]
bbvalues=[]

bb_hist = TH1F('BadBumps','BadBumps',16,0,16)

hrfile = open(options.HRinputfile,'r')
lines = hrfile.readlines()
for l in range(0,len(lines)):
    if effstring in lines[l]:
        effwords = string.rsplit(lines[l].strip(), ' ' , 16)
        del effwords[0]
        roc= 0
        for effvalue in effwords:
            ineffvalues.append(100-float(effvalue))
    elif fluxstring in lines[l]:
        fluxwords = string.rsplit(lines[l].strip(),' ',16)
        del fluxwords[0]
        roc = 0 
        for fluxvalue in fluxwords:
            fluxvalues.append(float(fluxvalue))   
    elif bbstring in lines[l]:
        bbwords = lines[l].rsplit('   ')
        bbwords.pop(0)
        bbwords.pop(0)
        roc= 0
        print bbwords
        for bbvalue in bbwords:
            bb_hist.SetBinContent(roc+1,float(bbvalue))
            bb_hist.GetXaxis().SetBinLabel(roc+1,'ROC'+str(roc))
            bb_hist.GetYaxis().SetTitle('Num. bad bumps')
            roc += 1
bb_hist.Draw()
maxineff = max(ineffvalues)
minineff= min(ineffvalues)
bins = maxineff-minineff
ineff_hist = TH2F('Ineffiency', 'Ineffiency',16,0,16, int(maxineff*10),0,maxineff+1)
for i in range(0,16):
    print ineffvalues[i]
    ineff_hist.Fill(i, ineffvalues[i],fluxvalues[i])
    ineff_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
    ineff_hist.GetYaxis().SetTitle('Inefficiency [%]')
    ineff_hist.GetZaxis().SetTitle('Flux [MHz/cm2]')
ineff_hist.Draw()
f.Write()    
f.Close




