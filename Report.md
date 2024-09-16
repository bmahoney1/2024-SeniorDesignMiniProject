# Exercise 1:

    For this exercise we installed Micropython and configured pi pico to Thonny. The circuit for exercise 1 comprised of the 10Kohm resistor and a photocell both interconnected with the ADC. 
    An issue we ran into when testing this was not having the resistor and photocell securely placed within the microntroller, which led to us not getting any data when first running the script. 
    After fixing this, we then found the max and min values of this sensor by putting flashlights to the sensor and by putting the sensor in a completely dark drawer. 
    The values we found from this were Min: 2500 Max: 51000.
    
    However, for theoritical values that the in-built ADC can yeild us is 2V to 3.3V. These values are based on the ADC's maximum and minimum 16-bit resolution values i.e 0 to 65536. 

# Exercise 2:

    For this exercise, I modified the original code to play a sequence of musical notes from the song Toky Drift.
    I defined a dictionary containing frequencies for musical notes and frequencies described for each note along with the duration for each specific note. 
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


Testing:

There was a lot of testing that went into setting up the API communication between the microcontroller, the api server and our firebase cloud.
Some of the testing that was done was using Postman to test if the API server was setup correctly and that it was receving the rest APIs.
We also had to test how to correctly link the API server to the cloud, and then how to put in the data into the collection of documents.
Additionally, we had to setup our database in a way that we could retrieve only data for the corresponding user.


Initially, after setting up firestore data base our testing was based on coomunications between the rest API server and pi pico via wifi interface. For this part of the testing json files were a format of communication between hardware and our local server. For initial testing the json files were saved to the cloud with a document ID of year, month, day, weekday, hour, minute, second, microsecond. After we successfully received these files at our database from the front end, we applied the unique user ID for the document ID to these files. We received this ID when the user logged in or signed up so this was our way of keep our data organized. This is how we conducted rigourous testing between hardware, local server and firebase to achieve accurate results in real time for the user playing the game exercise. 
