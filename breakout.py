#モジュールをインポート
import tkinter
import datetime
import time
import random

#フォント
FNT= ("Times New Roman",20, "bold")

#キー入力の値
key = ""
keyoff= False

#処理する内容の指定番号(0:準備,1:動作,2:ゲームオーバー,3:ラウンドクリア)
idx = 0

#処理する内容の時間指定
tmr = 0

#ラウンド数,スコア
round_cnt = 0
score = 0

#バーの位置
bar_x = 0
bar_y = 0

#バーの位置
ball_x = 0
ball_y = 0

#ポールの動くpxの初期値
ball_xp = 0
ball_yp = 0

#タイマー
start_time = 0
now_time = 0
play_time = 0

#ミスカウント
miss_count = 0

#クリア判別(クリアならTrue)
is_clr = True

#ブロックの処理
block = []
for i in range(5):
    block.append([1]*10)    #ブロックを置きたい場所に1を代入
for i in range(10):
    block.append([0]*10)    #空白にしたい場所に0を代入

#ポールの動くpx(round_cntと連動)
speed = [0,15,20,25,25]

#現在のスピード
now_speed = 0

#キー操作をしている時の関数
def key_down(e):
    global key
    key = e.keysym
    move_bar()  # キーが押されたときにバーを移動させる

# キー操作をしていない時の関数
def key_up(e):
    global key
    if key == "":
        keyoff = True
    key = ""

#ブロックの色を指定する関数
def block_color(x, y): # format()命令で16進数の値に変換できる
    col = "#{0:x}{1:x}{2:x}".format(15-x-int(y/3), x+1, y*3+3)
    return col

#ブロックを描く関数
def draw_block():
    global is_clr
    is_clr = True
    cvs.delete("BG")
    for y in range(5):
        for x in range(10):
            gx = x * 80
            gy = y * 40
            if block[y][x] == 1:
                col = block_color(x, y)
                cvs.create_rectangle(gx+1, gy+4, gx+79, gy+32, fill=col, width=0, tag="BG")
                is_clr = False

#バーを描く関数
def draw_bar():
    cvs.delete("BAR")
    cvs.create_rectangle(bar_x-80, bar_y-12, bar_x+80, bar_y+12, fill="silver", width=0, tag="BAR")
    cvs.create_rectangle(bar_x-78, bar_y-14, bar_x+78, bar_y+14, fill="silver", width=0, tag="BAR")
    cvs.create_rectangle(bar_x-78, bar_y-12, bar_x+78, bar_y+12, fill="white", width=0, tag="BAR")

# バーを動かす関数
def move_bar():
    global bar_x
    root.focus_force()
    # キー操作時のバーの処理
    if key == "Left" and bar_x > 80:
        bar_x = bar_x - 40
    if key == "Right" and bar_x < 720:
        bar_x = bar_x + 40

    # キー操作時のバーの処理
    mouse_x = root.winfo_pointerx() - root.winfo_rootx()
    mouse_y = root.winfo_pointery() - root.winfo_rooty()
    if 80 < mouse_x < 720 and 0 < mouse_y < 600:
        bar_x = mouse_x


#ボールを描く関数
def draw_ball():
    cvs.delete("BALL")
    if now_speed >= 20:
        cvs.create_oval(ball_x-20, ball_y-20, ball_x+20, ball_y+20, fill="red", outline="gray", width=2, tag="BALL")
    else:
        cvs.create_oval(ball_x-20, ball_y-20, ball_x+20, ball_y+20, fill="gold", outline="orange", width=2, tag="BALL")
        cvs.create_oval(ball_x-16, ball_y-16, ball_x+12, ball_y+12, fill="yellow", width=0, tag="BALL")

