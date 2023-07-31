/*
 * Leaflet.curve v0.6.0 - a plugin for Leaflet mapping library. https://github.com/elfalem/Leaflet.curve
 * (c) elfalem 2015-2020
 */
/*
 * note that SVG (x, y) corresponds to (long, lat)
 */

L.Spline = L.Path.extend({
	options: {
	},

	initialize: function(path, options){
		L.setOptions(this, options);
		this._setPath(path);
	},

	// Added to follow the naming convention of L.Polyline and other Leaflet component classes:
	// (https://leafletjs.com/reference-1.6.0.html#polyline-setlatlngs)
	setLatLngs: function(path) {
		return this.setPath(path);
	},

	_updateBounds: function() {
		// Empty function to satisfy L.Path.setStyle() method
	},

	getPath: function(){
		return this._coords;
	},

	setPath: function(path){
		this._setPath(path);
		return this.redraw();
	},

	getBounds: function() {
		return this._bounds;
	},

	_setPath: function(path){
		this._coords = path;
		this._bounds = this._computeBounds();
	},

	//修改
	_computeBounds: function(){
		var bound = new L.LatLngBounds();
		for(let i=0;i<this._coords.length;i++){
			bound.extend(this._coords[i]);
		}
		return bound;
	},

	getCenter: function () {
		return this._bounds.getCenter();
	},

	_update: function(){
		if (!this._map) { return; }

		this._updatePath();
	},

	_updatePath: function() {
		if(this._usingCanvas){
			this._updateCurveCanvas();
		}else{
			this._updateCurveSvg();
		}
	},

	_project: function() {
		var coord, curPoint;
		this._points = [];
		for(var i = 0; i < this._coords.length; i++){
			coord = this._coords[i];
			curPoint = this._latLngToPointFn.call(this._map, coord);
			this._points.push(curPoint);
		}
	},

	_curvePointsToPath: function(points){
		var point, str = '';
		for(var i = 0; i < points.length; i++){
			point = points[i];
			str += 'L';
			str += point.x + ',' + point.y + ' ';
		}
		return str || 'M0 0';
	},

	beforeAdd: function(map){
		L.Path.prototype.beforeAdd.call(this, map);

		this._usingCanvas = this._renderer instanceof L.Canvas;

		this._latLngToPointFn = this._usingCanvas ? map.latLngToContainerPoint : map.latLngToLayerPoint;
		if(this._usingCanvas){
			this._pathSvgElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');
		}
	},

	onAdd: function(map){
		if(this._usingCanvas){
			// determine if dash array is set by user
			this._canvasSetDashArray = !this.options.dashArray;
		}

		L.Path.prototype.onAdd.call(this, map); // calls _update()

		if(this._usingCanvas){
			this._animationCanvasElement = this._insertCustomCanvasElement();

			this._resizeCanvas();

			map.on('resize', this._resizeCanvas, this);

			if(this.options.animate && typeof(TWEEN) === 'object'){
				this._pathLength = this._pathSvgElement.getTotalLength();

				this._normalizeCanvasAnimationOptions();

				this._tweenedObject = {offset: this._pathLength};
				this._tween = new TWEEN.Tween(this._tweenedObject)
					.to({offset: 0}, this.options.animate.duration)
					// difference of behavior with SVG, delay occurs on every iteration
					.delay(this.options.animate.delay)
					.repeat(this.options.animate.iterations - 1)
					.onComplete(function(scope){
						return function(){
							scope._canvasAnimating = false;
						}
					}(this))
					.start();

				this._canvasAnimating = true;
				this._animateCanvas();
			}else{
				this._canvasAnimating = false;
			}
		}else{
			if(this.options.animate && this._path.animate){
				var length = this._svgSetDashArray();

				this._path.animate([
					{strokeDashoffset: length},
					{strokeDashoffset: 0}
				], this.options.animate);
			}
		}
	},

	onRemove: function(map){
		L.Path.prototype.onRemove.call(this, map);

		if(this._usingCanvas){
			this._clearCanvas();
			L.DomUtil.remove(this._animationCanvasElement);
			map.off('resize', this._resizeCanvas, this);
		}
	},

	// SVG specific logic
	_updateCurveSvg: function(){
		this._renderer._setPath(this, this._curvePointsToPath(this._points));

		if(this.options.animate){
			this._svgSetDashArray();
		}
	},

	_svgSetDashArray: function(){
		var path = this._path;
		var length = path.getTotalLength();

		if(!this.options.dashArray){
			path.style.strokeDasharray = length + ' ' + length;
		}
		return length;
	},

	// Needed by the `Canvas` renderer for interactivity
	_containsPoint: function(layerPoint) {
		return this._bounds.contains(this._map.layerPointToLatLng(layerPoint));
	},

	// Canvas specific logic below here
	_insertCustomCanvasElement: function(){
		var element = L.DomUtil.create('canvas', 'leaflet-zoom-animated');
		var originProp = L.DomUtil.testProp(['transformOrigin', 'WebkitTransformOrigin', 'msTransformOrigin']);
		element.style[originProp] = '50% 50%';
		var pane = this._map.getPane(this.options.pane);
		pane.insertBefore(element, pane.firstChild);

		return element;
	},

	_normalizeCanvasAnimationOptions: function(){
		var opts = {
			delay: 0,
			duration: 0,
			iterations:	1
		};
		if(typeof(this.options.animate) == "number"){
			opts.duration = this.options.animate;
		}else{
			if(this.options.animate.duration){
				opts.duration = this.options.animate.duration;
			}
			if(this.options.animate.delay){
				opts.delay =this.options.animate.delay;
			}
			if(this.options.animate.iterations){
				opts.iterations = this.options.animate.iterations;
			}
		}

		this.options.animate = opts;
	},

	_updateCurveCanvas: function(){
		this._project();

		var pathString = this._curvePointsToPath(this._points);
		this._pathSvgElement.setAttribute('d', pathString);

		if(this.options.animate && typeof(TWEEN) === 'object' && this._canvasSetDashArray){
			this._pathLength = this._pathSvgElement.getTotalLength();
			this.options.dashArray = this._pathLength + '';
			this._renderer._updateDashArray(this);
		}

		this._path2d = new Path2D(pathString);

		if(this._animationCanvasElement){
			this._resetCanvas();
		}


	},

	_animationCanvasElement: null,

	_resizeCanvas: function() {
		var size = this._map.getSize();
		this._animationCanvasElement.width = size.x;
		this._animationCanvasElement.height = size.y;

		this._resetCanvas();
	},

	_resetCanvas: function() {
		var topLeft = this._map.containerPointToLayerPoint([0, 0]);
		L.DomUtil.setPosition(this._animationCanvasElement, topLeft);

		this._redrawCanvas();
	},

	_redrawCanvas: function(){
		if(!this._canvasAnimating){
			this._clearCanvas();
			var ctx = this._animationCanvasElement.getContext('2d');
			this._curveFillStroke(this._path2d, ctx);
		}
	},

	_clearCanvas: function() {
		this._animationCanvasElement.getContext('2d').clearRect(0, 0, this._animationCanvasElement.width, this._animationCanvasElement.height);
	},

	_animateCanvas: function(time){
		TWEEN.update(time);

		var ctx = this._animationCanvasElement.getContext('2d');
		ctx.clearRect(0, 0, this._animationCanvasElement.width, this._animationCanvasElement.height);
		ctx.lineDashOffset = this._tweenedObject.offset;

		this._curveFillStroke(this._path2d, ctx);

		if(this._canvasAnimating){
			this._animationFrameId = L.Util.requestAnimFrame(this._animateCanvas, this);
		}
	},

	// similar to Canvas._fillStroke(ctx, layer)
	_curveFillStroke: function (path2d, ctx) {
		var options = this.options;

		if (options.fill) {
			ctx.globalAlpha = options.fillOpacity;
			ctx.fillStyle = options.fillColor || options.color;
			ctx.fill(path2d, options.fillRule || 'evenodd');
		}

		if (options.stroke && options.weight !== 0) {
			if (ctx.setLineDash) {
				ctx.setLineDash(this.options && this.options._dashArray || []);
			}
			ctx.globalAlpha = options.opacity;
			ctx.lineWidth = options.weight;
			ctx.strokeStyle = options.color;
			ctx.lineCap = options.lineCap;
			ctx.lineJoin = options.lineJoin;
			ctx.stroke(path2d);
		}
	},

	// path tracing logic below here
	trace: function() {
		for(let i=0;i<points.length;i++){
			var x = x.push.apply(points[i].x);
			var y = y.push.apply(points[i].y);
		}
		var samples = [].concat(this.give_nodes(x,y));
		return samples;
	},

	give_nodes:function (x, y, lval=0, rval=0){
    	let res = solution_of_equation(spline3_Parameters(x), x, y);
    	//for i in range(len(x) - 1):
    	//    print(f"x in [{x[i]:.3f}, {x[i + 1]:.3f}]: S(x) = {res[4 * i]:.3f}x^3 + {res[1 + 4 * i]:.3f}x^2 + {res[2 + 4 * i]:.3f}x + {res[3 + 4 * i]:.3f}");
    	var x_axis4 = [];
    	var y_axis4 = [];
    	for(let i=0;i<x.length - 1;i++){
        	//let temp = math.range(x[i], x[i + 1], 0.01);
        	return map(interval => {
        		x_axis4 = x_axis4.push.apply(interval);
        		y_axis4 = y_axis4.push.apply(calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], interval))
				return this._map.layerPointToLatLng([x, y]);
        	});
    	}
	},

	spline3_Parameters: function spline3_Parameters(x_vec){
		//建立三对角矩阵的 4n 个方程的左边部分
		//parameter为二维数组，用来存放参数，size_of_Interval为区间的个数
		let x_new = [].concat(x_vec);
		//let x_new = math.clone(x_vec);
		let parameter = [];
		let size_of_Interval = x_new.length - 1;
		let i = 1;
		// 相邻两区间公共节点处函数值相等的方程，共2n-2个
		while (i < x_new.length - 1){
			let data = math.zeros(size_of_Interval * 4);
			//let data = new Array(size_of_Interval * 4).fill(0);
			data[(i - 1) * 4] = x_new[i] * x_new[i] * x_new[i];
			data[(i - 1) * 4 + 1] = x_new[i] * x_new[i];
			data[(i - 1) * 4 + 2] = x_new[i];
			data[(i - 1) * 4 + 3] = 1;
			parameter.push(data);

			//data = new Array(size_of_Interval * 4).fill(0);
			data = math.zeros(size_of_Interval * 4);
			data[i * 4] = x_new[i] * x_new[i] * x_new[i];
			data[i * 4 + 1] = x_new[i] * x_new[i];
			data[i * 4 + 2] = x_new[i];
			data[i * 4 + 3] = 1;
			parameter.push(data);
			i += 1;
		}
		// 左右端点处的函数值。为两个方程, 加上前面的2n-2个方程，一共2n个方程
		//let data = new Array(size_of_Interval * 4).fill(0);
		let data = math.zeros(size_of_Interval * 4);
		data[0] = x_new[0] * x_new[0] * x_new[0];
		data[1] = x_new[0] * x_new[0];
		data[2] = x_new[0];
		data[3] = 1;
		parameter.push(data);
		//data = new Array(size_of_Interval * 4).fill(0);
		data = math.zeros(size_of_Interval * 4);
		data[(size_of_Interval - 1) * 4] = x_new[x_new.length - 1] * x_new[x_new.length - 1] * x_new[x_new.length - 1];
		data[(size_of_Interval - 1) * 4 + 1] = x_new[x_new.length - 1] * x_new[x_new.length - 1];
		data[(size_of_Interval - 1) * 4 + 2] = x_new[x_new.length - 1];
		data[(size_of_Interval - 1) * 4 + 3] = 1;
		parameter.push(data);
		//端点函数一阶导数值相等为n-1个方程。加上前面的方程为3n-1个方程。
		i = 1;
		while(i < size_of_Interval)
		{
			//data = new Array(size_of_Interval * 4).fill(0);
			let data = math.zeros(size_of_Interval * 4);
			data[(i - 1) * 4] = 3 * x_new[i] * x_new[i];
			data[(i - 1) * 4 + 1] = 2 * x_new[i];
			data[(i - 1) * 4 + 2] = 1;
			data[i * 4] = -3 * x_new[i] * x_new[i];
			data[i * 4 + 1] = -2 * x_new[i];
			data[i * 4 + 2] = -1;
			parameter.push(data);
			i += 1
		}
		i = 1;
		while(i < x_new.length - 1){
			//data = new Array(size_of_Interval * 4).fill(0);
			let data = math.zeros(size_of_Interval * 4);
			data[(i - 1) * 4] = 6 * x_new[i];
			data[(i - 1) * 4 + 1] = 2;
			data[i * 4] = -6 * x_new[i];
			data[i * 4 + 1] = -2;
			parameter.push(data);
			i += 1
		}
		//两个附加条件
		//默认情况：opt = 0，not-a-knot边界条件：左边两端点三阶导相等，右边两端点三阶导也相等
		//data = new Array(size_of_Interval * 4).fill(0);
		data = math.zeros(size_of_Interval * 4);
		data[0] = 6;
		data[4] = -6;
		parameter.push(data);
		//data = np.zeros(size_of_Interval * 4);
		data = math.zeros(size_of_Interval * 4);
		data[-4] = 6;
		data[-8] = -6;
		parameter.push(data);

		return parameter
	},

	solution_of_equation: function (parametes, x, y=0){
		//建立三对角线性方程组并求解，得到各段三次函数的系数并返回
		//functype 表示需要拟合的是给定函数 / 给定点集
		let size_of_Interval = x.length - 1;
		//let result = new Array(size_of_Interval * 4).fill(0);
		let result = math.zeros(size_of_Interval * 4);
		let i = 1;

		if(x.length !== y.length){
			throw {Error:"Expect a node set!"}
			//     raise ValueError("Expect a node set!");
		}
		while(i < size_of_Interval){
			result[(i - 1) * 2] = y[i];
			result[(i - 1) * 2 + 1] = y[i];
			i += 1;
		}
		result[(size_of_Interval - 1) * 2] = y[0];
		result[(size_of_Interval - 1) * 2 + 1] = y[y.length-1];

		//默认情况：opt = 0，not-a-knot边界条件：左边两端点三阶导相等，右边两端点三阶导也相等
		result[result.length-2] = result[result.length-1] = 0;

		let a = [].concat(parametes);
		let b = [].concat(result);
	//    return np.linalg.solve(a, b)
		return math.lsolve(a,b);
	},

	calculate: function(paremeters, x){
		//计算x在拟合得到的函数中的点值
		let res = [];
		for(let dx in x)
			res.push(paremeters[0] * dx * dx * dx + paremeters[1] * dx * dx + paremeters[2] * dx + paremeters[3]);
		return res
	}

});

L.spline = function (path, options){
	return new L.Spline(path, options);
};
