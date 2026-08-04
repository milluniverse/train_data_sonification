{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 9,
			"minor" : 0,
			"revision" : 8,
			"architecture" : "x64",
			"modernui" : 1
		},
		"classnamespace" : "box",
		"rect" : [ 100.0, 100.0, 1100.0, 750.0 ],
		"default_fontsize" : 12.0,
		"gridsize" : [ 15.0, 15.0 ],
		"boxes" : [
			{
				"box" : 				{
					"fontface" : 1,
					"fontsize" : 18.0,
					"id" : "obj-header",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 30.0, 20.0, 600.0, 27.0 ],
					"text" : "NATIONAL RAIL DARWIN TRAIN DATA SONIFICATION ENGINE"
				}

			},
			{
				"box" : 				{
					"fontsize" : 12.0,
					"id" : "obj-desc",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 30.0, 50.0, 750.0, 20.0 ],
					"text" : "Creative Coding for Sound - Assignment 2 (Musical Sonification). Receives OSC events from Python over UDP 127.0.0.1:7400."
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-udpreceive",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 100.0, 100.0, 22.0 ],
					"text" : "udpreceive 7400"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-oscroute",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "", "", "", "" ],
					"patching_rect" : [ 50.0, 140.0, 310.0, 22.0 ],
					"text" : "route /train/event /train/delay /train/trigger"
				}

			},
			{
				"box" : 				{
					"id" : "obj-comment-delay",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 180.0, 180.0, 250.0, 20.0 ],
					"text" : "<-- 1. CONTINUOUS MACRO: Delay Seconds"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-delay-num",
					"maxclass" : "number",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 150.0, 180.0, 50.0, 22.0 ]
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-delay-scale",
					"maxclass" : "newobj",
					"numinlets" : 6,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 150.0, 220.0, 130.0, 22.0 ],
					"text" : "scale -180 1800 200 4000"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-macro-osc",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 150.0, 260.0, 70.0, 22.0 ],
					"text" : "saw~ 220"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-macro-filter",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 150.0, 300.0, 80.0, 22.0 ],
					"text" : "lores~ 800 0.6"
				}

			},
			{
				"box" : 				{
					"id" : "obj-comment-trigger",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 350.0, 220.0, 300.0, 20.0 ],
					"text" : "<-- 2. DISCRETE TRIGGERS: Status Code Route"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-trig-route",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 6,
					"outlettype" : [ "", "", "", "", "", "" ],
					"patching_rect" : [ 250.0, 220.0, 180.0, 22.0 ],
					"text" : "route 0 1 2 3 4"
				}

			},
			{
				"box" : 				{
					"id" : "obj-button-ontime",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 250.0, 260.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-button-late",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 310.0, 260.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-button-cancelled",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 340.0, 260.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-env-line",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "bang" ],
					"patching_rect" : [ 250.0, 300.0, 80.0, 22.0 ],
					"text" : "line~ 0."
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-ontime-msg",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 250.0, 330.0, 80.0, 22.0 ],
					"text" : "0.5, 0. 200"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-pluck-osc",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 350.0, 330.0, 80.0, 22.0 ],
					"text" : "cycle~ 440"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-pluck-mult",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 250.0, 370.0, 50.0, 22.0 ],
					"text" : "*~"
				}

			},
			{
				"box" : 				{
					"id" : "obj-gain",
					"maxclass" : "gain~",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "int" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 250.0, 420.0, 120.0, 30.0 ]
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-dac",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 0,
					"patching_rect" : [ 250.0, 470.0, 50.0, 22.0 ],
					"text" : "ezdac~"
				}

			}
		],
		"lines" : [
			{
				"patchline" : 				{
					"destination" : [ "obj-oscroute", 0 ],
					"source" : [ "obj-udpreceive", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-delay-num", 0 ],
					"source" : [ "obj-oscroute", 1 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-trig-route", 0 ],
					"source" : [ "obj-oscroute", 2 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-delay-scale", 0 ],
					"source" : [ "obj-delay-num", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-macro-filter", 1 ],
					"source" : [ "obj-delay-scale", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-macro-filter", 0 ],
					"source" : [ "obj-macro-osc", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-button-ontime", 0 ],
					"source" : [ "obj-trig-route", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-button-late", 0 ],
					"source" : [ "obj-trig-route", 2 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-button-cancelled", 0 ],
					"source" : [ "obj-trig-route", 3 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-ontime-msg", 0 ],
					"source" : [ "obj-button-ontime", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-env-line", 0 ],
					"source" : [ "obj-ontime-msg", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pluck-mult", 0 ],
					"source" : [ "obj-pluck-osc", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-pluck-mult", 1 ],
					"source" : [ "obj-env-line", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-gain", 0 ],
					"source" : [ "obj-pluck-mult", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-gain", 0 ],
					"source" : [ "obj-macro-filter", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dac", 1 ],
					"source" : [ "obj-gain", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dac", 0 ],
					"source" : [ "obj-gain", 0 ]
				}

			}
		],
		"autosave" : 0
	}
}
