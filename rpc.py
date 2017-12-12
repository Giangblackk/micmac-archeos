

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