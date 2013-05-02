var districts = [];
var paper;
var loader;
var overlay;
var paths = [];
var max_h = 700;
var max_w = 800;
var clicked = false;
var offsetx = 700;
var offsety = -120;

function overlay_hide()
{
	overlay.stop().toFront().animate(
	{
		opacity : 0,
	}, 1000, '<>');
}

function animate_holder(left, top, bottom, h, func)
{
	$('#map_holder').animate(
	{
		marginLeft : left,
		marginTop : top,
		marginBottom : bottom,
		height : h
	}, 400, func);
}
var district = function(PATH, INDEX, FILL, EVENTS, C, TITLE, HAS_SUB, IS_SUB)
{
	var me = this;
	me.moi;
	me.path = PATH;
	me.index = INDEX;
	me.max_scale = 1;
	me.fill = FILL;
	me.enableEvents = EVENTS;
	me.children_url = C;
	me.markers = [];
	me.first = 0;
	me.sub_districts = []
	me.label;
	me.label_outline;
	me.title = TITLE;
	me.is_sub = IS_SUB;
	me.has_sub = HAS_SUB;

	me.toggleMarkers = function(bool)
	{
		size = me.markers.length
		for ( var i = 0; i < size; i++)
			if (!bool) me.markers[i].hide()
			else me.markers[i].show()
	}

	me.zoom = function(s, t)
	{
		me.moi.stop().toFront().animate(
		{
			scale : s
		}, t, '<>');
	}

	me.zoom_text = function(isZoomIn, t)
	{
		me.label_outline.remove()
		me.label.remove()
		if (isZoomIn)
		{
			me.setUp_labels(18, 10);
		}
		else
		{
			me.setUp_labels(11, 4);
		}

		var t = paper.set();
		t.push(me.label_outline, me.label);
	}

	me.setUp_labels = function(size, stroke)
	{
		var offx = -20 + me.moi.getBBox().width / 2 + me.moi.getBBox().x;
		var offy = me.moi.getBBox().y + me.moi.getBBox().height / 2
		if (me.is_sub)
		{
			offx -= 50
			offy += 470
		}

		me.label_outline = paper.print(offx, offy, me.title.toUpperCase(), paper.getFont("cabin"), size);
		me.label_outline.attr(
		{
			fill : "#000",
			'stroke-width' : stroke + 'px',
			stroke : '#000',
			'stroke-miterlimit' : '4',
			'stroke-linejoin' : 'round',
			'stroke-linecap' : 'round',
		}).toFront();
		me.label = paper.print(offx, offy, me.title.toUpperCase(), paper.getFont("cabin"), size);
		me.label.attr('fill', '#fff').toFront();
	}

	me.init = function()
	{
		me.moi = paper.path(me.path).translate(offsetx, offsety)

		me.moi.attr('fill', me.fill);
		me.moi.attr('stroke', me.fill);

		if (me.index != '0' || me.enableEvents != '0')
		{

			me.moi.attr('stroke', '#fff');
			me.moi.attr('stroke-width', '2px');
			if (me.is_sub)
			{
				me.moi.toFront();
				me.setUp_labels(14, 6);
			}
			else
			{
				me.moi.toBack();
				me.setUp_labels(11, 4);
			}
			districts[0].moi.toBack();
		}
		var scale_x = max_w / me.moi.getBBox().width;
		var scale_y = max_h / me.moi.getBBox().height;

		if (scale_x < scale_y) me.max_scale = scale_x;
		else me.max_scale = scale_y;
	};

	me.mouseover = function()
	{
		if (clicked) return;

		overlay.show().stop().toFront().animate(
		{
			opacity : 1,
		}, 120, '<>');
		me.zoom(2, 120)
		me.zoom_text(true, 120)
	}

	me.mouseout = function()
	{
		if (clicked) return;
		overlay_hide();
		me.zoom(1, 100)
		me.zoom_text(false, 120)
	}
	me.events = function()
	{
		me.label.mouseover(function(event)
		{
			me.mouseover()
		})
		me.label_outline.mouseover(function(event)
		{
			me.mouseover()
		})
		me.moi.mouseover(function(event)
		{
			me.mouseover()
		}).mouseout(function(event)
		{
			me.mouseout()
		}).click(function(event)
		{
			if (clicked)
			{
				if (me.has_sub > 0)
				{
					for ( var i = 0; i < me.sub_districts.length; i++)
					{
						me.sub_districts[i].moi.hide();
						me.sub_districts[i].label_outline.hide();
						me.sub_districts[i].label.hide();
						me.sub_districts[i].toggleMarkers(false);
					}
				}
				else
				{
					me.toggleMarkers(false);
				}
				me.zoom(1, 400);
				animate_holder(0, 0, -393, 1234 - 250, null)
				loader.hide();
				overlay_hide();
				clicked = false;
				return;
			}

			clicked = true;
			me.zoom(me.max_scale, 120)
			var l = $(window).width() / 2 - me.moi.getBBox().x + 400 - me.moi.getBBox().width / 2
			var r = $(window).height() / 2 - me.moi.getBBox().y + 400 - me.moi.getBBox().height / 2
			f = function()
			{
				loader.show().toFront().translate(me.moi.getBBox().x + (me.moi.getBBox().width / 2), me.moi.getBBox().y + (me.moi.getBBox().height / 2)).animate(
				{
					rotation : '72000'
				}, 300000);
				if (me.first > 0)
				{

					for ( var i = 0; i < me.sub_districts.length; i++)
					{
						me.sub_districts[i].moi.show();
						me.sub_districts[i].label_outline.show();
						me.sub_districts[i].label.show();
					}

				}
				else
				{
					getPaths(me.children_url, true, me, me.has_sub);
					me.first++;
				}
			}
			animate_holder(l, r, -393, 1234, f)
		});
	}

	me.init();
	if (me.children_url == '-1') me.moi.translate(-35, 465);
	if (me.enableEvents == '1' && me.children_url != '-1' && me.index != '0')
	{
		me.events();
	}
	districts.push(me);
};

