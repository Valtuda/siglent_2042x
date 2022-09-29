"""
Translates a position on a calibrated grid to a voltage to be send to the galvo mirrors.
"""
import json
import numpy as np
from scipy.optimize import curve_fit
from .sdg_settings import sdg_settings as sdg

def fit_func(x,*p,degree = 2):
    x = np.array(x)

    # If it's only one point, convert to a list.
    if len(x.shape) != 2:
        x = np.array([x])

    y = x.T[1]
    x = x.T[0]

    p = np.array(p).reshape(degree+1,degree+1)
    xpower,ypower = np.mgrid[0:degree+1,0:degree+1]

    output = np.sum(p[None,:,:] * x[:,None,None] ** xpower[None,:,:] * y[:,None,None] ** ypower[None,:,:],axis=-1).sum(axis=-1)

    return output

class GalvoMirrors:
    def __init__(self,calibration_file,backend = "waveform",backend_args=None,starting_pos=None):
        self._calib_file   = calibration_file
        self._backend      = backend
        self._backend_args = backend_args

        self._calib_params = None

        if backend == "waveform":
            if "ip" not in backend_args.keys() or "port" not in backend_args.keys():
                raise ValueError("Please specify IP and port for the waveform generator in backend_args.")
            
            self._comm     = sdg(backend_args["ip"],backend_args["port"])

            self.calib_table = None
            self.calibrate()

            if starting_pos is not None:
                self.move_to(starting_pos[0],starting_pos[1])
            else:
                self._V1 = 0
                self._V2 = 0
                self._x  = None
                self._y  = None

        else:
            raise ValueError("Only waveform generator backend is currently supported")

    def calib_func(self,x,y):
        popt1 = self._calib_params[0]
        popt2 = self._calib_params[1]
        return fit_func([x,y],*popt1),fit_func([x,y],*popt2)
 
    def calibrate(self,degree = 2):
        with open("calib_table_test.json","r") as f:
            self.calib_table = np.array(json.load(f)["calib_table"])

        xdata  = self.calib_table[:,3:]
        y1data = self.calib_table[:,1]
        y2data = self.calib_table[:,2]
          

        popt1, pcov = curve_fit(fit_func,xdata,y1data,p0=np.zeros((degree+1)**2))
        popt2, pcov = curve_fit(fit_func,xdata,y2data,p0=np.zeros((degree+1)**2))

        self._calib_params = [popt1,popt2]

    def move_to(self,x,y):
        V1,V2 = self.calib_func(x,y)

        self._comm.set_voltage(1,V1[0])
        self._comm.set_voltage(2,V2[0])

        self._V1 = V1[0]
        self._V2 = V2[0]

        self._x  = x
        self._y  = y


    def to_dict(self):
        _dict = dict()
        
        _dict["x"] = float(self._x)
        _dict["y"] = float(self._y)

        _dict["V1"] = float(self._V1)
        _dict["V2"] = float(self._V2)

        _dict["backend"] = self._backend
        _dict["ip"] = self._backend_args["ip"]
        _dict["port"] = self._backend_args["port"]

        _dict["calib_table"] = self.calib_table.tolist()

        return _dict

    
