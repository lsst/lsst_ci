# lsst_ci - A build target for LSST DM Continous Integration

Build target package to ensure that supported cameras pass their tests:

```
obs_cfht
obs_decam
```

Intended for quick (minutes scale) integration testing.  Currently the test is just that this package successfully builds, which just means that its dependencies (`obs_cfht` and `obs_decam`) successfully build with their full tests as enabled by the `validation_data_cfht` and `validation_data_decam` packages.

