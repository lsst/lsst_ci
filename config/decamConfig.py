# use "instcal" exposures from the community pipeline until DecamIsrTask is up to snuff
from lsst.obs.decam.decamNullIsr import DecamNullIsrTask
config.processCcd.isr.retarget(DecamNullIsrTask)

from lsst.meas.astrom.matchPessimisticB import MatchPessimisticBTask
config.processCcd.calibrate.astrometry.matcher.retarget(MatchPessimisticBTask)
