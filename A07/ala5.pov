#version 3.6;

global_settings {
  assumed_gamma 1.0
}

background { color rgb <0.97, 0.98, 1.0> }

camera {
  location <0, 0, -34>
  look_at <0, 0, 0>
  angle 50
  right x * image_width / image_height
}

light_source {
  <-8, 12, -14>
  color rgb <1, 1, 1>
}

light_source {
  <10, 4, -8>
  color rgb <0.55, 0.62, 0.8>
}

#include "alanine.pov"

#declare PentagonRadius = 8;
#for (vertex, 0, 4)
  #declare Angle = 90 + 72 * vertex;
  object {
    mol_0
    translate mol_0_center
    translate <PentagonRadius * cos(Angle), PentagonRadius * sin(Angle), 0>
  }
#end
