# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def get_preview(txt):
    '''
    Parameters: 
        txt: str
    Returns:
        txt : str

    Gets txt and checks the length of it.  If it is too long it trims it to a shorter length for a preview.
    '''
    if len(txt) < 150:
        return txt
    # return up until the last whitespace.
    idx = txt.rfind(' ', 0, 150)
    return txt[:idx]