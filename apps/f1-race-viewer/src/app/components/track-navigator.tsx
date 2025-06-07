import {
  Color,
  ConstantProperty,
  DistanceDisplayCondition,
  Cartesian3,
  JulianDate,
  Transforms,
  Matrix4,
  LabelGraphics as CesiumLabelGraphics,
} from 'cesium';
import { useState } from 'react';
import { CameraFlyTo, GeoJsonDataSource } from 'resium';

export function TrackNavigator() {
  const [cameraPosition, setCameraPosition] = useState<Cartesian3 | undefined>(
    undefined
  );
  return (
    <>
      {cameraPosition && (
        <CameraFlyTo duration={3} destination={cameraPosition} />
      )}
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
        onClick={(m, target) => {
          const track_location: Cartesian3 | undefined =
            target.id.position.getValue(JulianDate.now());
          if (track_location) {
            const offset = Cartesian3.fromElements(0, 0, 4000);
            const enuTransform =
              Transforms.eastNorthUpToFixedFrame(track_location);
            const cameraDestination = Matrix4.multiplyByPoint(
              enuTransform,
              offset,
              new Cartesian3()
            );
            setCameraPosition(cameraDestination);
          }
        }}
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
    </>
  );
}

export default TrackNavigator;
