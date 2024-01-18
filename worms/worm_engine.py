import math
import pickle
import sys

import pygame

pygame.init()

# Set up the display
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Nigga")

# Set up the circle
circle_radius = 10
clock = pygame.time.Clock()


DEFAULT_EDGE_LENGTH = 100.0
COMPRESSED_EDGE_LENGTH = 50
FLOOR_Y = 100
KONSTANT = 0.3
FRICTION = 0.1
GROUND_FRICTION = 0.4
GRABITY = 1


class WormSimulation:
    def __init__(self):
        horizontal_vertices = 10
        self.vertices = []
        self.edges = []
        self.controlled_edges = []
        last_vertex_1 = Vertex(0, 0)
        last_vertex_2 = Vertex(0, DEFAULT_EDGE_LENGTH)
        self.vertices.extend([last_vertex_1, last_vertex_2])
        self.edges.append(Edge(last_vertex_1, last_vertex_2))
        for x in range(1, horizontal_vertices):
            new_vertex_1 = Vertex(x * DEFAULT_EDGE_LENGTH, 0)
            new_vertex_2 = Vertex(x * DEFAULT_EDGE_LENGTH, DEFAULT_EDGE_LENGTH)
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

    def run_simulation(self, network, show_simulation):
        for _ in range(20):
            inputs = self.get_network_inputs()
            moving_directions = network.predict(inputs)
            self.fire_inputs(moving_directions, 4, show_simulation)
        return self.get_progress()

    def fire_inputs(self, inputs, physics_steps, show_simulation):
        for input, edge in zip(inputs, self.controlled_edges):
            if input > 0.5:
                edge.length = COMPRESSED_EDGE_LENGTH
            else:
                edge.length = DEFAULT_EDGE_LENGTH

        for _ in range(physics_steps):
            self.simulate_step(show_simulation)

    def simulate_step(self, show_simulation):
        for vertex in self.vertices:
            vertex.force = Vector(0, GRABITY)

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
            draw_the_shit(self)

    def get_progress(self):
        middle_x = 0
        for v in self.vertices:
            middle_x += v.position.x
        middle_x /= len(self.vertices)
        return middle_x

    def get_network_inputs(self):
        return [(e.get_length() - COMPRESSED_EDGE_LENGTH) / (DEFAULT_EDGE_LENGTH - COMPRESSED_EDGE_LENGTH)
                for e in self.controlled_edges]


class Vertex:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.velocity = Vector()
        self.force = Vector()


class Edge:
    def __init__(self, v1, v2, length=DEFAULT_EDGE_LENGTH):
        self.length = length
        self.v1 = v1
        self.v2 = v2

    def get_force(self):
        diff = self.v1.position.minus(self.v2.position)
        actual_length = diff.length()
        force = KONSTANT * (self.length - actual_length)
        return Vector.from_cartesian(force, diff.angle())

    def get_length(self):
        diff = self.v1.position.minus(self.v2.position)
        return diff.length()


class Vector:
    def __init__(self, x=0, y=0):
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


def draw_the_shit(worm):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the circle
    for vertex in worm.vertices:
        pygame.draw.circle(screen, (0, 0, 255), (vertex.position.x, vertex.position.y), circle_radius)

    for edge in worm.edges:
        pygame.draw.line(screen, (0, 0, 0),
                         (edge.v1.position.x, edge.v1.position.y),
                         (edge.v2.position.x, edge.v2.position.y), 2)  # 2 is the line thickness

    pygame.draw.line(screen, (0, 0, 0), (0, FLOOR_Y + circle_radius), (10000, FLOOR_Y + circle_radius), 2)  # 2 is the line thickness

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)


if __name__ == '__main__':
    file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\networks\\save_worm_network_generation.pkl"

    # Now, you can load the instance back from the file
    with open(file_path, "rb") as file:
        loaded_network = pickle.load(file)
    worm = WormSimulation()
    worm.run_simulation(loaded_network, True)
