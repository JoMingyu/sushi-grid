from itertools import islice
from os import listdir
from os.path import join

from PIL import Image
from click import command, argument


def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))


def square_and_resize_image(image: Image, resize_scale: int):
    width, height = image.size

    if width > height:
        # 가로로 긴 이미지
        pivot = (width - height) // 2
        image = image.crop((pivot, 0, width - pivot, height))
    elif width < height:
        # 세로로 긴 이미지
        pivot = (width - height) // 2
        image = image.crop((0, pivot, width, height - pivot))

    image = image.resize((resize_scale, resize_scale))

    return image


def make_2by2_grid(images, grid_scale) -> Image:
    margin_per_item = grid_scale // 80 // 4

    background = Image.new("RGBA", (grid_scale, grid_scale), (255, 255, 255, 255))

    offsets = [
        (0, 0),
        (grid_scale // 2 + margin_per_item, 0),
        (0, grid_scale // 2 + margin_per_item),
        (grid_scale // 2 + margin_per_item, grid_scale // 2 + margin_per_item),
    ]

    for index, _ in enumerate(images):
        image = square_and_resize_image(
            Image.open(_), grid_scale // 2 - margin_per_item
        )
        background.paste(image, offsets[index])

    return background


def build_grids(source_path: str, output_path: str):
    filenames = [join(source_path, f) for f in listdir(source_path)]

    chunks_of_grid_target_filenames = chunk(filenames, 4)

    pil_images = []

    for grid_target_filenames in chunks_of_grid_target_filenames:
        if len(grid_target_filenames) < 4:
            pil_images += [Image.open(filename) for filename in grid_target_filenames]
        else:
            pil_images.append(make_2by2_grid(grid_target_filenames, 2048))

    for seq, grid in enumerate(pil_images):
        grid.save(join(output_path, f"grid-{seq}.png"))


@command()
@argument("folder_path")
@argument("output_path", default=".")
def handler(folder_path: str, output_path: str):
    build_grids(source_path=folder_path, output_path=output_path)
