import { Viewer, Clock } from 'resium';
import { JulianDate } from 'cesium';
import TrackNavigator from './components/track-navigator';
import F1Cars from './components/f1-cars';

export function App() {
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
      <TrackNavigator />
      <F1Cars />
    </Viewer>
  );
}

export default App;
