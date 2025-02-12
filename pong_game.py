import tkinter as tk
import tkinter.ttk as ttk
import random
import threading
import serial
import time

# Constants
WIDTH, HEIGHT = 1280, 800
BALL_SPEED = 3
PADDLE_SPEED = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 160
BALL_SIZE=20
BALL_COLOR=0

# Arduino Connection
arduino = serial.Serial('COM8', 9600, timeout=1)  
time.sleep(2)

# Game variables
slow_l, slow_r,con_l,con_r = 1,1,1,1
left_paddle_speed, right_paddle_speed = 0, 0
pause = True
game_time = 0
stop_thread = threading.Event()

# Score and Power-up variables
left_score, right_score = 0, 0
power_1, power_2 = 0, 0
can_use_power_R, can_use_power_L = True, True

# Power-up effects
def slow_enemy(paddle):
    global can_use_power_R,can_use_power_L,power_1,power_2,slow_l,slow_r
    if paddle=="L":
        can_use_power_L=False
        slow_r=3
        threading.Timer(5, lambda: stop_slow(paddle)).start()
        threading.Timer(10, lambda: reset_cooldown(paddle)).start()
    else:
        can_use_power_R=False
        slow_l=3
        threading.Timer(5, lambda: stop_slow(paddle)).start()
        threading.Timer(10, lambda: reset_cooldown(paddle)).start()
def stop_slow(paddle):
    global slow_l,slow_r
    if paddle=="L":
        slow_r=1
    else:
        slow_l=1

def confuse_enemy(paddle):
    global can_use_power_R,can_use_power_L,power_1,power_2,con_r,con_l
    if paddle=="L":
        can_use_power_L=False
        con_r=-1
        threading.Timer(5, lambda: stop_confuse(paddle)).start()
        threading.Timer(10, lambda: reset_cooldown(paddle)).start()
    else:
        can_use_power_R=False
        con_l=-1
        threading.Timer(5, lambda: stop_confuse(paddle)).start()
        threading.Timer(10, lambda: reset_cooldown(paddle)).start()
def stop_confuse(paddle):
    global con_r,con_l
    if paddle=="L":
        con_r=1
    else:
        con_l=1

def enlarge_paddle(paddle):
    global can_use_power_R,can_use_power_L,power_1,power_2
    if paddle == "L":
        can_use_power_L=False
        x1, y1, x2, y2 = canvas.coords(left_paddle)
        canvas.coords(left_paddle, x1, y1 - 40, x2, y2 + 40)  # Expand equally up & down
        threading.Timer(5, lambda: reset_paddle(paddle)).start()
        threading.Timer(10, lambda: reset_cooldown(paddle)).start()

    elif paddle == "R":
        can_use_power_R=False
        print("right up")
        x1, y1, x2, y2 = canvas.coords(right_paddle)
        canvas.coords(right_paddle, x1, y1 - 40, x2, y2 + 40)  # Expand equally up & down
        threading.Timer(5, lambda: reset_paddle(paddle)).start()
        threading.Timer(10, lambda: reset_cooldown(paddle)).start()

def reset_cooldown(paddle):
    global can_use_power_R,can_use_power_L
    if paddle=="R":
        can_use_power_R = True  # Enable power again
    else:
        can_use_power_L = True  # Enable power again
        
