import logging

from h2o_wave import Q, ui, app, main
from src.enum import GameMode, GameState
from src.game import Game

# Initial variables
slots = 9
clicked = [-1] * slots
game_mode = GameMode.EASY
game = Game(game_mode=game_mode, clicked=clicked)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')


@app('/tic_tac_toe')
async def serve(q: Q):
    """
    Entry point to the app
    :param q: Query argument from the H2O Wave server
    :return: None
    """

    # Reset handler
    if q.args.reset:
        reset(q)
        logging.info("Game is reset.")

    # Game Mode handler
    if q.args.submit_mode:
        global game_mode, game
        game.game_mode = game_mode = q.args.drop_down
        q.page['modes'].items[0].dropdown.value = game_mode
        logging.info(f"{game_mode} is selected as the game mode.")

    if not q.client.initialized:
        # setup app
        setup_app(q)
        logging.info("Game initialization is successful.")
    else:
        for slot in range(slots):
            # If player clicked a slot, game arena is updated.
            if q.args[f'button{slot}']:
                logging.info(f"Player X move : slot {slot}.")
                clicked[slot] = 1
                update_button(q=q, slot=slot, icon='Cancel', disable=True)
                game_state = game.check_game_state()
                show_result(q=q, game_state=game_state)

                # Opponent play move updating
                if game_state == GameState.PLAYING:
                    opponent_slot = game.play_opponent()
                    logging.info(f"Player O move : slot {opponent_slot}.")
                    clicked[opponent_slot] = 0
                    update_button(q=q, slot=opponent_slot, icon='LocationCircle', disable=True)
                    game_state = game.check_game_state()
                    show_result(q=q, game_state=game_state)

    await q.page.save()


def setup_app(q: Q) -> None:
    """
    Activities that happen the first time someone comes to this app, such as user variables and home page cards
    :param q: Query argument from the H2O Wave server
    :return: None
    """
    logging.info("Setting up the app for a new browser tab.")

    # UI Zones
    q.page['meta'] = ui.meta_card(title="Tic Tac Toe", box='', layouts=[
        ui.layout(
            breakpoint='xl',
            width='1200px',
            zones=[
                # Header Zone
                ui.zone(name='header_zone', align='center', justify='center', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone(name='header', size='35%'),
                    ui.zone(name='reset', size='15%'),
                    ui.zone(name='game_mode', size='15%'),
                ]),
                # Game Arena Zone
                ui.zone(name='play_zone_row1', align='center', justify='center', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone(name='slot0', size='10%'),
                    ui.zone(name='slot1', size='10%'),
                    ui.zone(name='slot2', size='10%'),
                ]),
                ui.zone(name='play_zone_row2', align='center', justify='center', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone(name='slot3', size='10%'),
                    ui.zone(name='slot4', size='10%'),
                    ui.zone(name='slot5', size='10%'),
                ]),
                ui.zone(name='play_zone_row3', align='center', justify='center', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone(name='slot6', size='10%'),
                    ui.zone(name='slot7', size='10%'),
                    ui.zone(name='slot8', size='10%'),
                ]),
                # Output result Zone
                ui.zone(name='result', align='center', justify='center', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone(name='result_card', size='30%'),
                ]),
            ]
        )
    ])

    # Game title
    q.page['header'] = ui.header_card(
        box="header",
        title="TIC TAC TOE GAME",
        subtitle="Fun game"
    )

    # Reset Button
    q.page['reset'] = ui.form_card(
        box='reset',
        items=[
            ui.buttons([ui.button(
                name='reset',
                label="Reset",
                icon='refresh',
            )], 'center')
        ],
    )

    choices = [
        ui.choice(GameMode.EASY, GameMode.EASY),
        ui.choice(GameMode.MEDIUM, GameMode.MEDIUM),
        ui.choice(GameMode.HARD, GameMode.HARD)
    ]

    # Game mode selection
    q.page['modes'] = ui.form_card(box='game_mode', items=[
        ui.dropdown(name='drop_down', label='Game Mode', value=GameMode.EASY, choices=choices),
        ui.button(name='submit_mode', label='Submit', primary=True),
    ])

    # Game arena setting up
    for slot in range(slots):
        q.page[f'button{slot}'] = ui.form_card(
            box=f'slot{slot}',
            items=[
                ui.buttons([ui.button(
                    name=f'button{slot}',
                    primary=True,
                )], 'center')
            ],
        )

    q.client.initialized = True


def reset(q):
    """
    Reset all the parameters
    :param q: Query argument from the H2O Wave server
    :return: None
    """
    # Game arena resetting
    for slot in range(slots):
        update_button(q=q, slot=slot, icon='', disable=False)
        clicked[slot] = -1
    # Output result resetting
    q.page['result'] = ui.label(label='', visible=False)
    # Game mode submit button resetting
    q.page['modes'].items[1].button.disabled = False


def update_button(q, slot, icon, disable):
    """
    Update game arena slots after played
    :param q: Query argument from the H2O Wave server
    :param slot: Button slot
    :param icon: Button icon
    :param disable: Button disability
    :return: None
    """
    q.page[f'button{slot}'].items[0].buttons.items[0].button.icon = icon
    q.page[f'button{slot}'].items[0].buttons.items[0].button.disabled = disable


def show_result(q, game_state):
    """
    Show final game result
    :param q: Query argument from the H2O Wave server
    :param game_state: Game state - WIN, LOOSE, DRAW, PLAYING
    :return: None
    """

    # Game mode selection is disabled while playing.
    q.page['modes'].items[1].button.disabled = True

    if game_state == GameState.WIN:
        q.page['result'] = ui.form_card(
            box='result_card',
            items=[
                ui.message_bar(type="success", text="You won. Congratulations!!!!"),
            ]
        )
        logging.info("Output - Player X wins")

    if game_state == GameState.LOOSE:
        q.page['result'] = ui.form_card(
            box='result_card',
            items=[
                ui.message_bar(type="warning", text="Better luck next time"),
            ]
        )
        logging.info("Output - Player O wins")

    if game_state == GameState.DRAW:
        q.page['result'] = ui.form_card(
            box='result_card',
            items=[
                ui.message_bar(type="info", text="Game is drawn. Try again"),
            ]
        )
        logging.info("Output - Game is drawn")

    # If final result of WIN or LOOSE or DRAW state is achieved, all the button slots are disable to stop further
    # playing
    if game_state != GameState.PLAYING:
        for slot in range(slots):
            q.page[f'button{slot}'].items[0].buttons.items[0].button.disabled = True
        logging.info("Output - Game is finished")
    else:
        logging.info("Output - Still playing")
