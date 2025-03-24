import mindwave, time
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Initialize headset
headset = mindwave.Headset('COM7')
time.sleep(2)

# Load images (replace with your image paths)
alert_image_path = "uglyface.png"  # Low attention warning
reward_image_path = "goodfocus.png"  # High attention reward
neutral_image_path = "neutral.png"  # Default neutral image

alert_image = Image.open(alert_image_path)
reward_image = Image.open(reward_image_path)
neutral_image = Image.open(neutral_image_path)

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
low_attention_start = None  # Track when attention falls below 20
high_attention_start = None  # Track when attention exceeds 80

# Function to display image
def show_image(image, title):
    plt.figure()
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.title(title)
    plt.show()

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

            # Check for prolonged low or high attention
            if attention_value < 30:
                if low_attention_start is None:
                    low_attention_start = current_time
                elif current_time - low_attention_start > 5:  # More than 5 seconds
                    show_image(alert_image, "Pay Attention!")
                    low_attention_start = None  # Reset timer
                    high_attention_start = None  # Reset high attention timer
            else:
                low_attention_start = None  # Reset if attention rises

            if attention_value > 50:
                if high_attention_start is None:
                    high_attention_start = current_time
                elif current_time - high_attention_start > 5:  # More than 5 seconds
                    show_image(reward_image, "Great Focus!")
                    high_attention_start = None  # Reset timer
                    low_attention_start = None  # Reset low attention timer
            else:
                high_attention_start = None  # Reset if attention drops

            # Show neutral image if neither condition is met
            if low_attention_start is None and high_attention_start is None:
                show_image(neutral_image, "Keep Going!")

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
