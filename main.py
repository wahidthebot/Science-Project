# Sullivan, Wahid
# Science Fair Project

import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

print("Beginning to create animations...")

SaveCSVAsAnimation("decompositionData.csv", "outputAnimations/decomposition.mp4", measure="Decomposition_Rate_Percent", title="Decomposition Rate Per Decade")
SaveCSVAsAnimation("diversityData.csv", "outputAnimations/diversity.mp4", measure="Diversity_Index", title="TODO")
SaveCSVAsAnimation("extendedData.csv", "outputAnimations/extended.mp4", measure="Growth_Rate_Per_Day", title="TODO")
SaveCSVAsAnimation("growthData.csv", "outputAnimations/growth.mp4", measure="Growth_Rate_Per_Day", title="TODO")

print("Finished")