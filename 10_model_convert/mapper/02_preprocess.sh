#!/usr/bin/env bash
# Copyright (c) 2024 D-Robotics.All Rights Reserved.
#
# The material in this file is confidential and contains trade secrets
# of D-Robotics Inc. This is proprietary information owned by
# D-Robotics Inc. No part of this work may be disclosed,
# reproduced, copied, transmitted, or used in any way for any purpose,
# without the express written permission of D-Robotics Inc.

set -e -v

cd $(dirname $0) || exit

python3 ../../../data_preprocess.py \
  --src_dir /open_explorer/ddk/samples/ai_toolchain/horizon_model_convert_sample/03_classification/10_model_convert/mapper/image_dataset \
  --dst_dir ./calibration_data_bgr_f32 \
  --pic_ext .rgb \
  --read_mode opencv
