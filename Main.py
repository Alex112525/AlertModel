import pandas as pd
import Model
import os


if __name__ == "__main__":
    # Sets a list of range tuples in the circadian rhythm
    circadian = [(80, 90), (50, 60), (20, 30), (80, 70), (50, 40), (20, 10)]
    # Set the type of memory that we use
    memory = ["loss", "mean"]
    # Set the number of samples 
    sample = 64
    
    for cir in circadian:
        for mem in memory:
            dir = "Data/" + mem + "_" + str(cir[0]) + "-" + str(cir[1])
            set1, set2, set3 = Model.AlertModel(sample, cir, mem, dir)
            # s1 = pd.DataFrame(set1)
            # s2 = pd.DataFrame(set2)
            # s3 = pd.DataFrame(set3)

            # os.makedirs(dir, exist_ok=True)
            # s1.to_csv(dir + "/set1.csv")
            # s2.to_csv(dir + "/set2.csv")
            # s3.to_csv(dir + "/set3.csv")


