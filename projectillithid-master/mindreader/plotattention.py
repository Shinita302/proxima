import mindwave, time
import matplotlib
# Set backend before any other matplotlib imports
matplotlib.use('TkAgg')  # Works well with macOS and Python 2.7
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import sys

# Initialize headset
headset = mindwave.Headset('COM7')
time.sleep(2)

cumulative_focus = 0
ticks = 0

# Use deque for faster append/pop operations
max_points = 100
x_data = deque(maxlen=max_points)
y_data = deque(maxlen=max_points)

# Initialize plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
line, = ax.plot([], [], 'b-', linewidth=2)

ax.set_xlabel('Time (s)')
ax.set_ylabel('Attention Level')
ax.set_ylim(0, 100)
ax.set_title('Mindwave Attention Level Over Time')
ax.grid(True, alpha=0.3)

plt.ion()  # Turn on interactive mode AFTER creating the figure
plt.show(block=False)  # Show non-blocking

start_time = time.time()
plot_update_counter = 0
update_frequency = 20  # Slower updates for stability

print("Starting data collection... Press Ctrl+C to stop")

try:
    while True:
        time.sleep(0.2)  # Increased sleep time for Python 2.7 stability
        current_time = time.time() - start_time
        attention_value = headset.attention
        print(attention_value)
        #attention_value = np.random.randint(20, 80)
        
        ticks += 1
        cumulative_focus += attention_value
        
        if attention_value != 0:
            x_data.append(current_time)
            y_data.append(attention_value)
            
            # Only update plot every few iterations
            plot_update_counter += 1
            if plot_update_counter >= update_frequency:
                plot_update_counter = 0
                
                try:
                    # Update plot data
                    line.set_data(list(x_data), list(y_data))
                    if len(x_data) > 1:
                        ax.set_xlim(x_data[0], x_data[-1])
                    
                    # Redraw the plot
                    ax.relim()
                    ax.autoscale_view()
                    plt.draw()
                    
                    # Force GUI update (important for macOS)
                    if hasattr(plt.get_current_fig_manager(), 'canvas'):
                        plt.get_current_fig_manager().canvas.flush_events()
                    
                except Exception as e:
                    print("Plot update error: {}".format(e))
                    continue
        
        # Print current values every 100 iterations
        if ticks % 100 == 0:
            print("Time: {:.2f}s, Attention: {}, Data points: {}".format(
                current_time, attention_value, len(x_data)))
            # Force garbage collection occasionally
            import gc
            gc.collect()

except KeyboardInterrupt:
    print("\nPlotting stopped by user.")
except Exception as e:
    print("Error occurred: {}".format(e))
    import traceback
    traceback.print_exc()
finally:
    plt.ioff()
    try:
        plt.close('all')
    except:
        pass
    print("Cleanup completed.")
