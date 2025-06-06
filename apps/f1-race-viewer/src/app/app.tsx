import { useEffect, useRef } from 'react';
import {
  Entity,
  Viewer,
  Clock,
  ModelGraphics,
  CameraFlyTo,
  LabelGraphics,
  BillboardGraphics,
  GeoJsonDataSource,
} from 'resium';
import useWebSocket from 'react-use-websocket';
import { F1CarTelemetryReport } from '@f1-race-replay/data-model';
import {
  Cartesian3,
  Color,
  ExtrapolationType,
  JulianDate,
  SampledPositionProperty,
  LagrangePolynomialApproximation,
  VelocityOrientationProperty,
  TrackingReferenceFrame,
  VerticalOrigin,
  HorizontalOrigin,
  Cartesian2,
  DistanceDisplayCondition,
  ConstantProperty,
  LabelGraphics as CesiumLabelGraphics,
} from 'cesium';

export function App() {
  const { lastMessage, readyState, getWebSocket } = useWebSocket(
    'ws://127.0.0.1:8765'
  );
  const lastReport = useRef<F1CarTelemetryReport | null>(null);
  const sampledPositionProperty = useRef<SampledPositionProperty>(
    new SampledPositionProperty()
  );

  // Set interpolation options once
  useEffect(() => {
    sampledPositionProperty.current.forwardExtrapolationType =
      ExtrapolationType.HOLD;
    sampledPositionProperty.current.forwardExtrapolationDuration = 10;
    sampledPositionProperty.current.setInterpolationOptions({
      interpolationDegree: 8,
      interpolationAlgorithm: LagrangePolynomialApproximation,
    });
  }, []);

  useEffect(() => {
    if (!getWebSocket()) return;
    getWebSocket().binaryType = 'arraybuffer';
  }, [getWebSocket, readyState]);

  useEffect(() => {
    if (!lastMessage) return;
    if (!(lastMessage.data instanceof ArrayBuffer)) return;

    const report: F1CarTelemetryReport = F1CarTelemetryReport.decode(
      new Uint8Array(lastMessage.data)
    );
    console.log('Received message:', report);
    lastReport.current = report;
    sampledPositionProperty.current.addSample(
      JulianDate.now(),
      Cartesian3.fromDegrees(report.longitude, report.latitude, 0)
    );
  }, [lastMessage]);

  return (
    <Viewer
      full
      timeline={false}
      baseLayerPicker={false}
      navigationHelpButton={false}
      scene3DOnly={true}
    >
      <Clock
        shouldAnimate
        currentTime={JulianDate.fromDate(new Date(Date.now() - 1500))}
      />
      <CameraFlyTo
        duration={5}
        destination={Cartesian3.fromDegrees(9.285138, 45.62154, 4000)}
        once={true}
      />
      <GeoJsonDataSource
        data={'./src/assets/f1-circuits.geojson'}
        stroke={Color.RED}
        strokeWidth={6}
        onLoad={(g) => {
          g.entities.values.forEach((entity) => {
            if (entity.polyline) {
              entity.polyline.distanceDisplayCondition = new ConstantProperty(
                new DistanceDisplayCondition(400, 10000)
              );
            }
          });
        }}
      />
      <GeoJsonDataSource
        data={'./src/assets/f1-locations.geojson'}
        markerColor={Color.RED}
        markerSymbol="car"
        onLoad={(g) => {
          g.entities.values.forEach((entity) => {
            entity.label = new CesiumLabelGraphics({
              text: entity.properties.name,
              font: '24px Helvetica',
              distanceDisplayCondition: new DistanceDisplayCondition(
                10000,
                99999999
              ),
            });
            if (entity.billboard) {
              entity.billboard.distanceDisplayCondition = new ConstantProperty(
                new DistanceDisplayCondition(10000, 99999999)
              );
            }
          });
        }}
      />
      <Entity
        key={lastReport.current?.driver}
        position={sampledPositionProperty.current}
        orientation={
          new VelocityOrientationProperty(sampledPositionProperty.current)
        }
        // point={{ pixelSize: 10, color: Color.RED }}
        trackingReferenceFrame={TrackingReferenceFrame.INERTIAL}
        name={lastReport.current ? lastReport.current.driver : ''}
      >
        <ModelGraphics
          uri={'./src/assets/low_poly_f1.glb'}
          scale={0.4}
          runAnimations={true}
          distanceDisplayCondition={new DistanceDisplayCondition(1, 400)}
        />
        <BillboardGraphics
          image={'./src/assets/red_bull_pin.png'}
          scale={0.02}
          distanceDisplayCondition={new DistanceDisplayCondition(400, 10000)}
          eyeOffset={Cartesian3.fromElements(0, 0, -100)}
        />
        <LabelGraphics
          text={lastReport.current ? lastReport.current.driver : ''}
          verticalOrigin={VerticalOrigin.TOP}
          horizontalOrigin={HorizontalOrigin.CENTER}
          font={'24px Helvetica'}
          pixelOffset={Cartesian2.fromElements(0, 18)}
          distanceDisplayCondition={new DistanceDisplayCondition(400, 10000)}
          eyeOffset={Cartesian3.fromElements(0, 0, -100)}
        />
      </Entity>
    </Viewer>
  );
}

export default App;
