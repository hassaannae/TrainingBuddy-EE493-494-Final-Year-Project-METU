from espeak import espeak
import speech_recognition as sr
import pyaudio
import time
import pvporcupine
import struct
import os
import sys
import MotorControlRaw

launcher = MotorControlRaw.PingPongLauncher()

# Text to Speech
def speak(text): 
    print("J.A.R.V.I.S.: " + text + " \n")
    espeak.synth(text)


# Speech to Text
def takeCommand() : #Hear what is being said
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...", end="")
        audio = r.record(source, duration=5)
        query = ''
        transcribed_text = ""
        try:
            print("Recognizing...", end="")
            query = r.recognize_google(audio, language= 'en-US', show_all= True)
            alternatives = query.get('alternative', [])
            transcribed_text = " ".join([alternative.get('transcript', '') for alternative in alternatives])
            print(f"User said: {transcribed_text}")
        except Exception as e:
            print ("Exception: " + str(e))

    return transcribed_text.lower()

def RepetitionMode():
    print("repetition mode")
    launcher.set_mode("repetition")
    userSaid = takeCommand()
    if "spin" in userSaid:
        if "no spin" in userSaid:
            speak("Setting spin to No Spin")
            #Call No Spin here
            launcher.set_spin_style("no spin")
            
        if "backspin" in userSaid:
            if "slight" in userSaid:
                speak("Setting spin to slight backspin")
                #Call Slight Backspin here
                launcher.set_spin_style("slight backspin")
                
            elif "heavy" in userSaid:
                speak("Setting spin to heavy backspin")
                #Call Heavy Backspin here
                launcher.set_spin_style("heavy backspin")
                
            else:
                speak("Setting spin to slight backspin")
                #Call Slight Backspin here
                launcher.set_spin_style("slight backspin")
                
        if "topspin" in userSaid:
            if "slight" in userSaid:
                speak("Setting spin to slight topspin")
                #Call Slight topspin here
                launcher.set_spin_style("slight topspin")
                
            elif "heavy" in userSaid:
                speak("Setting spin to heavy topspin")
                #Call Heavy topspin here
                launcher.set_spin_style("heavy topspin")
                
            else:
                speak("Setting spin to slight topspin")
                #Call Slight topspin here
                launcher.set_spin_style("slight topspin")

    if "angle" in userSaid:
        if "left" in userSaid:
            speak("Setting launch angle to left")
            #Call Left angle change here
            launcher.set_launch_angle("left")

        if "right" in userSaid:
            speak("Setting launch angle to right")
            #Call right angle change here
            launcher.set_launch_angle("right")

        if "mid" in userSaid:
            speak("Setting launch angle to mid")
            #Call mid angle change here
            launcher.set_launch_angle("mid")

    if "speed" in userSaid:
        if "slow" in userSaid:
            speak("Setting ball speed to slow")
            #Call slow ball speed change here
            launcher.set_ball_speed("slow")

        if "medium" in userSaid:
            speak("Setting ball speed to medium")
            #Call medium ball speed change here
            launcher.set_ball_speed("medium")

        if "fast" in userSaid:
            speak("Setting ball speed to fast")
            #Call fast ball speed change here
            launcher.set_ball_speed("fast")

    if "frequency" in userSaid:
        if "slow" in userSaid:
            speak("Setting serve frequency to slow")
            #Call slow serve freq change here
            launcher.serve_freq="slow"
            launcher.thread()

        if "medium" in userSaid:
            speak("Setting serve frequency to medium")
            #Call medium serve freq change here
            launcher.serve_freq="medium"
            launcher.thread()

        if "fast" in userSaid:
            speak("Setting serve frequency to fast")
            #Call fast serve freq change here
            launcher.serve_freq="fast"
            launcher.thread()

    if "mode" in userSaid:
        if "repetition" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                speak("This is Repetition Mode")

        if "randomized repetition" in userSaid:
            RandomizedRepetitionMode()

        if "sequence" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                SequenceMode()

        if "randomized sequence" in userSaid:
            RandomizedSequenceMode()

        if "game" in userSaid:
            GameMode()

    if "power of" in userSaid:
        speak("Powering off")
        launcher.turn_off()

    if "power on" in userSaid:
        speak("Powering on")
        launcher.turn_on()

in_RR = False

def RandomizedRepetitionMode():
    global in_RR
    print("randomized repetition mode")
    launcher.set_mode("randomized repetition")
    if in_RR == False:
        in_RR = True
        speak("Randomized Repetition Mode. Select spin style")
        userSaid = takeCommand()
        if "spin" in userSaid:
            if "no spin" in userSaid:
                speak("Setting spin to No Spin")
                #Call No Spin here
                launcher.randomlaunch("no spin")
                
            elif "backspin" in userSaid:
                speak("Setting spin to backspin")
                #Call Slight Backspin here
                launcher.randomlaunch("backspin")
                             
            elif "topspin" in userSaid:
                speak("Setting spin to topspin")
                #Call Slight topspin here
                launcher.randomlaunch("topspin")
            else:
                speak("Setting spin to no spin")
                #Call No Spin here
                launcher.randomlaunch("no spin")

    userSaid = takeCommand()
    if "change" in userSaid:
        in_RR = False
        RandomizedRepetitionMode()
    
    if "mode" in userSaid:
        if "repetition" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                speak("Repitition Mode")
                RepetitionMode()

        if "randomized repetition" in userSaid:
            speak("This is Randamized Repetition Mode")

        if "sequence" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                SequenceMode()

        if "randomized sequence" in userSaid:
            RandomizedSequenceMode()

        if "game" in userSaid:
            GameMode()

    if "power of" in userSaid:
        speak("Powering off")
        launcher.turn_off()

    if "power on" in userSaid:
        speak("Powering on")
        launcher.turn_on()

