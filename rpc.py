class Pt3di(object):

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class cIncIntervale(object):
    mI0Alloc = 0
    mI1Alloc = 0
    mI0Solve = 0
    mI1Solve = 0

    mSet = []
    mId = ''
    mNumBlocAlloc = 0
    mNumBlocSolve = 0
    mFiged = False
    mOrder = 0.0
    mIsTmp = False
    
    def __init__(self):
        pass
    def NumBlocSolve(self):
        return self.mNumBlocSolve


class cSsBloc(object):
    mI0 = 0  # Relatif au ss bloc
    mNb = 0  # Nb d'elet
    mInt = cIncIntervale()
    mCpt = 0
    theCptGlob = 0

    def __init__(self, aI0, aI1):
        self.mI0 = aI0
        self.mNb = aI1-aI0
        self.mCpt =  self.theCptGlob
        self.theCptGlob += 1
    
    def Intervale(self):
        return self.mInt

class L2SysSurResol(object):
    mNbVar = 0
    mtLi_Li = [] # Sigma des trans(Li) Li
    mDatatLi_Li = []
    mInvtLi_Li = [];    # Inverse Sigma des trans(Li) Li
    mDataInvtLi_Li = []
    mbi_Li = [];  # Sigma des bi * Li
    mDatabi_Li = []
    mBibi = 0.0
    mSolL2 = []
    mDataSolL2 = []
    mNbEq = 0; # Debug
    mMaxBibi = 0.0; # Debug

    def __init__(self, aNbVar, IsSym=True):
        mNbVar = aNbVar

    def V_GSSR_AddNewEquation_Indexe(self,
            aVSB, aFullCoef, aNbTot,
           aVInd, aPds, aCoeff, aB):
           if aVSB:
               aPB = aPds * aB
               aNbBl = len(aVSB)
               Y0InBloc =0
               for aKBly in range(aNbBl):
                   aBlY = aVSB[aKBly]
                   aIntY = aBlY.Intervale()
                   aNumBlocIntervY = aIntY.NumBlocSolve()

    def AddEquation(self, aPds, aCoeff, aB):
        VInd = []
        VALS = []
        for iVar1 in range(self.mNbVar):
            if (aCoeff[iVar1] != 0.0): # Acceleration pour les formes creuses
                VInd.append(iVar1)
                VALS.append(aCoeff[iVar1])
        self.V_GSSR_AddNewEquation_Indexe(0, 0, 0, VInd, aPds, VALS,aB)


