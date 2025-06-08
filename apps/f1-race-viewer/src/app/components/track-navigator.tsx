import {
  Color,
  ConstantProperty,
  DistanceDisplayCondition,
  Cartesian3,
  JulianDate,
  Transforms,
  Matrix4,
  LabelGraphics as CesiumLabelGraphics,
  GeoJsonDataSource as CesiumGeoJsonDataSource,
  Cartesian2,
} from 'cesium';
import { useCallback, useState } from 'react';
import {
  CameraFlyTo,
  CesiumMovementEvent,
  EventTarget,
  GeoJsonDataSource,
} from 'resium';

const TRACK_NAVIGATOR_COLOUR_SCHEME: Color = Color.RED;
const PIN_OUTLINE_TRANSITION_DISTANCE_METERS = 10000;

export function TrackNavigator() {
  const [cameraPosition, setCameraPosition] = useState<Cartesian3 | undefined>(
    undefined
  );

  const handleF1TrackPinsLoaded = useCallback(
    (geoJsonDataSource: CesiumGeoJsonDataSource) => {
      geoJsonDataSource.entities.values.forEach((entity) => {
        entity.label = new CesiumLabelGraphics({
          text: entity.properties?.location,
          font: '24px Helvetica',
          pixelOffset: Cartesian2.fromElements(0, 10),
          distanceDisplayCondition: new DistanceDisplayCondition(
            PIN_OUTLINE_TRANSITION_DISTANCE_METERS,
            99999999
          ),
        });
        if (!entity.billboard) return;
        entity.billboard.distanceDisplayCondition = new ConstantProperty(
          new DistanceDisplayCondition(
            PIN_OUTLINE_TRANSITION_DISTANCE_METERS,
            99999999
          )
        );
      });
    },
    []
  );

  const handleF1TrackOutlinesLoaded = useCallback(
    (geoJsonDataSource: CesiumGeoJsonDataSource) => {
      geoJsonDataSource.entities.values.forEach((entity) => {
        if (!entity.polyline) return;
        entity.polyline.distanceDisplayCondition = new ConstantProperty(
          new DistanceDisplayCondition(
            400,
            PIN_OUTLINE_TRANSITION_DISTANCE_METERS
          )
        );
      });
    },
    []
  );

  const handleF1TrackPinClicked = useCallback(
    (m: CesiumMovementEvent, target: EventTarget) => {
      const track_location: Cartesian3 | undefined =
        target.id?.position?.getValue(JulianDate.now());
      if (!track_location) return;
      const offset = Cartesian3.fromElements(0, 0, 4000);
      const enuTransform = Transforms.eastNorthUpToFixedFrame(track_location);
      const cameraDestination = Matrix4.multiplyByPoint(
        enuTransform,
        offset,
        new Cartesian3()
      );
      setCameraPosition(cameraDestination);
    },
    []
  );

  return (
    <>
      {cameraPosition && (
        <CameraFlyTo duration={3} destination={cameraPosition} />
      )}
      <GeoJsonDataSource
        data={'/f1-circuits.geojson'}
        stroke={TRACK_NAVIGATOR_COLOUR_SCHEME}
        strokeWidth={6}
        onLoad={(geoJsonDataSource) =>
          handleF1TrackOutlinesLoaded(geoJsonDataSource)
        }
      />
      <GeoJsonDataSource
        data={'/f1-locations.geojson'}
        markerColor={TRACK_NAVIGATOR_COLOUR_SCHEME}
        markerSymbol="car"
        onClick={(movement, target) =>
          handleF1TrackPinClicked(movement, target)
        }
        onLoad={(geoJsonDataSource) =>
          handleF1TrackPinsLoaded(geoJsonDataSource)
        }
      />
    </>
  );
}

export default TrackNavigator;
