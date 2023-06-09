<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc"
xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
<NamedLayer>
    <Name>$name</Name>
    <UserStyle>
    <Name>$name</Name>
    <Title>$name</Title>
    <FeatureTypeStyle>
        <Rule>
        <RasterSymbolizer>
            <Opacity>1.0</Opacity>
            <ColorMap type="ramp">
              <ColorMapEntry color="$min_color" quantity="$min"/>
              <ColorMapEntry color="$max_color" quantity="$max"/>
            </ColorMap>
        </RasterSymbolizer>
        </Rule>
    </FeatureTypeStyle>
    </UserStyle>
</NamedLayer>
</StyledLayerDescriptor>
