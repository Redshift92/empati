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

import helpers

class AffectiveObject:

    def __init__(self, type_name, type_input_coeff, all_minmax):
        self.name = type_name
        self.input_coeff = type_input_coeff
        self.last_inputs = {}
        self.state, self.eval_state = [0.0, 0.0], [None,None]
        self.input_minmax = {}
        for input_type in self.input_coeff.keys():
            self.input_minmax[input_type] = all_minmax[input_type]


    def eval_input(self, inputs):
        up_val, up_ar, extra_inputs = 0.0, 0.0, {}
        for input_type in self.input_coeff.keys():
            minmax = self.input_minmax[input_type]
            try:
                input_val = inputs[input_type]
            except KeyError:
                input_val = self.__dict__.get(input_type)()
                extra_inputs[input_type] = input_val
            input_norm = helpers.normalize(input_val, minmax[0],minmax[1])
            # make the interval symmetric [0,1] -> [-0.5,0.5]
            input_norm -= 0.5
            # scale the interval
            up_val += (input_norm * self.input_coeff[input_type][0])
            if isinstance(self.input_coeff[input_type][1],str):
                f_coeff = float(self.input_coeff[input_type][1].replace('f',''))
                up_ar += input_norm * f_coeff
            else:
                if (self.last_inputs):
                    diff = input_val - self.last_inputs[input_type]
                    # amplify differences:
                    # in a [0,100] range a change of 100/sensibility is enough
                    # to reach max possible arousal caused by the selected sensed value
                    try:
                        sensibility = self.input_coeff[input_type][2]
                    except IndexError:
                        sensibility = 1
                    diff = 0.5 * sensibility * ( float(diff) / (minmax[1] - minmax[0]))
                    # saturates
                    if (diff < -0.5):
                        diff = -0.5
                    elif (diff > 0.5):
                        diff = 0.5
                    up_ar += (diff * self.input_coeff[input_type][1])
        self.last_inputs = inputs.copy()
        self.last_inputs.update(extra_inputs)
        self.eval_state[0] = up_val
        self.eval_state[1] = up_ar

    def update_state(self):
        self.state[0] = self.eval_state[0]
        self.state[1] = self.eval_state[1]
