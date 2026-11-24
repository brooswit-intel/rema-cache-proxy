"""This proxy's fixed, allowlisted upstream and native request shape.

Inventoried from Earth Platform 0.1.0-alpha.73 (tag combined-73 / commit
88b13c33954550c6ac660dceb743a4288a9aafac),
geography/src/main/java/io/earthplatform/geography/globe/RemaSource.java:
the mod reads one cloud-optimised GeoTIFF per square from the Polar
Geospatial Center's public AWS Open Data bucket, in two products -- FINE
(2m, 50 km squares, half-square suffix) and COARSE (32m, 100 km squares, no
suffix) -- named 2m/RR_CC/RR_CC_SR_SC_2m_v2.0_dem.tif and
32m/RR_CC/RR_CC_32m_v2.0_dem.tif respectively. Live checks against the
bucket below confirm Accept-Ranges: bytes, 206 Partial Content with a
correct Content-Range. License per the bucket's own STAC metadata
(rema.json): CC-BY-4.0, free, attribution-only, no caching/republishing
restriction found.
"""
import re

from range_cache_proxy import SourceConfig

_PATH_RE = re.compile(
    r"^/(2m)/(\d{2}_\d{2})/\2_[12]_[12]_2m_v2\.0_dem\.tif$"
    r"|^/(32m)/(\d{2}_\d{2})/\4_32m_v2\.0_dem\.tif$"
)


def _validate_path(path: str):
    return path.lstrip("/") if _PATH_RE.match(path) else None


SOURCE = SourceConfig(
    name="rema",
    dataset_id="rema-v2.0",
    default_upstream="https://pgc-opendata-dems.s3.us-west-2.amazonaws.com/rema/mosaics/v2.0/",
    upstream_env_var="REMA_CACHE_UPSTREAM",
    validate_path=_validate_path,
    probe_path="/2m/27_11/27_11_1_1_2m_v2.0_dem.tif",
)
