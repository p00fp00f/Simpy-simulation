import simpy
import random
import matplotlib.pyplot as plt

# Initialize lists to store results
avg_waiting_times_ferris_wheel = []
avg_waiting_times_rollercoaster = []
people_left_ferris_wheel = []
people_left_rollercoaster = []

# Define simulation parameters
max_queue_size = 30  # Maximum queue size
ferris_wheel_capacity = 4  # Number of visitors per ride for Ferris Wheel
rollercoaster_capacity = 6  # Number of visitors per ride for Roller Coaster
ferris_wheel_duration = 7  # Duration of the Ferris Wheel ride (in minutes)
rollercoaster_duration = 5  # Duration of the Roller Coaster ride (in minutes)
arrival_interval = 3  # Average interval between visitor arrivals (in minutes)

# Define your visitor function
def visitor(env, name, queue, max_queue_size, waiting_times):
    """A visitor who joins the queue."""
    if len(queue.items) < max_queue_size:
        yield queue.put(env.now)  # Visitor joins the queue
        waiting_times.append(env.now)  # Record the waiting time
    else:
        # Visitor leaves the queue if it's full
        pass

# Define your ride function
def ride(env, name, ride_capacity, ride_duration, queue, count):
    """Ride operation, boarding passengers."""
    while True:
        passengers = []
        for _ in range(ride_capacity):
            if len(queue.items) > 0:
                passenger_time = yield queue.get()
                passengers.append(passenger_time)
        yield env.timeout(ride_duration)  # Simulate ride duration

# Define your visitor generation function
def generate_visitors(env, queue, max_queue_size, waiting_times):
    """Generate visitors to the queue."""
    for i in range(1, 101):  # Total of 100 visitors
        yield env.timeout(random.expovariate(1.0 / arrival_interval))  # Generate visitors based on Poisson process
        env.process(visitor(env, i, queue, max_queue_size, waiting_times))

# Run the simulation 100 times
for simulation in range(50):
    # Reset environment and data for each simulation
    env = simpy.Environment()
    ferris_wheel_queue = simpy.Store(env)
    rollercoaster_queue = simpy.Store(env)

    ferris_wheel_waiting_times = []
    rollercoaster_waiting_times = []
    
    # Start processes for visitors and rides
    env.process(generate_visitors(env, ferris_wheel_queue, max_queue_size, ferris_wheel_waiting_times))
    env.process(generate_visitors(env, rollercoaster_queue, max_queue_size, rollercoaster_waiting_times))
    
    # Start rides
    env.process(ride(env, "Ferris Wheel", ferris_wheel_capacity, ferris_wheel_duration, ferris_wheel_queue, None))
    env.process(ride(env, "Roller Coaster", rollercoaster_capacity, rollercoaster_duration, rollercoaster_queue, None))

    # Run the simulation
    env.run(until=120)

    # Calculate average waiting times and people left
    average_ferris_wheel_waiting_time = sum(ferris_wheel_waiting_times) / len(ferris_wheel_waiting_times) if ferris_wheel_waiting_times else 0
    average_rollercoaster_waiting_time = sum(rollercoaster_waiting_times) / len(rollercoaster_waiting_times) if rollercoaster_waiting_times else 0

    avg_waiting_times_ferris_wheel.append(average_ferris_wheel_waiting_time)
    avg_waiting_times_rollercoaster.append(average_rollercoaster_waiting_time)
    
    # Store the number of people who left the queue
    people_left_ferris_wheel.append(max(0, len(ferris_wheel_waiting_times) - max_queue_size))
    people_left_rollercoaster.append(max(0, len(rollercoaster_waiting_times) - max_queue_size))

# Now we can plot the results
plt.figure(figsize=(12, 6))

# Average Waiting Times
plt.subplot(1, 2, 1)
plt.boxplot([avg_waiting_times_ferris_wheel, avg_waiting_times_rollercoaster], labels=['Ferris Wheel', 'Roller Coaster'])
plt.title('Average Waiting Times')
plt.ylabel('Waiting Time (minutes)')

# People Left in Queue
plt.subplot(1, 2, 2)
plt.boxplot([people_left_ferris_wheel, people_left_rollercoaster], labels=['Ferris Wheel', 'Roller Coaster'])
plt.title('People Who Left the Queue')
plt.ylabel('Number of People')

plt.tight_layout()
plt.show()
