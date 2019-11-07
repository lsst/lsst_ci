# We do not have transmission curves attached to our validation repos yet
config.processCcd.isr.doAttachTransmissionCurve = False
# Run meas_modelfit to compute CModel fluxes
import lsst.meas.modelfit
config.processCcd.calibrate.measurement.plugins.names |= [
            "modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]
config.processCcd.calibrate.measurement.slots.modelFlux = 'modelfit_CModel'
