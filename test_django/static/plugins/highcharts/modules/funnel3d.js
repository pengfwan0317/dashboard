/*
 Highcharts JS v8.0.2 (2020-03-03)

 Highcharts funnel module

 (c) 2010-2019 Kacper Madej

 License: www.highcharts.com/license
*/
(function(d){"object"===typeof module&&module.exports?(d["default"]=d,module.exports=d):"function"===typeof define&&define.amd?define("highcharts/modules/funnel3d",["highcharts","highcharts/highcharts-3d","highcharts/modules/cylinder"],function(t){d(t);d.Highcharts=t;return d}):d("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(d){function t(d,m,l,h){d.hasOwnProperty(m)||(d[m]=h.apply(null,l))}d=d?d._modules:{};t(d,"modules/funnel3d.src.js",[d["parts/Globals.js"],d["parts/Color.js"],
d["parts/Utilities.js"]],function(d,m,l){var h=m.parse,t=l.error,D=l.extend,k=l.merge,B=l.pick,v=l.relativeLength;l=l.seriesType;var H=d.charts,J=d.seriesTypes;m=d.Renderer.prototype;var K=m.cuboidPath;l("funnel3d","column",{center:["50%","50%"],width:"90%",neckWidth:"30%",height:"100%",neckHeight:"25%",reversed:!1,gradientForSides:!0,animation:!1,edgeWidth:0,colorByPoint:!0,showInLegend:!1,dataLabels:{align:"right",crop:!1,inside:!1,overflow:"allow"}},{bindAxes:function(){d.Series.prototype.bindAxes.apply(this,
arguments);D(this.xAxis.options,{gridLineWidth:0,lineWidth:0,title:null,tickPositions:[]});D(this.yAxis.options,{gridLineWidth:0,title:null,labels:{enabled:!1}})},translate3dShapes:d.noop,translate:function(){d.Series.prototype.translate.apply(this,arguments);var a=0,b=this.chart,c=this.options,g=c.reversed,u=c.ignoreHiddenPoint,e=b.plotWidth,E=b.plotHeight,f=0,I=c.center,w=v(I[0],e),r=v(I[1],E),l=v(c.width,e),p,k,n=v(c.height,E),m=v(c.neckWidth,e),t=v(c.neckHeight,E),h=r-n/2+n-t;e=this.data;var z,
F,x,A,G,C,q;this.getWidthAt=k=function(b){var a=r-n/2;return b>h||n===t?m:m+(l-m)*(1-(b-a)/(n-t))};this.center=[w,r,n];this.centerX=w;e.forEach(function(b){u&&!1===b.visible||(a+=b.y)});e.forEach(function(e){G=null;z=a?e.y/a:0;x=r-n/2+f*n;A=x+z*n;p=k(x);C=A-x;q={gradientForSides:B(e.options.gradientForSides,c.gradientForSides),x:w,y:x,height:C,width:p,z:1,top:{width:p}};p=k(A);q.bottom={fraction:z,width:p};x>=h?q.isCylinder=!0:A>h&&(G=A,p=k(h),A=h,q.bottom.width=p,q.middle={fraction:C?(h-x)/C:0,width:p});
g&&(q.y=x=r+n/2-(f+z)*n,q.middle&&(q.middle.fraction=1-(C?q.middle.fraction:0)),p=q.width,q.width=q.bottom.width,q.bottom.width=p);e.shapeArgs=D(e.shapeArgs,q);e.percentage=100*z;e.plotX=w;e.plotY=g?r+n/2-(f+z/2)*n:(x+(G||A))/2;F=d.perspective([{x:w,y:e.plotY,z:g?-(l-k(e.plotY))/2:-k(e.plotY)/2}],b,!0)[0];e.tooltipPos=[F.x,F.y];e.dlBoxRaw={x:w,width:k(e.plotY),y:x,bottom:q.height,fullWidth:l};u&&!1===e.visible||(f+=z)})},alignDataLabel:function(a,b,c){var g=a.dlBoxRaw,u=this.chart.inverted,e=a.plotY>
B(this.translatedThreshold,this.yAxis.len),d=B(c.inside,!!this.options.stacking),f={x:g.x,y:g.y,height:0};c.align=B(c.align,!u||d?"center":e?"right":"left");c.verticalAlign=B(c.verticalAlign,u||d?"middle":e?"top":"bottom");"top"!==c.verticalAlign&&(f.y+=g.bottom/("bottom"===c.verticalAlign?1:2));f.width=this.getWidthAt(f.y);this.options.reversed&&(f.width=g.fullWidth-f.width);d?f.x-=f.width/2:"left"===c.align?(c.align="right",f.x-=1.5*f.width):"right"===c.align?(c.align="left",f.x+=f.width/2):f.x-=
f.width/2;a.dlBox=f;J.column.prototype.alignDataLabel.apply(this,arguments)}},{shapeType:"funnel3d",hasNewShapeType:d.seriesTypes.column.prototype.pointClass.prototype.hasNewShapeType});l=k(m.elements3d.cuboid,{parts:"top bottom frontUpper backUpper frontLower backLower rightUpper rightLower".split(" "),mainParts:["top","bottom"],sideGroups:["upperGroup","lowerGroup"],sideParts:{upperGroup:["frontUpper","backUpper","rightUpper"],lowerGroup:["frontLower","backLower","rightLower"]},pathType:"funnel3d",
opacitySetter:function(a){var b=this,c=b.parts,g=d.charts[b.renderer.chartIndex],u="group-opacity-"+a+"-"+g.index;b.parts=b.mainParts;b.singleSetterForParts("opacity",a);b.parts=c;g.renderer.filterId||(g.renderer.definition({tagName:"filter",id:u,children:[{tagName:"feComponentTransfer",children:[{tagName:"feFuncA",type:"table",tableValues:"0 "+a}]}]}),b.sideGroups.forEach(function(a){b[a].attr({filter:"url(#"+u+")"})}),b.renderer.styledMode&&(g.renderer.definition({tagName:"style",textContent:".highcharts-"+
u+" {filter:url(#"+u+")}"}),b.sideGroups.forEach(function(b){b.addClass("highcharts-"+u)})));return b},fillSetter:function(a){var b=this,c=h(a),g=c.rgba[3],d={top:h(a).brighten(.1).get(),bottom:h(a).brighten(-.2).get()};1>g?(c.rgba[3]=1,c=c.get("rgb"),b.attr({opacity:g})):c=a;c.linearGradient||c.radialGradient||!b.gradientForSides||(c={linearGradient:{x1:0,x2:1,y1:1,y2:1},stops:[[0,h(a).brighten(-.2).get()],[.5,a],[1,h(a).brighten(-.2).get()]]});c.linearGradient?b.sideGroups.forEach(function(a){var e=
b[a].gradientBox,f=c.linearGradient,g=k(c,{linearGradient:{x1:e.x+f.x1*e.width,y1:e.y+f.y1*e.height,x2:e.x+f.x2*e.width,y2:e.y+f.y2*e.height}});b.sideParts[a].forEach(function(b){d[b]=g})}):(k(!0,d,{frontUpper:c,backUpper:c,rightUpper:c,frontLower:c,backLower:c,rightLower:c}),c.radialGradient&&b.sideGroups.forEach(function(a){var c=b[a].gradientBox,e=c.x+c.width/2,g=c.y+c.height/2,d=Math.min(c.width,c.height);b.sideParts[a].forEach(function(a){b[a].setRadialReference([e,g,d])})}));b.singleSetterForParts("fill",
null,d);b.color=b.fill=a;c.linearGradient&&[b.frontLower,b.frontUpper].forEach(function(a){(a=(a=a.element)&&b.renderer.gradients[a.gradient])&&"userSpaceOnUse"!==a.attr("gradientUnits")&&a.attr({gradientUnits:"userSpaceOnUse"})});return b},adjustForGradient:function(){var a=this,b;a.sideGroups.forEach(function(c){var g={x:Number.MAX_VALUE,y:Number.MAX_VALUE},d={x:-Number.MAX_VALUE,y:-Number.MAX_VALUE};a.sideParts[c].forEach(function(c){b=a[c].getBBox(!0);g={x:Math.min(g.x,b.x),y:Math.min(g.y,b.y)};
d={x:Math.max(d.x,b.x+b.width),y:Math.max(d.y,b.y+b.height)}});a[c].gradientBox={x:g.x,width:d.x-g.x,y:g.y,height:d.y-g.y}})},zIndexSetter:function(){this.finishedOnAdd&&this.adjustForGradient();return this.renderer.Element.prototype.zIndexSetter.apply(this,arguments)},onAdd:function(){this.adjustForGradient();this.finishedOnAdd=!0}});m.elements3d.funnel3d=l;m.funnel3d=function(a){var b=this.element3d("funnel3d",a),c=this.styledMode,d={"stroke-width":1,stroke:"none"};b.upperGroup=this.g("funnel3d-upper-group").attr({zIndex:b.frontUpper.zIndex}).add(b);
[b.frontUpper,b.backUpper,b.rightUpper].forEach(function(a){c||a.attr(d);a.add(b.upperGroup)});b.lowerGroup=this.g("funnel3d-lower-group").attr({zIndex:b.frontLower.zIndex}).add(b);[b.frontLower,b.backLower,b.rightLower].forEach(function(a){c||a.attr(d);a.add(b.lowerGroup)});b.gradientForSides=a.gradientForSides;return b};m.funnel3dPath=function(a){this.getCylinderEnd||t("A required Highcharts module is missing: cylinder.js",!0,H[this.chartIndex]);var b=H[this.chartIndex],c=a.alphaCorrection=90-Math.abs(b.options.chart.options3d.alpha%
180-90),d=K.call(this,k(a,{depth:a.width,width:(a.width+a.bottom.width)/2})),l=d.isTop,e=!d.isFront,m=!!a.middle,f=this.getCylinderEnd(b,k(a,{x:a.x-a.width/2,z:a.z-a.width/2,alphaCorrection:c})),h=a.bottom.width,w=k(a,{width:h,x:a.x-h/2,z:a.z-h/2,alphaCorrection:c}),r=this.getCylinderEnd(b,w,!0),y=h,p=w,v=r,n=r;m&&(y=a.middle.width,p=k(a,{y:a.y+a.middle.fraction*a.height,width:y,x:a.x-y/2,z:a.z-y/2}),v=this.getCylinderEnd(b,p,!1),n=this.getCylinderEnd(b,p,!1));d={top:f,bottom:r,frontUpper:this.getCylinderFront(f,
v),zIndexes:{group:d.zIndexes.group,top:0!==l?0:3,bottom:1!==l?0:3,frontUpper:e?2:1,backUpper:e?1:2,rightUpper:e?2:1}};d.backUpper=this.getCylinderBack(f,v);f=1!==Math.min(y,a.width)/Math.max(y,a.width);d.rightUpper=this.getCylinderFront(this.getCylinderEnd(b,k(a,{x:a.x-a.width/2,z:a.z-a.width/2,alphaCorrection:f?-c:0}),!1),this.getCylinderEnd(b,k(p,{alphaCorrection:f?-c:0}),!m));m&&(f=1!==Math.min(y,h)/Math.max(y,h),k(!0,d,{frontLower:this.getCylinderFront(n,r),backLower:this.getCylinderBack(n,r),
rightLower:this.getCylinderFront(this.getCylinderEnd(b,k(w,{alphaCorrection:f?-c:0}),!0),this.getCylinderEnd(b,k(p,{alphaCorrection:f?-c:0}),!1)),zIndexes:{frontLower:e?2:1,backLower:e?1:2,rightLower:e?1:2}}));return d}});t(d,"masters/modules/funnel3d.src.js",[],function(){})});
//# sourceMappingURL=funnel3d.js.map