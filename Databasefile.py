from optparse import OptionParser
parser = OptionParser()

from ROOT import *
import numpy as npy
import re
import glob
import os

parser.add_option('--outputfile', type='string', action='store',
                  default='DB_file.root',
                  dest='outputfile',
                  help='Set first part of the name of outputfile: Usually DB_MXXYYY')
parser.add_option('--inputfile', type='string', action='store',
                  default='SummaryDistributionTable.txt',
                  dest='inputfile',
                  help='Name of the file to be used, usually SummaryDistributionTable_MXXYYY.txt')
parser.add_option('--badrocs', type='string', action='store',
                  default='',
                  dest='badrocs',
                  help='List of bad rocs, for example [2,4,5]')
(options, args) = parser.parse_args()
argv = []

rocs = range(0,16)
Badrocs = options.badrocs
badrocs = Badrocs.split(',')
badrocs = [int(x) for x in badrocs]   
for x in badrocs:
    rocs.remove(x)
f = TFile(options.outputfile, 'recreate')
slope_hist = TH1F('Ele/Vcal', 'Ele/Vcal', 16,0,16)
offset_hist = TH1F('Offset','Offset', 16,0,16)
means_hist = TH2F('Means','Means',16,0,16,5,0,5)
qfile = open(options.inputfile,'r')
line = qfile.readlines()
for l in range(0,len(line)):
    values = re.split('\t',line[l])
    slope = float(values[0])
    offset = float(values[1].strip('\n'))
    slope_hist.SetBinContent(l+1,slope)
    slope_hist.GetXaxis().SetBinLabel(l+1,'ROC'+str(l))
    offset_hist.SetBinContent(l,offset)
    offset_hist.GetXaxis().SetBinLabel(l+1,'ROC'+str(l))
slope_hist.Draw()
#f.Write()
offset_hist.Draw()
#f.Write()
for i in rocs:
    cumeans = []
    for file in  glob.glob('*'+str(i)+'_stats.txt'):
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
        cu = sum(cumeans)/len(cumeans)
        means_hist.SetBinContent(i+1,1,cu)
        means_hist.GetXaxis().SetBinLabel(i+1,'ROC'+str(i))
        means_hist.GetYaxis().SetBinLabel(1,'Cu')
means_hist.Draw('lego2')
f.Write()    
f.Close




