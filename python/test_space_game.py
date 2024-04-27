import pygame
import sys
from space_game import Spaceship, Aliens, Trees, Monster


def test_spaceship_initial_health():
    spaceship = Spaceship(0, 0, 5)
    assert spaceship.health_remaining == 5


def test_alien_creation():
    alien = Aliens(0, 0)
    assert alien.rect.center == (0, 0)


def test_tree_creation():
    tree = Trees(0, 0)
    assert tree.rect.center == (0, 0)


def test_monster_initial_health():
    monster = Monster(0, 0, 50)
    assert monster.health_remaining == 50


if __name__ == "__main__":
    pygame.init()
    test_spaceship_initial_health()
    test_alien_creation()
    test_tree_creation()
    test_monster_initial_health()
    pygame.quit()
    sys.exit()