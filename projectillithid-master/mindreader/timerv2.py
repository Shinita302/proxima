import mindwave, time
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for macOS compatibility
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import sys

# === User-specified session duration ===
try:
    user_input = input("Enter session duration in minutes: ")
    session_duration = int(user_input) * 60  # Convert to seconds
except ValueError:
    print("Invalid input. Defaulting to 5 minutes.")
    session_duration = 300

# === Initialize headset ===
# headset = mindwave.Headset('COM7')  # Uncomment if using real headset
time.sleep(2)

cumulative_focus = 0
ticks = 0

# === Data buffers ===
max_points = 100
x_data = deque(maxlen=max_points)
y_data = deque(maxlen=max_points)

# === Attention Plot Setup ===
fig1 = plt.figure(figsize=(10, 6))
ax1 = fig1.add_subplot(111)
line, = ax1.plot([], [], 'b-', linewidth=2)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Attention Level')
ax1.set_ylim(0, 100)
ax1.set_title('Mindwave Attention Level Over Time')
ax1.grid(True, alpha=0.3)

# === Timer Window Setup ===
fig2 = plt.figure(figsize=(6, 4))
ax2 = fig2.add_subplot(111)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

# Timer Texts
timer_text = ax2.text(0.5, 0.7, '00:00:00', fontsize=36, ha='center', va='center', weight='bold', color='blue')
session_text = ax2.text(0.5, 0.4, 'Session Time', fontsize=14, ha='center', va='center')
avg_attention_text = ax2.text(0.5, 0.2, 'Avg Attention: --', fontsize=12, ha='center', va='center')
ax2.set_title('Session Timer', fontsize=16, weight='bold')

plt.ion()

# Position plot windows (adjust as needed)
mngr1 = fig1.canvas.manager
mngr1.window.wm_geometry("+100+100")
mngr2 = fig2.canvas.manager
mngr2.window.wm_geometry("+800+100")

plt.show(block=False)

start_time = time.time()
plot_update_counter = 0
timer_update_counter = 0
update_frequency = 20
timer_update_frequency = 5

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

print("Starting data collection... Press Ctrl+C to stop")

try:
    while True:
        time.sleep(0.2)
        current_time = time.time() - start_time

        # === Auto-exit on timeout ===
        if current_time >= session_duration:
            print("\nSession completed.")
            avg_attention = cumulative_focus / ticks if ticks > 0 else 0
            print("Your average focus value was: {:.1f}".format(avg_attention))
            break

        # Simulated attention value (replace with headset.attention)
        attention_value = np.random.randint(20, 80)
        print(attention_value)

        ticks += 1
        cumulative_focus += attention_value

        if attention_value != 0:
            x_data.append(current_time)
            y_data.append(attention_value)

            plot_update_counter += 1
            if plot_update_counter >= update_frequency:
                plot_update_counter = 0
                try:
                    line.set_data(list(x_data), list(y_data))
                    if len(x_data) > 1:
                        ax1.set_xlim(x_data[0], x_data[-1])
                    ax1.relim()
                    ax1.autoscale_view()
                    fig1.canvas.draw()
                except Exception as e:
                    print("Plot update error: {}".format(e))

        timer_update_counter += 1
        if timer_update_counter >= timer_update_frequency:
            timer_update_counter = 0
            try:
                timer_text.set_text(format_time(current_time))
                if ticks > 0:
                    avg_attention = cumulative_focus / ticks
                    avg_attention_text.set_text('Avg Attention: {:.1f}'.format(avg_attention))

                if avg_attention > 60:
                    timer_text.set_color('green')
                elif avg_attention > 30:
                    timer_text.set_color('yellow')
                else:
                    timer_text.set_color('red')

                fig2.canvas.draw()
            except Exception as e:
                print("Timer update error: {}".format(e))

        try:
            fig1.canvas.flush_events()
            fig2.canvas.flush_events()
        except:
            pass

        if ticks % 100 == 0:
            avg_attention = cumulative_focus / ticks if ticks > 0 else 0
            print("Time: {}, Attention: {}, Avg: {:.1f}, Data points: {}".format(
                format_time(current_time), attention_value, avg_attention, len(x_data)))
            import gc
            gc.collect()

except KeyboardInterrupt:
    print("\nSession stopped by user.")
    print("Final Statistics:")
    print("Session Duration: {}".format(format_time(current_time)))
    if ticks > 0:
        print("Average Attention: {:.1f}".format(cumulative_focus / ticks))
    print("Total Data Points: {}".format(len(x_data)))

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
