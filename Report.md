# Exercise 1:

    For this exercise we installed Micropython and Thonny and then setup our Microcontroller with the resistor and light sensor. 
    An issue we ran into when testing this was not having the resistor and sensor securely placed within the microntroller, which led to us not getting any data when first running the script. 
    After fixing this, we then found the max and min values of this sensor by putting flashlights to the sensor and by putting the sensor in a completely dark drawer. 
    The values we found from this were Min: 2500 Max: 51000.

# Exercise 2:

    For this exercise, I modified the original code to play a sequence of musical notes from the song Twinkle, Twinkle, Little Star.
    I defined a dictionary containing frequencies for musical notes and created a list of tuples representing the melody, with each tuple consisting of a note and its duration.
    I then implemented the `play_song()` function to loop through the melody, playing each note for its corresponding duration using PWM output on pin GP16, connected to a speaker. 
    After each note, the speaker is silenced to create a pause, and the PWM signal is turned off once the song is complete.

# Exercise 3:

    For this exercise, we created a dictionary to create the JSON data for the user after they play the game. 
    After doing this, we created our FireBase cloud which is what we used for authentication and data storage.
    We then setup an API server which we used as the "middle-man" between the microcontroller and cloud.
    This server was an express application and house many endpoints for the micropython file.
    The way the interactions worked was the micropython file will run, since it is connected to the internet, it will send Rest APIs to the API server and then the server will communicate with the cloud for the desired information.
    The way the game is played is that the user is able to either log in or sign up. 
    If they don't have an account they will be able to sign up using a gmail account. 
    If they do they will have to use their gmail username and their password.
    After the authentication is done, the user is prompted to either play the game or view their scores. 
    If they select view, they will be able to only see their data.
    If they play, they will be creating new data for their account.

    
