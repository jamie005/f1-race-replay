import { F1CarTelemetryReport } from '@f1-race-replay/data-model';
import {
  Cartesian2,
  Cartesian3,
  DistanceDisplayCondition,
  ExtrapolationType,
  HorizontalOrigin,
  JulianDate,
  LagrangePolynomialApproximation,
  SampledPositionProperty,
  TrackingReferenceFrame,
  VelocityOrientationProperty,
  VerticalOrigin,
} from 'cesium';
import { useEffect, useRef } from 'react';
import useWebSocket from 'react-use-websocket';
import {
  BillboardGraphics,
  Entity,
  LabelGraphics,
  ModelGraphics,
} from 'resium';

export function F1Cars() {
  const { lastMessage, readyState, getWebSocket } = useWebSocket(
    'ws://127.0.0.1:8765'
  );
  const lastReport = useRef<F1CarTelemetryReport | null>(null);
  const sampledPositionProperty = useRef<SampledPositionProperty>(
    new SampledPositionProperty()
  );

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
    if (!lastMessage || !(lastMessage.data instanceof ArrayBuffer)) return;

    const report: F1CarTelemetryReport = F1CarTelemetryReport.decode(
      new Uint8Array(lastMessage.data)
    );
    console.debug('Received message:', report);
    lastReport.current = report;
    sampledPositionProperty.current.addSample(
      JulianDate.now(),
      Cartesian3.fromDegrees(report.longitude, report.latitude, 0)
    );
  }, [lastMessage]);
  return (
    <Entity
      key={lastReport.current?.driver}
      position={sampledPositionProperty.current}
      orientation={
        new VelocityOrientationProperty(sampledPositionProperty.current)
      }
      trackingReferenceFrame={TrackingReferenceFrame.INERTIAL}
      name={lastReport.current ? lastReport.current.driver : ''}
    >
      <ModelGraphics
        uri={'/low_poly_f1.glb'}
        scale={0.4}
        runAnimations={true}
        distanceDisplayCondition={new DistanceDisplayCondition(1, 400)}
      />
      <BillboardGraphics
        image={'/red_bull_pin.png'}
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
  );
}

export default F1Cars;
