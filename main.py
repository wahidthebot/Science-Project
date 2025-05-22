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
DRAW_INTERVAL = 1000

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
def GetGraphDataFromCSV(csvPath):
    df = pd.read_csv(csvPath)

    fig, ax = plt.subplots()
    xData = df["Year"]
    yData = df["Growth_Rate_Per_Day"]

    global line
    line, = ax.plot([], [], marker='o', linestyle='-')

    ax.set_xlim(min(xData), max(xData))
    ax.set_ylim(min(yData), max(yData))
    ax.set_xlabel("X-axis Label")
    ax.set_ylabel("Y-axis Label")
    ax.set_title("Animated Graph from CSV Data")

    return GraphData(df, fig, xData, yData)

def UpdateGraph(frame):
    global currentGraph
    line.set_data(currentGraph.xData[:frame], currentGraph.yData[:frame])
    return line,

def SaveCSVAsAnimation(csvPath, animPath):
    global currentGraph
    currentGraph = GetGraphDataFromCSV(csvPath)
    global anim
    anim = animation.FuncAnimation(currentGraph.fig, UpdateGraph, frames=len(currentGraph.df), interval=DRAW_INTERVAL)
    anim.save(animPath, writer="ffmpeg")

SaveCSVAsAnimation("decompositionData.csv", "outputAnimations/decomposition.mp4")
SaveCSVAsAnimation("diversityData.csv.csv", "outputAnimations/diversity.mp4")
SaveCSVAsAnimation("extendedData.csv", "outputAnimations/extended.mp4")
SaveCSVAsAnimation("growthData.csv", "outputAnimations/growth.mp4")