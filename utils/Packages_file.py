#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 08:18:24 2021

@author: mleeuwen
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import sys 
import time
from tqdm import tqdm
import nibabel as nib
from sklearn.feature_extraction import image
from skimage.measure import label, regionprops
import random
import pandas as pd
from scipy.ndimage import zoom
import json
import io 
import copy
import csv
import subprocess
