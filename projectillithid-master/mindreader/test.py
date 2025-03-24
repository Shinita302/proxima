import mindwave, time
import matplotlib.pyplot as plt
import numpy as np

# Initialize headset
headset = mindwave.Headset('COM7')
time.sleep(2)

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data, 'b-')  # Blue line

ax.set_xlabel('Time (s)')
ax.set_ylabel('Attention Level')
ax.set_ylim(0, 100)  # Attention values range from 0-100
ax.set_title('Mindwave Attention Level Over Time')

start_time = time.time()

try:
    while True:
        time.sleep(0.1)  # Update every 100ms
        current_time = time.time() - start_time
        attention_value = headset.attention

        if attention_value != 0:  # Avoid plotting invalid values
            x_data.append(current_time)
            y_data.append(attention_value)

            # Keep the last 100 points for a rolling window effect
            if len(x_data) > 100:
                x_data.pop(0)
                y_data.pop(0)

            # Update plot
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            ax.relim()  # Recalculate limits
            ax.autoscale_view()  # Rescale view
            plt.draw()
            plt.pause(0.01)  # Allow time for the plot to update

except KeyboardInterrupt:
    print("Plotting stopped.")

plt.ioff()  # Turn off interactive mode
plt.show()  # Show final static plot
