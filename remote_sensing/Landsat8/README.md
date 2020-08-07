## Analysing Landsat 8 Satellite Images With Python Scientific Stack

#### Various image analyses of Landsat 8 data are explored:

 - [Explanation of Landsat 8 bands](https://github.com/GKalliatakis/HRBDT-UNHCR-Innovation/tree/master/Landsat8/landsat8_bands.py)
 - [Processing Landsat 8 color images](https://github.com/GKalliatakis/HRBDT-UNHCR-Innovation/blob/master/Landsat8/colour_img_processing_examples.py)
 - [Calculating NDVI](https://github.com/GKalliatakis/HRBDT-UNHCR-Innovation/tree/master/Landsat8/NDVI_calculation.py)

#### [Landsat 8 Bands](https://landsat.gsfc.nasa.gov/landsat-8/landsat-8-bands/) 
 
| Bands                        | Wavelength (micrometres) | Resolution (metres) |
|------------------------------|--------------------------|---------------------|
| Band 1 – Coastal aerosol     | 0.43 – 0.45              | 30                  |
| Band 2 – Blue                | 0.45 – 0.51              | 30                  |
| Band 3 – Green               | 0.53 – 0.59              | 30                  |
| Band 4 – Red                 | 0.64 – 0.67              | 30                  |
| Band 5 – Near Infrared (NIR) | 0.85 – 0.88              | 30                  |
| Band 6 – SWIR 1              | 1.57 – 1.65              | 30                  |
| Band 7 – SWIR 2              | 2.11 – 2.29              | 30                  |
| Band 8 – Panchromatic        | 0.50 – 0.68              | 15                  |
| Band 9 – Cirrus              | 1.36 – 1.38              | 30                  |


##### [The Many Band Combinations of Landsat 8](https://www.harrisgeospatial.com/Learn/Blogs/Blog-Details/ArtMID/10198/ArticleID/15691/The-Many-Band-Combinations-of-Landsat-8)


|               Name               | Combination |
|:--------------------------------:|:-----------:|
|           Natural Color          |    4 3 2    |
|        False Color (urban)       |    7 6 4    |
|    Color Infrared (vegetation)   |    5 4 3    |
|            Agriculture           |    6 5 2    |
|      Atmospheric Penetration     |    7 6 5    |
|        Healthy Vegetation        |    5 6 2    |
|            Land/Water            |    5 6 4    |
| Natural With Atmospheric Removal |    7 5 3    |
|        Shortwave Infrared        |    7 5 4    |
|        Vegetation Analysis       |    6 5 4    |


---


#### Normalized Difference Vegetation Index (NDVI)
The normalized difference vegetation index (NDVI) is used to assess the state of vegetation. 
In living plants chlorophyll-A, from the photosynthetic machinery, strongly absorbs red color; 
on the other hand, near-infrared light is strongly reflected. 
Live, healthy vegetation reflects around 8% of red light and 50% of near-infrared light. 
Dead, unhealthy, or sparse vegetation reflects approximately 30% of red light and 40% of near-infrared light.


[Milos Milijkovic - Analyzing Satellite Images with Python Scientific Stack - Video](https://www.youtube.com/watch?v=4QpwcjD2Lpw)

[NDVI from Landsat 8 in SNAP](https://www.youtube.com/watch?v=isCtts8-6Ls)




#### Enhanced Vegetation Index (EVI)
EVI is similar to Normalized Difference Vegetation Index (NDVI) and can be used to quantify vegetation greenness. 
However, EVI corrects for some atmospheric conditions and canopy background noise and is more sensitive in 
areas with dense vegetation. It incorporates an “L” value to adjust for canopy background, 
“C” values as coefficients for atmospheric resistance, and values from the blue band (B).  
These enhancements allow for index calculation as a ratio between the R and NIR values, 
while reducing the background noise, atmospheric noise, and saturation in most cases.

EVI = G * ((NIR - R) / (NIR + C1 * R – C2 * B + L))

In Landsat 4-7, EVI = 2.5 * ((Band 4 – Band 3) / (Band 4 + 6 * Band 3 – 7.5 * Band 1 + 1)).

In Landsat 8, EVI = 2.5 * ((Band 5 – Band 4) / (Band 5 + 6 * Band 4 – 7.5 * Band 2 + 1)).


#### Normalized Difference Water Index (NDWI)
Normalize Difference Water Index (NDWI) is use for the water bodies analysis. 
The index uses Green and Near infra-red bands of remote sensing images. 
The NDWI can enhance water information efficiently in most cases. 
It is sensitive to build-up land and result in over-estimated water bodies. 
The NDWI products can be used in conjunction with NDVI change products to assess context of apparent change areas.

NDWI = (NIR – SWIR) / (NIR + SWIR)

For Landsat 7 data, NDWI = (Band 4 – Band 5) / (Band 4 + Band 5)

For Landsat 8 data, NDWI = (Band 5 – Band 6) / (Band 5 + Band 6)



But result appear form above formula is poor in quality. The pure water neither reflects NIR nor SWIR. The formula of NDWI then modified by Xu (2005). It uses Green and SWIR band.

MNDWI = (Green – SWIR) / (Green + SWIR)

For Landsat 7 data, NDWI = (Band 2 – Band 5) / (Band 2 + Band 5)

For Landsat 8 data, NDWI = (Band 3 – Band 6) / (Band 3 + Band 6)


Similarly, Normalize Difference Water Index (NDWI) value lies between -1 to 1. 
Generally, water bodies NDWI value is greater than 0.5. 
Vegetation has much smaller values which distinguishing vegetation from water bodies easily. 
Build-up features having positive values lies between 0 to 0.2. 



