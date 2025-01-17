import sys
import os
import threading

from multiprocessing.pool   import ThreadPool
from configparser           import ConfigParser

from bladerf               import _bladerf

b = _bladerf.BladeRF()
board_name = b.board_name
fpga_size = b.fpga_size
