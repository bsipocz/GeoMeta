import json

import rasterio
import rasterio.warp
import rasterio.features


def get_meta(datafile, dataset_doi=None, publication_doi=None,
             outputfile=None):
    """
    Generating geospatial metadata from Digital Elevation Model files.

    Parameters
    ----------
    datafile : str
        Filename for data file. Format should be supported by the
        rasterio packgage.
    dataset_doi : str
        DOI for the original raw data
    publication_doi : str
        Reference publication for this dataset
    outputfile : str
        Name of output file to dump the metadata information


    """
    with rasterio.open(datafile) as data:
        # Read the dataset's valid data mask as a ndarray.
        mask = data.dataset_mask()

        # Extract feature shapes and values from the array.
        for geo_info, val in rasterio.features.shapes(
                mask, transform=data.transform):

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geo_info = rasterio.warp.transform_geom(
                data.crs, data.crs, geo_info, precision=6)

    metadata = {
        'georeferencing': {
            'spatial extent': geo_info,
            'EPSG': data.crs.to_string()},
        'driver': data.driver,
        'width': data.width,
        'height': data.height,
        'count': data.count,
        'dtypes': data.dtypes,
        'crs': data.crs.to_string(),
        'transform': data.transform,
        'nodata': data.nodata,
        'bounding_box': data.bounds,
        'source info': {}
    }

    if dataset_doi is not None:
        metadata['source info']['dataset DOI'] = source_info

    if publication_doi is not None:
        metadata['source info']['publication DOI'] = publication_doi

    if outputfile:
        with open(outputfile, 'w') as of:
            json.dump(metadata, of)
    else:
        return json.dumps(metadata, indent=2)


def from_metadata(datafile, metadata):
    pass
