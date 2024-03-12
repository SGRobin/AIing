import math
import pickle
import sys
import time

import numpy as np
import pygame

global screen
global circle_radius
global clock
FRAMES_PER_PREDICTION = 4
NUM_PREDICTIONS = 50


def draw_window():
    global screen
    global circle_radius
    global clock
    # Set up the display
    width, height = 1200, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Worming Window")

    # Set up the circle
    circle_radius = 10
    clock = pygame.time.Clock()

    pygame.init()


DEFAULT_EDGE_LENGTH = 100.0
COMPRESSED_EDGE_LENGTH = 50
FLOOR_Y = 400
CONSTANT = 0.6
# FRICTION = 0.2
FRICTION = 0.3
GROUND_FRICTION = 0.8
GRAVITY = 1

input_time = 0
predict_time = 0
fire_input_time = 0
start_overall = time.time()


def create_and_run_simulation(network):
    worm = WormSimulation()
    return worm.run_simulation(network)


class WormSimulation:
    """
    Represents the worm
    all the vertices and edges
    """

    def __init__(self):
        horizontal_vertices = 10
        self.vertices = []
        self.edges = []
        self.controlled_edges = []
        last_vertex_1 = Vertex(0, FLOOR_Y - DEFAULT_EDGE_LENGTH)
        last_vertex_2 = Vertex(0, FLOOR_Y)
        self.vertices.extend([last_vertex_1, last_vertex_2])
        self.edges.append(Edge(last_vertex_1, last_vertex_2))
        for x in range(1, horizontal_vertices):
            new_vertex_1 = Vertex(x * DEFAULT_EDGE_LENGTH, FLOOR_Y - DEFAULT_EDGE_LENGTH)
            new_vertex_2 = Vertex(x * DEFAULT_EDGE_LENGTH, FLOOR_Y)
            self.vertices.extend([new_vertex_1, new_vertex_2])

            # Vertical edge
            self.edges.append(Edge(new_vertex_1, new_vertex_2))

            # Side edges
            side_edge_1 = Edge(new_vertex_1, last_vertex_1)
            self.edges.append(side_edge_1)
            self.controlled_edges.append(side_edge_1)

            side_edge_2 = Edge(new_vertex_2, last_vertex_2)
            self.edges.append(side_edge_2)
            self.controlled_edges.append(side_edge_2)

            # Diagonals
            self.edges.append(Edge(new_vertex_1, last_vertex_2, math.sqrt(2 * (DEFAULT_EDGE_LENGTH ** 2))))
            self.edges.append(Edge(new_vertex_2, last_vertex_1, math.sqrt(2 * (DEFAULT_EDGE_LENGTH ** 2))))

            last_vertex_1 = new_vertex_1
            last_vertex_2 = new_vertex_2

    def run_simulation(self, network, show_simulation=False):
        """
        runs the simulation for a set amount of frames
        :param network: NeuralNetwork
        :param show_simulation: Boolean - decides weather to show the simulation
        :return: float - distance traveled
        """
        if show_simulation:
            draw_window()
        global input_time, predict_time, fire_input_time
        for _ in range(NUM_PREDICTIONS):
            start_time = time.time()
            inputs = self.get_network_inputs()
            input_time += time.time() - start_time

            start_time = time.time()
            moving_directions = network.predict(np.array(inputs))
            predict_time += time.time() - start_time

            start_time = time.time()
            self.fire_inputs(moving_directions, FRAMES_PER_PREDICTION, show_simulation)
            fire_input_time += time.time() - start_time

        return self.get_progress()

    def fire_inputs(self, inputs, physics_steps, show_simulation):
        """
        function that gets the inputs for the network, runs them through the network,
        and translates the outputs into movements
        :param inputs: array of inputs
        :param physics_steps: int - how many steps to runs in the simulation with these inputs
        :param show_simulation: Boolean
        :return: Nothing
        """
        for network_input, edge in zip(inputs, self.controlled_edges):
            edge.length = COMPRESSED_EDGE_LENGTH + network_input * (DEFAULT_EDGE_LENGTH - COMPRESSED_EDGE_LENGTH)
        for _ in range(physics_steps):
            self.simulate_step(show_simulation)

    def simulate_step(self, show_simulation):
        """
        progresses a single step in the simulation
        :param show_simulation: Boolean
        :return: Nothing
        """
        for vertex in self.vertices:
            vertex.force = Vector(0, GRAVITY)

        for edge in self.edges:
            force = edge.get_force()
            edge.v1.force = edge.v1.force.plus(force)
            edge.v2.force = edge.v2.force.minus(force)

        for vertex in self.vertices:
            vertex.velocity = vertex.velocity.plus(vertex.force)
            vertex.velocity = vertex.velocity.times(1 - FRICTION)
            vertex.position.y = vertex.position.y + vertex.velocity.y

            if vertex.position.y > FLOOR_Y:
                vertex.position.y = FLOOR_Y
                vertex.velocity.y = 0
                vertex.velocity.x = vertex.velocity.x * (1 - GROUND_FRICTION)

            vertex.position.x = vertex.position.x + vertex.velocity.x

        if show_simulation:
            draw_worm(self)

    def get_progress(self):
        """
        gets the distance travelled
        :return: float - distance
        """
        middle_x = 0
        for v in self.vertices:
            middle_x += v.position.x
        middle_x /= len(self.vertices)
        return middle_x

    def get_network_inputs(self):
        """
        translates position of the worm into network inputs
        :return: array[inputs]
        """
        # return [((e.get_length() - COMPRESSED_EDGE_LENGTH) / (DEFAULT_EDGE_LENGTH - COMPRESSED_EDGE_LENGTH) - 1) * 2
        #         for e in self.controlled_edges]
        return [(e.get_length() - COMPRESSED_EDGE_LENGTH) / (DEFAULT_EDGE_LENGTH - COMPRESSED_EDGE_LENGTH)
                for e in self.controlled_edges]


