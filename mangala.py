# Mangala Game Implementation
import logging
import copy
import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from time import sleep

class Pool():
    def __init__(self, number, type):
        self.number = number
        self.type = type

    def set(self, number):
        self.number = number

def print_game(game_array):
    print("\n\n")
    for k, i in enumerate(game_array):
        print("Type: " + str(i.type)+" || Content:"+ str(i.number) +"|| index: " +str(k))
    print("\n\n")

def calculate_piece_count(game_array, player):
    piece_count = 0
    if player == "Player":
        for i in range(0, 6):
            piece_count += game_array[i].number
    else:
        for i in range(7, 13):
            piece_count += game_array[i].number

    return piece_count

def game_over(game_array):
    players_piece_count = calculate_piece_count(game_array, "Player")
    computers_piece_count = calculate_piece_count(game_array, "Computer")

    if players_piece_count == 0 or computers_piece_count == 0:
        return True
    else:
        return False

def initalize_game():
    game_array = []
    for i in range(0, 14):
        # Player 1's Treasure
        if i==6:
            game_array.append(Pool(0, "Treasure"))

        # Player 2's Treasure
        elif i==13:
            game_array.append(Pool(0, "Treasure"))

        # Pools
        else:
            game_array.append(Pool(4, "Pool"))

    return game_array


def distribute_pieces(game_array, selection, turn):
    piece_count, temp_count = game_array[selection].number, game_array[selection].number
    last_placed = selection
    is_valid = True

    if piece_count == 0:
        print("No pieces in this pool, select again. Selection:", selection)
        return game_array, last_placed, False

    elif piece_count == 1:
        game_array[selection].set(0)
        game_array[selection+1].set(game_array[selection+1].number+1)
        piece_count -= 1
        last_placed = selection + 1

    else:
        placement_index = selection
        for i in range(0, temp_count):
            placement_index = (selection + i) % 14
            if i == 0:
                game_array[selection].set(1)
                piece_count -= 1
            else:
                game_array[placement_index].set(game_array[placement_index].number+1)
                piece_count -= 1

            if i == temp_count-1:
                last_placed = placement_index
    if turn == 1:
        # If the last piece is placed in one of the opponent's pool, and the pool is even, add the pool to the treasure
        if last_placed > 6 and game_array[last_placed].number % 2 == 0 and game_array[last_placed].type == "Pool":
            game_array[6].set(game_array[6].number + game_array[last_placed].number)
            game_array[last_placed].set(0)

        # If the last piece is placed in one of the player's pool, and the pool is empty before placing the piece, and the opponent's pool is not empty, add the player's pool and the opponent's pool, to the treasure.
        elif last_placed < 6 and game_array[last_placed].number == 1 and game_array[last_placed].type == "Pool" and game_array[12-last_placed].number > 0:
            game_array[6].set(game_array[6].number + game_array[last_placed].number + game_array[12-last_placed].number)
            game_array[last_placed].set(0)
            game_array[12-last_placed].set(0)
    else:
        # If the last piece is placed in one of the opponent's pool, and the pool is even, add the pool to the treasure
        if last_placed < 6 and game_array[last_placed].number % 2 == 0 and game_array[last_placed].type == "Pool":
            game_array[13].set(game_array[13].number + game_array[last_placed].number)
            game_array[last_placed].set(0)

        # If the last piece is placed in one of the computer's pool, and the pool is empty before placing the piece, and the opponent's pool is not empty, add the player's pool and the opponent's pool, to the treasure.
        elif last_placed > 6 and game_array[last_placed].number == 1 and game_array[last_placed].type == "Pool" and game_array[12-last_placed].number > 0:
            game_array[13].set(game_array[13].number + game_array[last_placed].number + game_array[12-last_placed].number)
            game_array[last_placed].set(0)
            game_array[12-last_placed].set(0)
    return game_array, last_placed, is_valid


