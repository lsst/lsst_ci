"""
THE ASTROMETRY_NET_DATA NO LONGER EXISTS IN PIPE_TASKS see
https://jira.lsstcorp.org/browse/DM-22233

"""

# We do not have transmission curves attached to our validation repos yet
config.processCcd.isr.doAttachTransmissionCurve = False
# these commissioning data do not have the correct header info to apply the
# stray light correction
config.processCcd.isr.doStrayLight = False

from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
config.processCcd.calibrate.astromRefObjLoader.retarget(LoadAstrometryNetObjectsTask)
config.processCcd.calibrate.photoRefObjLoader.retarget(LoadAstrometryNetObjectsTask)

# Run meas_modelfit to compute CModel fluxes
config.processCcd.calibrate.measurement.plugins.names |= [
            "modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]
config.processCcd.calibrate.measurement.slots.modelFlux = 'modelfit_CModel'
