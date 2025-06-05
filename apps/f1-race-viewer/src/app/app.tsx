import { useEffect, useRef } from 'react';
import {
  Entity,
  Viewer,
  Clock,
  ModelGraphics,
  CameraFlyTo,
  LabelGraphics,
  PointGraphics,
  BillboardGraphics,
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
  HeightReference,
  VerticalOrigin,
  NearFarScalar,
  HorizontalOrigin,
  Cartesian2,
  DistanceDisplayCondition,
} from 'cesium';

const NEAR_FAR_SCALAR: NearFarScalar = new NearFarScalar(
  5000, // Near distance (meters)
  0, // Scale at near (invisible when close)
  20000, // Far distance (20km)
  1.0 // Scale at far (fully visible when far)
);

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
      <Entity position={Cartesian3.fromDegrees(9.285138, 45.62154)}>
        <LabelGraphics
          text={'Monza'}
          heightReference={HeightReference.RELATIVE_TO_GROUND}
          verticalOrigin={VerticalOrigin.TOP}
          scaleByDistance={NEAR_FAR_SCALAR}
        />
        <PointGraphics
          color={Color.RED}
          pixelSize={10}
          scaleByDistance={NEAR_FAR_SCALAR}
        />
      </Entity>
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
          distanceDisplayCondition={new DistanceDisplayCondition(400, 5000)}
        />
        <LabelGraphics
          text={lastReport.current ? lastReport.current.driver : ''}
          verticalOrigin={VerticalOrigin.TOP}
          horizontalOrigin={HorizontalOrigin.CENTER}
          font={'24px Helvetica'}
          pixelOffset={new Cartesian2(-12, 0)}
          distanceDisplayCondition={new DistanceDisplayCondition(400, 5000)}
        />
      </Entity>
    </Viewer>
  );
}

export default App;
