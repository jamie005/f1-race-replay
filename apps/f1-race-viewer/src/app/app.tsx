import { useEffect} from 'react';
import { Viewer } from "resium";
import useWebSocket from 'react-use-websocket';
import { F1CarTelemetryReport } from '@f1-race-replay/data-model'

export function App() {
  const { lastMessage, readyState, getWebSocket } = useWebSocket("ws://127.0.0.1:8765");
  
  useEffect(() => {
    if (!getWebSocket()) return;
    getWebSocket().binaryType = 'arraybuffer';
  }, [getWebSocket, readyState]);

  useEffect(() => {
    if (!lastMessage) return;
    if (!(lastMessage.data instanceof ArrayBuffer)) return;

    console.log("Received message:", F1CarTelemetryReport.decode(new Uint8Array(lastMessage.data)));
    
    
  }, [lastMessage]);

  return (
    <Viewer full></Viewer>
  );
}

export default App;
