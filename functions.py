import re

def compose_CodPos(x):
    if len(x) > 1:
        return re.sub('[^0-9]','', x[0]) + "-" + re.sub('[^0-9]','', x[1])
    else:
        return re.sub('[^0-9]','', x[0]) + "-" + "000"