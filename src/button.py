import pygame

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # Initialize the button with an image, position, text, font, and colors
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        
        # Render the text with the base color
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        # If no image is provided, use the text as the button image
        if self.image is None:
            self.image = self.text
        
        # Get the rectangle for the button image and center it at the given position
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        # Get the rectangle for the text and center it at the given position
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """Draw the button on the screen."""
        # Composition: Button class uses the screen object to draw itself
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """Check if the button is clicked."""
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """Change button color on hover."""
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
