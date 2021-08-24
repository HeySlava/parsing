from bs4 import BeautifulSoup
import csv
import datetime
import json
import lxml
import os
import requests
import time

if not os.path.isdir('data/'):
    os.mkdir('data')

