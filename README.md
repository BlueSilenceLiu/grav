This file if from turtledemo's file (a more general version)

1, You can create the planet derectly because the GravSys is auto-created and can be created automatically.  
2, Use Window() to get the Screen.

  _(information below are copied from file's comment)_
3, must add a mainloop() in the lastline of your code! or there will be an error from Threading!  
   but you can use GravSys.run() instead of GravSys.start() to avoid this, the disadvantage is that you must wait before  
   emulating end, and without mainloop(), the window will close after graphing.  
4, ##Planet(m, x, v, **kwargs)  
    atributes
```
    m: mass
    x: initial position(a Vec2D object, or Vec as an alia we provide)  
    v: initial position(a Vec2D object, or Vec as an alia we provide)  
    kwargs:  
        gravSys: a GravSys object, the gravity system that ths star exist;  
            If the attribute not exist, then:  
                1: if there have been a gravSys built, use the last one that created;  
                2: if there haven't been any gravSys, create one automatically.  

        shape: the shape of star;  
              we recommend you to use PLANET(equals to 'planet') as a planet that can be delight,  
                                   or STAR(equals to 'circle') as a sun that make light.   
              otherwise, it would be harder for user to watch(unless you have a specific use).  

        pc: pencolor, effective when pd is True.  
        pd: is pendown, a boolean.  
            default value: True  
```


# for more information, please look at the comments.
