from collections import namedtuple
from enum import Enum
from itertools import count

Terrain = Enum('Terrain', zip(['OPEN', 'WOOD', 'MOUNTAIN', 'DESERT', 'SWAMP'], count(0)))

Product = Enum('Product', zip(['STONE', 'PRODUCE', 'TEXTILE', 'CLAY', 'WOOD', 'ORE'], count(0)))

City = namedtuple('City', 'coordinate products')
