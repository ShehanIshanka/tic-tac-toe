from h2o_wave import Q, ui, app
from h2o_wave import main
import random

game_mode = ["Easy"]
slots = 9
col_start = 5
row_start = 4
graph = []
clicked = []
for row in range(row_start, row_start + 3):
    for col in range(col_start, col_start + 3):
        graph.append(f'{col} {row} 1 1')
        clicked.append(-1)


def reset(q):
    for slot in range(slots):
        q.page[str(slot)].items[0].buttons.items[0].button.icon = ''
        q.page[str(slot)].items[0].buttons.items[0].button.disabled = False
        clicked[slot] = -1
    q.page['result'] = ui.label(label='', visible=False)


def get_result(q, game_state):
    if game_state == "WIN":
        q.page['result'] = ui.form_card(
            box='5 7 2 1',
            items=[
                ui.message_bar(type="success", text="You won. Congratulations!!!!"),
            ]
        )
    if game_state == "LOOSE":
        q.page['result'] = ui.form_card(
            box='5 7 2 1',
            items=[
                ui.message_bar(type="warning", text="Better luck next time"),
            ]
        )
    if game_state == "DRAW":
        q.page['result'] = ui.form_card(
            box='5 7 2 1',
            items=[
                ui.message_bar(type="info", text="Game is drawn. Try again"),
            ]
        )
    for slot in range(slots):
        q.page[str(slot)].items[0].buttons.items[0].button.disabled = True


def check_game_state(q):
    x_winner_string = "111"
    o_winner_string = "000"
    for i in range(0, slots - 2, 3):
        cur_string = "".join(map(str, clicked[i:i + 3]))
        if cur_string == x_winner_string:
            get_result(q, "WIN")
            return None
        elif cur_string == o_winner_string:
            get_result(q, "LOOSE")
            return None

    for i in range(0, 3):
        cur_string = "".join(map(str, [clicked[i], clicked[i + 3], clicked[i + 6]]))
        if cur_string == x_winner_string:
            get_result(q, "WIN")
            return None
        elif cur_string == o_winner_string:
            get_result(q, "LOOSE")
            return None

    cur_string = "".join(map(str, [clicked[0], clicked[4], clicked[8]]))
    if cur_string == x_winner_string:
        get_result(q, "WIN")
        return None
    elif cur_string == o_winner_string:
        get_result(q, "LOOSE")
        return None

    cur_string = "".join(map(str, [clicked[2], clicked[4], clicked[6]]))
    if cur_string == x_winner_string:
        get_result(q, "WIN")
        return None
    elif cur_string == o_winner_string:
        get_result(q, "LOOSE")
        return None

    if -1 not in clicked:
        get_result(q, "DRAW")
        return None


def set_mode(mode):
    if mode == "Easy":
        indices = [i for i, x in enumerate(clicked) if x == -1]
        if len(indices) != 0:
            return indices[random.randint(0, len(indices)) - 1]
    elif mode == "Medium":
        return 1
    elif mode == "Hard":
        return 1


async def get_mode(q, mode):
    game_mode[0] = mode
    q.page['modes'].items[0].dropdown.value = mode


def play(q, slot, mode):
    print(mode)
    clicked[slot] = 1
    q.sleep(10)
    check_game_state(q)
    clicked[set_mode(mode)] = 0
    check_game_state(q)


choices = [
    ui.choice('Easy', 'Easy'),
    ui.choice('Medium', 'Medium'),
    ui.choice('Hard', 'Hard')
]

r = 1


@app('/tic_tac_toe')
async def serve(q: Q):
    for slot in range(slots):
        if q.args[f'SLOT{slot}']:
            play(q, slot, game_mode[0])
    if q.args.reset:
        reset(q)

    if q.args.submit_mode:
        await get_mode(q, str(q.args.drop_down))

    if not q.client.initialized:
        q.client.initialized = True
        q.page['header'] = ui.form_card(
            box='5 1 2 1',
            items=[
                ui.text_xl('TIC TAC TOE GAME')
            ]
        )

        q.page['reset'] = ui.form_card(
            box='7 1 1 1',
            items=[
                ui.buttons([ui.button(
                    name='reset',
                    label="Reset",
                    icon='refresh',
                )], 'center')
            ],
        )

        q.page['modes'] = ui.form_card(box='5 2 2 2', items=[
            ui.dropdown(name='drop_down', label='Game Mode', value='Easy', choices=choices),
            ui.button(name='submit_mode', label='Submit', primary=True),
        ])

        for slot in range(slots):
            q.page[str(slot)] = ui.form_card(
                box=graph[slot],
                items=[
                    ui.buttons([ui.button(
                        name=f'SLOT{slot}',
                        primary=True,
                    )], 'center')
                ],
            )
    else:
        for slot in range(slots):
            if clicked[slot] == 1:
                q.page[str(slot)].items[0].buttons.items[0].button.icon = 'Cancel'
                q.page[str(slot)].items[0].buttons.items[0].button.disabled = True
            elif clicked[slot] == 0:
                q.page[str(slot)].items[0].buttons.items[0].button.icon = 'LocationCircle'
                q.page[str(slot)].items[0].buttons.items[0].button.disabled = True

    await q.page.save()
