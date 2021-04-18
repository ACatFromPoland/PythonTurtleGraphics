# PythonTurtleGraphics
This is mainly a joke, I was trying to see if I could make some retro game where each frame is drawn by a turtle.


Neither the Pong or the Asteroid game is finished as I ran out of time on my time **budget**.
The Asteroid game is the most functional.

I decided to take inspiration from the SMFL Library and made some custom classes for rendering.

## This has no deltatime ## I was planning on adding it but I wasn't bothered in the end

- How it works? -
**Using Asteroid as example;**
    When I got this idea, the basic concept is everything on the screen EACH FRAME would be drawn by a turtle pen.
    Each shape contains a mesh, this mesh is filled with vertice positions
    When we draw the shapes onto the screen, we get the objects turtle and make it go to the origin vertice and follow the mesh list order to draw the rest.
   
- Does it work? -
  Answer - Yes, horribly but yes.
  I found a big problem with optimization is the bigger the shapes the longer the turtle has to draw increasing the time of a frame.
  Another thing is the further the objects are from the center from the screen the longer it takes the turtle to travel from the center to each point.
 
 
- Conclusion? -
  Horrible.
  
  
  
  
If you want to try to make your own little thing.
There is a template file in the template folder(duh)
Have fun :) 
