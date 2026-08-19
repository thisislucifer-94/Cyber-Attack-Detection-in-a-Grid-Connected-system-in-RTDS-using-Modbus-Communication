# # # # from pymodbus.client import ModbusTcpClient

# # # # client = ModbusTcpClient("10.16.28.92", port=502)

# # # # if client.connect():

# # # #     rr = client.read_input_registers(
# # # #         address=0,
# # # #         count=1,
# # # #         device_id=1
# # # #     )

# # # #     if not rr.isError():
# # # #         print("Register 0 =", rr.registers[0])
# # # #     else:
# # # #         print("Read Error")

# # # #     client.close()

# # # # else:
# # # #     print("Connection Failed")


# # # from pymodbus.client import ModbusTcpClient
# # # import time

# # # GTNET_IP = "10.16.28.92"
# # # PORT = 502
# # # DEVICE_ID = 1

# # # client = ModbusTcpClient(GTNET_IP, port=PORT)

# # # if not client.connect():
# # #     print("Connection Failed")
# # #     quit()

# # # print("Connected to GTNET")

# # # try:
# # #     while True:

# # #         rr = client.read_input_registers(
# # #             address=0,
# # #             count=1,
# # #             device_id=DEVICE_ID
# # #         )

# # #         if not rr.isError():
# # #             print("Register 0 =", rr.registers[0])
# # #         else:
# # #             print("Read Error")

# # #         time.sleep(0.1)  # 100 ms

# # # except KeyboardInterrupt:
# # #     print("\nStopped by User")

# # # finally:
# # #     client.close()
# # #     print("Connection Closed")

# # from pymodbus.client import ModbusTcpClient
# # import struct
# # import time

# # client = ModbusTcpClient("10.16.28.92", port=502)

# # if not client.connect():
# #     print("Connection Failed")
# #     quit()

# # print("Connected")

# # try:
# #     while True:

# #         r0 = client.read_input_registers(
# #             address=0,
# #             count=1,
# #             device_id=1
# #         )

# #         r1 = client.read_input_registers(
# #             address=1,
# #             count=1,
# #             device_id=1
# #         )

# #         if not r0.isError() and not r1.isError():

# #             word1 = r0.registers[0]
# #             word2 = r1.registers[0]

# #             try:
# #                 vdc = struct.unpack(
# #                     ">f",
# #                     struct.pack(">HH", word1, word2)
# #                 )[0]

# #                 print("vdc =", vdc)

# #             except:
# #                 print("Float conversion failed")

# #         time.sleep(0.1)

# # except KeyboardInterrupt:
# #     pass

# # finally:
# #     client.close()


# from pymodbus.client import ModbusTcpClient
# import struct
# import time

# GTNET_IP = "10.16.28.92"
# PORT = 502
# DEVICE_ID = 1

# client = ModbusTcpClient(GTNET_IP, port=PORT)

# if not client.connect():
#     print("Connection Failed")
#     quit()

# print("Connected to GTNET")

# try:
#     while True:

#         # Read two registers
#         rr0 = client.read_input_registers(
#             address=0,
#             count=1,
#             device_id=DEVICE_ID
#         )

#         rr1 = client.read_input_registers(
#             address=1,
#             count=1,
#             device_id=DEVICE_ID
#         )

#         if not rr0.isError() and not rr1.isError():

#             R0 = rr0.registers[0]
#             R1 = rr1.registers[0]

#             # Float32 CDAB
#             value = struct.unpack(
#                 ">f",
#                 struct.pack(">HH", R1, R0)
#             )[0]

#             print(f"Vdc = {value:.6f}")

#         else:
#             print("Read Error")

#         time.sleep(0.1)   # 100 ms

# except KeyboardInterrupt:
#     print("\nStopped by User")

# finally:
#     client.close()
#     print("Connection Closed")

from pymodbus.client import ModbusTcpClient
import struct
import time
import matplotlib.pyplot as plt

# =====================================================
# GTNET Configuration
# =====================================================
GTNET_IP = "10.16.28.92"
PORT = 502
DEVICE_ID = 1

# =====================================================
# Connect to GTNET
# =====================================================
client = ModbusTcpClient(GTNET_IP, port=PORT)

if not client.connect():
    print("Connection Failed")
    quit()

print("Connected to GTNET")

# =====================================================
# Initialize Plot
# =====================================================
plt.ion()

x_data = []
y_data = []

fig, ax = plt.subplots()

line, = ax.plot([], [], linewidth=2)

ax.set_title("RTDS Vdc Monitoring")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Vdc (pu)")
ax.grid(True)

start_time = time.time()

# =====================================================
# Read Data Continuously
# =====================================================
try:

    while True:

        rr0 = client.read_input_registers(
            address=0,
            count=1,
            device_id=DEVICE_ID
        )

        rr1 = client.read_input_registers(
            address=1,
            count=1,
            device_id=DEVICE_ID
        )

        if not rr0.isError() and not rr1.isError():

            R0 = rr0.registers[0]
            R1 = rr1.registers[0]

            # Float32 CDAB Conversion
            Vdc = struct.unpack(
                ">f",
                struct.pack(">HH", R1, R0)
            )[0]

            # Print in terminal
            print(f"\rVdc = {Vdc:.6f}", end="")

            # Time Axis
            t = time.time() - start_time

            x_data.append(t)
            y_data.append(Vdc)

            # Keep last 200 samples
            if len(x_data) > 200:
                x_data.pop(0)
                y_data.pop(0)

            # Update graph
            line.set_xdata(x_data)
            line.set_ydata(y_data)

            ax.relim()
            ax.autoscale_view()

            plt.draw()
            plt.pause(0.001)

        else:
            print("\nRead Error")

        time.sleep(0.1)

except KeyboardInterrupt:

    print("\nStopped by User")

finally:

    client.close()
    plt.ioff()
    plt.show()

    print("Connection Closed")
