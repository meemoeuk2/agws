
; node as opposed to vertex
; the basic map element of this world growth simulation
; the locating aspects of node is dist,ang, which define its (polar) location relative to its parent node
; cartesian x y ( to be converted to latitude and longitude ) are results of algorithms based on dist,ang

Type node
 Field ang#,dist# ; defining polar coord relative to parent node
 Field parent.node
 Field child.node[5] ; parent , child, nodes are organised in a tree structure
 Field id
 
 Field x#,y# ; resultant cartisean coords
 Field j     ; an internal ( private ) counter used for incrementing thru child nodes
 Field lat    ; last active time ; when was the node last changed?
End Type


; growth bee
; these represent places of rapid growth on the world
; essentially this is where growth manifests in the world and in this program
; why call it a bee?
;  cos it buzzes around from node to node causing growth around its current node
; however in ultra simple v001 bees don't buzz from node to node, they just sit on their start node
Type growth_bee 
 Field node.node
End Type

Global root.node=New node
Global non=1 ; number of nodes
Global world_time=-1

Graphics 1024,768,16,2
Global gw=GraphicsWidth()
Global gh=GraphicsHeight()



; ****** main loop ******
While Not KeyHit(1)
 world_time=world_time+1
 grow_world()
 display_world(gw/2,gh/2)
Wend
End



; ****** functions ********

Function sprout_node(n.node)
; a node sprouts a new node located ontop of itself. The new node will typically move away from 
n2.node=New node
n2\child[0]=n
n2\parent=n\parent

If n2\parent<>Null
 While n2\parent\child[i]<>Null
  If n2\parent\child[i]=n Then n2\parent\child[i]=n2:Exit
  i=i+1
 Wend
EndIf

n\parent=n2
If root=n Then root=n2

n2\id=non
non=non+1
 
End Function



Function get_next_node.node(n.node)

While n<>Null
 If n\j<=5
  If n\child[n\j]<>Null
   n\j=n\j+1

   n\child[n\j-1]\j=0
   Return n\child[n\j-1]
  EndIf
 EndIf

 n=n\parent 
Wend

Return Null

End Function



Function grow_world()

gb.growth_bee=First growth_bee
If gb=Null
 gb=New growth_bee
 gb\node=get_rand_node()
EndIf

For gb.growth_bee=Each growth_bee
 If gb\node\dist<10 And gb\node<>root
  gb\node\dist=gb\node\dist+0.1
  gb\node\lat=world_time
 Else
  sprout_node(gb\node)
  gb\node=gb\node\parent
  gb\node\lat=world_time
 EndIf
 If Rand(250)=1 Then Delete gb
Next

If Rand(200)=1
 gb=New growth_bee
 gb\node=get_rand_node()
 If gb\node\lat=world_time Then Delete gb ; not allowed 2 growth_bees on same node
EndIf

End Function




Function get_rand_node.node()

For n.node=Each node:i=i+1:Next
If i=0 Then Return Null
i=Rand(i)-1

For n=Each node
 If j=i Then Return n
 j=j+1
Next

RuntimeError "get rand node fail : "+i+" "+j

End Function



Global xlen
Function display_world(x#,y#)

min_x=99999
min_y=99999
x=x-xlen/2

Cls
Color 222,222,222
n.node=root
n\j=0

While n<>Null
 x=x+n\dist*Cos(ang)
 y=y+n\dist*Sin(ang)
 Rect x,y,3,3,1
 n\x=x
 n\y=y 

 If x<min_x Then min_x=x
 If y<min_y Then min_y=y
 If x>max_x Then max_x=x ; lazy grab, use them next time
 If y>max_y Then max_y=y ;

 n=get_next_node(n) 
 If n<>Null
  If n\parent<>Null
   x=n\parent\x
   y=n\parent\y
  Else
   RuntimeError " get_next_node returned node "+n\id+" that doesn't have parent "
  EndIf

 EndIf
 m=m+1
Wend

xlen=max_x-min_x
If xlen>gw Then End ; end of this program!

Flip

End Function