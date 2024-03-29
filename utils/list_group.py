# Copyright (c) 2023, University of Washington
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the University of Washington nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF WASHINGTON AND CONTRIBUTORS
# “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF WASHINGTON OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import h5coro
from utils import args, credentials, execute

def main():
    # read object
    h5obj = h5coro.H5Coro(args.granule, args.driver, errorChecking=args.checkErrors, verbose=args.verbose, credentials=credentials, multiProcess=args.multiProcess)
    variables, attributes, groups= h5obj.list(args.group, w_attr=args.enableAttributes)

    # list groups
    for group, listing in groups.items():
        print(f'[g] {group}')
        for key, value in listing.items():
            print(f'  {key}: {value}')

    # list variables
    for variable, listing in variables.items():
        metadata = ""
        if '__metadata__' in listing:
            metadata = str(listing['__metadata__'])
            del listing['__metadata__']
        print(f'[v] {variable}: {metadata}')
        for key, value in listing.items():
            print(f'  {key}: {value}')

    # list attributes
    for attribute, value in attributes.items():
        print(f'[a] {attribute}: {value}')

execute(main)