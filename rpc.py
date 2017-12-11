

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
    def __init__(self):
        pass
    def ReadRPB(self, filename):
        pass