def reset_paddle(paddle):
    """Reset the paddle to its original size at the current position."""
    global can_use_power_L, can_use_power_R

    if paddle == "L":
        x1, y1, x2, y2 = canvas.coords(left_paddle)
        paddle_center = (y1 + y2) // 2
        canvas.coords(left_paddle, x1, paddle_center - PADDLE_HEIGHT // 2, x2, paddle_center + PADDLE_HEIGHT // 2)


    elif paddle == "R":
        x1, y1, x2, y2 = canvas.coords(right_paddle)
        paddle_center = (y1 + y2) // 2
        canvas.coords(right_paddle, x1, paddle_center - PADDLE_HEIGHT // 2, x2, paddle_center + PADDLE_HEIGHT // 2)

# Power-up activation        
def power(paddle):
    global can_use_power_R,can_use_power_L,power_1,power_2
    if (can_use_power_R and paddle=="R") or (can_use_power_L and paddle=="L"):
        if paddle=="R":
            if power_2==1:
                enlarge_paddle(paddle)
            elif power_2==2:
                slow_enemy(paddle)
            elif power_1==3:
                confuse_enemy(paddle)
        if paddle=="L":
            if power_1==1:
                enlarge_paddle(paddle)
            elif power_1==2:
                slow_enemy(paddle)
            elif power_1==3:
                confuse_enemy(paddle)

# Get commands from Arduino
def get_arduino_command():
    global left_paddle_speed, right_paddle_speed, pause,power_1,power_2,can_use_power_R,can_use_power_L
    while not stop_thread.is_set():
        if arduino.in_waiting > 0:
            response = arduino.readline().decode('utf-8').rstrip()
            if response:
                if response[0] == "P":
                    print(response)
                    pause = not pause
                elif response == "R":
                    print(can_use_power_R)
                    power("R")
                elif response=="L":
                    print(can_use_power_L)
                    power("L")
                elif response[0]=="C":
                    if response[1]=="N":
                        x=1
                    elif response[1]=="B":
                        print("Blue")
                        p=1
                    elif response[1]=="R":
                        print("Red")
                        p=2
                    elif response[1]=="G":
                        print("Green")
                        p=3
                    if response[2]=="L" and response[1] != "N":
                        power_1=p
                    elif response[1] != "N":
                        power_2=p
                else:
                    move = int(response[1:])
                    temp = 0 if move > 50 else (move - 20 if move >= 20 else -(20 - move))
                    if response[0] == "l":
                        left_paddle_speed = -temp*con_l
                    elif response[0] == "r":
                        right_paddle_speed = -temp*con_r

# Initialize window
root = tk.Tk()
root.title("Pong Game")

# Menu Frame
menu_frame = tk.Frame(root, width=WIDTH, height=HEIGHT, bg="black")
menu_frame.pack_propagate(False)
menu_frame.pack()

title_frame = tk.Frame(menu_frame, bg="black")
title_frame.pack(pady=100)

# Title
title_text = "PONG GAME"
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan", "white"]

# Create labels for each letter
for i, letter in enumerate(title_text):
    if letter == " ":
        tk.Label(title_frame, text=" ", font=("Arial", 72), bg="black").pack(side="left")
    else:
        tk.Label(title_frame, text=letter, font=("Arial", 72), fg=colors[i], bg="black").pack(side="left")

def start_game():
    global game_time
    game_time = 0  # Reset timer
    menu_frame.pack_forget()
    reset_game()
    canvas.pack()
    move_paddles()
    move_ball()
    update_timer()  # Start timer

    if not arduino_thread.is_alive():
        arduino_thread.start()  

def restart_game():
    end_frame.pack_forget()
    reset_game()
    canvas.pack()

def back_to_menu():
    end_frame.pack_forget()
    menu_frame.pack()

#Hover for buttons    
def on_enter(e):
    start_button.config(bg="yellow", fg="blue")  # Change background and text color on hover
    restart_button.config(bg="yellow", fg="blue")  # Change background and text color on hover

def on_leave(e):
    start_button.config(bg="blue", fg="yellow")  # Restore original colors when mouse leaves
    restart_button.config(bg="blue", fg="yellow")  # Restore original colors when mouse leaves

#start button
start_button = tk.Button(menu_frame, text="Start Game", font=("Arial", 64), fg="yellow", bg="blue",activebackground="red", activeforeground="yellow", command=start_game)
start_button.pack(pady=20)

# Bind hover effects
start_button.bind("<Enter>", on_enter)  # Mouse enters button area
start_button.bind("<Leave>", on_leave)  # Mouse leaves button area

# Game Canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")

# End Frame
end_frame = tk.Frame(root, width=WIDTH, height=HEIGHT, bg="black")
end_frame.pack_propagate(False)

score_label = tk.Label(end_frame, text="Player Won", font=("Arial", 64), fg="yellow", bg="black")
score_label.pack(pady=50)


restart_button = tk.Button(end_frame, text="Restart", font=("Arial", 64), fg="yellow", bg="blue",activebackground="red", activeforeground="yellow", command=restart_game)
restart_button.pack(pady=100)

# Hover effects for restart button
restart_button.bind("<Enter>", on_enter)  # Mouse enters button area
restart_button.bind("<Leave>", on_leave)  # Mouse leaves button area

#back_to_menu_button = tk.Button(end_frame, text="Back to Menu", font=("Arial", 16), command=back_to_menu)
#back_to_menu_button.pack(pady=20)

# Create paddles, ball, and score display
left_paddle = canvas.create_rectangle(10, HEIGHT//2 - PADDLE_HEIGHT//2, 10 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2, fill="yellow")
right_paddle = canvas.create_rectangle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, WIDTH - 10, HEIGHT//2 + PADDLE_HEIGHT//2, fill="blue")

ball = canvas.create_oval(WIDTH//2 - BALL_SIZE, HEIGHT//2 - BALL_SIZE, WIDTH//2 + BALL_SIZE, HEIGHT//2 + BALL_SIZE, fill=colors[0])
score_display = canvas.create_text(WIDTH//2, 50, text="0 - 0", font=("Arial", 24), fill="white")
timer_display = canvas.create_text(WIDTH//2, 100, text="Time: 0s", font=("Arial", 24), fill="blue")

# Ball movement variables
ball_dx = BALL_SPEED * random.choice([-1, 1])
ball_dy = BALL_SPEED * random.choice([-1, 1])

# Update game timer
def update_timer():
    global game_time, pause,BALL_SPEED,ball_dx,ball_dy
    if not pause:
        game_time += 1
        if game_time%10==0:
            BALL_SPEED+=0.5
            ball_dx=(abs(ball_dx)/ball_dx)*BALL_SPEED
            ball_dy=(abs(ball_dy)/ball_dy)*BALL_SPEED
        canvas.itemconfig(timer_display, text=f"Time: {game_time}s")
    root.after(1000, update_timer)  # Call again after 1 second

# Update score display
def update_score():
    if left_score>right_score:
        canvas.itemconfig(score_display, text=f"{left_score} - {right_score}",fill="yellow")
    elif left_score<right_score:
        canvas.itemconfig(score_display, text=f"{left_score} - {right_score}",fill="blue")
    else:
        canvas.itemconfig(score_display, text=f"{left_score} - {right_score}",fill="white")
    if left_score == 5 or right_score == 5:
        show_end_frame()

def show_end_frame():
    global left_score, right_score
    canvas.itemconfig(timer_display, text=f"Final Time: {game_time}s")
    winner = "Left Player Won!" if left_score > right_score else "Right Player Won!"
    score_label.config(text=winner)
    canvas.pack_forget()
    end_frame.pack()



def move_paddles():
    global left_paddle_speed, right_paddle_speed, pause
    if not pause:
        left_coords = canvas.coords(left_paddle)
        right_coords = canvas.coords(right_paddle)

        if 0 <= left_coords[1] + left_paddle_speed and left_coords[3] + left_paddle_speed <= HEIGHT:
            canvas.move(left_paddle, 0, left_paddle_speed//slow_l)

        if 0 <= right_coords[1] + right_paddle_speed and right_coords[3] + right_paddle_speed <= HEIGHT:
            canvas.move(right_paddle, 0, right_paddle_speed//slow_r)

    root.after(20, move_paddles)

def move_ball():
    global ball_dx, ball_dy, pause, left_score, right_score, BALL_COLOR

    if not pause:
        canvas.move(ball, ball_dx, ball_dy)
        ball_coords = canvas.coords(ball)
        left_coords = canvas.coords(left_paddle)
        right_coords = canvas.coords(right_paddle)

        if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
            ball_dy = -ball_dy
            canvas.itemconfig(ball, fill=colors[BALL_COLOR % len(colors)])
            BALL_COLOR += 1

        if (ball_coords[0] <= left_coords[2] and left_coords[1] <= ball_coords[1] <= left_coords[3]) or \
           (ball_coords[2] >= right_coords[0] and right_coords[1] <= ball_coords[1] <= right_coords[3]):
            ball_dx = -ball_dx
            # Change the ball's color
            canvas.itemconfig(ball, fill=colors[BALL_COLOR % len(colors)])
            BALL_COLOR += 1

        if ball_coords[0] <= 0:
            right_score += 1
            reset_ball()
        elif ball_coords[2] >= WIDTH:
            left_score += 1
            reset_ball()

        update_score()

    root.after(20, move_ball)

# Reset the ball to the center
def reset_ball():
    global ball_dx, ball_dy,BALL_SPEED
    canvas.coords(ball, WIDTH//2 - BALL_SIZE, HEIGHT//2 - BALL_SIZE, WIDTH//2 + BALL_SIZE, HEIGHT//2 + BALL_SIZE)
    BALL_SPEED=3
    ball_dx = BALL_SPEED * random.choice([-1, 1])
    ball_dy = BALL_SPEED * random.choice([-1, 1])

def reset_game():
    """Reset game state for a new game"""
    global left_score, right_score,game_time
    left_score, right_score,game_time = 0, 0,0
    canvas.itemconfig(score_display, text="0 - 0")
    reset_ball()
    canvas.coords(left_paddle, 10, HEIGHT//2 - PADDLE_HEIGHT//2, 10 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2)
    canvas.coords(right_paddle, WIDTH - 10-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, WIDTH - 10, HEIGHT//2 + PADDLE_HEIGHT//2)

def on_closing():
    stop_thread.set()
    arduino_thread.join()
    root.destroy()
    arduino.close()

root.protocol("WM_DELETE_WINDOW", on_closing)

arduino_thread = threading.Thread(target=get_arduino_command, daemon=True)

root.mainloop()
