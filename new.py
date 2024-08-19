import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from yaml import safe_load

# read data
data = safe_load(open('new.yml'))
slices = data['process']['slices']
services = list(reversed(data['services']))
roles = list(reversed(data['roles']))

# make sure not to draw duplicates
already_drawn = set()

# setup the figure
fig, ax = plt.subplots()
print(fig)
fig.suptitle(data['process']['name'])

# define colors
colors = {
  'event': 'orange',
  'view': '#9acd32',
  'command': '#00bfff',
  'ui': '#d3d3d3'
}

# define block dimensions
block_width = 1.5
block_height = 1.5

# axes functions
x, y = 0, 0
def offset_x(modifier = 0.5):
  global x
  x += block_width * modifier

def offset_y(modifier = 2):
  global y
  y += block_width * modifier

y_positions = {}
def add_y_position(block: str):
  global y
  y_positions[block] = y
  
# define swimlanes
swimlane_length = len(slices) * 2.5
labels = services + ['command_view', 'api'] + roles

for label in labels:
  add_y_position(label)
  if not (label == 'command_view' or label == 'api'):
    ax.text(-1, y, label, va='center', ha='right', fontsize=12, fontweight='bold')
    ax.add_patch(
      Rectangle(
        (0, y - block_height/2), 
        width = swimlane_length, 
        height = block_height, 
        fill=False, 
        edgecolor='black'
      )
    )
  offset_y()
  
# functions to add elements
def add_block(x, y, color, text, id):
  if id in already_drawn:
    return
  print(id)
  already_drawn.add(id)
  ax.add_patch(
    Rectangle(
      (x, y - block_height / 2), 
      width=block_width, 
      height=block_height,
      color=color
    )
  )
  ax.text(x+block_width/2, y, text, ha='center', va='center', fontsize=8, color='black')
  
def command_view_block(type):
  add_block(
    id = slice[type]['id'],
    x = x, 
    y = y_positions['command_view'], 
    color = colors[type], 
    text = slice[type]['name']
  )

def automation_block():
  pass
  
def translation_block():
  pass

def ui_block():
  id = slice['trigger']['id']
  # x = x+block_width if id in already_drawn else x
  add_block(
    id = id,
    x = x+block_width*2 if id in already_drawn else x, 
    y = y_positions[slice['trigger']['role']], 
    color = colors['ui'], 
    text = slice['trigger']['name']
  )
  
def event_block():
  add_block(
    id = slice['event']['id'],
    x = x, 
    y = y_positions[slice['event']['service']], 
    color = colors['event'], 
    text = slice['event']['name']
  )

def down_arrow(start_x, start_y, end_x, end_y):
  ax.add_patch(
    FancyArrowPatch(
      (start_x + block_width * 0.75, start_y - block_height * 0.5), 
      (end_x + block_width * 0.75, end_y + block_height * 0.5),
      # connectionstyle='arc3,rad=0.3',
      mutation_scale=8
      )
    )
  
def up_arrow(start_x, start_y, end_x, end_y):
  ax.add_patch(
    FancyArrowPatch(
      (start_x - block_width * 0.25, start_y + block_height * 0.5), 
      (end_x + block_width * 0.25, end_y - block_height * 0.5),
      # connectionstyle='arc3,rad=0.3',
      mutation_scale=8
    )
  )

# trigger -> command -> view 
def add_command_pattern():
  ui_block()
  down_arrow(
    x, y_positions[slice['trigger']['role']],
    x, y_positions['command_view']
  )
  offset_x()
  command_view_block('command')
  down_arrow(
    x, y_positions['command_view'],
    x, y_positions[slice['event']['service']]
  )
  offset_x()
  event_block()
  offset_x()
  
# event -> view -> trigger
def add_view_pattern():
  event_block()
  up_arrow(
    x, y_positions[slice['event']['service']],
    x, y_positions['command_view']
  )
  command_view_block('view')
  up_arrow(
    x + block_width, y_positions['command_view'],
    x + block_width, y_positions[slice['trigger']['role']]
  )
  offset_x()
  ui_block()
  
def add_automation_pattern():
  pass

def add_translation_pattern():
  pass

# add patterns
for slice in slices:
  match slice['pattern']:
    case 'command':
      add_command_pattern()
    case 'view':
      add_view_pattern()
    case 'automation':
      add_automation_pattern()
    case 'translation':
      add_translation_pattern()
    case _:
      raise Exception(f'No such pattern: {slice['pattern']}')
  offset_x()
  
# set limits and remove axes
ax.set_xlim(-block_width, swimlane_length)
ax.set_ylim(-block_height, y + 1)
ax.axis('off')

# show the plot
plt.show()