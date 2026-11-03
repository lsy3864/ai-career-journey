import pandas as pd

data = {
    "desk" : ["Equity", "Bond", "FX", "Credit", "Derivatives"],
    "limit" : [100, 200, 80, 150, 120],
    "exposure" : [72, 195, 85, 90, 110],
}

df = pd.DataFrame(data)


print(df)
print("Step1-------------------------")

df["usage"] = df["exposure"] / df["limit"]

def check_status(usage):
    if usage > 1.0:
        return "BREACH"

    elif usage >= 0.9:
        return "WARNING"

    else:
        return "OK"

df["status"] = df["usage"].apply(check_status)

print(df)
print("Step2-------------------------")

print("Desks requiring action:")
print(df[df["status"] != "OK"])

df.to_csv("practice/limit_report.csv", index = False)
print("\nSaved: practice/limit_report.csv")