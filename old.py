from pathlib import Path
import json
import pandas as pd
from datetime import datetime
from typing import List
import streamlit as st
import plotly.express as px
from data_cleaning import gdata
import streamlit.components.v1 as components

components.html('<h1>Hery</h1>')
components.html('<img height="250" src="https://github.com/Brandt-moreThan4/chicken_sammy/blob/v2/data/sample_images/156842797118905542_1200x1200.437da0a46bc84c24a4e5a359e3fe071c.jpeg?raw=true" alt="Sammy Image">',height=800)
