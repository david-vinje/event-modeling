import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from yaml import safe_load

# read data
data = safe_load(open('new.yml'))
slices = data['process']['slices']
services = list(reversed(data['services']))
ui = list(reversed(data['ui']))

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
swimlane_length = len(slices) * 3
labels = services + ['command_view', 'automation_translation'] + ui

for label in labels:
  add_y_position(label)
  if not (label == 'command_view' or label == 'automation_translation'):
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
def add_block(x, y, color, text):
  ax.add_patch(
    Rectangle(
      (x, y - block_height / 2), 
      width=block_width, 
      height=block_height,
      color=color
    )
  )
  ax.text(x+block_width/2, y, text, ha='center', va='center', fontsize=8, color='black')
  

def command_block():
  add_block(
    x = x, 
    y = y_positions['command_view'], 
    color = colors['command'], 
    text = slice['command']['name']
  )

def view_block():
  add_block(
    x = x, 
    y = y_positions['command_view'], 
    color = colors['view'], 
    text = slice['view']['name']
  )
  
def automation_block():
  pass
  
def translation_block():
  pass

def ui_block():
  add_block(
    x = x, 
    y = y_positions[slice['trigger']['ui']], 
    color = colors['ui'], 
    text = slice['trigger']['name']
  )
  
def event_block():
  add_block(
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

# UI -> command -> view 
def add_command_pattern(slice):
  ui_block()
  down_arrow(
    x, y_positions[slice['trigger']['ui']],
    x, y_positions['command_view']
  )
  offset_x()
  command_block()
  down_arrow(
    x, y_positions['command_view'],
    x, y_positions[slice['event']['service']]
  )
  offset_x()
  event_block()
  offset_x()
  
# event -> view -> UI
def add_view_pattern(slice):
  offset_x()
  up_arrow(
    x, y_positions[slice['event']['service']],
    x, y_positions['command_view']
  )
  view_block()
  offset_x()
  up_arrow(
    x, y_positions['command_view'],
    x, y_positions[slice['trigger']['ui']]
  )
  offset_x()
  ui_block()
  
def add_automation_pattern(slice):
  pass

def add_translation_pattern(slice):
  pass

# add patterns
for slice in slices:
  match slice['pattern']:
    case 'command':
      add_command_pattern(slice)
    case 'view':
      add_view_pattern(slice)
    case 'automation':
      add_automation_pattern(slice)
    case 'translation':
      add_translation_pattern(slice)
    case _:
      raise Exception(f'No such pattern: {slice['pattern']}')
  
# set limits and remove axes
ax.set_xlim(-block_width, swimlane_length)
ax.set_ylim(-block_height, y + 1)
ax.axis('off')

# show the plot
plt.show()