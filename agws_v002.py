import pygame,math,random

gwidth,gheight=1024,200
screen = pygame.display.set_mode((gwidth, gheight))
pygame.display.set_caption('agws v0.002')
background_colour = (255,255,255)
screen.fill(background_colour)
#random.seed(1)

pygame.font.init()
global myfont
myfont = pygame.font.SysFont('Comic Sans MS', 18)

global root,non,gb_list,node_list,world_time,time_direction
global active_nl,history,future

class node():
# node the basic map element of this world growth simulation
# the locating aspects of node is dist, ang, which define its(polar) location relative to its parent node \
# cartesian x y(to be converted to latitude and longitude ) are results calculated on dist, ang
    global root,non,node_list,history

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
        global root,non,history

        n = node()
        n.child.append(self) # sprout a parent not a child
        n.parent=self.parent

        try :
            n.parent.child.remove(self)
            n.parent.child.append(n)
        except:
            pass

        self.parent=n
        if root==self: root=n

        history.append((world_time,'sprout',(self.id,n.id)))


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


    def grow_node(self):
        global history

        if (self != root) and (self.dist < 10.0):  # and
            self.dist += 0.5
            self.lat = world_time
        else:
            self.sprout_node()
            if self.parent != root:
                active_nl.remove(self)
                self = self.parent
                active_nl.append(self)
            self.lat = world_time

        if random.randint(1, 300) == 1:
            active_nl.remove(self)
            history.append((world_time,'deactivated',self.id))


    def shrink_node(self):

        if (self!=root) and (self.dist>0):
            self.dist -= 0.5
        self.lat = world_time-1


    def reduct_node(self,an): # an = active node, to pass activity to
        # its actually the node's parent that gets reducted

  #      active_nl.remove(self.parent)
  #      node_list.remove(self.parent)

  #      try:
  #          self.parent.parent.child.remove(self.parent)
  #          self.parent=self.parent.parent
  #          self.parent.child.append(self)
   #     except:
   #         self.parent=None

        try :
            active_nl.remove(self)
        except:
            pass

        try :
            node_list.remove(self) # huh? node appears to have been removed already at this point
        except:
            pass

        try:
            for c in self.child:
                self.parent.child.append(c)
                self.parent.child.remove(self)
                c.parent=self.parent

                if c.id==an[0] : # pass on the activity to this node
                    if not (c in active_nl): active_nl.append(c)
        except: # no parent
            c.parent=None






def active_rand_node():
    global history

    n=random.choice(node_list)
    if not (n in active_nl):         # will this line work?
        active_nl.append(n)
        history.append((world_time,'activated',n.id))


def grow_world():
    global world_time,root

    world_time+=1
    for n in active_nl: n.grow_node()
    if active_nl==[]: active_rand_node()
    if random.randint(1,200)==1: active_rand_node()

def shrink_world():
    global world_time

    for n in active_nl: n.shrink_node()
    recall_history()

    world_time-=1


def recall_history():
    global history

    while True:
        try :
            h=history[-1]
            if h[0]==world_time:
                history.pop()

                if h[1] == 'deactivated':
                    active_nl.append(node_list[h[2]])
                elif h[1] == 'activated':
                    active_nl.remove(node_list[h[2]])
                elif h[1] == 'sprout':

                    n=node_list.pop()
                    n.reduct_node(h[2])

                future.append(h)
            else:
                break
        except:
            break


global xlen # some variables useful in display_world
xlen=0
background_colour=(30,30,30)

def display_world(x,y):

    global xlen,time_direction
    min_x,min_y,max_x,max_y = 99999,99999,0,0
    x=x-xlen/2

    screen.fill(background_colour)
    col=(222,222,222,100)
    n=root
    n.j=0
    ang=0
    i=0

    textsurface = myfont.render('World Time : '+str(world_time), False, (222, 222, 222))
    screen.blit(textsurface, (gwidth/2,10))

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

        i+=1

    xlen=max_x-min_x
    if xlen>gwidth : time_direction=-time_direction

    pygame.display.flip()

# startup

world_time=0
time_direction=1
non=0
node_list=[]
active_nl=[]
history=[]
future=[]
root=node()
run=1

while run: # main loop

    if time_direction==1:
        grow_world()
    else:
        shrink_world()

    pygame.time.wait(10)
    if non>100 :
        time_direction=-1
    if world_time<0 :quit()

    display_world(gwidth/2,gheight/2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run=0