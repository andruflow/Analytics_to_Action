import os

DIR_ROOT=os.path.dirname(os.path.abspath(__file__))
DIR_CONF="{0}{1}conf{1}".format(DIR_ROOT, os.sep)
DIR_DATA="{0}{1}data{1}".format(DIR_ROOT, os.sep)
DIR_DATA_RAW="{0}{1}1_Raw{1}".format(DIR_DATA, os.sep)
DIR_DATA_STAGE="{0}{1}2_Stage{1}".format(DIR_DATA, os.sep)
DIR_DATA_ANALYTICS="{0}{1}3_Analytics{1}".format(DIR_DATA, os.sep)