#ボールを動かす関数
def move_ball():
    global idx, tmr, score, ball_x, ball_y, ball_xp, ball_yp, round_cnt

    ball_x = ball_x + ball_xp   #ボールのx座標を変える処理
    if ball_x < 20:     #左側にボールがめり込まないようにする
        ball_x = 20
        ball_xp = -ball_xp
    if ball_x > 780:    #右側にボールがめり込まないようにする
        ball_x = 780
        ball_xp = -ball_xp
    x = int(ball_x/80)  #現在のボールのx座標と配列blockのx座標のリンク
    y = int(ball_y/40)  #現在のボールのy座標と配列blockのy座標のリンク
    if block[y][x] == 1:        #ブロックの置き換え処理
        block[y][x] = 0
        ball_xp = -ball_xp      #ボールを反対側に弾く処理
        score = score + 10      #スコア加算

    ball_y = ball_y + ball_yp   #ボールのy座標を変える処理
    if ball_y >= 600:   #ゲームオーバー処理の準備
        idx = 2
        tmr = 0
        return
    if ball_y < 20:     #上側にボールがめり込まないようにする
        ball_y = 20
        ball_yp = -ball_yp
    x = int(ball_x/80)  #現在のボールのx座標と配列blockのx座標のリンク
    y = int(ball_y/40)	#現在のボールのx座標と配列blockのy座標のリンク
    if block[y][x] == 1: #ブロックの置き換え処理 
        block[y][x] = 0
        ball_yp = -ball_yp      #ボールを反対側に弾く処理
        score = score + 10      #スコア加算

    if bar_y-50 <= ball_y and ball_y <= bar_y:
        if bar_x-80 <= ball_x and ball_x <= bar_x+80:
            ball_yp = -speed[int(round_cnt)]
            score = score + 1
        elif bar_x-100 <= ball_x and ball_x <= bar_x-80:
            ball_yp = -speed[int(round_cnt)]
            ball_xp = random.randint(-25, -15)
            score = score + 1
        elif bar_x+80 <= ball_x and ball_x <= bar_x+100:
            ball_yp = -speed[int(round_cnt)]
            ball_xp = random.randint(15, 25)
            score = score + 1
    draw_ball()

#障害物を生成する関数
def jam_screen():
    #壁の作成
    cvs.create_rectangle(0, 235, 800, 238, fill="white", width=0, tag="BAR")
    cvs.create_rectangle(0, 238, 800, 418, fill="black", width=0, tag="BAR")
    cvs.create_rectangle(0, 418, 800, 421, fill="white", width=0, tag="BAR")

    #文字の配置
    cvs.create_text(180, 320, text="壁", fill="white", font=FNT, tag="BG")
    cvs.create_text(610, 320, text="壁", fill="white", font=FNT, tag="BG")

#プレイ詳細を記載する関数
def show_detail():
    global now_speed
    #背景
    cvs.create_rectangle(800, 0, 1010, 610, fill="silver", width=0, tag="BG")

    #ラウンド数
    cvs.create_rectangle(810, 10, 990, 70, fill="white", width=0, tag="BAR")
    cvs.create_text(900, 40, text="ROUND:"+str(round_cnt)+" / 4", fill="black", font=FNT, tag="BG")

    #タイマー
    now_time = datetime.datetime.now()
    play_time = now_time - start_time
    cvs.create_rectangle(810, 100, 990, 160, fill="white", width=0, tag="BAR")
    cvs.create_text(900, 130, text="TIME:"+ str(play_time.seconds) + "s", fill="black", font=FNT, tag="TXT")

    #スコア
    cvs.create_rectangle(810, 190, 990, 250, fill="white", width=0, tag="BAR")
    cvs.create_text(900, 220, text="SCORE:"+str(score), fill="black", font=FNT, tag="BG")

    #ミス回数
    cvs.create_rectangle(810, 290, 990, 350, fill="white", width=0, tag="BAR")
    cvs.create_text(900, 320, text="MISS:" + str(miss_count), fill="black", font=FNT, tag="BG")

    #ボールのスピード
    cvs.create_rectangle(810, 390, 990, 450, fill="white", width=0, tag="BAR")
    now_speed = (abs(ball_xp) + abs(ball_yp))/2
    if now_speed >= 20:
        speed_text = "SPEED:{:.1f}".format(now_speed)
        cvs.create_text(900, 420, text=speed_text, fill="RED", font=FNT, tag="BG")
    else:
        speed_text = "SPEED:{:.1f}".format(now_speed)
        cvs.create_text(900, 420, text=speed_text, fill="black", font=FNT, tag="BG")

    #解説
    cvs.create_rectangle(810, 490, 990, 580, fill="white", width=0, tag="BAR")
    cvs.create_text(900, 530, text="マウスor\n←→で移動", fill="black", font=FNT, tag="BG")

#メイン関数
def main_proc():
    global key, keyoff, flag
    global idx, tmr, round_cnt, score, start_time, now_time, play_time, miss_count
    global bar_x, bar_y, ball_x, ball_y, ball_xp, ball_yp
