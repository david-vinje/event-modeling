import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# Update the visualization to include all slices in one swim lane diagram

# Setup the figure
fig, ax = plt.subplots(figsize=(20, 9))

# Define colors
colors = {
    "UI/API": "#A9A9A9",       # Gray
    "Command": "#1E90FF",      # Blue
    "Event": "#FFA500",        # Orange
    "View": "#32CD32",         # Green
    "TodoList": "#32CD32",     # Green
    "AutomatedProcess": "#FFFFFF", # White
}

# Define positions for the swimlanes
y_positions = {
    "Role": 12,
    "Interaction": 9,
    "Sales": 6,
    "Shipping": 3,
    "Payment": 0,
}

# Add swimlanes
for label, y in y_positions.items():
    ax.text(-1, y, label, va='center', ha='right', fontsize=12, fontweight='bold')
    ax.add_patch(Rectangle((0, y-0.5), 40, 1, fill=False, edgecolor='black'))

# Function to add elements
def add_element(x, y, width, height, color, text):
    ax.add_patch(Rectangle((x, y-0.5), width, height, color=color))
    ax.text(x + width/2, y, text, ha='center', va='center', color='black')

# Function to add arrows
def add_arrow(start_x, start_y, end_x, end_y):
    ax.add_patch(FancyArrowPatch((start_x, start_y), (end_x, end_y), mutation_scale=15))

# Add UI/API elements and connect them with arrows
x = 0.5
add_element(x, y_positions["Role"], 1.5, 1, colors["UI/API"], "WebShop UI\nAdd Item")
add_arrow(x + 1.5, y_positions["Role"], x + 2, y_positions["Interaction"])

x += 2.5
add_element(x, y_positions["Interaction"], 2, 1, colors["Command"], "AddItemToShoppingBasket\nCommand")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Sales"])

x += 3
add_element(x, y_positions["Sales"], 2, 1, colors["Event"], "ItemAddedToShoppingBasket\nEvent")
add_arrow(x + 2, y_positions["Sales"], x + 3, y_positions["Interaction"])

x += 3.5
add_element(x, y_positions["Interaction"], 2, 1, colors["View"], "ShoppingBasket\nView")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Role"])

x += 3
add_element(x, y_positions["Role"], 1.5, 1, colors["UI/API"], "WebShop UI\nRequest Checkout")
add_arrow(x + 1.5, y_positions["Role"], x + 2, y_positions["Interaction"])

x += 2.5
add_element(x, y_positions["Interaction"], 2, 1, colors["Command"], "RequestCheckOut\nCommand")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Sales"])

x += 3
add_element(x, y_positions["Sales"], 2, 1, colors["Event"], "CheckOutRequested\nEvent")
add_arrow(x + 2, y_positions["Sales"], x + 3, y_positions["Interaction"])

x += 3.5
add_element(x, y_positions["Interaction"], 2, 1, colors["View"], "ShoppingBasket\nUpdate View")

x = 0.5
add_element(x + 16, y_positions["Role"], 1.5, 1, colors["UI/API"], "WebShop UI\nAdd Shipping Details")
add_arrow(x + 17.5, y_positions["Role"], x + 18, y_positions["Interaction"])

x += 18.5
add_element(x, y_positions["Interaction"], 2, 1, colors["Command"], "AddShippingDetailsToOrder\nCommand")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Shipping"])

x += 3
add_element(x, y_positions["Shipping"], 2, 1, colors["Event"], "ShippingDetailsAddedToOrder\nEvent")
add_arrow(x + 2, y_positions["Shipping"], x + 3, y_positions["Interaction"])

x += 3.5
add_element(x, y_positions["Inter2action"], 2, 1, colors["View"], "OrderShippingDetails\nView")

# Additional elements for Payment Details and Place Order process
x = 0.5
add_element(x + 33, y_positions["Role"], 1.5, 1, colors["UI/API"], "WebShop UI\nAdd Payment Details")
add_arrow(x + 34.5, y_positions["Role"], x + 35, y_positions["Interaction"])

x += 35.5
add_element(x, y_positions["Interaction"], 2, 1, colors["Command"], "AddPaymentDetailsToOrder\nCommand")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Payment"])

x += 3
add_element(x, y_positions["Payment"], 2, 1, colors["Event"], "PaymentDetailsAddedToOrder\nEvent")
add_arrow(x + 2, y_positions["Payment"], x + 3, y_positions["Interaction"])

x += 3.5
add_element(x, y_positions["Interaction"], 2, 1, colors["View"], "OrderPaymentDetails\nView")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Role"])

x += 3
add_element(x, y_positions["Role"], 1.5, 1, colors["UI/API"], "WebShop UI\nPlace Order")
add_arrow(x + 1.5, y_positions["Role"], x + 2, y_positions["Interaction"])

x += 2.5
add_element(x, y_positions["Interaction"], 2, 1, colors["Command"], "PlaceOrder\nCommand")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Sales"])

x += 3
add_element(x, y_positions["Sales"], 2, 1, colors["Event"], "OrderPlaced\nEvent")
add_arrow(x + 2, y_positions["Sales"], x + 3, y_positions["Interaction"])

x += 3.5
add_element(x, y_positions["Interaction"], 2, 1, colors["TodoList"], "Orders Ready for Packaging\nTodoList")
add_arrow(x + 2, y_positions["Interaction"], x + 2.5, y_positions["Shipping"])

x += 3
add_element(x, y_positions["Shipping"], 2, 1, colors["Command"], "PackageOrder\nCommand")
add_arrow(x + 2, y_positions["Shipping"], x + 2.5, y_positions["Shipping"])

x += 3.5
add_element(x, y_positions["Shipping"], 2, 1, colors["Event"], "OrderPackagingRequested\nEvent")

# Set limits and remove axes
ax.set_xlim(-2, 40)
ax.set_ylim(-2, 14)
ax.axis('off')

# Show the plot
plt.show()