# coding: utf-8
import rjpl
hkp = rjpl.stopsNearby(55.713, 12.55993) [0]
rp = rjpl.stopsNearby(55.7154065239803, 12.558852402226337)[1]
# hkp = rjpl.location("Hans Knudsens Plads (Lyngbyvej)")["StopLocation"][0]
import time
import datetime
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
layout = Layout()
layout.split_row(
   Layout(name="left"),
   Layout(name="right"),
)
#print(layout)
console = Console()
def colorize(r_):
    if "S" in r_["name"]:
        return "blue"
    elif "E" in r_["name"]:
        return "green"
    else:
        return "yellow"
def generate_table(stopObj) -> Table:  # update 4 times a second to feel fluid
    table = Table(title=str(datetime.datetime.today()))
    table.add_column("Bus Nr.")
    table.add_column("Expected time")
    table.add_column("Real time")
    table.add_column("Direction")
    table.add_column("Stop Name")
    # import ipdb; ipdb.set_trace()
    try:
        departures = rjpl.multiDepartureBoard(*[int(s_["id"]) for s_ in stopObj], useTrain=False, useBus=True, useMetro=False)
    except:
        return table
    onlyBusDept = []
    for d_ in departures:
        # if d_['type'] == 'BUS':
        #if "Nørreport" not in d_["direction"]:
        onlyBusDept.append(d_)
    for row in onlyBusDept:

        if "Hans" in row["stop"]:
            stopSted = "HKP"
        else:
            stopSted = "RP"
        table.add_row("[{}]{}".format(colorize(row), row["name"]),
            "{}".format(row["time"]),
            "{}".format(row["rtTime"] if "rtTime" in row.keys() else "N/A"),
            "{}".format(row['direction']),
                    "{}".format(stopSted))
    return table
with Live(generate_table([hkp, rp]), refresh_per_second=0.1, console=console) as live:
    while 1:
        live.update(generate_table([hkp, rp]))