class Vertex:
    """
    A vertex is a corner point of a polygon
    """

    def __init__(self, x, y):
        """
        initialize
        :param x: position
        :param y: position
        """
        self.position = Vector(x, y)
        self.velocity = Vector()
        self.force = Vector()


class Edge:
    """
    one of the edges of the worm (lines)
    """

    def __init__(self, v1, v2, length=DEFAULT_EDGE_LENGTH):
        """
        initialize
        :param v1: Vertex
        :param v2: Vertex
        :param length: float
        """
        self.length = length
        self.v1 = v1
        self.v2 = v2

    def get_force(self):
        """
        gets the force applied on it
        :return: float
        """
        diff = self.v1.position.minus(self.v2.position)
        actual_length = diff.length()
        force = CONSTANT * (self.length - actual_length)
        return Vector.from_cartesian(force, diff.angle())

    def get_length(self):
        """
        gets length
        :return: float
        """
        diff = self.v1.position.minus(self.v2.position)
        return diff.length()


class Vector:
    """
    Vector
    """

    def __init__(self, x=0, y=0):
        """
        initialize
        :param x: x
        :param y: y
        """
        self.x = x
        self.y = y

    def plus(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def minus(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def times(self, num):
        return Vector(self.x * num, self.y * num)

    def angle(self):
        return math.atan2(self.y, self.x)

    def inverted(self):
        return Vector(-self.x, -self.y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @staticmethod
    def from_cartesian(length, angle):
        return Vector(math.cos(angle) * length, math.sin(angle) * length)


def draw_worm(current_worm):
    """
    draws the worm
    :param current_worm: WormSimulation
    :return: Nothing
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the circle
    for vertex in current_worm.vertices:
        pygame.draw.circle(screen, (0, 0, 255), (vertex.position.x, vertex.position.y), circle_radius)

    for edge in current_worm.edges:
        pygame.draw.line(screen, (0, 0, 0),
                         (edge.v1.position.x, edge.v1.position.y),
                         (edge.v2.position.x, edge.v2.position.y), 2)  # 2 is the line thickness

    pygame.draw.line(screen, (0, 0, 0), (0, FLOOR_Y + circle_radius), (10000, FLOOR_Y + circle_radius),
                     2)  # 2 is the line thickness

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)


# Runs the simulation with visual to let one network walk
if __name__ == '__main__':
    file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\networks\\save_network_generation.pkl"
    # file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\save_network_1.pkl"

    # Load the instance from the file
    with open(file_path, "rb") as file:
        loaded_network = pickle.load(file)
    worm = WormSimulation()
    worm.run_simulation(loaded_network, True)
