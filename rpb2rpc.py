from rpc import RPC

def DigitalGlobe2Grid_main(aNameFile,targetSyst,altiMin, altiMax,nbLayers):
    inputSyst = "+proj=longlat +datum=WGS84 "; #input syst proj4
    refineCoef=""
    binaire = True
    stepPixel = 100.
    stepCarto = 50.
    # Reading Inverse RPC, computing Direct RPC and setting up RPC object
    aRPC = RPC()

if __name__ == "__main__":
    aNameFile = "/media/mybutt/DATA/Skymapdev/data/semiglobalmatching/SV1-01_20171009_L1B0000169008_1109170084002_01-MUX1.rpb"
    targetSyst = "+proj=longlat +datum=WGS84 "
    altiMin = 0
    altiMax = 100
    nbLayers = 4
    DigitalGlobe2Grid_main(aNameFile,targetSyst,altiMin, altiMax, nbLayers)