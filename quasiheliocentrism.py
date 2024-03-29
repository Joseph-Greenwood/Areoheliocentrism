import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from time import time

startTime = time()

starting_angles = {
    "Mercury": 0,  # Example angles, adjust as needed
    "Venus": 0,
    "Earth": 0,
    "Mars": 0,  # Angle for Sun's position relative to Mars
    "Jupiter": 0,
    "Saturn": 0,
}

# Constants and Scale
scale_factor = 1.0e6  # Adjust as needed
orbital_periods = {
    "Mercury": 88,
    "Venus": 225,
    "Earth": 365,
    "Mars": 687,  # Period for Sun's orbit around Mars
    "Jupiter": 4333,
    "Saturn": 10759,
}
radii = {
    "Mercury": 57.9e6 / scale_factor,
    "Venus": 108.2e6 / scale_factor,
    "Earth": 149.6e6 / scale_factor,
    "Mars": 227.9e6 / scale_factor,
    "Jupiter": 778.6e6 / scale_factor,
    "Saturn": 1433.5e6 / scale_factor,
}

# Updated Colors for Planets
planet_colors = {
    "Mercury": "darkorange",
    "Venus": "magenta",
    "Earth": "turquoise",
    "Mars": "red",
    "Jupiter": "white",
    "Saturn": "goldenrod",
}

central_planet = input("Central planet? ")

# Input: Number of days for the animation and starting angles
animation_days = (
    float(input("How many years? ")) * orbital_periods[central_planet]
)  # Example: 365 days


number_of_frames = int(animation_days)


# Function to calculate position
def position(radius, angle):
    x = radius * np.cos(np.radians(angle))
    y = radius * np.sin(np.radians(angle))
    return x, y


# Initialize plot with black background
fig, ax = plt.subplots()
ax.set_facecolor("black")
frame_radius = 800
ax.set_xlim(-frame_radius, frame_radius)
ax.set_ylim(-frame_radius, frame_radius)
ax.set_aspect("equal")

# Mars as a stationary point
venus_point = ax.plot(
    0, 0, "o", color=planet_colors[central_planet], label=central_planet
)[0]

# Sun as a point orbiting Mars, and its trajectory
sun_point = ax.plot([], [], "o", color="yellow", markersize=10, label="Sun")[0]
sun_trajectory = ([], [])

# Initialize planets and their trajectories
planet_points = {}
trajectories = {}
for planet in ["Mercury", "Venus", "Mars", "Earth", "Jupiter", "Saturn"]:
    if planet != central_planet:
        planet_points[planet] = ax.plot([], [], "o", color=planet_colors[planet])[0]
        trajectories[planet] = ([], [])


# Update function for animation
def update(frame):
    days_passed = frame * animation_days / number_of_frames

    # Update Sun's position (orbiting Mars)
    sun_angle = (
        starting_angles[central_planet]
        + (days_passed % orbital_periods[central_planet])
        / orbital_periods[central_planet]
        * 360
    )
    sun_x, sun_y = position(radii[central_planet], sun_angle)
    sun_point.set_data(sun_x, sun_y)
    sun_trajectory[0].append(sun_x)
    sun_trajectory[1].append(sun_y)
    ax.plot(
        sun_trajectory[0],
        sun_trajectory[1],
        color="yellow",
        linestyle=":",
        linewidth=1,
        alpha=0.5,
    )

    # Update positions of other planets relative to the Sun
    for planet, period in orbital_periods.items():
        if planet != central_planet:
            angle = starting_angles[planet] + (days_passed % period) / period * 360
            x, y = position(radii[planet], angle)
            planet_x, planet_y = sun_x + x, sun_y + y
            planet_points[planet].set_data(planet_x, planet_y)
            trajectories[planet][0].append(planet_x)
            trajectories[planet][1].append(planet_y)
            ax.plot(
                trajectories[planet][0],
                trajectories[planet][1],
                color=planet_colors[planet],
                linestyle=":",
                linewidth=1,
                alpha=0.5,
            )

    return [sun_point] + list(planet_points.values())


# Create animation
ani = FuncAnimation(
    fig, update, frames=np.linspace(0, animation_days, number_of_frames), blit=True
)

# Uncomment to save the animation
ani.save(
    f"{central_planet.lower()}_solar_system_animation.gif", writer="pillow", fps=20
)

print(f"This took {time() - startTime} seconds!")
