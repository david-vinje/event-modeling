import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from yaml import safe_load

# read data
data = safe_load(open('new.yml'))
slices = data['process']['slices']

# Setup the figure
fig = plt.figure()
fig.suptitle(data['process']['name'])
ax = fig.gca()

# Define colors
colors = {
  'service': 'orange',
  'view': '#9acd32',
  'command': '#00bfff',
  'trigger': '#d3d3d3'
}

block_width = 1.5
block_height = 1

x, y = 0, 0
def offset_x(modifier = 0.5):
  global x
  x += block_width * modifier

def offset_y():
  global y
  y += block_height * 2

# Define positions for the swimlanes
y_positions = {}
for service in reversed(data['services']):
  y_positions[service] = y
  offset_y()

command_view_y_position = y
offset_y()

for role in reversed(data['roles']):
  y_positions[role] = y
  offset_y()

swimlane_length = len(slices) * 3
swimlanes_height = y

# Add swimlanes
line = plt.Line2D((0, 0), (0, 0), lw=0)
for label, y in y_positions.items():
  ax.text(-1, y, label, va='center', ha='right', fontsize=12, fontweight='bold')
  ax.add_patch(Rectangle(
    (0, y-0.5), 
    width = swimlane_length, 
    height = block_height, 
    fill=False, edgecolor='black'
  ))
    
# Function to add elements
def add_block(x, y, color, text):
  ax.add_patch(Rectangle(
    (x, y-0.5), 
    width=block_width, 
    height=block_height,
    color=color
  ))
  ax.text(x+block_width/2, y, text, ha='center', va='center', fontsize=8, color='black')

def down_arrow(start_x, start_y, end_x, end_y):
  ax.add_patch(FancyArrowPatch(
    (start_x + block_width * 0.75, start_y - block_height * 0.5), 
    (end_x + block_width * 0.75, end_y + block_height * 0.5),
    # connectionstyle='arc3,rad=0.3',
    mutation_scale=8
  ))
  
def up_arrow(start_x, start_y, end_x, end_y):
  ax.add_patch(FancyArrowPatch(
    (start_x - block_width * 0.25, start_y + block_height * 0.5), 
    (end_x + block_width * 0.25, end_y - block_height * 0.5),
    # connectionstyle='arc3,rad=0.3',
    mutation_scale=8
  ))

# Add UI/API elements and connect them with arrows
for slice in slices:
  if slice['pattern'] == 'command':
    add_block(
      x=x, 
      y=y_positions[slice['role']], 
      color=colors['trigger'], 
      text=slice['id']
    )
    down_arrow(
      x, y_positions[slice['role']], 
      x, command_view_y_position
    )
    offset_x()
    add_block(
      x=x, 
      y=command_view_y_position, 
      color=colors['command'], 
      text=slice['text']
    )
    down_arrow(
      x, command_view_y_position,
      x, y_positions[slice['service']]
    )
    offset_x()
    add_block(
      x=x,
      y=y_positions[slice['service']], 
      color=colors['service'], 
      text=slice['service_text']
    )
  elif slice['type'] == 'view':
    offset_x()
    up_arrow(
      x, y_positions[slice['service']],
      x, command_view_y_position
    )
    add_block(
      x=x, 
      y=command_view_y_position, 
      color=colors['view'], 
      text=slice['text']
    )
    up_arrow(
      x + block_width, command_view_y_position,
      x + block_width * 0.75, y_positions[slice['role']]
    )
    offset_x(modifier=0.25)
  offset_x()
  
# Set limits and remove axes
ax.set_xlim(-1, swimlane_length + 1)
ax.set_ylim(-1, swimlanes_height)
ax.axis('off')

# Show the plot
plt.show()