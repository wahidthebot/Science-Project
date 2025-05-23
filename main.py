# Sullivan, Wahid
# Science Fair Project

# All of the libraries used

import sys
import re
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# GraphData(CSV df, DataFrame fig, Series xData, Series yData);
# -- This type is used to store all relevant graph data per drawing session
class GraphData:
    def __init__(self, df, fig, xData, yData):
        self.df = df
        self.fig = fig
        self.xData = xData 
        self.yData = yData

# Global variables

global currentGraph 
global line
global anim

# Global constants

BASE_RATE = .42
DRAW_INTERVAL = 750

# string FmtForAxis(yAxisName):
# -- turns string like: "This_Is_The_Y_Axis" into: "This Is The Y Axis"
def FmtForAxis(yAxisName):
    return yAxisName.replace("_", " ")

# float calculateGrowthRate(float temp, float co2);
# -- returns the growth data based on temp && co2 input
def CalculateGrowthRate(temp, co2):
    # Growth_Rate = Base_Rate * (1.02^((Temperature - 15)/1)) * (1.01^((CO2 - 330)/10))
    # Where:
    # - Base_Rate = 0.42 (baseline growth rate at 15°C and 330ppm CO2)
    # - Temperature is in Celsius
    # - CO2 is in ppm
    tempFactor = math.pow(1.02, ((temp - 15) / 2))
    co2Factor = math.pow(1.01, ((co2 - 330) / 10))
    growthData = BASE_RATE * tempFactor * co2Factor
    return growthData

# GraphData GetGraphDataFromCSV(string csvPath);
# -- returns data read from the CSV file given through the csvPath as a GraphData object
def GetGraphDataFromCSV(csvPath, measure, title):
    df = pd.read_csv(csvPath)

    fig, ax = plt.subplots(figsize=(10, 6))
    xData = df["Year"]
    yData = df[measure]

    global line
    line, = ax.plot([], [], marker='o', linestyle='-')

    ax.set_xlim(min(xData), max(xData))
    ax.set_ylim(min(yData), max(yData))
    ax.set_xlabel("Time")
    ax.set_ylabel(FmtForAxis(measure))
    ax.set_title(title)

    return GraphData(df, fig, xData, yData)

# Line2D UpdateGraph(frame?);
# -- returns the current line given the frame of the graph animation
def UpdateGraph(frame):
    global currentGraph
    line.set_data(currentGraph.xData[:frame], currentGraph.yData[:frame])

    # Clear all of the previous annotations
    for text in currentGraph.fig.axes[0].texts:
        text.remove()
    
    # Add annotations only for points that are literally drawn
    for i in range(frame):
        if i == 0: continue # Skip the first one because it will always overlap with the y-axis text 
        plt.annotate(f"T: {currentGraph.df['Temperature_C'][i]}°C\nCO2: {currentGraph.df['CO2_ppm'][i]} ppm\nGR: {CalculateGrowthRate(currentGraph.df['Temperature_C'][i], currentGraph.df['CO2_ppm'][i]):.2f}%",
                     (currentGraph.xData[i], currentGraph.yData[i]),
                     textcoords="offset points",
                     xytext=(10, 10),
                     ha='right',
                     fontsize=8)

    return line,

# void SaveCSVAsAnimation(string csvPath, string animPath, string measure);
# -- saves the csv (given in csvPath) as an animation (at animPath) given the y-axis: (measure)
def SaveCSVAsAnimation(csvPath, animPath, measure, title):
    print("creating animation:", animPath, "from csv:", csvPath, "given the y-axis:", measure, end="...\n")
    global currentGraph
    currentGraph = GetGraphDataFromCSV(csvPath, measure, title)
    global anim
    anim = animation.FuncAnimation(currentGraph.fig, UpdateGraph, frames=len(currentGraph.df), interval=DRAW_INTERVAL, blit=False)
    anim.save(animPath, writer="ffmpeg")

# void Main(void);
# -- entry point of the program
def Main():
    print("Beginning to create animations...")

    with open("instructions.txt", "r") as inst:
        content = inst.read()

    pattern = r'\(input="([^"]+)", output="([^"]+)", measure="([^"]+)", title="([^"]+)"\)'
    matches = re.findall(pattern, content)
    dataEntries = [{"input": m[0], "output": m[1], "measure": m[2], "title": m[3]} for m in matches]

    for entry in dataEntries:
        try:
            SaveCSVAsAnimation(entry['input'], entry['output'], entry['measure'], entry['title'])
        except Exception as e:
            print(f"Error from ('{entry['input']}') {type(e).__name__} - {e}", file=sys.stderr)
            return False

    print("Finished")

    return True

# Call Main()
if __name__ == "__main__":
    if not Main(): # If the main fn encounters an error
        print("Animation creating halted; error encountered")
        exit(1)