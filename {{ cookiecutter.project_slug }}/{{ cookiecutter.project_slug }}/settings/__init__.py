from . base import * 
import os 
from decouple import config 




if config('ENV_NAME') == "Production":
    from . production import * 
elif config('ENV_NAME') == 'Local':
    from local import * 
else:
    raise NameError("ENV not configured")