function getPaths(url, isNested, parent, has_subs)
{
	console.log('trying to open ' + url)
	if (window.XMLHttpRequest)
	{
		xmlhttp = new XMLHttpRequest();
	}
	else
	{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.open("GET", url, false);
	xmlhttp.send();
	xmlDoc = xmlhttp.responseXML;

	xml_paths = $(xmlDoc).find("district");
	var temp = []
	for (i = 0; i < xml_paths.length; i++)
	{
		var d = $(xml_paths[i]).attr('d');
		var f = $(xml_paths[i]).attr('fill');
		var e = $(xml_paths[i]).attr('events');
		var c = $(xml_paths[i]).attr('children');
		var t = $(xml_paths[i]).attr('title');
		var s = $(xml_paths[i]).attr('has_subs');
		var m;
		if (isNested & has_subs >= 1) m = new district(d, i, f, e, c, t, s, true);
		else if (parent == null) m = new district(d, i, f, e, c, t, s, false);

		if (isNested && $(xml_paths[i]).find('marker').length > 0)
		{
			markers = $(xml_paths[i]).find('marker')
			for ( var j = 0; j < markers.length; j++)
			{
				url = $(markers[j]).attr('img_url');
				x = $(markers[j]).attr('x');
				y = $(markers[j]).attr('y');
				h = $(markers[j]).attr('h');
				w = $(markers[j]).attr('w');
				var marker = paper.image(url, x, y, w, h).toFront();
				var circle = paper.print(x, y, $(markers[j]).attr('count'), paper.getFont("cabin"), 11);
				circle.attr(
				{
					fill : '#000',
					stroke : '#000',
					'stroke-width' : '10px',
					'stroke-miterlimit' : '4',
					'stroke-linejoin' : 'round',
					'stroke-linecap' : 'round',
				})
				var count = paper.print(x, y, $(markers[j]).attr('count'), paper.getFont("cabin"), 11);
				count.attr('fill', '#fff')
				var marker_set = paper.set();
				marker_set.push(count, circle, marker)
				marker_set.hide();
				if (has_subs == 0)
				{
					parent.markers.push(marker_set)
				}
				else m.markers.push(marker_set)

			}
		}
		temp.push(m)

	}
	if (isNested & has_subs >= 1)
	{
		loader.hide()
		parent.sub_districts = temp
		for (i = 0; i < parent.sub_districts.length; i++)
		{
			parent.sub_districts[i].moi.show();
			parent.sub_districts[i].toggleMarkers(true);
		}
	}
	else if (has_subs == 0)
	{
		loader.hide()
		parent.toggleMarkers(true);
	}
	console.log(has_subs)
}

function init()
{
	register_map()
	register_font()
	register_loader()
	register_overlay()
}

function register_map()
{
	$('div#map_holder').css(
	{
		width : 690 + $(window).width() + 'px',
		height : 1234 + 'px'
	})
	paper = Raphael("map_holder", 690 + $(window).width(), 1234);
}

function register_overlay()
{
	overlay = paper.rect(-500, -500, 3500, 3500)
	overlay.attr('fill', 'rgba(0,0,0,0.7)').hide();
	$(overlay.node).attr('pointer-events', 'none');
}

function register_loader()
{
	loader = paper.path("M15.999,4.308c1.229,0.001,2.403,0.214,3.515,0.57L18.634,6.4h6.247l-1.562-2.706L21.758,0.99l-0.822,1.425c-1.54-0.563-3.2-0.878-4.936-0.878c-7.991,0-14.468,6.477-14.468,14.468c0,3.317,1.128,6.364,3.005,8.805l2.2-1.689c-1.518-1.973-2.431-4.435-2.436-7.115C4.312,9.545,9.539,4.318,15.999,4.308zM27.463,7.203l-2.2,1.69c1.518,1.972,2.431,4.433,2.435,7.114c-0.011,6.46-5.238,11.687-11.698,11.698c-1.145-0.002-2.24-0.188-3.284-0.499l0.828-1.432H7.297l1.561,2.704l1.562,2.707l0.871-1.511c1.477,0.514,3.058,0.801,4.709,0.802c7.992-0.002,14.468-6.479,14.47-14.47C30.468,12.689,29.339,9.643,27.463,7.203z").attr(
	{
		fill : "#fff",
		stroke : "none"
	});
}
