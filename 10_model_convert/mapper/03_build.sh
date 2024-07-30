#!/bin/bash
# Copyright (c) 2024 D-Robotics.All Rights Reserved.
#
# The material in this file is confidential and contains trade secrets
# of D-Robotics Inc. This is proprietary information owned by
# D-Robotics Inc. No part of this work may be disclosed,
# reproduced, copied, transmitted, or used in any way for any purpose,
# without the express written permission of D-Robotics Inc.


cd $(dirname $0) || exit
set -e
config_file="./resnet18_config.yaml"
model_type="onnx"
# build model
hb_mapper makertbin --config ${config_file}  \
                    --model-type  ${model_type}
