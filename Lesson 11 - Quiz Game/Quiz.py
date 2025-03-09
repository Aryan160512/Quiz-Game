import pgzrun

WIDTH = 870
HEIGHT = 650
TITLE = 'Quiz Game'

marqueeBox = Rect(0, 0, 880, 80)
questionBox = Rect(0, 0, 650, 150)
timerBox = Rect(0, 0, 150, 150)

answerBox1 = Rect(0, 0, 300, 150)
answerBox2 = Rect(0, 0, 300, 150)
answerBox3 = Rect(0, 0, 300, 150)
answerBox4 = Rect(0, 0, 300, 150)

skipBox = Rect(0, 0, 150, 330)

answers = [answerBox1, answerBox2, answerBox3, answerBox4]

marqueeBox.move_ip(0, 0)
questionBox.move_ip(20, 100)
timerBox.move_ip(700, 100)

answerBox1.move_ip(20, 270)
answerBox2.move_ip(370, 270)
answerBox3.move_ip(20, 450)
answerBox4.move_ip(370, 450)

skipBox.move_ip(700, 270)

score = 0
timeLeft = 10
marqueeMessage = ''

questions = []
questionIndex = 0
questionCount = 0

question = ''


isGameOver = False

def marquee_message():
    marqueeBox.x -= 2
    if marqueeBox.right < 0:
        marqueeBox.left = WIDTH

def readQuestionFile():
    global questionCount, questions

    #Opening a File in Read Mode
    questionFile = open('Questions.txt', 'r')

    for line in questionFile:
        questions.append(line)
        questionCount += 1

    questionFile.close()
    print(questions)

def readNextQuestion():
    global questionIndex

    questionIndex += 1
    return questions.pop(0).split(',')

def skipQuestion():
    global questions, timeLeft, question

    if questions and not isGameOver:
        question = readNextQuestion()
        timeLeft = 10
    else:
        gameOver()

def updateTimer():
    global timeLeft

    if timeLeft:
        timeLeft -= 1
    else:
        gameOver()

def on_mouse_down(pos):

    index = 1
    for box in answers:
        if box.collidepoint(pos):
            if index is int(question[5]):
               correctAnswer()
            else:
               gameOver()
        index += 1
    if skipBox.collidepoint(pos):
        skipQuestion()
        
def correctAnswer():
    global timeLeft, question, questions, score

    score += 1
    if questions:
        question = readNextQuestion()
        timeLeft = 10
    else:
        gameOver()


def gameOver():
    global question, timeLeft, isGameOver

    isGameOver = True
    timeLeft = 0

    message = f'GAME OVER. YOU GOT {questionIndex} OF {questionCount}'
    question = [message, '-', '-', '-', '-', 5]
        

def update():
    marquee_message()
    
def draw():
    global marqueeMessage

    screen.clear()
    screen.fill('black')

    screen.draw.filled_rect(marqueeBox, 'black')
    screen.draw.filled_rect(questionBox, 'blue')
    screen.draw.filled_rect(timerBox, 'green')
    screen.draw.filled_rect(skipBox, 'yellow')


    for i in answers:
        screen.draw.filled_rect(i, 'red')

    marqueeMessage = f'Welcome to the Quiz Game. You are at {questionIndex} of {questionCount}.'

    screen.draw.textbox(marqueeMessage, marqueeBox, color = 'white')
    screen.draw.textbox('SKIP', skipBox, color = 'black', angle = -90)
    screen.draw.textbox(str(timeLeft), timerBox, color = 'black', shadow = (0.5, 0.5), scolor = 'darkGreen')

    screen.draw.textbox(question[0].strip(), questionBox, color = 'white')

    index = 1
    for box in answers:
        screen.draw.textbox(question[index].strip(), box, color = 'black')
        index += 1

readQuestionFile()
question = readNextQuestion()
clock.schedule_interval(updateTimer, 1)
pgzrun.go()