#==============================準備処理==============================
    if idx == 0:
        tmr = tmr + 1
        show_detail()
        if tmr == 1:
            round_cnt = 1
            score = 0
        if tmr == 2:
            bar_x = 400
            bar_y = 540
            ball_x = 400
            ball_y = 240
            ball_xp = 15
            ball_yp = 15
            draw_block()
            draw_ball()
            draw_bar()
            show_detail()
            if round_cnt == 4:
                jam_screen()
            cvs.create_text(400, 300, text="START", fill="cyan", font=FNT, tag="TXT")
        if tmr == 30:
            cvs.delete("TXT")
            idx = 1
#==============================準備処理==============================

#==============================動作処理==============================
    elif idx == 1:
        move_ball()
        move_bar()
        draw_block()
        draw_ball()
        draw_bar()
        show_detail()
        if round_cnt == 4:
            jam_screen()
        if is_clr:      #ゲームクリア処理をするための準備
            idx = 3
            tmr = 0
#==============================動作処理==============================
            
#=========================ゲームオーバー処理=========================
    elif idx == 2:
        tmr = tmr + 1
        show_detail()
        if tmr == 1:
            miss_count += 1
            cvs.create_text(400, 250, text="GAME OVER", fill="red", font=FNT, tag="TXT")
        if tmr == 30:
            cvs.create_text(300, 300, text="Replay [SPACE]", fill="yellow", font=FNT, tag="TXT")
            cvs.create_text(500, 300, text="Exit [ENTER]", fill="red", font=FNT, tag="TXT")
        if key == "space":      #リトライ処理
            cvs.delete("TXT")
            idx = 0
            tmr = 1
            ball_xp = 14
            ball_yp = 14
        if key == "Return":     #ゲーム終了処理
            if root.winfo_exists():
                root.destroy()
#=========================ゲームオーバー処理=========================

#==========================ゲームクリア処理==========================
    elif idx == 3:
        tmr = tmr + 1
        show_detail()
        if round_cnt != 4:      #ラウンド1～3の時の処理
            if tmr == 1:
                cvs.create_text(400, 250, text="ROUND CLEAR", fill="lime", font=FNT, tag="TXT")
            if tmr == 30:
                cvs.create_text(300, 300, text="NEXT [SPACE]", fill="yellow", font=FNT, tag="TXT")
                cvs.create_text(500, 300, text="Exit [ENTER]", fill="red", font=FNT, tag="TXT")
            if key == "space":  #次のラウンドに進む処理
                cvs.delete("TXT")
                for y in range(5):
                    for x in range(10):
                        block[y][x] = 1
                idx = 0
                tmr = 1
                round_cnt = round_cnt + 1
            if key == "Return": #ゲーム終了処理
                if root.winfo_exists():
                    root.destroy()
                
        else:   #ラウンド4の時の処理
            now_time = datetime.datetime.now()
            play_time = now_time - start_time
            if tmr == 1:
                cvs.create_text(400, 250, text="GAME CLEAR", fill="lime", font=FNT, tag="TXT")
                cvs.create_text(200, 300, text="TIME:"+str(play_time.seconds) + "s", fill="white", font=FNT, tag="BG")
                cvs.create_text(400, 300, text="SCORE:"+str(score), fill="white", font=FNT, tag="BG")
                cvs.create_text(600, 300, text="MISS:" + str(miss_count), fill="white", font=FNT, tag="TXT")
            if tmr == 30:
                cvs.create_text(400, 350, text="Exit [ENTER]", fill="yellow", font=FNT, tag="TXT")
            if key == "Return": #ゲーム終了処理
                if root.winfo_exists():
                    root.destroy()
#==========================ゲームクリア処理==========================

#============================キー入力処理============================
    if keyoff == True:
        keyoff = False
        if key != "":
            key = ""
#============================キー入力処理============================
    root.after(50, main_proc)   #繰り返し処理

#キャンバスの設定
root = tkinter.Tk()
root.title("ブロック崩し")
root.resizable(False, False)
root.bind_all("<Key>", key_down)
root.bind_all("<KeyRelease>", key_up)
cvs = tkinter.Canvas(root, width=1000, height=600, bg="black")
start_time = datetime.datetime.now()
cvs.pack()
main_proc()
root.mainloop()
