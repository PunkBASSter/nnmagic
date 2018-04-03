import math
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import time

import cntk as C
import cntk.tests.test_utils
from cntk.ops.functions import load_model
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


class ModelEvaluator:
    _modelFilePath = None
