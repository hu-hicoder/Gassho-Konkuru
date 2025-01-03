from pygame import Surface, image, transform


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
