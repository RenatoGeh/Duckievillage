# Intro to Robotics - MAC0318
#
# Name:
# NUSP:
#
# ---
#
# Assignment 3 - Topological maps
# Carefully read this header and follow submission instructions!
# Failure to follow instructions may result in a zero!
#
# Task:
#  - By making use of your last assignment (navigation by waypoints), implement shortest-path
#    navigation by calling the BFS path finding algorithm on the topological map.
#  - Adapt your navigation plan to the usual traffic rules, creating a directed graph G such that
#    nodes are lanes, and an edge e=(p, q) exists only if the agent is able to go from p to q without
#    breaking any of the following rules:
#    1. No U-turns allowed.
#    2. Right lane only.
#    3. Always go forward, never backwards.
#    Run BFS to test your digraph.
#
# Don't forget that you can (and should!) read the Duckievillage code in search of anything that
# can be useful for your work.
#
# The topological map is already implemented within the duckievillage module. You can access the
# map graph through env.topo_graph. This field contains a TopoGraph object that maps all drivable
# tiles as nodes in the graph, with tiles connected by edges. To find the optimal shortest path
# between two drivable tiles, call env.topo_graph.path(p, q), where p and q are the source and
# target nodes. This'll return a list of positions corresponding to the center of each tile.
#
# Don't forget to run this from the Duckievillage root directory!
# From within the root directory, run python with the -m flag.
#   python3 -m assignments.topomap
#
# Submission instructions:
#  0. Add your name and USP number to the header's header.
#  1. Make sure everything is running fine and there are no errors during startup. If the code does
#     not even start the environment, you will receive a zero.
#  2. Test your code and make sure it's doing what it's supposed to do.
#  3. Append your NUSP to this file name.
#  4. Submit your work to PACA.

import sys
import pyglet
from pyglet.window import key
from pyglet.window import mouse
import numpy as np
import gym
import gym_duckietown
import duckievillage
from duckievillage import DuckievillageEnv

TRACKS = (('./maps/dense.yaml', 5), ('./maps/large.yaml', 15))
which = 0

env = DuckievillageEnv(
  seed = 101,
  map_name = TRACKS[which][0],
  is_external_map = True,
  draw_curve = False,
  draw_bbox = False,
  domain_rand = False,
  distortion = False,
  top_down = False,
  cam_height = TRACKS[which][1]
)

env.reset()
env.render()

# Use G to create the directed graph mentioned in the assignment task list.
G = duckievillage.TopoGraph(env.road_tile_size)

@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
  if symbol == key.ESCAPE:
    env.close()
    sys.exit(0)
  env.render()

# On mouse press, register waypoint.
@env.unwrapped.window.event
def on_mouse_press(x, y, button, mods):
  if button == mouse.LEFT:
    if x < 0 or x > duckievillage.WINDOW_WIDTH or y < 0 or y > duckievillage.WINDOW_HEIGHT:
      return
    # Convert coordinates from window position to Duckietown coordinates.
    px, py = env.convert_coords(x, y)
    # The function below calls BFS from the bot's current position to your mouse's position,
    # returning a list of positions to go to.
    Q = env.topo_graph.bfs(env.get_position(), (px, py))
    print(Q, len(Q))

    # Once you implement your new digraph, you should be able to call BFS in the following way:
    # Q = G.bfs(env.get_position(), (px, py))

key_handler = key.KeyStateHandler()
env.unwrapped.window.push_handlers(key_handler)

def update(dt):
  action = [0.0, 0.0]

  # This is where you'll write the Duckie's logic.
  # You can fetch your duckiebot's position with env.get_position().

  obs, reward, done, info = env.step(action)

  env.render()

pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)

pyglet.app.run()

env.close()
