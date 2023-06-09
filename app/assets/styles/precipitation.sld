<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
<NamedLayer>
    <Name>timeseries_precipitation</Name>
    <UserStyle>
    <Name>timeseries_precipitation</Name>
    <Title>timeseries_precipitation</Title>
    <FeatureTypeStyle>
        <Rule>
        <RasterSymbolizer>
            <Opacity>1.0</Opacity>
            <ColorMap type="ramp">
              <ColorMapEntry label="0" color="#f7fbff" quantity="0"/>
              <ColorMapEntry label="12" color="#08306b" quantity="12"/>
            </ColorMap>
        </RasterSymbolizer>
        </Rule>
    </FeatureTypeStyle>
    </UserStyle>
</NamedLayer>
</StyledLayerDescriptor>
