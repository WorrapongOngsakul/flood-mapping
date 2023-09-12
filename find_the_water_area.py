import os
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
from snappy import jpy


# Helper functions
def showProductInformation(product):
    width = product.getSceneRasterWidth()
    print("Width: {} px".format(width))
    height = product.getSceneRasterHeight()
    print("Height: {} px".format(height))
    name = product.getName()
    print("Name: {}".format(name))
    band_names = product.getBandNames()
    print("Band names: {}".format(", ".join(band_names)))

# Preprocessing functions
def calibration(product):
    print("Calibration")
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', 'Intensity_VV')
    parameters.put('selectedPolarisations', "VV")
    parameters.put('outputImageScaleInDb', False)
    return GPF.createProduct("Calibration", parameters, product)

def speckleFilter(product):
    print("SpeckleFilter")
    parameters = HashMap()
    filterSizeY = '7'
    filterSizeX = '7'
    parameters.put('sourceBands', 'Sigma0_VV')
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', filterSizeX)
    parameters.put('filterSizeY', filterSizeY)
    parameters.put('dampingFactor', '2')
    parameters.put('estimateENL', 'true')
    parameters.put('enl', '1.0')
    parameters.put('numLooksStr', '1')
    parameters.put('targetWindowSizeStr', '3x3')
    parameters.put('sigmaStr', '0.9')
    parameters.put('anSize', '50')
    return GPF.createProduct('Speckle-Filter', parameters, product)

def terrainCorrection(product):
    print("TerrainCorrection")
    parameters = HashMap()
    parameters.put('demName', 'SRTM 3Sec')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('sourceBands', 'flooded')
    return GPF.createProduct("Terrain-Correction", parameters, product)

# Flooding processing
def generateBinaryFlood(product):
    print("generateBinaryFlood")
    parameters = HashMap()
    BandDescriptor = snappy.jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')
    targetBand = BandDescriptor()
    targetBand.name = 'flooded'
    targetBand.type = 'uint8'
    targetBand.expression = '(Sigma0_VV < 1.13E-2) ? 1 : 0'
    targetBands = snappy.jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 1)
    targetBands[0] = targetBand
    parameters.put('targetBands', targetBands)
    return GPF.createProduct('BandMaths', parameters, product)

if __name__ == "__main__":
    pathData = "{PATH}"
    for x in os.listdir(pathData):
        print(x)
        fileName = x
        filePath = pathData + fileName
        saveName = fileName.replace(".zip", "")
        print(saveName)

        ## GPF Initialization
        GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

        ## Product initialization
        path_to_sentinel_data = filePath
        product = ProductIO.readProduct(path_to_sentinel_data)
        showProductInformation(product)

        # Apply remainder of processing steps in a nested function call
        product_preprocessed = (speckleFilter(calibration(product)))
        product_binaryflood = terrainCorrection(generateBinaryFlood(product_preprocessed))
        ProductIO.writeProduct(product_binaryflood, pathData+saveName, 'GeoTIFF')