class RPC(object):
    direct_line_num_coef = []
    direct_line_den_coef = []
    direct_samp_num_coef = []
    direct_samp_den_coef = []
    inverse_line_num_coef = []
    inverse_line_den_coef = []
    inverse_samp_num_coef = []
    inverse_samp_den_coef = []
    # Offsets and scale for ground space
    lat_off, lat_scale, long_off, long_scale, height_off, height_scale = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    # Offsets and scale for image space
    line_off, line_scale, samp_off, samp_scale =  0.0, 0.0, 0.0, 0.0
    # Boundaries of RPC validity for image space
    first_row, first_col, last_row, last_col = 0.0, 0.0, 0.0, 0.0
    # Boundaries of RPC validity for geo space
    first_lon, first_lat, last_lon, last_lat, first_height, last_height = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    IS_INV_INI = False

    def __init__(self):
        pass

    def ReadRPB(self, filename):
        f = open(filename,'r')
        # Pass 6 lines
        for _ in range(6):
            line = f.readline()
            print(line)
        # Line Offset
        line = f.readline()
        a, b, self.line_off = line.split()
        # Samp Offset
        line = f.readline()
        a, b, self.samp_off = line.split()
        # Lat Offset
        line = f.readline()
        a, b, self.lat_off = line.split()
        # Lon Offset
        line = f.readline()
        a, b, self.long_off = line.split()
        # Height Offset
        line = f.readline()
        a, b, self.height_off = line.split()
        # Line Scale
        line = f.readline()
        a, b, self.line_scale = line.split()
        # Samp Scale
        line = f.readline()
        a, b, self.samp_scale = line.split()
        # Lat Scale
        line = f.readline()
        a, b, self.lat_scale = line.split()
        # Lon Scale
        line = f.readline()
        a, b, self.long_scale = line.split()
        # Height Scale
        line = f.readline()
        a, b, self.height_scale = line.split()
        # inverse_line_num_coef
        line = f.readline()
        for _ in range(19):
            line = f.readline()
            self.inverse_line_num_coef.append(float(line[:-2]))
        line = f.readline()
        self.inverse_line_num_coef.append(float(line[:-3]))
        print(self.inverse_line_num_coef)
        # inverse_line_den_coef
        line = f.readline()
        for _ in range(19):
            line = f.readline()
            self.inverse_line_den_coef.append(float(line[:-2]))
        line = f.readline()
        self.inverse_line_den_coef.append(float(line[:-3]))
        print(self.inverse_line_den_coef)
        # inverse_samp_num_coef
        line = f.readline()
        for _ in range(19):
            line = f.readline()
            self.inverse_samp_num_coef.append(float(line[:-2]))
        line = f.readline()
        self.inverse_samp_num_coef.append(float(line[:-3]))
        print(self.inverse_samp_num_coef)
        # inverse_samp_den_coef
        line = f.readline()
        for _ in range(19):
            line = f.readline()
            self.inverse_samp_den_coef.append(float(line[:-2]))
        line = f.readline()
        self.inverse_samp_den_coef.append(float(line[:-3]))
        print(self.inverse_samp_den_coef)
        self.IS_INV_INI = True

    def GenerateNormGrid(self,aGridSz):
        aGridNorm = []
        aZS = 2/aGridSz.z
        aXS = 2/aGridSz.x
        aYS = 2/aGridSz.y
        for aR in range(aGridSz.x+1):
            for aC in range(aGridSz.y+1):
                for aH in range(aGridSz.z+1):
                    aPt = Pt3di()
                    aPt.x = aR*aXS -1
                    aPt.y = aC*aYS -1
                    aPt.z = aZS*aH -1
                    aGridNorm.append(aPt)
        return aGridNorm
    def InverseRPCNorm(self, PgeoNorm):
        X = PgeoNorm.x
        Y = PgeoNorm.y
        Z = PgeoNorm.z
        vecteurD = [ 1, X, Y, Z, Y*X, X*Z, Y*Z, X*X, Y*Y, Z*Z, X*Y*Z, X*X*X, Y*Y*X, X*Z*Z, X*X*Y, Y*Y*Y, Y*Z*Z, X*X*Z, Y*Y*Z, Z*Z*Z ]
        samp_den = 0.
        samp_num = 0.
        line_den = 0.
        line_num = 0.
        for i in range(20):
            line_num += vecteurD[i] * self.inverse_line_num_coef[i]
            line_den += vecteurD[i] * self.inverse_line_den_coef[i]
            samp_num += vecteurD[i] * self.inverse_samp_num_coef[i]
            samp_den += vecteurD[i] * self.inverse_samp_den_coef[i]
        # Final computation
        PimgNorm = Pt3di()
        if ((samp_den != 0) and (line_den != 0)):
            PimgNorm.x = (samp_num / samp_den)
            PimgNorm.y = (line_num / line_den)
            PimgNorm.z = PgeoNorm.z
        else:
            print("Computing error - denominator = 0")
        return PimgNorm

    def GCP2Direct(self, aGridGeoNorm, aGridImNorm):
        # Cleaning potential data in RPC object
        self.direct_samp_num_coef = []
        self.direct_samp_den_coef = []
        self.direct_line_num_coef = []
        self.direct_line_den_coef = []
        # Parameters too get parameters of P1 and P2 in ---  lon=P1(row,column,Z)/P2(row,column,Z)  --- where (row,column,Z) are image coordinates (idem for lat)
        # To simplify notations : Column->X and Row->Y
        # Function is 0=Poly1(Y,X,Z)-long*Poly2(Y,X,Z) with poly 3rd degree (up to X^3,Y^3,Z^3,XXY,XXZ,XYY,XZZ,YYZ,YZZ)
        # First param (cst) of Poly2=1 to avoid sol=0
        aSysLon = L2SysSurResol(39)
        aSysLat = L2SysSurResol(39)

        # For all lattice points
        for i in range(len(aGridGeoNorm)):
            # Simplifying notations
            X = aGridImNorm[i].x
            Y = aGridImNorm[i].y
            Z = aGridImNorm[i].z
            lon = aGridGeoNorm[i].x
            lat = aGridGeoNorm[i].y

            aEqLon = [
                1, X, Y, Z, X*Y, X*Z, Y*Z, X*X, Y*Y, Z*Z, Y*X*Z, X*X*X, X*Y*Y, X*Z*Z, Y*X*X, Y*Y*Y, Y*Z*Z, X*X*Z, Y*Y*Z, Z*Z*Z,
                -lon*X, -lon*Y, -lon*Z, -lon*X*Y, -lon*X*Z, -lon*Y*Z, -lon*X*X, -lon*Y*Y, -lon*Z*Z, -lon*Y*X*Z, -lon*X*X*X, -lon*X*Y*Y, -lon*X*Z*Z, -lon*Y*X*X, -lon*Y*Y*Y, -lon*Y*Z*Z, -lon*X*X*Z, -lon*Y*Y*Z, -lon*Z*Z*Z
            ]
            aSysLon.AddEquation(1, aEqLon, lon)


            aEqLat = [
                1, X, Y, Z, X*Y, X*Z, Y*Z, X*X, Y*Y, Z*Z, Y*X*Z, X*X*X, X*Y*Y, X*Z*Z, Y*X*X, Y*Y*Y, Y*Z*Z, X*X*Z, Y*Y*Z, Z*Z*Z,
                -lat*X, -lat*Y, -lat*Z, -lat*X*Y, -lat*X*Z, -lat*Y*Z, -lat*X*X, -lat*Y*Y, -lat*Z*Z, -lat*Y*X*Z, -lat*X*X*X, -lat*X*Y*Y, -lat*X*Z*Z, -lat*Y*X*X, -lat*Y*Y*Y, -lat*Y*Z*Z, -lat*X*X*Z, -lat*Y*Y*Z, -lat*Z*Z*Z
            ]
            aSysLat.AddEquation(1, aEqLat, lat)
 