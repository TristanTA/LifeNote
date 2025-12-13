

from app.ui.kahnban import KahnbanApp, Board, Task

app = KahnbanApp()
board = Board(app, "Project Alpha")
task1 = Task(app, "Example", board.bins[0], priority=1, deadline=None, important=True, urgent=False)
app.save()