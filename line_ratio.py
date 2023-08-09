from master import  get_snapshot, get_snapshot_raw


gas =input("Enter gas type [Ne or Ar] = ")

while True:
    shot = int(input("Enter shot number of measurment = "))
    power = float(input("Enter RF power [W] = "))
    fullname = get_snapshot(path='Spectrum_data/Line_ratio/',name=f"gas={gas}_shot={shot}_power={power}W_")

# The coil current is fixed at 63.8 A for shots 1 to 25
# The coil current is fixed at 0 A for shots 26 to 45