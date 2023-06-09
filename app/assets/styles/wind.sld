<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
<NamedLayer>
    <Name>timeseries_wind</Name>
    <UserStyle>
    <Name>timeseries_wind</Name>
    <Title>timeseries_wind</Title>
    <FeatureTypeStyle>
        <Rule>
        <RasterSymbolizer>
            <Opacity>1.0</Opacity>
            <ColorMap type="ramp">
              <ColorMapEntry color="#fff" opacity="0" quantity="0.0" label="0.0"/>
              <ColorMapEntry label="1" color="#f7fcf5" quantity="1"/>
              <ColorMapEntry label="15" color="#00441b" quantity="13"/>
            </ColorMap>
        </RasterSymbolizer>
        </Rule>
    </FeatureTypeStyle>
    </UserStyle>
</NamedLayer>
</StyledLayerDescriptor>
