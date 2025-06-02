import datetime

import pygame as pg


class Timer:
    """
    A pygame-based timer display component for real-time elapsed time tracking.
    
    This class provides a visual timer that displays elapsed time on a pygame surface,
    with support for pausing/resuming functionality. The timer shows time in MM:SS:mmm
    format (minutes:seconds:milliseconds) and is positioned at the center-top of the screen.
    
    Core functionality:
    - Real-time elapsed time calculation and display
    - Pause/resume capability with accurate time tracking
    - Customizable font, color, and size
    - Automatic screen positioning and rendering
    
    Constructor parameters:
        screen (pg.Surface): The pygame surface to render the timer on
        font (str or None): Path to font file, or None for default pygame font
        color: Color for the timer text (pygame Color object or tuple)
        size (int): Font size for the timer display
    
    Note:
        - Timer must be started with start() method before use
        - The timer position is automatically centered horizontally at y=45
        - Paused time is accurately tracked and excluded from elapsed time calculation
    """
    def __init__(self, screen: pg.Surface, font, color, size):
        self.screen = screen
        self.font = pg.font.Font(font, size)
        self.pos = (screen.get_width() / 2, 45)
        self.color = color
        self.size = size
        self.time = datetime.timedelta(0)
        self.time_text = self.font.render("00:00", True, self.color)
        self.paused_time = datetime.timedelta(0)
        self.paused_at = datetime.datetime.now()
        self.time_rect = self.time_text.get_rect(center=self.pos)

    def start(self) -> None:
        """
        Initialize and start the time display component.
        
        This method captures the current time, renders it as text using the configured
        font and color, and positions the rendered text at the specified center position.
        
        The method performs three main operations:
        1. Records the current datetime as the start time
        2. Renders the time string (HH:MM format) as a surface object
        3. Creates a rectangle for positioning the rendered text
        
        Side Effects:
            - Sets self.start_time to current datetime
            - Updates self.time_text with rendered time surface
            - Updates self.time_rect with positioned rectangle
        """
        self.start_time = datetime.datetime.now()
        self.time_text = self.font.render(self.start_time.strftime("%H:%M"), True, self.color)
        self.time_rect = self.time_text.get_rect(center=self.pos)

    def pause(self, paused: bool) -> None:
        """
        Pause or resume the timer and track paused time.
        
        This method handles pausing and resuming functionality by recording
        pause timestamps and accumulating total paused duration.
        
        Args:
            paused (bool): True to pause the timer, False to resume it.
                          When True, records the current timestamp as pause start.
                          When False, calculates pause duration and adds it to total paused time.
        
        Note:
            When pausing (paused=True), stores current datetime in paused_at.
            When resuming (paused=False), calculates pause duration by subtracting
            paused_at from current time, then adds this duration to paused_time.
        """
        if paused:
            self.paused_at = datetime.datetime.now()
        else:
            self.paused_at = datetime.datetime.now() - self.paused_at
            self.paused_time += datetime.timedelta(
                self.paused_at.days,
                self.paused_at.seconds,
                self.paused_at.microseconds
            )

    def update(self) -> None:
        """
        Update the timer display on the screen.
        
        This method calculates the elapsed time since the timer started,
        subtracting any paused time, and renders the time as a formatted
        string in MM:SS:mmm format (minutes:seconds:milliseconds).
        The rendered time text is then displayed on the screen at the
        specified position.
        
        Time format breakdown:
        - Minutes: Total seconds divided by 60
        - Seconds: Remainder of total seconds divided by 60  
        - Milliseconds: Microseconds divided by 1000, modulo 1000
        
        The text is rendered with the configured font and color,
        with a semi-transparent dark background.
        """
        self.time = datetime.datetime.now() - self.start_time - self.paused_time
        self.time_text = self.font.render(
            f"{self.time.seconds // 60}:{self.time.seconds % 60}:{self.time.microseconds // 1000 % 1000}",
            True,
            self.color,
            pg.color.Color(32, 32, 32, 0)
        )

        self.screen.blit(self.time_text, self.time_rect)
