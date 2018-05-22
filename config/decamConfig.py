# use "instcal" exposures from the community pipeline until DecamIsrTask is up to snuff
from lsst.obs.decam.decamNullIsr import DecamNullIsrTask
config.processCcd.isr.retarget(DecamNullIsrTask)

from lsst.pipe.tasks.setConfigFromEups import setPhotocalConfigFromEups
from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
config.processCcd.calibrate.astromRefObjLoader.retarget(LoadAstrometryNetObjectsTask)
config.processCcd.calibrate.photoRefObjLoader.retarget(LoadAstrometryNetObjectsTask)

setPhotocalConfigFromEups(config.processCcd.calibrate.photoCal)
