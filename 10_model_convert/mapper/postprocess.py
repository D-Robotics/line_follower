# Copyright (c) 2024 D-Robotics.All Rights Reserved.
#
# The material in this file is confidential and contains trade secrets
# of D-Robotics Inc. This is proprietary information owned by
# D-Robotics Inc. No part of this work may be disclosed,
# reproduced, copied, transmitted, or used in any way for any purpose,
# without the express written permission of D-Robotics Inc.

import numpy as np
import logging
from multiprocessing.pool import ApplyResult
from horizon_tc_ui.data.imagenet_val import imagenet_val
from horizon_tc_ui.utils import tool_utils


def postprocess(model_output):
    prob = np.squeeze(model_output[0])
    idx = np.argsort(-prob)
    print(prob[0], prob[1])
    top_five_label_probs = [(idx[i], prob[idx[i]], imagenet_val[idx[i]])
                            for i in range(5)]
    return top_five_label_probs


def eval_postprocess(model_output, label):
    predict_label, _, _ = postprocess(model_output)[0]
    if predict_label == label:
        sample_correction = 1
    else:
        sample_correction = 0
    return predict_label, sample_correction


def calc_accuracy(accuracy, total_batch):
    if isinstance(accuracy[0], ApplyResult):
        accuracy = [i.get() for i in accuracy]
        batch_result = sorted(list(accuracy), key=lambda e: e[0])
    else:
        batch_result = sorted(list(accuracy), key=lambda e: e[0])
    total_correct_samples = 0
    total_samples = 0
    acc_all = 0
    with open("resnet18_eval.log", "w") as eval_log_handle:
        for data_id, predict_label, sample_correction, filename in batch_result:
            total_correct_samples += sample_correction
            total_samples += 1
            if total_samples % 10 == 0:
                record = 'Batch:{}/{}; accuracy(all):{:.4f}'.format(
                    data_id + 1, total_batch,
                    total_correct_samples / total_samples)
                logging.info(record)
            acc_all = total_correct_samples / total_samples
            eval_log_handle.write(
                f"input_image_name: {filename[0]} class_id: {predict_label:3d} class_name: {imagenet_val[predict_label][0]} \n"
            )
    return acc_all


def gen_report(acc):
    print()
    tool_utils.report_flag_start('MAPPER-EVAL')
    print('{:.4f}'.format(acc))
    tool_utils.report_flag_end('MAPPER-EVAL')
