//convert ascii to root
//the most complete header (tree descriptor): dat/Auger_FD_ICRC2019_XmaxMoments.dat
void ASCII2ROOT()
{
  //name of .dat file (will be searched in dat/folder)
  TString inputFile =  "LOFAR_PRD2021_XmaxMoments.dat";

  TTree *DataTree=new TTree("XmaxData","XmaxData");
  DataTree->ReadFile("dat/" +  inputFile);
  inputFile.ReplaceAll(".dat", ".root");
  TFile outFile("root/" +  inputFile,"recreate");
  DataTree->Write();
  outFile.Save();
}
