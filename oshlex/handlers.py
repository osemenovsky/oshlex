# Copyright (C) 2016  Semenovsky, Oleg <o.semenovsky@gmail.com>
# Author: Semenovsky, Oleg <o.semenovsky@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class UnacceptableTokenCount(Exception):
    pass

class UnacceptableToken(Exception):
    pass


def text(tokens):
    if len(tokens) > 1:
        raise UnacceptableTokenCount("This handler accepts 1 token at most")

    return tokens[0]

def integer(tokens):
    if len(tokens) > 1:
        raise UnacceptableTokenCount("This handler accepts 1 token at most")

    return int(tokens[0])
