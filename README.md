# PyHum Adaptation
PyHumAdaptation is the code written to adapt [PyHum](https://github.com/dbuscombe-usgs/PyHum) to process Humminbird images to fit specifications detailed in my paper:  
    Bollinger, M.A. and Kline R.J. (2017).  Validating side scan sonar as a fish survey tool over artificial reefs. Journal of Coastal Research. DOI: [10.2112/JCOASTRES-D-16-00174.1](http://www.jcronline.org/doi/abs/10.2112/JCOASTRES-D-16-00174.1)



It creates echograms that are:
<ol>
  <li>cropped at a user input depth</li>
  <li>focus on the water column of side scan sonar images</li>
  <li>correct for attenuation away from the transducer</li>
</ol>

![alt tag](http://dbuscombe-usgs.github.io/figs/Texas_reef_merged_cropped.png)
Artificial reef structure off the coast of South Padre Island with school of reef associated fish.
