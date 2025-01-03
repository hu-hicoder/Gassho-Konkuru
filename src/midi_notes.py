import pygame
import pygame.midi
import mido
import threading


# MIDIファイルを再生する関数
def play_midi(midi_file):
    def _play():
        pygame.midi.init()
        output_id = pygame.midi.get_default_output_id()
        if output_id == -1:
            print("MIDIデバイスが見つかりません。")
            pygame.midi.quit()
            return

        player = pygame.midi.Output(output_id)
        player.set_instrument(0)  # 標準ピアノ
        midi_data = mido.MidiFile(midi_file)

        try:
            for msg in midi_data.play():
                if not hasattr(msg, "channel"):
                    continue
                elif msg.channel == 9:  # ドラムトラックは再生しない
                    continue

                if msg.type == "note_on":
                    player.note_on(msg.note, msg.velocity)
                elif msg.type == "note_off":
                    player.note_off(msg.note, msg.velocity)
        except Exception as e:
            print(f"MIDI再生中にエラーが発生しました: {e}")
        finally:
            player.close()
            pygame.midi.quit()

    threading.Thread(target=_play, daemon=True).start()
