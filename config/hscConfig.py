"""
Configure to force using astrometry_net instead of directly 
loading Pan-STARRS1 reference catalogs
"""

from lsst.pipe.tasks.setConfigFromEups import setPhotocalConfigFromEups, setAstrometryConfigFromEups

# We do not have transmission curves attached to our validation repos yet
config.processCcd.isr.doAttachTransmissionCurve = False
# these commissioning data do not have the correct header info to apply the stray light correction
config.processCcd.isr.doStrayLight = False

from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
config.processCcd.calibrate.astromRefObjLoader.retarget(LoadAstrometryNetObjectsTask)
config.processCcd.calibrate.photoRefObjLoader.retarget(LoadAstrometryNetObjectsTask)

setPhotocalConfigFromEups(config.processCcd.calibrate.photoCal)

menu = { "ps1*": {}, # No changes
         "sdss*": { "filterMap": {"y": "z"} }, # No y-band, use z instead
         "2mass*": { "filterMap": {ff:"J" for ff in 'grizy'} }, # No optical; use J 
       }

# Both configs need to have the filterMap set
setAstrometryConfigFromEups(config.processCcd.calibrate.photoRefObjLoader, menu)
setAstrometryConfigFromEups(config.processCcd.calibrate.astromRefObjLoader, menu)
