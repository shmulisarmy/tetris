from random import randint as r, choice as c
import pygame as p 

shapes = [
    [[0, 0], [0, 1], [0, 2], [0, -1]],  # I-Piece
    [[0, 0], [0, 1], [1, 0], [1, 1]],  # O-Piece
    [[0, 1], [1, 0], [1, 1], [1, 2]],  # T-Piece
    [[0, -1], [1, -1], [1, 0], [1, 1]],  # L-Piece
    [[0, 1], [1, -1], [1, 0], [1, 1]],  # J-Piece
    [[0, 1], [0, 2], [1, 0], [1, 1]],  # S-Piece
    [[0, 0], [0, 1], [1, 1], [1, 2]]   # Z-Piece
]

colors = [
    (0, 255, 255),    # Cyan (I-Piece)
    (255, 255, 0),    # Yellow (O-Piece)
    (128, 0, 128),    # Purple (T-Piece)
    (255, 165, 0),    # Orange (L-Piece)
    (0, 0, 255),      # Blue (J-Piece)
    (0, 255, 0),      # Green (S-Piece)
    (255, 0, 0)       # Red (Z-Piece)
] 
board = [[0 for _ in range(10)]for _ in range(20)]
clock = p.time.Clock()
spots = [[r(0, 400), r(0, 800)] for _ in range(50)]
moon = p.image.load('moon.png')
p.mixer.init()

class piece:
    size = 30
    can_switch = True
    def __init__(self):
        self.right = r(0, 8)
        self.down = 0
        self.shape = c(shapes)
        self.color = shapes.index(self.shape)+1 #to avoid using 0 as a color since empty spots in the 2d array called board are gonna be 0's
        self.si = shapes.index(self.shape)

    def move_right(self, num):
        for i in self.shape:
            if board[i[1] + self.down][i[0] + self.right + num] > 0 or i[0] + self.right + num < 0:
                return self.right
        return self.right + num

    def move_down(self):
        for i in self.shape:
            if board[i[1] + self.down + 1][i[0] + self.right] > 0:
                raise
        return self.down + 1
    
    def rotate(self):
        newshape = [[i[1], -(i[0])] for i in self.shape]
        for i in newshape:
            if i[0] + self.right > 9: self.right -= 1
            if i[0] + self.right < 0: self.right += 1
            if board[i[1] + self.down][i[0] + self.right] > 0:
                return self.shape
        return newshape

    def draw(self, pre_right, pre_down):
        ps = piece.size
        color = colors[self.color-1]
        for i in self.shape:
            right = i[0] + pre_right
            down = i[1] + pre_down
            p.draw.rect(Game.window, color, p.Rect(right*ps + 1, down*ps + 1, ps - 2, ps - 2))

        top_left = (right*ps, down*ps)
        top_right = ((right + 1)*ps, down*ps)
        bottom_left = ((right)*ps, (down + 1)*ps)
        bottom_right = ((right + 1)*ps, (down + 1)*ps)

    def draw_next(self):
        ps = piece.size
        color = colors[self.color-1]
        for i in self.shape:
            right = i[0] + 12
            down = i[1] + 4
            p.draw.rect(Game.window, (color), p.Rect(right*ps, down*ps, ps-1, ps-1))

    def draw_hold(self):
        ps = piece.size
        color = colors[self.color-1]
        for i in self.shape:
            right = i[0] + 12
            down = i[1] + 12
            p.draw.rect(Game.window, (color), p.Rect(right*ps, down*ps, ps-1, ps-1))



