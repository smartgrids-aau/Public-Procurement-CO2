import os
import pandas as pd
from pandas import DataFrame
import ABCAnalyzer
import DataVisualizer
from TablePlotter import Plot_Data
import TablePreprocessor
import TimeFilter
import XYZ_Analyzer
from co2data import CO2Values
from config import Config
from tableConfig import TableRunConfig
import matplotlib.pyplot as plt
import seaborn as sns
import ValAggr
from pandas import DataFrame
import TableFilePrinter
#tbldata

def analyze(runConfigs : list[TableRunConfig]):
       
    runConfigs = [item for item in runConfigs if item.isValid()]
    
    for runConfig in runConfigs:
        print(runConfig.tableFilePath)
        runConfig.tableData = pd.read_excel(runConfig.tableFilePath)
        
        runConfig.output = './output/{gemeinde}_{yearmin}_{yearmax}/'.format(gemeinde=runConfig.outFileNameWithoutExtension, yearmin=str(Config.get("MinYear")), yearmax=str(Config.get("MaxYear")))
        if not os.path.exists(runConfig.output):
            os.makedirs(runConfig.output)
        
    #now preprocess (throw out times, split tables, and merge common terms)
    TablePreprocessor.PreProcess(runConfigs)
    
    for runConfig in runConfigs:
        analyze_single(runConfig)
    
    TableFilePrinter.PrintTables(runConfigs)    
        
    DataVisualizer.Visualize(runConfigs)
      
def analyze_single(runConfig : TableRunConfig):
    #aggregate data
    ValAggr.Aggregate_Numbers_Analysis(runConfig)
   
    ABCAnalyzer.Analyze(runConfig)
    
    #now examine xyz on most expensive items
    XYZ_Analyzer.Analyze(runConfig)