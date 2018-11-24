#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
    Mochimo miner monitoring web server
	v1.0
	
	Requirements/Setup:
		> sudo apt-get install python3-pip
		> pip3 install dash
		> pip3 install dash-core-components
		> pip3 install dash-html-components
		> pip3 install gpustat
		> pip3 install numpy
		> pip3 install pandas
		
	Dash based on https://github.com/plotly/dash-salesforce-crm
"""

__author__ = ['0xFF (https://github.com/0xFF0)']
__version__ = "1.0"
__date__ = '2018.11.24'


import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import numpy as np
from plotly import graph_objs as go
import os.path
import pandas as pd
import gpustat
import datetime
import argparse
from pathlib import Path
import sys
from collections import OrderedDict

	
ENABLE_DEBUG_LOG = False
	
HAIKU_HASHRATE_DICT = OrderedDict()
DIFFICULTY_DICT = OrderedDict()
NETHASH_DICT = OrderedDict()
LAST_GPU_QUERY = OrderedDict()
MOCHIMO_DATA_DIR = ""

MOCHIMO_LOGO = "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"


MOCHIMO_DONATION = "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"


#Indicators: Hashrate, Average days, Difficulty, Current block, Solved, Status
def indicator(color, text, id_value):
    return html.Div(
        [        
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator", 
    )
	
#GPU dropdown
def gpuLabelOptions():
	gpuInfo = gpustat.new_query().jsonify()
	labelOptions = []
	
	for gpu in gpuInfo["gpus"]:
		labelOptions.append({'label': "[" + str(gpu["index"]) + "] " + gpu["name"], 'value': gpu["index"]})

			
	return labelOptions

	
app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(
    [
        # header
        html.Div
		(
			[
				html.Span("Miner monitoring", className='app-title'),
				html.Div(html.Img(src='data:image/png;base64,{}'.format(MOCHIMO_LOGO),height="100%"), style={"float":"right","height":"100%"})			
            ],
            className="row header"
        ),

		# top controls
		html.Div(
			[		
				html.Div(				
					dcc.Dropdown(
						id='set-time',
						options=[
							{'label': 'Update every second', 'value': 1000},
							{'label': 'Update every 10 seconds', 'value': 10000},
							{'label': 'Update every 30 seconds', 'value': 30000},
							{'label': 'Update every minute', 'value': 60000},
							{'label': 'Update every 15 minute', 'value': 900000},
							{'label': 'Off', 'value': 60*60*1000*24} # Every day
						],
						value=1000,
						clearable=False,
					),
					className="two columns",	
				),
				html.Div(		
					dcc.Dropdown(
						id='set-gpu',
						options=gpuLabelOptions(),
						value=0,
						clearable=False,
					),
					className="two columns",	
				),
				dcc.Interval(id='interval-of-time', interval=1000),
				html.Div(
					html.Span(
						"Last update: - ",
						id='lastupdate_textarea',
						style={
							"height": "34",
							"background": "#119DFF",
							"border": "1px solid #119DFF",
							"color": "white",
						},
					),
					className="two columns",
					style={"float": "right"},
				),
			],
			className="row",
			style={"marginBottom": "10", "marginTop": "5"},
		),
			
		#Indicators
		html.Div(
			[
				indicator(
					"#00cc96", "Haiku/second", "hashrate_left_indicator"
				),
				indicator(
					"#119DFF", "Average days to find a block", "avgDay_middle_indicator"
				),
				indicator(
					"#EF553B", "Difficulty", "difficulty_right_indicator"
				),
			],
			className="row",
		),

		# charts row div
		html.Div(
			[
				html.Div(
					[
						html.P("Haiku/second" ),
						dcc.Graph(
							id="hashrate_graph",
							style={"height": "90%", "width": "98%"},				
						),
					],
					className="four columns chart_div"
				),

				html.Div(
					[
						html.P("Network hash rate"),
						dcc.Graph(
							id="network_hashrate_graph",
							style={"height": "90%", "width": "98%"},
						),
					],
					className="four columns chart_div"
				),

				html.Div(
					[
						html.P("Difficulty"),
						dcc.Graph(
							id="difficulty_graph",
							style={"height": "90%", "width": "98%"},
						),
					],
					className="four columns chart_div"
				),

			],
			className="row",
			style={"marginTop": "5"},
		),

		#Indicators
		html.Div(
			[
				indicator(
					"#00cc96", "Current block", "currentblock_left_indicator"
				),
				indicator(
					"#EF553B", "Blocks solved", "solved_middle_indicator"
				),
				indicator(
					"#00cc96", "Status", "status_right_indicator"
				),
			],
			className="row",
			style={"marginTop": "5"},
		),
		
		#GPU Infos
		html.Div(
			[
				indicator(
					"#00cc96", "GPU Power draw", "powerDraw_left_indicator"
				),
				indicator(
					"#EF553B", "GPU temperature", "gputemp_middle_indicator"
				),
				indicator(
					"#00cc96", "GPU utilization", "gpuutilization_right_indicator"
				),
			],
			className="row",
			style={"marginTop": "5"},
		),				
		

		# Tab content
		html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
			
		# footer
        html.Div
		(
			[
				html.Div(["Author: ", html.A('0xFF', href='http://github.com/0xFF0')], style={"float":"right"}),	
				html.Div(["Please donate if you find this project useful: "]),
				html.Span([html.A('Mochimo', href='data:application/octet-stream;base64,{}'.format(MOCHIMO_DONATION), download="DONATE-0xFF")," ", " "]),
				html.Span([html.A('BTC', href='bitcoin:18DfQCf5RHAMDqLK38RsqvoXkXKH3jtQSF'), " ", " "]),
				html.Span([html.A('ETH', href='ethereum:0x55D1f78755830c2F7E778447aeC6F0e194968c0c')," ", " "]),
				html.Span([html.A('Monero', href='monero:4AxmF8vdSZsVxc8mMpyLscFEhe3w9vEXV2KnfMXb3aogEvJ5HPezeCp5Vz5M49gfhmRUrJouz33nD4La5KKkxHBgUY1xoWt')," ", " "]),						
            ],
            className="row header"
        ),			
			html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
			html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
			html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
			html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
			html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
			html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")	
    ],
    className="row",
    style={"margin": "0%"},
)

#Timer Callback - Last update 
@app.callback(
    dash.dependencies.Output('lastupdate_textarea', 'children'),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback_last_update():
    return "Last update: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	
#Dropdown Callback - Update the interval of time
@app.callback(
    dash.dependencies.Output('interval-of-time', 'interval'),
    [dash.dependencies.Input('set-time', 'value')])
def dropdown_callback_update_interval(value):
    return value

	
#Timer Callback - Update Haiku/sec
@app.callback(
    dash.dependencies.Output("hashrate_left_indicator", "children"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback_hashrate():
	time = datetime.datetime.now().strftime("%H:%M:%S")
	f = open(os.path.join(MOCHIMO_DATA_DIR,"hps.dat"), "rb")
	hps = np.fromfile(f, dtype=np.uint64)[0]	
	HAIKU_HASHRATE_DICT[time] = hps
	return str(hps)
	
#Timer Callback - Update hashrate graph
@app.callback(
    dash.dependencies.Output("hashrate_graph", "figure"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')],
)
def timer_callback_hashrate_graph():
    trace = go.Scatter(
        x=list(HAIKU_HASHRATE_DICT.keys())[-10:],
        y=list(HAIKU_HASHRATE_DICT.values())[-10:],
        name="haiku hashrate",
        fill="tozeroy",
        fillcolor="#e6f2ff",
    )

    data = [trace]

    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=33, r=25, b=37, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}
	
	
#Timer Callback - Update difficulty
@app.callback(
    dash.dependencies.Output("difficulty_right_indicator", "children"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback_difficulty():
	time = datetime.datetime.now().strftime("%H:%M:%S")
	if os.path.exists(os.path.join(MOCHIMO_DATA_DIR,"global.dat")):
		f = open(os.path.join(MOCHIMO_DATA_DIR,"global.dat"), "rb")
		blockNum = np.fromfile(f, dtype=np.uint64)[0]	
		f.seek(89)
		diff = np.fromfile(f, dtype=np.uint32)[0]	
		f.close()
		DIFFICULTY_DICT[time] = diff
		
		#Nethash = Difficulty/block time 
		#ex: 833 999 930 994 = (2^48)/337.5 
		NETHASH_DICT[time] = np.int64(pow(2,diff)/337.5)
		return str(diff)
	return "N/A"

#Timer Callback - Diffuculty graph
@app.callback(
    dash.dependencies.Output("difficulty_graph", "figure"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')],
)
def timer_callback_difficulty_graph():
    trace = go.Scatter(
        x=list(DIFFICULTY_DICT.keys())[-10:],
        y=list(DIFFICULTY_DICT.values())[-10:],
        name="difficulty",
        fill="tozeroy",
        fillcolor="#e6f2ff",
    )

    data = [trace]

    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=33, r=25, b=37, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}

	
#Timer Callback - Update average day
@app.callback(
    dash.dependencies.Output("avgDay_middle_indicator", "children"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback_average_day():
	hashrate = list(HAIKU_HASHRATE_DICT.values())[-1:][0]
	nethash = list(NETHASH_DICT.values())[-1:][0]
	#Days to find a block - nethash/hashrate/256 (256 block per day)	
	days = nethash/hashrate/256
	return str("{:.3f}".format(days))
	
	
#Timer Callback - Network hashrate graph
@app.callback(
    dash.dependencies.Output("network_hashrate_graph", "figure"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')],
)
def timer_callback_networkhashrate_graph():
    trace = go.Scatter(
        x=list(NETHASH_DICT.keys())[-10:],
        y=list(NETHASH_DICT.values())[-10:],
        name="network hashrate",
        fill="tozeroy",
        fillcolor="#e6f2ff",
    )

    data = [trace]

    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=33, r=25, b=37, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}

	
#Timer Callback - Update currentblock
@app.callback(
    dash.dependencies.Output("currentblock_left_indicator", "children"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback_currentblock():
	f = open(os.path.join(MOCHIMO_DATA_DIR,"global.dat"), "rb")
	blockNum = np.fromfile(f, dtype=np.uint64)[0]		
	f.close()
	return str(blockNum)

#Timer Callback - Update solved
@app.callback(
    dash.dependencies.Output("solved_middle_indicator", "children"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback():
	if os.path.exists(os.path.join(MOCHIMO_DATA_DIR,"solved.dat")):
		f = open(os.path.join(MOCHIMO_DATA_DIR,"solved.dat"), "rb")
		solved = np.fromfile(f, dtype=np.uint32)[0]		
		f.close()
		return str(solved)

	return str(0)	
	
#Timer Callback - Update Status and GPU
@app.callback(
    dash.dependencies.Output("status_right_indicator", "children"),
    events=[dash.dependencies.Event('interval-of-time', 'interval')])
def timer_callback_status():
	if "query_time" in LAST_GPU_QUERY:
		now = datetime.datetime.now()
		delta = now - LAST_GPU_QUERY["query_time"]
	else:
		delta = datetime.timedelta(seconds=31) #datetime.time(0, 0, 31) - datetime.time(0, 0, 0)
		LAST_GPU_QUERY["nbActiveGPU"] = 0
	
	if delta.seconds > 30:
		gpuInfo = gpustat.new_query().jsonify()
		nbActiveGPU = 0
		
		for gpu in gpuInfo["gpus"]:
			if any(d.get('command', None) == 'mochimo' for d in gpu["processes"]):
				nbActiveGPU = nbActiveGPU + 1
			LAST_GPU_QUERY[gpu["index"]] = {}
			LAST_GPU_QUERY[gpu["index"]]["utilization.gpu"] = gpu["utilization.gpu"] 
			LAST_GPU_QUERY[gpu["index"]]["power.draw"] = gpu["power.draw"] 
			LAST_GPU_QUERY[gpu["index"]]["temperature.gpu"] = gpu["temperature.gpu"] 
			
		LAST_GPU_QUERY["nbActiveGPU"] = nbActiveGPU
		LAST_GPU_QUERY["query_time"] = gpuInfo["query_time"]
	
	return str(LAST_GPU_QUERY["nbActiveGPU"]) + " GPU mining"	

	
#Timer Callback - Update GPU power
@app.callback(
    dash.dependencies.Output("powerDraw_left_indicator", "children"),
	[dash.dependencies.Input('set-gpu', 'value')],
    events=[dash.dependencies.Event('interval-of-time', 'interval')]
	)
def gpuPower_callback(value):
	power = "N/A"
	if(value in LAST_GPU_QUERY):
		power = LAST_GPU_QUERY[value]["power.draw"]
	return str(power)
	
#Timer Callback - Update GPU Temp
@app.callback(
    dash.dependencies.Output("gputemp_middle_indicator", "children"),
	[dash.dependencies.Input('set-gpu', 'value')],
    events=[dash.dependencies.Event('interval-of-time', 'interval')]
	)
def gpuTemp_callback(value):
	temp = "N/A"
	if(value in LAST_GPU_QUERY):
		temp = LAST_GPU_QUERY[value]["temperature.gpu"]
	return str(temp)

#Timer Callback - Update GPU utilization
@app.callback(
    dash.dependencies.Output("gpuutilization_right_indicator", "children"),
	[dash.dependencies.Input('set-gpu', 'value')],
    events=[dash.dependencies.Event('interval-of-time', 'interval')]
	)
def gpuUtilization_callback(value):
	utilization = "N/A"
	if(value in LAST_GPU_QUERY):
		utilization = LAST_GPU_QUERY[value]["utilization.gpu"]
	return str(utilization) + "%"

	

	
def main():	
	desc = "Mochimo miner monitoring v" + __version__
	parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-d", action="store", type=str, dest="mochimoDataDir", help="Select the mochimo data directory")
	options = parser.parse_args()
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
		
	if options.mochimoDataDir is None:
		if not os.path.exists(os.path.join(options.mochimoDataDir,"global.dat")):
			print("Please specify the mochimo data directory.\n")
			parser.print_help()
			exit(1)	
	
	global MOCHIMO_DATA_DIR
	MOCHIMO_DATA_DIR = options.mochimoDataDir
	
	app.run_server(debug=False,port=8050,host='0.0.0.0')

	
	
if __name__ == '__main__':
	main()
    
	
