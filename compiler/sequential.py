#!/usr/bin/env python3
# Copyright 2019 Google LLC
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


import kfp
from kfp import dsl


def gcs_download_op(url, output_path):
    return dsl.ContainerOp(
        name='GCS - Download',
        image='google/cloud-sdk:216.0.0',
        command=['sh', '-c'],
        arguments=['gsutil cat $0 | tee $1', url, output_path],
    )


def echo_op(output_path):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4.4.23',
        command=['sh', '-c'],
        arguments=['echo "$0"', output_path]
    )

@dsl.pipeline(
    name='Sequential pipeline',
    description='A pipeline with two sequential steps.'
)
def sequential_pipeline(url='gs://ml-pipeline-playground/shakespeare1.txt', output_path='/tmp/results.txt'):
    """A pipeline with two sequential steps."""

    download_task = gcs_download_op(url, output_path)
    echo_task = echo_op(output_path)    

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(sequential_pipeline, __file__ + '.zip')
