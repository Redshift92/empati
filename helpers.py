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

def normalize(value, min, max):
    if (value < min):
        return 0
    if (value > max):
        return 1
    return (float(value - min) / (max - min))
