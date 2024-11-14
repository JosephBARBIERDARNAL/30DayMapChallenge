library(rayshader)
library(terra)

localtif <- raster::raster("data/EBK1KM/ebk1km1.tif")

elevation_matrix <- raster_to_matrix(localtif)

elevation_matrix %>%
  sphere_shade(texture = "desert") %>%
  add_water(detect_water(elevation_matrix), color = "desert") %>%
  add_shadow(ray_shade(elevation_matrix, zscale = 3), 0.5) %>%
  add_shadow(ambient_shade(elevation_matrix), 0) %>%
  plot_3d(elevation_matrix)
render_snapshot()
