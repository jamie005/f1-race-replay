import { useEffect, useRef } from 'react';
import { Entity, Viewer, Clock } from "resium";
import useWebSocket from 'react-use-websocket';
import { F1CarTelemetryReport } from '@f1-race-replay/data-model'
import { Cartesian3, Color, ExtrapolationType, JulianDate, SampledPositionProperty, LagrangePolynomialApproximation, LinearApproximation } from 'cesium';

export function App() {
  const { lastMessage, readyState, getWebSocket } = useWebSocket("ws://127.0.0.1:8765");
  const lastReport = useRef<F1CarTelemetryReport | null>(null);
  const sampledPositionProperty = useRef<SampledPositionProperty>(
    new SampledPositionProperty()
  );
  
  // Set interpolation options once
  useEffect(() => {
    sampledPositionProperty.current.forwardExtrapolationType = ExtrapolationType.HOLD;
    sampledPositionProperty.current.forwardExtrapolationDuration = 10;
    sampledPositionProperty.current.setInterpolationOptions({
      interpolationDegree: 1,
      interpolationAlgorithm: LinearApproximation,
    });
  }, []);

  useEffect(() => {
    if (!getWebSocket()) return;
    getWebSocket().binaryType = 'arraybuffer';
  }, [getWebSocket, readyState]);

  useEffect(() => {
    if (!lastMessage) return;
    if (!(lastMessage.data instanceof ArrayBuffer)) return;

    const report: F1CarTelemetryReport = F1CarTelemetryReport.decode(new Uint8Array(lastMessage.data))
    console.log("Received message:", report);
    lastReport.current = report;
    sampledPositionProperty.current.addSample(
      JulianDate.fromDate(new Date(Date.now() + 3000)),
      Cartesian3.fromDegrees(report.longitude, report.latitude, 0)
    );


  }, [lastMessage]);

  return (
    <Viewer full>
      <Clock shouldAnimate/>
      <Entity
        key={lastReport.current?.driver}
        position={sampledPositionProperty.current}
        point={{ pixelSize: 10, color: Color.RED }}
      />
    </Viewer>
  );
}

export default App;
