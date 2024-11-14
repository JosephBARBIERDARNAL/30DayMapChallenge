library(sf)
library(cartogram)
library(tidyverse)

region <- read_sf("data/china-counties.geojson")
# df <- read.csv("data/french-population.csv")
# region <- st_as_sf(merge(df, region, by.x = "Département", by.y = "nom", all = FALSE))

region_mercator <- st_transform(region, 3857)
region_cartogram <- cartogram_cont(region_mercator, "Total", itermax = 5)
region_cartogram <- st_transform(region_cartogram, st_crs(region))

ggplot(region_cartogram) +
  geom_sf(aes(fill = Total), linewidth = 0, alpha = 0.9) +
  theme_void()

ggsave("cartogram.png", dpi = 500)
