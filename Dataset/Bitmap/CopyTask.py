# Copyright 2017 Robert Csordas. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==============================================================================

import numpy as np
from .BitmapTask import BitmapTask
from ...Utils.Seed import get_randstate

class CopyData(BitmapTask):
    def __init__(self, datapoints, length=None, bit_w=8, transform=lambda x:x):
        super(CopyData, self).__init__(datapoints)
        self.length = length
        self.bit_w = bit_w
        self.transform = transform
        self.seed = None

    def __getitem__(self, key):
        if self.seed is None:
            self.seed = get_randstate()

        length = self.length() if callable(self.length) else self.length
        if length is None:
            #Random length batch hack.
            length = key

        d = self.seed.randint(0,2,[length+1, self.bit_w+1]).astype(np.float32)
        z = np.zeros_like(d)

        d[-1] = 0
        d[:, -1] = 0
        d[-1, -1] = 1

        i_p = np.concatenate((d, z), axis=0)
        o_p = np.concatenate((z,d), axis=0)
        i_p = i_p * 2.0 - 1.0 #???
        return i_p, o_p
        return self.transform({
            "input" : i_p,
            "output": o_p
        })




