import matplotlib.pyplot as plt

grid = [
["S",".",".","#",".","."],
[".","#",".","#",".","."],
[".","#",".",".",".","#"],
[".",".",".","#",".","."],
["#","#",".",".",".","."],
[".",".",".","#","#","G"]
]

start, goal = (0,0), (5,5)

def h(a,b): return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar():
    open = [start]
    came, g = {}, {start:0}

    while open:
        cur = min(open, key=lambda x: g[x] + h(x,goal))
        if cur == goal:
            path=[]
            while cur in came:
                path.append(cur)
                cur = came[cur]
            return [start] + path[::-1]

        open.remove(cur)
        x,y = cur

        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            n = (x+dx,y+dy)
            if 0<=n[0]<6 and 0<=n[1]<6 and grid[n[0]][n[1]]!="#":
                if n not in g or g[cur]+1 < g[n]:
                    g[n] = g[cur]+1
                    came[n] = cur
                    open.append(n)

path = astar()
print(path)

plt.imshow([[c=="#" for c in r] for r in grid], cmap="gray_r")
if path:
    x,y = zip(*path)
    plt.plot(y,x,'r')
plt.show()
