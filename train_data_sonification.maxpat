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
		"rect" : [ 80.0, 80.0, 1150.0, 800.0 ],
		"default_fontsize" : 12.0,
		"gridsize" : [ 15.0, 15.0 ],
		"boxes" : [
			{
				"box" : 				{
					"fontface" : 1,
					"fontsize" : 20.0,
					"id" : "obj-header",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 30.0, 20.0, 700.0, 30.0 ],
					"text" : "NATIONAL RAIL SONIFICATION ENGINE — GLASGOW CENTRAL (GLC) TEMPLATE"
				}

			},
			{
				"box" : 				{
					"fontsize" : 12.0,
					"id" : "obj-desc",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 30.0, 55.0, 800.0, 20.0 ],
					"text" : "Template station routing for Glasgow Central (GLC). Isolates events for GLC and routes each variable and event status to a dedicated bang button."
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
					"patching_rect" : [ 50.0, 100.0, 110.0, 22.0 ],
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
					"patching_rect" : [ 50.0, 140.0, 280.0, 22.0 ],
					"text" : "route /train/trigger /train/event /train/delay"
				}

			},
			{
				"box" : 				{
					"fontface" : 1,
					"fontsize" : 14.0,
					"id" : "obj-glc-title",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 200.0, 400.0, 23.0 ],
					"text" : "GLASGOW CENTRAL (GLC) ISOLATION ROUTE"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-route-glc-trig",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 50.0, 230.0, 85.0, 22.0 ],
					"text" : "route GLC"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-glc-any",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 150.0, 230.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-glc-any",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 180.0, 232.0, 150.0, 20.0 ],
					"text" : "<-- BANG: Any GLC Event"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-unpack-trig",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "int", "int" ],
					"patching_rect" : [ 50.0, 270.0, 80.0, 22.0 ],
					"text" : "unpack 0 0"
				}

			},
			{
				"box" : 				{
					"fontface" : 1,
					"fontsize" : 13.0,
					"id" : "obj-lbl-statuses",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 310.0, 450.0, 21.0 ],
					"text" : "GLC EVENT STATUSES (ROUTED TO INDIVIDUAL BANGS)"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-status-route",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 6,
					"outlettype" : [ "", "", "", "", "", "" ],
					"patching_rect" : [ 50.0, 340.0, 220.0, 22.0 ],
					"text" : "route 0 1 2 3 4"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-ontime",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 50.0, 380.0, 28.0, 28.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-ontime",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 40.0, 415.0, 70.0, 20.0 ],
					"text" : "ON TIME (0)"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-early",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 120.0, 380.0, 28.0, 28.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-early",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 110.0, 415.0, 70.0, 20.0 ],
					"text" : "EARLY (1)"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-late",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 190.0, 380.0, 28.0, 28.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-late",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 185.0, 415.0, 60.0, 20.0 ],
					"text" : "LATE (2)"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-cancelled",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 260.0, 380.0, 28.0, 28.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-cancelled",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 245.0, 415.0, 90.0, 20.0 ],
					"text" : "CANCELLED (3)"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-activated",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 340.0, 380.0, 28.0, 28.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-activated",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 330.0, 415.0, 90.0, 20.0 ],
					"text" : "ACTIVATED (4)"
				}

			},
			{
				"box" : 				{
					"fontface" : 1,
					"fontsize" : 13.0,
					"id" : "obj-lbl-variables",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 500.0, 200.0, 450.0, 21.0 ],
					"text" : "GLC EXTRACTED VARIABLES (BANGS & VALUE METRICS)"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-num-delay",
					"maxclass" : "number",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 500.0, 240.0, 70.0, 22.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-delay",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 580.0, 240.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-delay-var",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 615.0, 242.0, 200.0, 20.0 ],
					"text" : "<-- VARIABLE 1: Delay Seconds"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-route-event",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 500.0, 280.0, 85.0, 22.0 ],
					"text" : "route GLC"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-unpack-event",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 5,
					"outlettype" : [ "", "", "", "", "" ],
					"patching_rect" : [ 500.0, 310.0, 300.0, 22.0 ],
					"text" : "unpack s s s 0 s"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-trainid",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 500.0, 350.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-trainid",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 530.0, 352.0, 180.0, 20.0 ],
					"text" : "<-- VARIABLE 2: Train ID"
				}

			},
			{
				"box" : 				{
					"id" : "obj-bang-platform",
					"maxclass" : "button",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 500.0, 390.0, 24.0, 24.0 ]
				}

			},
			{
				"box" : 				{
					"id" : "obj-lbl-platform",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 530.0, 392.0, 180.0, 20.0 ],
					"text" : "<-- VARIABLE 3: Platform"
				}

			},
			{
				"box" : 				{
					"fontface" : 1,
					"fontsize" : 13.0,
					"id" : "obj-lbl-synth",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 470.0, 450.0, 21.0 ],
					"text" : "GLC SYNTHESIS VOICE (AUDIO SYNTHESIS RESPONSE)"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-msg-ontime-synth",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 50.0, 500.0, 80.0, 22.0 ],
					"text" : "0.6, 0. 250"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-msg-late-synth",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 190.0, 500.0, 80.0, 22.0 ],
					"text" : "0.8, 0. 600"
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
					"patching_rect" : [ 50.0, 540.0, 80.0, 22.0 ],
					"text" : "line~ 0."
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-osc-glc",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 150.0, 540.0, 80.0, 22.0 ],
					"text" : "cycle~ 523.25"
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-mult-glc",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 50.0, 580.0, 50.0, 22.0 ],
					"text" : "*~"
				}

			},
			{
				"box" : 				{
					"id" : "obj-gain-master",
					"maxclass" : "gain~",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "int" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 50.0, 620.0, 150.0, 30.0 ]
				}

			},
			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-dac-master",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 0,
					"patching_rect" : [ 50.0, 670.0, 60.0, 22.0 ],
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
					"destination" : [ "obj-route-glc-trig", 0 ],
					"source" : [ "obj-oscroute", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-route-event", 0 ],
					"source" : [ "obj-oscroute", 1 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-glc-any", 0 ],
					"source" : [ "obj-route-glc-trig", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-unpack-trig", 0 ],
					"source" : [ "obj-route-glc-trig", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-status-route", 0 ],
					"source" : [ "obj-unpack-trig", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-num-delay", 0 ],
					"source" : [ "obj-unpack-trig", 1 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-delay", 0 ],
					"source" : [ "obj-num-delay", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-ontime", 0 ],
					"source" : [ "obj-status-route", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-early", 0 ],
					"source" : [ "obj-status-route", 1 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-late", 0 ],
					"source" : [ "obj-status-route", 2 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-cancelled", 0 ],
					"source" : [ "obj-status-route", 3 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-activated", 0 ],
					"source" : [ "obj-status-route", 4 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-msg-ontime-synth", 0 ],
					"source" : [ "obj-bang-ontime", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-msg-late-synth", 0 ],
					"source" : [ "obj-bang-late", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-env-line", 0 ],
					"source" : [ "obj-msg-ontime-synth", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-env-line", 0 ],
					"source" : [ "obj-msg-late-synth", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-mult-glc", 0 ],
					"source" : [ "obj-env-line", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-mult-glc", 1 ],
					"source" : [ "obj-osc-glc", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-gain-master", 0 ],
					"source" : [ "obj-mult-glc", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dac-master", 1 ],
					"source" : [ "obj-gain-master", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-dac-master", 0 ],
					"source" : [ "obj-gain-master", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-unpack-event", 0 ],
					"source" : [ "obj-route-event", 0 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-trainid", 0 ],
					"source" : [ "obj-unpack-event", 1 ]
				}

			},
			{
				"patchline" : 				{
					"destination" : [ "obj-bang-platform", 0 ],
					"source" : [ "obj-unpack-event", 4 ]
				}

			}
		],
		"autosave" : 0
	}
}
