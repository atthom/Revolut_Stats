import functions as f
import os


for item in os.listdir('.'):
    if item.endswith(".csv"):
        try:
            f.make_stats(item)
        except:
            print("Bad format for file")

