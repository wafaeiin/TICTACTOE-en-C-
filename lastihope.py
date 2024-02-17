from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import QSize
import random


class Ui_MainWindow(object):
    def __init__(self):
        self.playerFlag = 0  # who's turn
        self.marks = ['O', 'X']
        self.playerX = 0
        self.PlayerO = 0
        self.winningLineColor = (141, 235, 152)  # color for win line
        self.drawColor = (163, 163, 163)  # color for a draw
        self.board = [' ' for _ in range(9)]  # board for minimax algorithm

    def computerMove(self):  # for finding best position
        bestScore = float('-inf')
        pos = 0
        moves = []  # for storing all better moves
        for i in range(len(self.board)):
            if self.board[i] == " ":  # if only it is empty
                self.board[i] = 'O'
                score = self.minimax(False)
                # reset it back to empty so it doesn't mess up everything
                self.board[i] = ' '
                if bestScore <= score:
                    bestScore = score
                    pos = i
                    moves.append((pos, bestScore))

        # first we pick all moves with bestScore
        # then we choose random option to make this game more entertaining
        return random.choice([move for move, score in moves if score == bestScore])

    def minimax(self, isMaximizing):  # function for calculating best possible moves
        result = self.checkGameOver()
        if result == 'X':
            return -1
        elif result == 'O':
            return 1
        elif result == 'Tie':
            return 0

        # else result == '':
        if isMaximizing:  # if this is true then it is computer's move
            bestScore = float('-inf')
            for i in range(len(self.board)):
                if self.board[i] == " ":
                    self.board[i] = 'O'
                    score = self.minimax(False)
                    # if we don't reset it back it isn't going to backtrack properly
                    self.board[i] = ' '
                    bestScore = max(bestScore, score)
        else:  # Minimizing
            bestScore = float('inf')
            for i in range(len(self.board)):
                if self.board[i] == " ":
                    self.board[i] = 'X'
                    score = self.minimax(True)
                    self.board[i] = ' '  # same here
                    bestScore = min(bestScore, score)

        return bestScore  # bestScore can either be 1, -1, 0

    def btnClk(self, btn):  # On Button Click
        mark = ''  # current player

        # switch between X and O so they are assigned easily
        # we do this so that every new game is started by different player
        if self.playerFlag == 0:
            self.marks[0], self.marks[1] = self.marks[1], self.marks[0]

        # Check Who's Turn it is
        if self.playerFlag % 2 == 0:
            mark = self.marks[0]
        else:
            mark = self.marks[1]

        # Change color by player's turn
        if mark == 'X':
            self.oScore.setStyleSheet(
                "color: red")
            self.xScore.setStyleSheet(
                "color: black")
        else:
            self.xScore.setStyleSheet(
                "color: red")
            self.oScore.setStyleSheet(
                "color: black")

        # this condition is handy after reset is called second time in computer game
        # btn == 10 gurantees that it is called from gameReset Function (so we didn't press any button)
        # if it is first move against computer, it's player's move and btn is 10(no button)
        if not self.playerFlag and mark == 'X' and btn == 10 and not self.friend:
            # we simply return but before that we have to revert changes we made to self.marks earlier in this function
            self.marks[0], self.marks[1] = self.marks[1], self.marks[0]
            return

        # not (if we are playing against computer, while is it a first move and mask='O' - it is computer's move)
        if not(not self.playerFlag and mark == 'O' and not self.friend):
            self.buttons[btn-1].setText(mark)
            self.buttons[btn-1].setDisabled(True)
            self.board[btn-1] = mark
            self.playerFlag += 1

        # Check if anyone won Everytime Button is Clicked
        result = self.checkGameOver(True)
        if result != '':  # gameover
            self.finishGame(result)

        # after every move Computer is going to do its move here
        elif not self.friend:
            # make computer wait some time
            if btn == 10:
                # reason i have only 1 ms here is that this is the first move computer makes
                # which takes a lot of time anyway
                # setting it to 1 makes it automatically go to next frame and then start calculation
                QtTest.QTest.qWait(1)
            else:
                QtTest.QTest.qWait(700)  # msecs

            # set computer's move
            pos = self.computerMove()
            self.board[pos] = 'O'
            button = self.buttons[pos]
            button.setText("O")
            button.setDisabled(True)
            self.playerFlag += 1

            # Chech again after computer made its move
            result = self.checkGameOver(True)
            if result != '':  # gameover
                self.finishGame(result)

    def checkGameOver(self, color=False):  # Check if Game is Over
        # color=False - so that when minimax calls it, self.winningLine doesn't change unnecessarily
        def checkLine(b1, b2, b3):  # reuse and simplify checking
            if self.board[b1-1] == self.board[b2-1] == self.board[b3-1] and self.board[b1-1] != " ":
                return True
            return False

        winner = ''

        # Horizontal Lines
        for i in range(1, 10, 3):
            if checkLine(i, i+1, i+2):
                if color:
                    self.winningLine = (i, i+1, i+2)
                return self.board[i-1]

        # Vertical Lines
        for i in range(1, 4):
            if checkLine(i, i+3, i+6):
                if color:
                    self.winningLine = (i, i+3, i+6)
                return self.board[i-1]

        # Diagonal Lines
        if checkLine(1, 5, 9):
            if color:
                self.winningLine = (1, 5, 9)
            return self.board[0]
        elif checkLine(3, 5, 7):
            if color:
                self.winningLine = (3, 5, 7)
            return self.board[2]

        # Draw
        elif self.board.count(' ') == 0:
            return 'Tie'

        return winner  # returns ''

    def finishGame(self, winner):  # takes care of coloring and labeling
        if winner == 'X':  # if X wins
            self.playerX += 1
            self.xScore.setText('Player X: ' + str(self.playerX))
            self.winner.setText(self.xWinLabel)
        elif winner == 'O':  # if O wins
            self.PlayerO += 1
            self.oScore.setText(self.oLabel + str(self.PlayerO))
            self.winner.setText(self.oWinLabel)
        else:  # Draw
            self.winner.setText("Draw!")
            # Change color If Draw
            for button in self.buttons:
                button.setStyleSheet(
                    f"background-color:rgb({str(self.drawColor[0])},{str(self.drawColor[1])},{str(self.drawColor[2])})")

        # disable all the buttons
        for button in self.buttons:
            button.setEnabled(False)

        # Change color of a winning line
        if winner != 'Tie':
            self.changeColor(
                self.winningLine[0], self.winningLine[1], self.winningLine[2])

    def gameReset(self):  # Start Game Over
        for button in self.buttons:
            button.setDisabled(False)
            button.setText("")
            button.setStyleSheet('background-color: None')
            self.board = [' ' for _ in range(9)]  # reset board

        self.winner.setText("")
        self.playerFlag = 0

        # to reset shortcuts (idk why)
        self.addShortcuts()

        # if it is against computer pass in 10 since is doesn't map to any button
        if not self.friend:
            self.btnClk(10)

    def addShortcuts(self):  # assign shortcuts to the keys
        _translate = QtCore.QCoreApplication.translate

        # easily map to proper buttons
        buttonsToKeys = [0, 7, 8, 9, 4, 5, 6, 1, 2, 3]
        for i, button in enumerate(self.buttons):
            button.setShortcut(_translate(
                "MainWindow", f"{buttonsToKeys[i+1]}"))

    def changeColor(self, b1, b2, b3):  # Change Color of a Winning Line
        self.buttons[b1-1].setStyleSheet(
            f"background-color:rgb({str(self.winningLineColor[0])},{str(self.winningLineColor[1])},{str(self.winningLineColor[2])})")
        self.buttons[b2-1].setStyleSheet(
            f"background-color:rgb({str(self.winningLineColor[0])},{str(self.winningLineColor[1])},{str(self.winningLineColor[2])})")
        self.buttons[b3-1].setStyleSheet(
            f"background-color:rgb({str(self.winningLineColor[0])},{str(self.winningLineColor[1])},{str(self.winningLineColor[2])})")

    def startup(self, MainWindow):  # first window that shows up

        # MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        background_pixmap = QPixmap("menu.jpg")

        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, 800, 600))  # Adjust the dimensions as needed
        self.background_label.setPixmap(background_pixmap)
        self.background_label.setObjectName("background_label")

        # Font
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)

        # Friend Button
        self.friend = QtWidgets.QPushButton(self.centralwidget)
        self.friend.setGeometry(QtCore.QRect(60, 210, 121, 81))
        self.friend.setFont(font)
        self.friend.setText("Friend")
        self.friend.setObjectName("friend")
        # this calls another "main" window
        self.friend.clicked.connect(lambda: self.setupUi(MainWindow, True))

        # Computer Button
        self.computer = QtWidgets.QPushButton(self.centralwidget)
        self.computer.setGeometry(QtCore.QRect(230, 210, 121, 81))
        self.computer.setFont(font)
        self.computer.setText("Computer")
        self.computer.setObjectName("computer")
        self.computer.clicked.connect(lambda: self.setupUi(MainWindow, False))


        # Main Setup
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 404, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Add Shortcuts
        _translate = QtCore.QCoreApplication.translate
        self.friend.setShortcut(_translate("MainWindow", "1"))
        self.computer.setShortcut(_translate("MainWindow", "2"))
        
        # Load and display the background image
        

    def setupUi(self, MainWindow, friend):  # Main Window

        # MainWindow Settings
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setFixedSize(800, 600)
        
        
        # custumize to play computer or 2 player
        self.friend = friend
        if self.friend:
            self.oLabel = 'Player O: '  # only for O because computer is always O
            self.xWinLabel = 'X won!'
            self.oWinLabel = 'O won!'
        else:
            self.oLabel = 'Computer: '
            self.xWinLabel = 'Player won!'
            self.oWinLabel = 'Computer won!'
        
        
        # Main Grid
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        if self.friend:
            background_pixmap = QPixmap("easy.bmp")
        else:
            background_pixmap = QPixmap("menu.jpg")

        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, 800, 600))  # Adjust the dimensions as needed
        self.background_label.setPixmap(background_pixmap)
        self.background_label.setObjectName("background_label")
        
        # Create a Back button with a picture
        back_button = QToolButton(self.centralwidget)
        back_button.setIcon(QIcon("back_icon.jpg"))  # Provide the path to your icon/image
        back_button.setIconSize(QSize(100, 100))  # Set the size of the icon
        back_button.setGeometry(10, 10, 100, 100)  # Set the position and size of the button
        back_button.clicked.connect(lambda: self.startup(MainWindow))  # Connect the button click event to a function

        
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 30, 301, 283))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        

        # Button 1
        self.pB1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB1.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB1.setFont(font)
        self.pB1.setObjectName("pB1")
        self.gridLayout.addWidget(self.pB1, 0, 0, 1, 1)
        self.pB1.clicked.connect(lambda: self.btnClk(1))

        # Button 2
        self.pB2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB2.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB2.setFont(font)
        self.pB2.setObjectName("pB2")
        self.gridLayout.addWidget(self.pB2, 0, 1, 1, 1)
        self.pB2.clicked.connect(lambda: self.btnClk(2))

        # Button 3
        self.pB3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB3.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB3.setFont(font)
        self.pB3.setObjectName("pB3")
        self.gridLayout.addWidget(self.pB3, 0, 2, 1, 1)
        self.pB3.clicked.connect(lambda: self.btnClk(3))

        # Button 4
        self.pB4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB4.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB4.setFont(font)
        self.pB4.setObjectName("pB4")
        self.gridLayout.addWidget(self.pB4, 1, 0, 1, 1)
        self.pB4.clicked.connect(lambda: self.btnClk(4))

        # Button 5
        self.pB5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB5.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB5.setFont(font)
        self.pB5.setObjectName("pB5")
        self.gridLayout.addWidget(self.pB5, 1, 1, 1, 1)
        self.pB5.clicked.connect(lambda: self.btnClk(5))

        # Button 6
        self.pB6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB6.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB6.setFont(font)
        self.pB6.setObjectName("pB6")
        self.gridLayout.addWidget(self.pB6, 1, 2, 1, 1)
        self.pB6.clicked.connect(lambda: self.btnClk(6))

        # Button 7
        self.pB7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB7.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB7.setFont(font)
        self.pB7.setObjectName("pB7")
        self.gridLayout.addWidget(self.pB7, 2, 0, 1, 1)
        self.pB7.clicked.connect(lambda: self.btnClk(7))

        # Button 8
        self.pB8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB8.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB8.setFont(font)
        self.pB8.setObjectName("pB8")
        self.gridLayout.addWidget(self.pB8, 2, 1, 1, 1)
        self.pB8.clicked.connect(lambda: self.btnClk(8))

        # Button 9
        self.pB9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pB9.setMinimumSize(QtCore.QSize(93, 93))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.pB9.setFont(font)
        self.pB9.setObjectName("pB9")
        self.gridLayout.addWidget(self.pB9, 2, 2, 1, 1)
        self.pB9.clicked.connect(lambda: self.btnClk(9))

        # Reset Button
        self.resB = QtWidgets.QPushButton(self.centralwidget)
        self.resB.setGeometry(QtCore.QRect(150, 380, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        self.resB.setFont(font)
        self.resB.setObjectName("resB")
        self.resB.clicked.connect(self.gameReset)

        # Winner Text
        self.winner = QtWidgets.QLabel(self.centralwidget)
        self.winner.setGeometry(QtCore.QRect(140, 315, 130, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        self.winner.setFont(font)
        self.winner.setObjectName("winner")
        self.winner.setAlignment(QtCore.Qt.AlignCenter)

        # X Score
        self.xScore = QtWidgets.QLabel(self.centralwidget)
        self.xScore.setGeometry(QtCore.QRect(50, 380, 111, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        self.xScore.setFont(font)
        self.xScore.setObjectName("xScore")
        self.xScore.setStyleSheet(
            "color: blue")

        # O score
        self.oScore = QtWidgets.QLabel(self.centralwidget)
        self.oScore.setGeometry(QtCore.QRect(260, 380, 111, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        self.oScore.setFont(font)
        self.oScore.setObjectName("oScore")

        # Others
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 404, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.buttons = [self.pB1, self.pB2, self.pB3, self.pB4,
                        self.pB5, self.pB6, self.pB7, self.pB8, self.pB9]

        self.addShortcuts()
        
        self.retranslateUi(MainWindow)
        
    

    def retranslateUi(self, MainWindow):
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MORPION"))
        self.resB.setText(_translate("MainWindow", "Reset"))
        self.resB.setShortcut(_translate("MainWindow", "Enter"))
        self.xScore.setText(_translate("MainWindow", "Player X: 0"))
        self.oScore.setText(_translate("MainWindow", self.oLabel+"0"))
        



if __name__ == "__main__":
    import sys

    # Create a Window
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.startup(MainWindow)
    MainWindow.setWindowTitle("Tic Tac Toe")
    MainWindow.show()  # this shows the startup windows

    # To Exit
    sys.exit(app.exec())