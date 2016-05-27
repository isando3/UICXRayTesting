#!/bin/bash
#This script assumes you have the Fluorescece results and the 5 files of the hr test, to run it simply do
# ./RunAllScripts (modulename) (directorywherefilesare) (date)
echo "Summary plots for module:" $1
cd ~/FPIX_ProductionMode/XRayResults
mkdir "$1"
cd "$1"
mkdir Fluorescence
mkdir HighRate
mkdir DataBase
echo "Done creating directories"
cd Fluorescence
cp "$2"/Fluorescence.root .
cp ~/XRayAnalysisTool_UIC_v2.py .
cp ~/XRayAnalyzingTools/UICXRayTesting/XRayAnalysisTool_UIC.py .
if [ -z "$4"]
then python XRayAnalysisTool_UIC_v2.py --outputfile=$1
else python XRayAnalysisTool_UIC_v2.py --outputfile=$1 --badrocs=$4
fi
mv Q*_C*.png ../DataBase
mv SummaryQ*.txt ../DataBase
echo "Done analyzing fluorescence test and moving files to DB dir"
echo "Now starting the highrate analysis"
cd ../
cd HighRate
pwd
mkdir "$1"
cd "$1"
cp ~/efficiency_v2_fix.C eff.C
sed  -i 's>std::string mod("paxxx");>std::string mod("'"$1"'");>g' eff.C
sed  -i 's>std::string phLowName("dc05_mn325_0503.root");>std::string phLowName("dc05_'"$1"'_'"$3"'.root");>g' eff.C 
sed  -i 's>std::string phHighName("dc15_mn325_0503.root");>std::string phHighName("dc15_'"$1"'_'"$3"'.root");>g' eff.C
mkdir "$1"
cd "$1"
cp "$2"/*dat .
cd ../
mkdir "$1"data
cd "$1"data
cp "$2"/hr*ma* .
cp "$2"/dc*root .
pwd
cd ../
root -l -b -q eff.C
echo "Done analyzing highrate results, now copying outputs to DB dir"
cp ~/FPIX_ProductionMode/XRayResults/$1/HighRate/"$1"/"$1"data/Results_Hr_Rate_by_DCol_* ~/FPIX_ProductionMode/XRayResults/$1/DataBase/
cp ~/FPIX_ProductionMode/XRayResults/$1/HighRate/"$1"/"$1"data/Results_Hr_DC_Uniformity_* ~/FPIX_ProductionMode/XRayResults/$1/DataBase/
cp ~/FPIX_ProductionMode/XRayResults/$1/HighRate/"$1"/"$1"data/Results_Hr_Eff_"$1"* ~/FPIX_ProductionMode/XRayResults/$1/DataBase/
cp ~/FPIX_ProductionMode/XRayResults/$1/HighRate/"$1"/"$1"data/hrEfficiency.log ~/FPIX_ProductionMode/XRayResults/$1/DataBase/
cd ~/FPIX_ProductionMode/XRayResults/$1/DataBase/
cp ~/XRayAnalyzingTools/UICXRayTesting/xRayUploadHR_FL.py xRayUpload.py
python xRayUpload.py $1
echo "Congratulations, the results for the Database for module" $1 "can be found in ~/FPIX_ProductionMode/XRayResults/ Now, please go to the Purdue DB to upload them"
cd ~/XRayAnalyzingTools/FPIXUtils/MRWxRayConvert/
echo "$2"
pathstring="$2"
IFS='/' read -ra DIR <<< "$pathstring"
directory="${DIR[4]}"
echo "Making directory for MoReWeb upload:" $directory
mkdir $directory
cd $directory
echo ${directory:0:8}
echo "Now located in" $PWD
mkdir 000_FPIXTest_p17
cd 000_FPIXTest_p17
cp "$2"/highrate.root .
cp "$2"/highrate.log .
cp "$2"/configParameters.dat .
cp "$2"/defaultMaskFile.dat .
cp "$2"/testParameters.dat .
cd ../../
python MRWxRayConvert_3_0.py ${DIR[4]}
echo ${directory:0:8}
cp ${directory:0:8}*_Xray*tar ~/FPIX_ProductionMode/XRayResults/$1/DataBase/