import { useEffect, useRef } from 'react';
import { Entity, Viewer, Clock, ModelGraphics } from 'resium';
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
    <Viewer full>
      <Clock shouldAnimate />
      <Entity
        key={lastReport.current?.driver}
        position={sampledPositionProperty.current}
        orientation={
          new VelocityOrientationProperty(sampledPositionProperty.current)
        }
        point={{ pixelSize: 10, color: Color.RED }}
        trackingReferenceFrame={TrackingReferenceFrame.INERTIAL}
        description={
          lastReport.current
            ? `
          Driver: ${lastReport.current.driver} <br/>
          Speed: ${lastReport.current.speedKmh} km/h <br/>
          Engine RPM: ${lastReport.current.engineRpm} <br/>
          Gear: ${lastReport.current.gear} <br/>
          Throttle Actuation: ${lastReport.current.throttlePercent}% <br/>
          Brake Actuation: ${lastReport.current.brakeOn}
          `
            : 'No data yet'
        }
      >
        <ModelGraphics uri={'./src/assets/CesiumMilkTruck.glb'} />
      </Entity>
    </Viewer>
  );
}

export default App;
