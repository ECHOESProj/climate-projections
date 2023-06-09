<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
	<sld:NamedLayer>
		<sld:Name>Simple</sld:Name>
		<sld:UserStyle>
			<sld:Name>Simple</sld:Name>
			<sld:FeatureTypeStyle>
				<sld:Name>Simple</sld:Name>
				<sld:Rule>
					<sld:RasterSymbolizer>
						<sld:ChannelSelection>
							<sld:GrayChannel>
								<sld:SourceChannelName>1</sld:SourceChannelName>
								<sld:ContrastEnhancement>
									<sld:GammaValue>1.0</sld:GammaValue>
								</sld:ContrastEnhancement>
							</sld:GrayChannel>
						</sld:ChannelSelection>
						<sld:ColorMap>
							<sld:ColorMapEntry label="0" quantity="0" color="#FFFFFF" opacity="0"/>
							<sld:ColorMapEntry label="1" quantity="1" color="#050505"/>
						</sld:ColorMap>
						<sld:ContrastEnhancement/>
					</sld:RasterSymbolizer>
				</sld:Rule>
			</sld:FeatureTypeStyle>
		</sld:UserStyle>
	</sld:NamedLayer>
</sld:StyledLayerDescriptor>
