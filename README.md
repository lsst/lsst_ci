# lsst_ci - A build target for LSST DM Continous Integration

Build target package to ensure that supported cameras pass their tests:

```
obs_cfht
obs_decam
obs_subaru
obs_lsstSim
testdata_cfht
testdata_decam
testdata_subaru
```

Intended for quick (minutes scale) integration testing.  Currently the test is just that this package successfully builds, which just means that its dependencies (`obs_cfht`, `obs_decam`, `obs_subaru`, and `obs_lsstSim`) successfully build with their full tests as enabled by the `testdata_cfht`, `testdata_decam`, and `testdata_subaru` packages.

The `testdata_*` packages total approximately 3 GB of data repositories.  For running on Jenkins or similar build system, this is a one-time cost that should be fine, but it may be annoying to an individual developer who would like to run this package.
