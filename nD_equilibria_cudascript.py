# this script should be compiled into a cuda-friendly language and run on the gu server
# it will save out the equilibria found in the games specified as numpy ndarray objects

import networkx as nx  # can these packages be used with cuda?
import pandas as pand
import numpy as np
import itertools
import copy

import nD_equilibria_finder as utils  # can this be sent to cuda?

