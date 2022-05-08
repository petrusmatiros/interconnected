
# config constants
WIDTH    = 960  	
HEIGHT   = 720
FPS      = 60
TILESIZE = 32
HITBOX_OFFSET = {
	'player': 0,
	'invisible': 0,
	'doorfront': -32
}
WALKING = 3.5
RUNNING = 6
IS_PLAYER = '300'
AIR = '-1'
DOORS = {
	'power supply' : '400',
    'motherboard' : '401',
    'CPU' : '402',
    'DRAM' : '403',
    'L1' : '404',
    'L2' : '405',
    'L3' : '406',
    'GPU' : '407',
    'VRAM' : '408',
    'SSD' : '409',
    'internet' : '410',
}
PATHS = {
	'401' : ['402','407','409','410'],
	'402' : ['401','403','404','405','406','407'],
}
