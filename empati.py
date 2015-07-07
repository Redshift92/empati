#======================================================================
# Copyright 2015 Lorenzo Rizzello, <redshif92@gmail.com>
#
# This file is part of EMPATI.
#
# EMPATI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EMPATI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EMPATI.  If not, see <http://www.gnu.org/licenses/>.
#======================================================================

import json
import sys
import types
import re
from affobjects import AffectiveObject
import matplotlib.pyplot as plt
import helpers

def init_objects():
    for a_obj_name in simulation_conf["objects_types"]:
        type_input_coeff = simulation_conf["objects_types"][a_obj_name]
        for _ in range(simulation_conf["simulation"][a_obj_name]):
            obj = AffectiveObject(a_obj_name,type_input_coeff,simulation_conf["minmax"])
            for m in dir(methods):
                if re.compile(a_obj_name).match(m):
                    setattr(obj,m.replace(a_obj_name+"_",""),types.MethodType(getattr(methods,m),obj))
            net_objects_list.append(obj)
    for obj in net_objects_list:
        obj.neighbours = [ o for o in net_objects_list if o != obj ]

def run():
    input_data = simulation_conf["input_data"]
    n_cycles = len(input_data[list(input_data.keys())[0]])
    plot_data, added_obj_plot_data = {}, {}
    for plot_name in simulation_conf["plot"]:
        plot_data[plot_name], added_obj_plot_data[plot_name] = {}, False
        for y_data in simulation_conf["plot"][plot_name]:
            plot_data[plot_name][y_data[0]] = [[],y_data[1]]
    for i in range(n_cycles):
        for plot_name in added_obj_plot_data:
            added_obj_plot_data[plot_name] = False
        cycle_input = dict((input_type,input_data[input_type][i]) for input_type in input_data)
        for obj in net_objects_list:
            obj.eval_input(cycle_input)
        for obj in net_objects_list:
            obj.update_state()
            if obj.name in simulation_conf["plot"].keys() and not added_obj_plot_data[obj.name]:
                added_obj_plot_data[obj.name] = True
                for y_data in simulation_conf["plot"][obj.name]:
                    if y_data[0] == 'valence':
                        to_app = obj.state[0]
                    elif y_data[0] == 'arousal':
                        to_app = obj.state[1]
                    else:
                        n_min,n_max = simulation_conf["minmax"][y_data[0]][0],simulation_conf["minmax"][y_data[0]][1]
                        to_app = helpers.normalize(obj.last_inputs[y_data[0]],n_min,n_max)
                    plot_data[obj.name][y_data[0]][0].append(to_app)
    i = 1
    for plot_name in plot_data:
        plt.title(plot_name)
        for y_label in plot_data[plot_name]:
            plt.plot(*plot_data[plot_name][y_label],label=y_label)
        plt.axis([0,n_cycles-1,-0.5,1.5])
        plt.legend()
        if i != len(simulation_conf["plot"].keys()):
            plt.figure()
        i += 1
    plt.show()


simulation_name, simulation_conf = sys.argv[1], { "minmax": {} }
net_objects_list = []
__import__(("simul.%s.methods" % simulation_name))
methods = sys.modules[("simul.%s.methods" % simulation_name)]
for json_file in ["input_data","simulation","objects_types","plot"]:
    with open(("simul/%s/%s.json" % (simulation_name,json_file))) as data:
        simulation_conf[json_file] = json.loads(data.read())
for input_type in simulation_conf["input_data"]:
    simulation_conf["minmax"][input_type] = simulation_conf["input_data"][input_type][1]
    if simulation_conf["input_data"][input_type][0]:
        simulation_conf["input_data"][input_type] = simulation_conf["input_data"][input_type][0]
    else:
        simulation_conf["input_data"][input_type] = None
simulation_conf["input_data"] = dict((k, v) for k, v in simulation_conf["input_data"].items() if v)
init_objects()
run()
