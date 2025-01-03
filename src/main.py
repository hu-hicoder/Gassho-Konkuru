import pygame
import numpy as np
import sounddevice as sd
from midi_notes import play_midi
from screen import screen_image, screen_text
import random

# setting
MIDI_FILE = r"src\data\midi\tabi.mid"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.Font("src/data/font/NotoSansJP-Medium.ttf", 74)

# タイトル画面の表示
def show_title_screen():
    screen.fill("white")
    title_font = pygame.font.Font("src/data/font/NotoSansJP-Medium.ttf", 90)
    start_font = pygame.font.Font("src/data/font/NotoSansJP-Medium.ttf", 50)
    title_text = title_font.render("合掌コンクール", True, (0, 0, 0))
    start_text = start_font.render("Press any key to start", True, (0, 0, 0))
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, 200))
    screen.blit(start_text, (screen.get_width() / 2 - start_text.get_width() / 2, 400))
    screen_image(screen, "src/data/images/open.png", (380, 540), (screen.get_width()/2 - 700, 100))
    screen_image(screen, "src/data/images/close.png", (380, 540), (screen.get_width()/2 + 300, 100))

    pygame.display.flip()

show_title_screen()

# キーが押されるまで待つ
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waiting = False

# initialize screen
screen.fill("white")

# Load images
screen_image(
    screen,
    "src/data/images/close.png",
    (380, 540),
    (screen.get_width() / 4 - 316 / 2, 100),
)
screen_image(
    screen,
    "src/data/images/little_open.png",
    (380, 540),
    (screen.get_width() / 2 - 316 / 2, 100),
)
screen_image(
    screen,
    "src/data/images/open.png",
    (380, 540),
    (3 * screen.get_width() / 4 - 316 / 2, 100),
)

# テキストを描画
screen_text(
    screen,
    "あなた",
    "src/data/font/NotoSansJP-Medium.ttf",
    74,
    (0, 0, 0),
    (screen.get_width() / 2 - 80, 600),
)
screen_text(
    screen,
    "octave multiplier: 1.0",
    None,
    50,
    (0, 0, 0),
    (50, 50),
)

# 基準音「ラ」の周波数
A4_FREQ = 440.0
# 半音の周波数比
SEMITONE_RATIO = 2 ** (1 / 12)


# 各音の周波数を計算
def calculate_frequencies(base_freq, num_keys):
    return [base_freq * (SEMITONE_RATIO**i) for i in range(num_keys)]


# ピアノの88鍵の周波数を計算
frequencies = calculate_frequencies(A4_FREQ, 88)


# 正弦波を生成する関数
def generate_sine_wave(frequency, duration, samplerate=44100):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave


# 音声データを再生する関数
def play_sound(frequency, duration=1.0):
    wave = generate_sine_wave(frequency, duration)
    sd.play(wave, samplerate=44100, loop=True)


# キーと周波数の対応
key_to_freq = {
    pygame.K_a: frequencies[0],  # ド
    pygame.K_w: frequencies[1],  # ド#
    pygame.K_s: frequencies[2],  # レ
    pygame.K_e: frequencies[3],  # レ#
    pygame.K_d: frequencies[4],  # ミ
    pygame.K_f: frequencies[5],  # ファ
    pygame.K_t: frequencies[6],  # ファ#
    pygame.K_g: frequencies[7],  # ソ
    pygame.K_y: frequencies[8],  # ソ#
    pygame.K_h: frequencies[9],  # ラ
    pygame.K_u: frequencies[10],  # ラ#
    pygame.K_j: frequencies[11],  # シ
    pygame.K_k: frequencies[12],  # ド（次のオクターブ）
}

# 現在再生中の音を管理する辞書
playing_sounds = {}

# オクターブの倍率
octave_multiplier = 1.0

play_midi(MIDI_FILE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_freq:
                # 現在再生中の音を停止
                if playing_sounds:
                    sd.stop()
                    playing_sounds.clear()
                # 新しい音を再生
                play_sound(key_to_freq[event.key] * octave_multiplier)
                playing_sounds[event.key] = True
                # 画像をランダムに変更
                images = [
                    "close",
                    "little_open",
                    "open",
                ]
                positions = [(screen.get_width() / 4 - 316 / 2, 100),(screen.get_width() / 2 - 316 / 2, 100),(3 * screen.get_width() / 4 - 316 / 2, 100)]
                screen_image(
                    screen,
                    f"src/data/images/{images[random.randint(0,2)]}.png",
                    (380, 540),
                    positions[random.randint(0,2)],
                )
            elif event.key == pygame.K_UP:
                octave_multiplier *= 2.0  # オクターブを上げる
                pygame.draw.rect(screen, (255, 255, 255), (30, 30, 1000, 50))
                screen_text(
                        screen,
                        f"octave multiplier: {octave_multiplier}",
                        None,
                        50,
                        (0, 0, 0),
                        (50, 50),
                    )
            elif event.key == pygame.K_DOWN:
                octave_multiplier /= 2.0  # オクターブを下げる
                pygame.draw.rect(screen, (255, 255, 255), (30, 30, 1000, 50))
                screen_text(
                        screen,
                        f"octave multiplier: {octave_multiplier}",
                        None,
                        50,
                        (0, 0, 0),
                        (50, 50),
                    )
        elif event.type == pygame.KEYUP:
            if event.key in playing_sounds:
                sd.stop()
                del playing_sounds[event.key]

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
