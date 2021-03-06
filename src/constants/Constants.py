# lines
LINE = 'line'

LINE_A = 'LINE_A'
LINE_B = 'LINE_B'

LINES = {
    LINE_A: LINE_A,
    LINE_B: LINE_A,
}

# channels
CHANNEL_PITCH = 'PITCH'
CHANNEL_YAW = 'YAW'
CHANNEL_ROLL = 'ROLL'

CHANNELS = {
    CHANNEL_PITCH: CHANNEL_PITCH,
    CHANNEL_YAW: CHANNEL_YAW,
    CHANNEL_ROLL: CHANNEL_ROLL,
}

# commands
GET_ANSWER = 'GET_ANSWER'
GET_DATA = 'GET_DATA'
SEND_DATA = 'SEND_DATA'
BLOCK = 'BLOCK'
RELEASE = 'RELEASE'
SWAP_LINE = 'SWAP_LINE'
BLOCK_THROUGH = 'BLOCK_THROUGH'
RELEASE_THROUGH = 'RELEASE_THROUGH'

COMMANDS = {
    GET_ANSWER: GET_ANSWER,
    GET_DATA: GET_DATA,
    SEND_DATA: SEND_DATA,
    BLOCK: BLOCK,
    RELEASE: RELEASE,
    SWAP_LINE: SWAP_LINE,
    BLOCK_THROUGH: BLOCK_THROUGH,
    RELEASE_THROUGH: RELEASE_THROUGH,
}

# endpoints

ENDPOINTS_COUNT = 18

IS_BUSY = 'IS_BUSY'
IS_GENERATING = 'IS_GENERATING'
IS_FROZEN = 'IS_FROZEN'
IS_SERVICE_NEEDED = 'IS_SERVICE_NEEDED'
IS_BREAKDOWN = 'IS_BREAKDOWN'
IS_FAILURE = 'IS_FAILURE'

STATES = {
    IS_BUSY: IS_BUSY,
    IS_GENERATING: IS_GENERATING,
    IS_FROZEN: IS_FROZEN,
    IS_SERVICE_NEEDED: IS_SERVICE_NEEDED,
    IS_BREAKDOWN: IS_BREAKDOWN,
    IS_FAILURE: IS_FAILURE,
}

ANGLE = 'ANGLE'
ANGULAR_VELOCITY = 'ANGLE_VELOCITY'
ANGULAR_ACCELERATION = 'ANGULAR_ACCELERATION'

CHARACTERISTICS = {
    ANGLE: ANGLE,
    ANGULAR_VELOCITY: ANGULAR_VELOCITY,
    ANGULAR_ACCELERATION: ANGULAR_ACCELERATION,
}

# RESPONSE

SUCCESS = 'success'
ERROR = 'error'
DATA = 'data'
TIME = 'time'

# ERROR MESSAGES

INCOMPATIBLE_COMMAND_TYPE = 'Error: this command type is incompatible with used transfer data format'
LINE_IS_BUSY = 'Error: line is busy'
ENDPOINT_NOT_FUNCTIONING = 'Error: endpoint is not functioning'
WRONG_NUMBER_OF_END_POINTS = 'Error: wrong number of endpoint: cannot divide by 3 without a remainder'
NO_RESPONSE = 'Error: no response from endpoint'

# TIME
# in messages

SESSION = 20000
PORTION = 1000

# DATA
# headers

HEADERS = [
    'Сообщений',
    'Сбой',
    'Отказ ОУ',
    'Абонент занят',
    'Генерация',
    'Время, мс',
    'МО сообщения, мс',
    'СКО сообщения, мс',
]

SESSION_HEADERS = [
    'Номер сеанса',
    'Сбоев',
    'Отказов',
    'Абонент занят',
    'Генерация',
    'МО сообщения, мс',
    'СКО сообщения, мс',
]

TESTS_NUMBER = 50