def getSpin(SpininSM):
    if "no spin" in SpininSM:
        spin = "no spin"
    elif "topsin" in SpininSM:
        spin = "topspin"
    elif "backspin" in SpininSM:
        spin = "backspin"
    elif "heavy" in SpininSM:
        return "heavy" + spin
    else:
        spin = "no spin"
    return spin

def getAngle(AngleinSM):
    if "right" in AngleinSM:
        angle = "right"
    elif "left" in AngleinSM:
        angle = "left"
    elif "mid" in AngleinSM:
        angle = "mid"
    else:
        angle = "mid"
    return angle

in_SM = False

def SequenceMode():
    global in_SM
    global Seq1spin, Seq1direction, Seq2spin, Seq2direction, Seq3spin, Seq3direction
    print("sequence mode")
    launcher.set_mode("sequence")
    if in_SM == False:
        in_SM = True
        speak("Sequence Mode. Setup Sequence")
        time.sleep(1)
        speak("order number 1")
        time.sleep(1)
        O1 = takeCommand()
        speak("order number 2")
        time.sleep(1)
        O2 = takeCommand()
        speak("order number 3")
        time.sleep(1)
        O3 = takeCommand()

        Seq1spin = getSpin(O1)
        Seq1direction = getAngle(O1)
        Seq2spin = getSpin(O2)
        Seq2direction = getAngle(O2)
        Seq3spin = getSpin(O3)
        Seq3direction = getAngle(O3)

        launcher.Sequence(Seq1spin, Seq1direction, Seq2spin, Seq2direction, Seq3spin, Seq3direction)

    userSaid = takeCommand()
    if "mode" in userSaid:
        if "repetition" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                speak("Repitition Mode")
                RepetitionMode()
                

        if "randomized repetition" in userSaid:
            RandomizedRepetitionMode()

        if "sequence" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                speak("This is Sequence Mode")

        if "randomized sequence" in userSaid:
            RandomizedSequenceMode()

        if "game" in userSaid:
            GameMode()

    if "reset sequence" in userSaid:
        speak("Resetting Sequence")
        in_SM = False
        SequenceMode()

    if "repeat sequence" in userSaid:
        speak("Repeating Sequence")
        launcher.Sequence(Seq1spin, Seq1direction, Seq2spin, Seq2direction, Seq3spin, Seq3direction)

    if "power of" in userSaid:
        speak("Powering off")
        launcher.turn_off()

    if "power on" in userSaid:
        speak("Powering on")
        launcher.turn_on()

in_RSM = False
def RandomizedSequenceMode():
    global in_RSM
    global RSeq1spin, RSeq1direction, RSeq2spin, RSeq2direction, RSeq3spin, RSeq3direction
    print("randomized sequence mode")
    launcher.set_mode("randomized sequence")
    if in_RSM == False:
        in_RSM = True
        speak("Randomized Sequence Mode. Setup Sequence")
        time.sleep(1)
        speak("order number 1")
        time.sleep(1)
        O1 = takeCommand()
        speak("order number 2")
        time.sleep(1)
        O2 = takeCommand()
        speak("order number 3")
        time.sleep(1)
        O3 = takeCommand()

        RSeq1spin = getSpin(O1)
        RSeq1direction = getAngle(O1)
        RSeq2spin = getSpin(O2)
        RSeq2direction = getAngle(O2)
        RSeq3spin = getSpin(O3)
        RSeq3direction = getAngle(O3)

        launcher.SequenceRandom(RSeq1spin, RSeq1direction, RSeq2spin, RSeq2direction, RSeq3spin, RSeq3direction)

    userSaid = takeCommand()
    if "mode" in userSaid:
        if "repetition" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                speak("Repitition Mode")
                RepetitionMode()

        if "randomized repetition" in userSaid:
            RandomizedRepetitionMode()

        if "sequence" in userSaid:
            if "randomized" in userSaid:
                pass
            else:
                SequenceMode()

        if "randomized sequence" in userSaid:
            speak("This is Randomized Sequence Mode")

        if "game" in userSaid:
            GameMode()

    if "reset sequence" in userSaid:
        speak("Resetting Sequence")
        in_RSM = False
        RandomizedSequenceMode()

    if "repeat sequence" in userSaid:
        speak("Repeating Sequence")
        launcher.SequenceRandom(RSeq1spin, RSeq1direction, RSeq2spin, RSeq2direction, RSeq3spin, RSeq3direction)

    if "power of" in userSaid:
        speak("Powering off")
        launcher.turn_off()

    if "power on" in userSaid:
        speak("Powering on")
        launcher.turn_on()    
    

def main():
    print("main")
    porcupine = None
    pa = None
    audio_stream = None


    print("J.A.R.V.I.S. version 1.2 - Online and Ready!")
    print('**********************************************************')
    print("J.A.R.V.I.S.: Awaiting your call")

    try:
        porcupine = pvporcupine.create(access_key = "ZkQ/pFyhVEzFm3XsJwPCgVY0NWCl48PkSJAoz0eZ721AVxuirhCdmg==", keywords=["jarvis"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

        while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Hotword Detected..", end="")
                    speak("Yes")
                    if launcher.mode == "repetition":
                        RepetitionMode()
                    elif launcher.mode == "randomized repetition":
                        RandomizedRepetitionMode()
                    elif launcher.mode == "sequence":
                        SequenceMode()
                    elif launcher.mode == "randomized sequence":
                        RandomizedSequenceMode()
                    elif launcher.mode == "gamemode":
                        GameMode()    
                        
                    time.sleep(1)
                    print("J. A. R. V. I.S.: Awaiting your call")

    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()


main()
