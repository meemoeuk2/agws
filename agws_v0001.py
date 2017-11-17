import pygame,math,random

width,height=640,480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('agws v0.1')
background_colour = (255,255,255)
screen.fill(background_colour)
random.seed(1)

global root,non,gb_list,node_list,world_time



class node():
# node the basic map element of this world growth simulation
# the locating aspects of node is dist, ang, which define its(polar) location relative to its parent node \
# cartesian x y(to be converted to latitude and longitude ) are results calculated on dist, ang
    global root,non,node_list
    def __init__(self):
        global non,node_list
        self.ang=0.0
        self.dist=0.0
        self.parent=None
        self.child=[]
        self.x=0.0
        self.y=0.0
        self.cang=0.0 # cumulate angle
        self.id=non
        self.j=0 # j is internal counter
        self.lat=world_time # last active time
        non=non+1
        node_list.append(self)

    def draw(self,x,y):
        col = (222, 222, 222, 100)
        pygame.draw.rect(screen, col, (x,y , 3, 3))

    def sprout_node(self):
        global root,non

        n = node()
        n.child.append(self)
        n.parent=self.parent

        try :
            n.parent.child.remove(self)
            n.parent.child.append(n)
        except:
            pass

        self.parent=n
        if root==self:
            root=n

    def get_next_node(self):
        n=self
        while n:
            try:
                n.j=n.j+1
                n.child[n.j-1].j=0
                return n.child[n.j-1]
            except:
                n=n.parent
        return None


class grow_bee:
    # objects that represent surface growth at a given node. A bee has a node and it tells that node to grow
    # called bee cos it will buzz around from node to node
    # in this initial version bees stay on their starting node

    def __init__(self):
        global node_list,gb_list
        self.bnode=random.choice(node_list) # will compiler know this global?
        gb_list.append(self)


def grow_world():
    global gb_list,world_time,root
    if gb_list==[]: grow_bee()

    for gb in gb_list:
        if (gb.bnode!=root) and (gb.bnode.dist<10.0):# and
            gb.bnode.dist+=0.1
            gb.bnode.lat=world_time
        else:
            gb.bnode.sprout_node()
            if gb.bnode.parent!=root : gb.bnode=gb.bnode.parent
            gb.bnode.lat=world_time

        if random.randint(1,300)==1:
            gb_list.remove(gb)

    if random.randint(1,200)==1:
        gb=grow_bee()
        if gb.bnode.lat==world_time:
            gb_list.remove(gb)


global xlen # some variables useful in display_world
xlen=0
background_colour=(30,30,30)

def display_world(x,y):

    global xlen
    min_x,min_y,max_x,max_y = 99999,99999,0,0
    x=x-xlen/2

    screen.fill(background_colour)
    col=(222,222,222,100)
    n=root
    n.j=0
    ang=0

    while n:
        ang=ang+n.ang
        x=x+n.dist*math.cos(ang)
        y=y+n.dist*math.sin(ang)

        pygame.draw.rect(screen,col,(x,y,3,3))
        n.x=x
        n.y=y
        n.cang=ang

        if x<min_x: min_x=x
        if y<min_y: min_y=y
        if x>max_x: max_x=x
        if y>max_y: max_y=y

        n=n.get_next_node()
        if n:
            if n.parent:
                x=n.parent.x
                y=n.parent.y
                ang=n.parent.cang

    xlen=max_x-min_x
    if xlen>640 : quit()

    pygame.display.flip()


world_time=0
gb_list=[]
non=0
node_list=[]
root=node()
run=1

while run: # main loop
    world_time+=1
    grow_world()
    display_world(320,240)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run=0