class Game:
    window = p.display.set_mode((piece.size*16, piece.size*20))
    p.init()
    p.mixer.init()
    def __init__(self):
        self.cur_piece = piece()
        self.next_piece = piece()
        self.hold = None
        self.eye_level = [5, 8]

    def next_up(self, pressed):
        if not pressed:
            for i in self.cur_piece.shape:
                board[i[1] + self.cur_piece.down][i[0] + self.cur_piece.right] = self.cur_piece.color
            self.cur_piece, self.next_piece = self.next_piece, piece()
            return True

    @staticmethod
    def draw_board():
        ps = piece.size
        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if col > 0:
                    p.draw.rect(Game.window, colors[col-1], p.Rect(j*ps + 1, i*ps + 1, ps - 2, ps - 2))

    def controls(self):
        pressed = False
        keys = p.key.get_pressed()
        if keys[p.K_z]:
            piece.size += 1
            Game.window = p.display.set_mode((piece.size*16, piece.size*20))
        if keys[p.K_o]:
            piece.size -= 1
            Game.window = p.display.set_mode((piece.size*16, piece.size*20))
        if keys[p.K_RIGHT]:
            try: self.cur_piece.right = self.cur_piece.move_right(1)
            except: pass
        if keys[p.K_LEFT]:
            try: self.cur_piece.right = self.cur_piece.move_right(-1)
            except: pass
        if keys[p.K_UP]:
            try: self.cur_piece.shape = self.cur_piece.rotate()
            except: pass
        if keys[p.K_UP] or keys[p.K_RIGHT] or keys[p.K_LEFT]:
            pressed = True

        if keys[p.K_DOWN]:
            try: self.cur_piece.down = self.cur_piece.move_down()
            except: 
                piece.can_switch = self.next_up(pressed)

        if keys[p.K_SPACE]:
            while True:
                try: 
                    self.cur_piece.down = self.cur_piece.move_down()
                    self.draw()
                    p.display.update()
                except: 
                    piece.can_switch = self.next_up(pressed)
                    break

        if keys[p.K_h] and piece.can_switch:
            if not self.hold:
                self.hold, self.next_piece = self.next_piece, piece()
            self.cur_piece, self.hold = self.hold, self.cur_piece
            self.hold.shape = shapes[self.hold.si]
            self.cur_piece.down = 0
            piece.can_switch = False

        if keys[p.K_s]: self.eye_level[1] = min(self.eye_level[1] + 1, 10)
        if keys[p.K_w]: self.eye_level[1] = max(self.eye_level[1] - 1, 0)
        if keys[p.K_a]: self.eye_level[0] = min(self.eye_level[0] + 1, 10)
        if keys[p.K_d]: self.eye_level[0] = max(self.eye_level[0] - 1, 0)


        return pressed
    @staticmethod
    def clear_rows():
        for i, row in enumerate(board):
            if 0 not in row:
                for i in range(i, 0, -1):
                    board[i] = board[i-1]
                board[0] = [0 for _ in row]

    @staticmethod
    def draw_polygon(color, r, d, eye_level):
        ps = piece.size
        #right includes left, and down includes up using negitive numbers
        r_a = (eye_level[0] - r)*2
        d_a = (eye_level[1] - d)*2
        
        top_left = (r*ps, d*ps)
        top_right = ((r + 1)*ps, d*ps)
        bottom_left = ((r)*ps, (d + 1)*ps)
        bottom_right = ((r + 1)*ps, (d + 1)*ps)
        
        top_left_corner = (top_left[0] + r_a, top_left[1] + d_a)
        top_right_corner = (top_right[0] + r_a, top_right[1] + d_a)
        bottom_left_corner = (bottom_left[0] + r_a, bottom_left[1] + d_a)
        bottom_right_corner = (bottom_right[0] + r_a, bottom_right[1] + d_a)

        p.draw.polygon(Game.window, color, (top_left, top_left_corner, top_right_corner, top_right))
        p.draw.polygon(Game.window, color, (top_left, top_left_corner, bottom_left_corner, bottom_left))
        p.draw.polygon(Game.window, color, (top_right, top_right_corner, bottom_right_corner, bottom_right))
        p.draw.polygon(Game.window, color, (bottom_left, bottom_left_corner, bottom_right_corner, bottom_right))

        p.draw.line(Game.window, (0,0,0), top_right, top_right_corner, 1)
        p.draw.line(Game.window, (0,0,0), top_left, top_left_corner, 1)
        p.draw.line(Game.window, (0,0,0), top_right, top_right_corner, 1)
        p.draw.line(Game.window, (0,0,0), bottom_left, bottom_left_corner, 1)

        p.draw.line(Game.window, (1,0,0), top_right, top_left, 1)
        p.draw.line(Game.window, (1,0,0), top_right, bottom_right, 1)
        p.draw.line(Game.window, (1,0,0), top_left, bottom_left, 1)
        p.draw.line(Game.window, (1,0,0), bottom_right, bottom_left, 1)


    def draw(self, time = [0]):
        time[0] += 1
        Game.window.fill('black')
        for i in spots:
            p.draw.circle(Game.window, (255, 255, 255), (i[0] + self.eye_level[0]/2, i[1] + self.eye_level[1]/2), 1)
        Game.window.blit(moon, (250 + self.eye_level[0], 50 + self.eye_level[1]))
        cp = self.cur_piece
        for i in cp.shape:
            c =  colors[cp.color-1]
            self.draw_polygon((c[0]/2, c[1]/2, c[2]/2), cp.right + i[0], cp.down + i[1], self.eye_level)

        for i, row in enumerate(board):
            for j, col in enumerate(row): 
                if col == 0: continue  
                c =  colors[col-1]
                self.draw_polygon((c[0]/2, c[1]/2, c[2]/2), j, i, self.eye_level)
        
        c = colors[self.next_piece.color-1]
        for i in self.next_piece.shape:
            self.draw_polygon((c[0]/2, c[1]/2, c[2]/2), 12 + i[0], 4 + i[1], self.eye_level)

        cp.draw(cp.right, cp.down)
        self.draw_board()
        self.next_piece.draw(12, 4)
        if self.hold: 
            c = colors[self.hold.color-1]
            for i in self.hold.shape:
                self.draw_polygon((c[0]/2, c[1]/2, c[2]/2), 12 + i[0], 12 + i[1], self.eye_level)
            self.hold.draw(12, 12)
        # for i in range(11):
        #     p.draw.line(Game.window, (i*20,40-i,100), (i*piece.size, 0), (i*piece.size, 800), 1)
        # for i in range(21):
        #     p.draw.line(Game.window, (i*10,40-i,100), (0, i*piece.size), (400, i*piece.size), 1)

        p.display.update()

    def update(self, time = [0]): 
        time[0] += 1
        pressed = self.controls()
        if time[0]%5 == 0:
            try: self.cur_piece.down = self.cur_piece.move_down()
            except: 
                piece.can_switch = self.next_up(pressed)
        self.clear_rows()
        self.draw()

    def run(self):
        while True:
            clock.tick(12)

            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    return

            self.update()

game = Game()
game.run()
