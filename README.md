# Next>> in the Buildiiiing!!!!!!
## Intro

Next>> (or Next77) is an app that is aimed towards people who enjoy partying from time to time (or everytime lol). 
Next>> simply helps make the connection between the DJ and audience even more magical by allowing the DJ to have a 
sneak peak at what his users are thinking while maintaining control throughout the event.

## Flow

1) ### Dj setup

    To use the [live project](https://next77-d78d18831bdf.herokuapp.com/), use the credidentials below

    email: abcd123@gmail.com
    password: Abcd1234

    Or, you could register using the register button(should be on the page if you clicked on the live project link).

    After this you'll be asked to enter an event name, enter whatever picks your interest and cotinue.

    You should have reached the dj screen.

2) ### User Setup

    if you reached the dj screen, you should see and id next to your event name. Just like this
![Screenshot from 2024-04-10 01-23-07](https://github.com/yvanroan/HeyDJ/assets/42220010/4de33d46-1ca4-4d01-8083-6b2116beb712)

    copy the link below and replace '{id}' with the id you got on your Dj screen.
   
        https://next77-d78d18831bdf.herokuapp.com/userentry?event_id={id}

    To ease the user's experience, this will eventually be replaced by a qrcode

3) ### User sending request

    You should have hopefully reached the user screen now.
    All you have to do is enter the correct spelling of both the artist and the title you have in mind.
    Note that if the song does not exist your request won't be sent and in some rare cases, the song might not exist in our api.

4) ### DJ recieving and processing request

    You would have to reload your screen to see the request being sent. (working on making this more efficient)
    The songs recieved are in the Dj's stack and he can either play them or just straight up remove them.

    If he choose to reject the request, he needs to enter the id of the request and slide to remove the request.
    If he choose to accept the request, the song must be playing before he enters the request id and click play.
![Screenshot from 2024-04-10 16-12-34](https://github.com/yvanroan/HeyDJ/assets/42220010/5906b22e-1a39-463b-96e1-e22fdd492df2)

    In both cases if the id is a valid one the request should leave the stack.

5) ### End Event(In progress)

    Once the DJ is done with his party, he clicks on the "End Event" button and the party stops for everyone.
    Every request in the DJ's stack is rejected and the user is notified of the party's end.

## Future Improvements

1) allow multiple dj to manage the an event sequentially

2)  let me know what y'all would like to see.


