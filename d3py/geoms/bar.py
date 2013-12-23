from geom import Geom, JavaScript, Selection, Function

class Bar(Geom):
    def __init__(self,x,y,**kwargs):
        """
        This is a vertical bar chart - the height of each bar represents the 
        magnitude of each class
        
        x : string
            name of the column that contains the class labels
        y : string
            name of the column that contains the magnitude of each class
        """
        Geom.__init__(self,**kwargs)
        self.x = x
        self.y = y
        self.name = "bar"
        self._id = 'bar_%s_%s'%(self.x,self.y)
        self._build_js()
        self._build_css()
        self.params = [x,y]
        self.styles = dict([(k[0].replace('_','-'), k[1]) for k in kwargs.items()])
    
    def _build_js(self):


        # build scales
        scales = """ 
            scales = {
                x : get_scales(['%s'], 'horizontal'),
                y : get_scales(['%s'], 'vertical')
            }
        """%(self.x, self.y)

        xfxn = Function(None, "d", "return scales.x(d.%s);"%self.x)
        yfxn = Function( None, "d", "return scales.y(d.%s)"%self.y)
        
        heightfxn = Function(
            None, 
            "d", 
            "return height - scales.y(d.%s)"%self.y
        )

        draw = Function("draw", ("data",), [scales])
        draw += scales
        draw += Selection("g").selectAll("'.bars'") \
            .data("data") \
            .enter() \
            .append("'rect'") \
            .attr("'class'", "'geom_bar'") \
            .attr("'id'", "'%s'"%self._id) \
            .attr("'x'", xfxn) \
            .attr("'y'", yfxn) \
            .attr("'width'", "scales.x.rangeBand()")\
            .attr("'height'", heightfxn)
        # TODO: rangeBand above breaks for histogram type bar-plots... fix!

        self.js = JavaScript() + draw
        self.js += (Function("init", autocall=True) + "console.debug('Hi');")
        return self.js
    
    def _build_css(self):
        bar = {
            "stroke-width": "1px",
             "stroke": "black",
             "fill-opacity": 0.7,
             "stroke-opacity": 1,
             "fill": "blue"
        }
        bar.update
        self.css[".geom_bar"] = bar 
        # arbitrary styles
        self.css["#"+self._id] = self.styles
        return self.css
