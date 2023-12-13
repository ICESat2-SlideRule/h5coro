"""Tests for h5 endpoint."""

import pytest
import h5coro
from h5coro import s3driver, webdriver
import earthaccess

auth = earthaccess.login()
credentials = auth.get_s3_credentials(daac="NSIDC")

ATL06_HTTP_URL = "https://data.nsidc.earthdatacloud.nasa.gov/nsidc-cumulus-prod-protected/ATLAS/ATL06/006/2018/10/14/ATL06_20181014001049_02350102_006_02.h5"
ATL06_DATASET = 'gt1r/land_ice_segments/h_li'

ATL03_S3_OBJECT = "nsidc-cumulus-prod-protected/ATLAS/ATL03/006/2018/10/17/ATL03_20181017222812_02950102_006_02.h5"
ATL03_ATTRIBUTE = 'gt2l/heights/h_ph/units'
ATL03_DATASET = 'gt2l/heights/h_ph'
ATL03_GROUP = 'gt2l/heights'

@pytest.mark.region
class TestIcesat2:

    def test_http_driver(self):
        edl_token = auth.token["access_token"] 
        h5obj = h5coro.H5Coro(ATL06_HTTP_URL, webdriver.HTTPDriver, credentials=edl_token)
        promise = h5obj.readDatasets([ATL06_DATASET], block=True)
        assert len(promise[ATL06_DATASET]) == 3880

    def test_s3driver(self):
        h5obj = h5coro.H5Coro(ATL03_S3_OBJECT, s3driver.S3Driver, credentials=credentials)
        promise = h5obj.readDatasets([ATL03_DATASET], block=True, enableAttributes=False)
        assert len(promise[ATL03_DATASET]) == 20622551
        assert abs(promise[ATL03_DATASET][0] - 2553.04) < 0.0001

    @pytest.mark.parametrize("attr", [True, False])
    @pytest.mark.parametrize("early", [True, False])
    @pytest.mark.parametrize("dataset", [ATL03_DATASET, "/"+ATL03_DATASET])
    def test_read_datasets(self, attr, early, dataset):
        h5obj = h5coro.H5Coro(ATL03_S3_OBJECT, s3driver.S3Driver, credentials=credentials)
        promise = h5obj.readDatasets([dataset], block=True, earlyExit=early, enableAttributes=attr)
        expected = [2693.3584, 2595.145, 2590.695, 2606.2778, 2492.0835, 2213.4001, 2059.4768, 2031.4877, 2627.5674, 2478.4314]
        for i in range(len(expected)):
            assert abs(promise[ATL03_DATASET][100:110][i] - expected[i]) < 0.001

    def test_inspect_variable(self):
        h5obj = h5coro.H5Coro(ATL03_S3_OBJECT, s3driver.S3Driver, credentials=credentials)
        metadata, attributes = h5obj.inspectVariable(ATL03_DATASET, w_attr=True)
        assert metadata.dimensions[0] == 20622551
        assert attributes['units'] == 'meters'

    def test_list_group(self):
        h5obj = h5coro.H5Coro(ATL03_S3_OBJECT, s3driver.S3Driver, credentials=credentials)
        variables, attributes = h5obj.listGroup(ATL03_GROUP, w_attr=True, w_inspect=True)
        assert len(variables.keys()) == 13
        assert 'dist_ph_along' in variables
        assert 'data_rate' in attributes
        assert type(attributes["data_rate"]) == str
        assert variables["weight_ph"]["valid_max"][0] == 255

    def test_read_attribute(self):
        h5obj = h5coro.H5Coro(ATL03_S3_OBJECT, s3driver.S3Driver, credentials=credentials)
        attribute = h5obj.readAttribute(ATL03_ATTRIBUTE)
        assert attribute == "meters"
