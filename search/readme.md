it is a little difficult to learn about the API. So I will make some notes.

vim is so difficult to use. Fortunately the clipboard is not so hmmmm.....

## game.py:
**Directions**: south east west and north 

left right stop      

**Configuration**: the config of the game(the state of the character?)

x,y = postion 

direction

it can generate a successor.

**AgentState**: AgentStates hold the state of an agent (configuration, speed, scared, etc).

It may be a pacman or a ghost.

**Grid**:网格 in Chinese.

A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

want to findout how the wall is denoted.

I know. we should think the wall/food/pacman/ghost is on the points.
## pacman.py
please read the notes of the project online.

A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes.


## util.py
Stack/Queue/PriorityQueue/PriorityQueueWithFunction/Counter/ManhatonDist.

## searchAgents.py
searchAgent.class use the search alg in the search.py we write.


highly abstract. first meet.