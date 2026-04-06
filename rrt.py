import pygame
import sys
from random import randint as RND
import math
from collections import namedtuple

print("initing ...")
pygame.init()
print("init done")
print(pygame.get_init())
print("\n" * 4)
WIDTH, HEIGHT = 1600, 1200
CLOSE = 50
FOUND = False
Point = namedtuple("Point", "x y")
Tree = namedtuple("Tree", "root V E")


def random_rectangle(w, h):
    x = RND(0, WIDTH - w)
    y = RND(0, HEIGHT - h)
    return pygame.Rect(x, y, w, h)


def random_point():
    x = RND(CLOSE, WIDTH - CLOSE)
    y = RND(CLOSE, HEIGHT - CLOSE)
    return Point(x, y)


def dist(p, q):
    return math.hypot(p.x - q.x, p.y - q.y)


def sample_tree_node(tree, obstacles, d=50):
    p = random_point()
    candidates = sorted([(dist(node, p), node) for node in tree.V])
    for _, node in candidates:
        direction = math.atan2(p.y - node.y, p.x - node.x)
        new_point = Point(
            int(node.x + d * math.cos(direction)), int(node.y + d * math.sin(direction))
        )
        if not any(obstacle.collidepoint(*new_point) for obstacle in obstacles):
            return new_point, node


def rrt(start, target, obstacles, n=1, tree=None):
    if tree is None:
        tree = Tree(start, set([start]), set())  # rapidly exploring random tree (RRT)
    for i in range(n):
        edge = sample_tree_node(tree, obstacles)
        if edge:
            q, v = edge
            tree.V.add(q)
            tree.E.add((q, v))
            if dist(q, target) < CLOSE:
                global FOUND
                print("FOUND")
                FOUND = True
    return tree


def get_path(start, target, tree):
    candidates = sorted([(dist(v, target), v) for v in tree.V])
    v = candidates[0][1]
    path = [(target, v)]
    while v != start:
        for p, q in tree.E:
            if p == v:
                path.append((p, q))
                v = q
    return path + [(v, start)]


########
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rapidly-Exploring Random Tree Search")

RND_RECT = lambda: (RND(10, WIDTH // 4), RND(10, HEIGHT // 4))

running = True
obstacles = [random_rectangle(*RND_RECT()) for _ in range(10)]
start = random_point()
while any(obstacle.collidepoint(*start) for obstacle in obstacles):
    start = random_point()

target = random_point()
while (
    any(obstacle.collidepoint(*target) for obstacle in obstacles)
    or dist(start, target) < 10 * CLOSE
):
    target = random_point()


n = 1
tree = rrt(start, target, obstacles, n)
PATH = []
it = 0
while running:
    it = it % 255
    it += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

    screen.fill((0, 0, 0))
    for obstacle in obstacles:
        pygame.draw.rect(screen, (80, 80, 80), obstacle)

    if not FOUND:
        pygame.time.delay(0)
        tree = rrt(start, target, obstacles, n, tree)

    for u, v in tree.E:
        pygame.draw.line(screen, (70, 70, 220), u, v, 2)

    if FOUND:
        if not PATH:
            PATH = get_path(start, target, tree)
        for u, v in PATH:
            pygame.draw.line(screen, (255, 255, 255), u, v, 10)

    for node in tree.V:
        pygame.draw.circle(screen, (100, 100, 240), node, 10)  # Tree node in blue
    pygame.draw.circle(screen, (150, 255, 150), start, 10)  # Start point in green
    pygame.draw.circle(screen, (255, 0, 0), target, 10)  # Target point in red

    pygame.display.flip()
    pygame.time.wait(10)
print("OUT OF THE LOOP")
pygame.quit()
print("Done quit")
sys.stdout.flush()
sys.exit()