def minimax(game_array, depth, minimize_or_maximize):

    if minimize_or_maximize:
        best_treasure_number = float('-inf')
        best_selection = 7
        for move in range(7, 13):
            if game_array[move].type == "Treasure":
                continue

            temp_game_array = copy.deepcopy(game_array)
            temp_game_array, last_placed, is_valid = distribute_pieces(temp_game_array, move, 0)
            if not is_valid:
                continue
            value = game_array[13].number
            if value > best_treasure_number:
                best_selection = move
                best_treasure_number = value

        return best_treasure_number, best_selection


def main():
    green = (0, 255, 0)
    blue = (0, 0, 128)

    pygame.init()
    surface = (1400, 600)
    pygame.display.set_caption('Mangala Game')
    window_surface = pygame.display.set_mode(surface)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Player's Turn", True, green, blue)
    textRect = text.get_rect()
    textRect.center = (200 // 2, 30 // 2)

    winfont = pygame.font.Font('freesansbold.ttf', 40)
    wintext = winfont.render("Start?", True, green, blue)
    winRect = wintext.get_rect()
    winRect.center = (1400 // 2, 600 // 2)

    background = pygame.Surface(surface)
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager(surface, 'theme.json')
    manager.set_visual_debug_mode(True)


    computer_treasure = UIButton(relative_rect=pygame.Rect(70, 0, 200, 500),
            text='Computer Treasure', manager=manager,
            anchors={
                    'centery': 'centery'})

    player_treasure = UIButton(relative_rect=pygame.Rect(-220, 0, 200, 500),
            text='Player Treasure', manager=manager,
            anchors={
                    'centery': 'centery',
                    'right': 'right'})

    computer_pool_12 = UIButton(relative_rect=pygame.Rect(-350, -200, 100, 100),
            text='12', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    computer_pool_11 = UIButton(relative_rect=pygame.Rect(-200, -200, 100, 100),
            text='11', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    computer_pool_10 = UIButton(relative_rect=pygame.Rect(-50, -200, 100, 100),
            text='10', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    computer_pool_9 = UIButton(relative_rect=pygame.Rect(100, -200, 100, 100),
            text='9', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    computer_pool_8 = UIButton(relative_rect=pygame.Rect(250, -200, 100, 100),
            text='8', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    computer_pool_7 = UIButton(relative_rect=pygame.Rect(400, -200, 100, 100),
            text='7', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    player_pool_0 = UIButton(relative_rect=pygame.Rect(-350, 200, 100, 100),
            text='0', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    player_pool_1 = UIButton(relative_rect=pygame.Rect(-200, 200, 100, 100),
            text='1', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    player_pool_2 = UIButton(relative_rect=pygame.Rect(-50, 200, 100, 100),
            text='2', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    player_pool_3 = UIButton(relative_rect=pygame.Rect(100, 200, 100, 100),
            text='3', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    player_pool_4 = UIButton(relative_rect=pygame.Rect(250, 200, 100, 100),
            text='4', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    player_pool_5 = UIButton(relative_rect=pygame.Rect(400, 200, 100, 100),
            text='5', manager=manager,
            anchors={
                    'center': 'center',
                    'left': 'left'})

    clock = pygame.time.Clock()
    is_running = True

    logging.basicConfig(level=logging.DEBUG)
    game_array = initalize_game()
    turn = 1 # Player's Turn

    selection = None
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if turn == 1:
                    if event.ui_element == player_pool_0:
                        selection=0

                    elif event.ui_element == player_pool_1:
                        selection=1

                    elif event.ui_element == player_pool_2:
                        selection=2

                    elif event.ui_element == player_pool_3:
                        selection=3

                    elif event.ui_element == player_pool_4:
                        selection=4

                    elif event.ui_element == player_pool_5:
                        selection=5

                    if selection != None:
                        if selection > 5 or game_array[selection].type == "Treasure" :
                            logging.info("Invalid selection")
                            continue
                        game_array, last_placed, is_valid = distribute_pieces(game_array, selection, turn)

                        if not is_valid:
                            continue

                        print("Last Placed: " + str(last_placed))

                        # If the last placed piece is in the treasure, it's the player's turn again
                        if last_placed == 6:
                            turn = 1
                            print("\nPlayer's Turn Again, make a selection")
                            text = font.render("Player's Turn Again", True, green, blue)

                        else:
                            turn = 0
                            print("\nComputer's Turn, press computer treasure")
                            text = font.render("Computer's Turn, press computer treasure", True, green, blue)

                        selection = None


                if event.ui_element == computer_treasure and turn == 0:

                    best_treasure_count, best_selection = minimax(game_array, 4, True)
                    print("Computer's Move:", best_selection)
                    game_array, last_placed, is_valid = distribute_pieces(game_array, best_selection, turn)

                    if not is_valid:
                        continue

                    print("Last Placed: " + str(last_placed))

                    # If the last placed piece is in the treasure, it's the computer's turn again
                    if last_placed == 13:
                        turn = 0
                        print("\nComputer's Turn again, press computer treasure")
                        text = font.render("Computer's Turn Again, press computer treasure", True, green, blue)




                    else:
                        turn = 1
                        print("\nPlayer's Turn, make a selection")
                        text = font.render("Player's Turn", True, green, blue)

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        draw_player_circles(game_array, window_surface)
        draw_computer_circles(game_array, window_surface)

        window_surface.blit(text, textRect)

        pygame.display.update()
        if game_over(game_array):
            if game_array[6].number > game_array[13].number:
                wintext = winfont.render("Player Wins!", True, green, blue)
                print("\n\n\nPlayer Wins!")

            elif game_array[6].number < game_array[13].number:
                wintext = winfont.render("Computer Wins!", True, green, blue)
                print("\n\n\nComputer Wins!")

            else:
                wintext = winfont.render("Tie!", True, green, blue)
                print("\n\n\nTie Game!")

            window_surface.blit(wintext, winRect)
            pygame.display.update()
            sleep(5) # Sleep for 5 secs before exiting
            break



def draw_player_circles(game_array, window_surface):
    coordx = 310
    for i in range(0,6):
        for i in range(game_array[i].number):
            if i > 10:
                pygame.draw.circle(window_surface, (200, 0, 0), (coordx+(i-11)*15, 540), 5, 10)
            elif i > 5:
                pygame.draw.circle(window_surface, (200, 0, 0), (coordx+(i-6)*15, 510), 5, 10)
            else:
                pygame.draw.circle(window_surface, (200, 0, 0), (coordx+i*15, 470), 5, 10)
        coordx += 150



    for i in range(game_array[6].number):
        if i > 20:
            pygame.draw.circle(window_surface, (200, 0, 0), (1200+(i-21)*15, 130), 5, 10)
        elif i > 10:
            pygame.draw.circle(window_surface, (200, 0, 0), (1200+(i-11)*15, 100), 5, 10)
        else:
            pygame.draw.circle(window_surface, (200, 0, 0), (1200+i*15, 70), 5, 10)

def draw_computer_circles(game_array, window_surface):
    coordx = 310
    for i in range(12,6, -1):
        for i in range(game_array[i].number):
            if i > 10:
                pygame.draw.circle(window_surface, (200, 0, 0), (coordx+(i-11)*15, 130), 5, 10)
            elif i > 5:
                pygame.draw.circle(window_surface, (200, 0, 0), (coordx+(i-6)*15, 110), 5, 10)
            else:
                pygame.draw.circle(window_surface, (200, 0, 0), (coordx+i*15, 70), 5, 10)
        coordx += 150

    for i in range(game_array[13].number):
        if i > 20:
            pygame.draw.circle(window_surface, (200, 0, 0), (100+(i-21)*15, 130), 5, 10)
        elif i > 10:
            pygame.draw.circle(window_surface, (200, 0, 0), (100+(i-11)*15, 100), 5, 10)
        else:
            pygame.draw.circle(window_surface, (200, 0, 0), (100+i*15, 70), 5, 10)


if __name__ == '__main__':
    main()
