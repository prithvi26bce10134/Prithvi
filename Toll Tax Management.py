import json
import datetime

datafile = "tollrecords.json"

rates = {
    "car": 50,
    "bus": 100,
    "truck": 150,
    "bike": 20
}

records = []
dailytravel = {}


def record():
    global records, dailytravel
    try:
        with open(datafile, "r") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []
    for r in records:
        dailytravel[(r["vn"], r["date"])] = True


def save():
    with open(datafile, "w") as f:
        json.dump(records, f, indent=2)


def showrates():
    print("\nToll Rates:")
    for vehicle, rate in rates.items():
        print(vehicle.title(), ": Rs.", rate)


def travel(vn, today):
    return (vn, today) in dailytravel


def toll():
    vn = input("Enter vehicle number: ").strip().upper()
    vt = input("Enter vehicle type (car/bus/truck/bike): ").lower()

    while vt not in rates:
        print("Invalid vehicle type!")
        vt = input("Enter vehicle type (car/bus/truck/bike): ").lower()

    now = datetime.datetime.now()
    today = now.date().isoformat()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    baseamt = rates[vt]

    if travel(vn, today):
        amt = baseamt / 2
        print("\nVehicle already traveled today — half toll applies.")
    else:
        amt = baseamt

    record = {
        "vn": vn,
        "vt": vt,
        "amt": amt,
        "date": today,
        "timestamp": timestamp
    }
    records.append(record)
    dailytravel[(vn, today)] = True
    save()

    print("\nToll collected: Rs.", amt, " from ", vn, " (", vt, ") at", timestamp)


def showrecords():
    if not records:
        print("\nNo records yet.")
        return
    print("\nVehicle No | Type | Amount | Timestamp")
    for r in records:
        print(r["vn"], " | ", r["vt"], " | Rs.", r["amt"], " | ", r["timestamp"])


def totalcollection():
    total = sum(r["amt"] for r in records)
    print("\nTotal toll collected: Rs.", total)


def searchrecords():
    vn = input("Vehicle number (leave blank to skip): ").strip().upper()
    d = input("Date YYYY-MM-DD (leave blank to skip): ").strip()

    results = records
    if vn:
        results = [r for r in results if r["vn"] == vn]
    if d:
        results = [r for r in results if r["date"] == d]

    if not results:
        print("\nNo matching records.")
        return

    print("\nVehicle No | Type | Amount | Timestamp")
    for r in results:
        print(r["vn"], " | ", r["vt"], " | Rs.", r["amt"], " | ", r["timestamp"])


def main():
    record()
    while True:
        print("\n---- TOLL TAX MANAGEMENT ----")
        print("1. Show Toll Rates")
        print("2. Collect Toll")
        print("3. Show All Records")
        print("4. Total Collection")
        print("5. Search Records")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            showrates()
        elif choice == "2":
            toll()
        elif choice == "3":
            showrecords()
        elif choice == "4":
            totalcollection()
        elif choice == "5":
            searchrecords()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice!")


main()
