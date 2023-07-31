!function(t){var n={};function e(i){if(n[i])return n[i].exports;var a=n[i]={i:i,l:!1,exports:{}};return t[i].call(a.exports,a,a.exports,e),a.l=!0,a.exports}e.m=t,e.c=n,e.d=function(t,n,i){e.o(t,n)||Object.defineProperty(t,n,{enumerable:!0,get:i})},e.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},e.t=function(t,n){if(1&n&&(t=e(t)),8&n)return t;if(4&n&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(e.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&n&&"string"!=typeof t)for(var a in t)e.d(i,a,function(n){return t[n]}.bind(null,a));return i},e.n=function(t){var n=t&&t.__esModule?function(){return t.default}:function(){return t};return e.d(n,"a",n),n},e.o=function(t,n){return Object.prototype.hasOwnProperty.call(t,n)},e.p="",e(e.s=0)}([function(t,n){L.Curve=L.Path.extend({options:{},initialize:function(t,n){L.setOptions(this,n),this._setPath(t)},setLatLngs:function(t){return this.setPath(t)},_updateBounds:function(){},getPath:function(){return this._coords},setPath:function(t){return this._setPath(t),this.redraw()},getBounds:function(){return this._bounds},_setPath:function(t){this._coords=t,this._bounds=this._computeBounds()},_computeBounds:function(){for(var t,n,e,i=new L.LatLngBounds,a=0;a<this._coords.length;a++)if("string"==typeof(e=this._coords[a])||e instanceof String)n=e;else if("H"==n)i.extend([t.lat,e[0]]),t=new L.latLng(t.lat,e[0]);else if("V"==n)i.extend([e[0],t.lng]),t=new L.latLng(e[0],t.lng);else if("C"==n){var s=new L.latLng(e[0],e[1]);e=this._coords[++a];var o=new L.latLng(e[0],e[1]);e=this._coords[++a];var r=new L.latLng(e[0],e[1]);i.extend(s),i.extend(o),i.extend(r),r.controlPoint1=s,r.controlPoint2=o,t=r}else if("S"==n){o=new L.latLng(e[0],e[1]);e=this._coords[++a];r=new L.latLng(e[0],e[1]),s=t;if(t.controlPoint2){var h=t.lat-t.controlPoint2.lat,l=t.lng-t.controlPoint2.lng;s=new L.latLng(t.lat+h,t.lng+l)}i.extend(s),i.extend(o),i.extend(r),r.controlPoint1=s,r.controlPoint2=o,t=r}else if("Q"==n){var c=new L.latLng(e[0],e[1]);e=this._coords[++a];r=new L.latLng(e[0],e[1]);i.extend(c),i.extend(r),r.controlPoint=c,t=r}else if("T"==n){r=new L.latLng(e[0],e[1]),c=t;if(t.controlPoint){h=t.lat-t.controlPoint.lat,l=t.lng-t.controlPoint.lng;c=new L.latLng(t.lat+h,t.lng+l)}i.extend(c),i.extend(r),r.controlPoint=c,t=r}else i.extend(e),t=new L.latLng(e[0],e[1]);return i},getCenter:function(){return this._bounds.getCenter()},_update:function(){this._map&&this._updatePath()},_updatePath:function(){this._usingCanvas?this._updateCurveCanvas():this._updateCurveSvg()},_project:function(){var t,n,e,i;this._points=[];for(var a=0;a<this._coords.length;a++)if("string"==typeof(t=this._coords[a])||t instanceof String)this._points.push(t),e=t;else{switch(t.length){case 2:i=this._latLngToPointFn.call(this._map,t),n=t;break;case 1:"H"==e?(i=this._latLngToPointFn.call(this._map,[n[0],t[0]]),n=[n[0],t[0]]):(i=this._latLngToPointFn.call(this._map,[t[0],n[1]]),n=[t[0],n[1]])}this._points.push(i)}},_curvePointsToPath:function(t){for(var n,e,i="",a=0;a<t.length;a++)if("string"==typeof(n=t[a])||n instanceof String)i+=e=n;else switch(e){case"H":i+=n.x+" ";break;case"V":i+=n.y+" ";break;default:i+=n.x+","+n.y+" "}return i||"M0 0"},beforeAdd:function(t){L.Path.prototype.beforeAdd.call(this,t),this._usingCanvas=this._renderer instanceof L.Canvas,this._latLngToPointFn=this._usingCanvas?t.latLngToContainerPoint:t.latLngToLayerPoint,this._usingCanvas&&(this._pathSvgElement=document.createElementNS("http://www.w3.org/2000/svg","path"))},onAdd:function(t){if(this._usingCanvas&&(this._canvasSetDashArray=!this.options.dashArray),L.Path.prototype.onAdd.call(this,t),this._usingCanvas)this._animationCanvasElement=this._insertCustomCanvasElement(),this._resizeCanvas(),t.on("resize",this._resizeCanvas,this),this.options.animate&&"object"==typeof TWEEN?(this._pathLength=this._pathSvgElement.getTotalLength(),this._normalizeCanvasAnimationOptions(),this._tweenedObject={offset:this._pathLength},this._tween=new TWEEN.Tween(this._tweenedObject).to({offset:0},this.options.animate.duration).delay(this.options.animate.delay).repeat(this.options.animate.iterations-1).onComplete(function(t){return function(){t._canvasAnimating=!1}}(this)).start(),this._canvasAnimating=!0,this._animateCanvas()):this._canvasAnimating=!1;else if(this.options.animate&&this._path.animate){var n=this._svgSetDashArray();this._path.animate([{strokeDashoffset:n},{strokeDashoffset:0}],this.options.animate)}},onRemove:function(t){L.Path.prototype.onRemove.call(this,t),this._usingCanvas&&(this._clearCanvas(),L.DomUtil.remove(this._animationCanvasElement),t.off("resize",this._resizeCanvas,this))},_updateCurveSvg:function(){this._renderer._setPath(this,this._curvePointsToPath(this._points)),this.options.animate&&this._svgSetDashArray()},_svgSetDashArray:function(){var t=this._path,n=t.getTotalLength();return this.options.dashArray||(t.style.strokeDasharray=n+" "+n),n},_containsPoint:function(t){return this._bounds.contains(this._map.layerPointToLatLng(t))},_insertCustomCanvasElement:function(){var t=L.DomUtil.create("canvas","leaflet-zoom-animated"),n=L.DomUtil.testProp(["transformOrigin","WebkitTransformOrigin","msTransformOrigin"]);t.style[n]="50% 50%";var e=this._map.getPane(this.options.pane);return e.insertBefore(t,e.firstChild),t},_normalizeCanvasAnimationOptions:function(){var t={delay:0,duration:0,iterations:1};"number"==typeof this.options.animate?t.duration=this.options.animate:(this.options.animate.duration&&(t.duration=this.options.animate.duration),this.options.animate.delay&&(t.delay=this.options.animate.delay),this.options.animate.iterations&&(t.iterations=this.options.animate.iterations)),this.options.animate=t},_updateCurveCanvas:function(){this._project();var t=this._curvePointsToPath(this._points);this._pathSvgElement.setAttribute("d",t),this.options.animate&&"object"==typeof TWEEN&&this._canvasSetDashArray&&(this._pathLength=this._pathSvgElement.getTotalLength(),this.options.dashArray=this._pathLength+"",this._renderer._updateDashArray(this)),this._path2d=new Path2D(t),this._animationCanvasElement&&this._resetCanvas()},_animationCanvasElement:null,_resizeCanvas:function(){var t=this._map.getSize();this._animationCanvasElement.width=t.x,this._animationCanvasElement.height=t.y,this._resetCanvas()},_resetCanvas:function(){var t=this._map.containerPointToLayerPoint([0,0]);L.DomUtil.setPosition(this._animationCanvasElement,t),this._redrawCanvas()},_redrawCanvas:function(){if(!this._canvasAnimating){this._clearCanvas();var t=this._animationCanvasElement.getContext("2d");this._curveFillStroke(this._path2d,t)}},_clearCanvas:function(){this._animationCanvasElement.getContext("2d").clearRect(0,0,this._animationCanvasElement.width,this._animationCanvasElement.height)},_animateCanvas:function(t){TWEEN.update(t);var n=this._animationCanvasElement.getContext("2d");n.clearRect(0,0,this._animationCanvasElement.width,this._animationCanvasElement.height),n.lineDashOffset=this._tweenedObject.offset,this._curveFillStroke(this._path2d,n),this._canvasAnimating&&(this._animationFrameId=L.Util.requestAnimFrame(this._animateCanvas,this))},_curveFillStroke:function(t,n){var e=this.options;e.fill&&(n.globalAlpha=e.fillOpacity,n.fillStyle=e.fillColor||e.color,n.fill(t,e.fillRule||"evenodd")),e.stroke&&0!==e.weight&&(n.setLineDash&&n.setLineDash(this.options&&this.options._dashArray||[]),n.globalAlpha=e.opacity,n.lineWidth=e.weight,n.strokeStyle=e.color,n.lineCap=e.lineCap,n.lineJoin=e.lineJoin,n.stroke(t))},trace:function(t){var n,e,i,a,s,o,r;t=t.filter(function(t){return t>=0&&t<=1});for(var h=[],l=0;l<this._points.length;l++)if("string"==typeof(n=this._points[l])||n instanceof String)"Z"==(e=n)&&(h=h.concat(this._linearTrace(t,a,i)));else switch(e){case"M":i=n,a=n;break;case"L":case"H":case"V":h=h.concat(this._linearTrace(t,a,n)),a=n;break;case"C":s=n,o=this._points[++l],r=this._points[++l],h=h.concat(this._cubicTrace(t,a,s,o,r)),a=r;break;case"S":s=this._reflectPoint(o,a),o=n,r=this._points[++l],h=h.concat(this._cubicTrace(t,a,s,o,r)),a=r;break;case"Q":s=n,o=this._points[++l],h=h.concat(this._quadraticTrace(t,a,s,o)),a=o;break;case"T":s=this._reflectPoint(s,a),o=n,h=h.concat(this._quadraticTrace(t,a,s,o)),a=o}return h},_linearTrace:function(t,n,e){return t.map(t=>{var i=this._singleLinearTrace(t,n.x,e.x),a=this._singleLinearTrace(t,n.y,e.y);return this._map.layerPointToLatLng([i,a])})},_quadraticTrace:function(t,n,e,i){return t.map(t=>{var a=this._singleQuadraticTrace(t,n.x,e.x,i.x),s=this._singleQuadraticTrace(t,n.y,e.y,i.y);return this._map.layerPointToLatLng([a,s])})},_cubicTrace:function(t,n,e,i,a){return t.map(t=>{var s=this._singleCubicTrace(t,n.x,e.x,i.x,a.x),o=this._singleCubicTrace(t,n.y,e.y,i.y,a.y);return this._map.layerPointToLatLng([s,o])})},_singleLinearTrace:function(t,n,e){return n+t*(e-n)},_singleQuadraticTrace:function(t,n,e,i){var a=1-t;return Math.pow(a,2)*n+2*a*t*e+Math.pow(t,2)*i},_singleCubicTrace:function(t,n,e,i,a){var s=1-t;return Math.pow(s,3)*n+3*Math.pow(s,2)*t*e+3*s*Math.pow(t,2)*i+Math.pow(t,3)*a},_reflectPoint:function(t,n){return x=n.x+(n.x-t.x),y=n.y+(n.y-t.y),L.point(x,y)}}),L.curve=function(t,n){return new L.Curve(t,n)}}]);