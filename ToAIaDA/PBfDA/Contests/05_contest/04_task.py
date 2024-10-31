import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(15, 6))

angle = np.linspace(0, 360, 100)
position = 5 * np.sin(np.deg2rad(angle)) 
axes[0].plot(angle, position, color="#008080")
axes[0].set_title("Position vs Angle")
axes[0].set_xlabel("Angle (degrees)")
axes[0].set_ylabel("Position (in)")
axes[0].set_xlim(0, 360)
axes[0].set_ylim(-2.5, 5.5)
axes[0].grid(True)

angle = np.linspace(0, 360, 100)
speed = 180 * np.cos(np.deg2rad(angle))
axes[1].plot(angle, speed, color="#008080", label="True Speed")
axes[1].plot([0, 360], [50, 50], color="#FFA500", label="Mean Piston Speed")
axes[1].scatter([90, 270], [0, 0], color="black", marker="*", label="Top Dead Center")
axes[1].scatter([90, 270], [0, 0], color="black", marker="o", label="Bottom Dead Center")
axes[1].set_title("Piston Speed vs Angle")
axes[1].set_xlabel("Angle (degrees)")
axes[1].set_ylabel("Piston Velocity (mph)")
axes[1].set_xlim(0, 360)
axes[1].set_ylim(-200, 200)
axes[1].grid(True)
axes[1].legend(loc="lower right")

angle = np.linspace(0, 360, 100)
force = 4500 * np.sin(2 * np.deg2rad(angle))
axes[2].plot(angle, force, color="#008080")
axes[2].set_title("Piston Net Force vs Angle")
axes[2].set_xlabel("Angle (degrees)")
axes[2].set_ylabel("Piston Acceleration (g)")
axes[2].set_xlim(0, 360)
axes[2].set_ylim(-9000, 5000)
axes[2].grid(True)

plt.tight_layout()

plt.show()