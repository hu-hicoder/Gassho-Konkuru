from pygame import Surface, image, transform, font


def screen_image(
    screen: Surface,
    image_path: str,
    image_size: tuple[int, int],
    position: tuple[int, int],
) -> None:
    """
    画像をスクリーンに描画する関数
    """
    i = image.load(image_path)
    i = transform.scale(i, image_size)
    screen.blit(i, position)

def screen_text(
    screen: Surface,
    text: str,
    font_path: str,
    font_size: int,
    color: tuple[int, int, int],
    position: tuple[int, int],
) -> None:
    """
    テキストをスクリーンに描画する関数
    """
    f = font.Font(font_path, font_size)
    text_surface = f.render(text, True, color)
    screen.blit(text_surface, position)