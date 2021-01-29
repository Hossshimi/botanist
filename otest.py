import numpy as np

white = 1
black = -1
blank = 0
tablesize = 8

class Board(object):
    # 初期設定
    def __init__(self):
        self.cell = np.zeros((tablesize,tablesize))
        self.cell = self.cell.astype(int)
        self.cell[3][3] = self.cell[4][4] = 1
        self.cell[3][4] = self.cell[4][3] = -1
        self.current = black
        self.pass_count = 0
        self.turn = 1

    def turnchange(self):  #  ＊
        self.current*= -1
    def stonenumber(self):
        return self.stones

    def rangecheck(self,x,y):  # ①　盤内かどうか　
        if x == None: x = -1
        if y == None: y = -1
        if x < 0 or tablesize <=x  or y < 0 or tablesize <= y:
            return False
        return True

    def check_can_reverse(self,x,y):  # 置けるかどうか
        if not self.rangecheck(x,y):   # →　①へ
            return False
        elif not self.cell[x][y] == blank:   #  ②
            return False
        elif not self.can_reverse_stone(x,y):   # →　③へ
            return False
        else: return True

    def can_reverse_one(self,x,y,dx,dy):  # ⑶、⑷　　(dx,dy)方向に敵石があり、その先に自石があるかどうか

        if not self.rangecheck(x+dx,y+dy):
            return False
            length = 0
            if not self.cell[x + dx][y + dy] == -self.current: #  ⑶
                return False # (dx,dy)方向が敵石じゃない時False
            else:    
                while self.cell[x+dx][y+dy] == -self.current: 
                    x +=dx
                    y +=dy
                    length += 1
                    if self.cell[x+dx][y+dy] == self.current:  # ⑷-True
                        return length
                    elif not self.cell[x+dx][y+dy] == -self.current:
                        continue
                    else: return False
                else: return False  # ⑷-False

    def can_reverse_stone(self,x,y):  # 　③入力座標ではひっくり返せる石はあるか
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == dy == 0: continue   # ⑴
                elif not self.rangecheck(x+dx,y+dy): continue  # ①（調べた範囲が番外だったらエラーが起こるため）
                elif not self.can_reverse_one(x,y,dx,dy):  # →　⑶、⑷の処理へ
                    continue
                else: return True

    def reverse_stone(self,x,y): #  ④ 座標に石を置いて石をひっくり返す
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    length = self.can_reverse_one(x,y,dx,dy)
                    if length == None: length = 0
                    if length > 0:
                        for l in range(length):
                            k = l+1
                            self.cell[x + dx*k][y + dy*k] *= -1

    def display(self):  # 盤面の状況を表示
        print('==='*10)   #  *(下の文を参照）
        for y in range(tablesize):
            for x in range(tablesize):
                if self.cell[x][y] == white:
                    print('W', end = '  ')
                elif self.cell[x][y] == black:
                    print('B', end = '  ')
                else:
                    print('*', end = '  ')
            print('\n', end = '')

    def put_stone(self,x,y):  # 一回のターン内の行動 
        if self.check_can_reverse(x,y):   # 入力座標に石を置ける
            self.pass_count = 0
            self.cell[x][y] = self.current
            self.reverse_stone(x,y)
            self.turnchange()
            return True
        else:  # 入力座標に石を置けない
            return False

    def check_put_place(self):  # ❶盤面上に石が置ける場所があるか　次のクラスの時に使用
        for i in range(tablesize):
            for j in range(tablesize):
                if self.check_can_reverse(i,j): # (i,j)座標に置いて石が置けたら成立
                    return True
                else:continue
        return False

import sys

class Game(Board):
    def __init__(self):
        self.white_count = 2
        self.black_scount = 2
        self.blank_count = 60

    # パスをする関数。一度パスするとpass_countが１増える
    # pass_count　== 2になるとゲームセット関数に飛ぶ
    def pass_system(self):  #  ②
        board.pass_count += 1
        board.turnchange()
        #if board.pass_count ==2:  # 連続二回パスしたので③のゲームを終わらせる関数へ移動
        #    self.gameset()
        return True

    def gameset(self): #  ③ ゲーム終了、石の数をカウントし勝敗を表示
        print('game set')
        self.count_system()
        print('white : ', self.white_count)
        print('black : ', self.black_count)
        if self.white_count > self.black_count:
            print('white WIN !!')
        if self.white_count < self.black_count:
            print('Black WIN !!')
        if self.white_count == self.black_count:
            print('Draw')
        sys.exit()


    def count_system(self):  #  ⑤ 石のカウントシステム
        self.white_count = np.sum(board.cell == white)
        self.black_count = np.sum(board.cell == black)
        self.blank_count = np.sum(board.cell == blank)

    def input_point(self):    #  ① 座標を入力
        print('石を置く座標を(1~8で)入力してください。(x,y)=(9,9)でpass、(0,0)で終了します。')
        x = input('x>>')
        y = input('y>>')
        try:
            x = int(x)-1
            y = int(y)-1
        except:
            self.input_point()
        return x, y


    def one_turn_play(self):  # ①〜⑤と❶をまとめる（❶に関しては上に記述）　
        if board.check_put_place():  #  ❶ 盤面に石が置ける場所があるかどうか
            (x,y) = self.input_point()   #  ① 座標を入力
            board.put_stone(x,y)  # Boardクラスで作ったやつ。石をおいてひっ繰り返してTrueを返すか、何もせずFalseを返す
            if not board.put_stone(x,y):
                    if (x,y) == (8,8):       #  ② パスするとき
                        self.pass_system()
                    elif (x,y) == (-1,-1):   #  ③ ゲームをやめる時
                        self.gameset()
                    #石をおけない時は もう一度同じことをする
                    while False:
                        self.one_turn_play()     
        #else:self.pass_system()


    # 最後まで続くようにしてみる   
    def gameplay(self):
        while self.blank_count >0:
            board.display()            #　盤面を出力
            print('-----'*10)
            board.turn += 1
            print('turn : ', board.turn, end = '  ')
            if board.current == -1:
                print(', turn black')
            elif board.current == 1:
                print(', turn white')
            self.one_turn_play()   # ターンでの行動
            self.count_system()   # 石とblankの数を出す
            print('white : ', self.white_count, ', black : ', self.black_count, ', blank : ', self.blank_count)
            print('pass_count : ',board.pass_count)
        self.gameset()

if __name__ == '__main__':
    board = Board()
    game = Game()
    game.gameplay()