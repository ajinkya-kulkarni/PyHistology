#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (C) 2022 Max Planck Institute for Multidisclplinary Sciences
# Copyright (C) 2022 University Medical Center Goettingen
# Copyright (C) 2022 Ajinkya Kulkarni <ajinkya.kulkarni@mpinat.mpg.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

########################################################################################

def extract_consecutive_digits(lst):
	"""
	Extracts consecutive digits from a list of strings and returns them as a list of integers.
	Ignores non-digit characters in the input list.
	"""
	result = []
	current_sequence = []
	for i in lst:
		if i.isdigit():
			current_sequence.append(i)
		else:
			if current_sequence:
				result.append(int("".join(current_sequence)))
				current_sequence = []
	if current_sequence:
		result.append(int("".join(current_sequence)))
	return result