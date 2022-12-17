import time
from itertools import islice
from multiprocessing import Process
from os import listdir
from os.path import join

from PIL import Image
from click import command, argument


def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))


def resize_image(image: Image, resize_scale: int):
    image = image.resize((resize_scale, resize_scale))

    return image


def make_2by2_grid(images, grid_scale, output_path) -> Image:
    if len(images) == 1:
        image = Image.open(images[0])
        image.save(output_path)
    else:
        margin_per_item = grid_scale // 80 // 4

        background = Image.new("RGBA", (grid_scale, grid_scale), (255, 255, 255, 255))

        offsets = [
            (0, 0),
            (grid_scale // 2 + margin_per_item, 0),
            (0, grid_scale // 2 + margin_per_item),
            (grid_scale // 2 + margin_per_item, grid_scale // 2 + margin_per_item),
        ]

        for index, _ in enumerate(images):
            image = resize_image(Image.open(_), grid_scale // 2 - margin_per_item)
            background.paste(image, offsets[index])

        background.save(output_path)


def build_grids(source_path: str, output_path: str):
    filenames = [
        join(source_path, f) for f in sorted(listdir(source_path)) if f != ".DS_Store"
    ]

    chunks = chunk(filenames, 4)
    chunks_splited = []
    for c in chunks:
        if len(c) < 4:
            chunks_splited += [(_,) for _ in c]
        else:
            chunks_splited.append(c)

    processes = []

    for index, grid_target_filenames in enumerate(chunks_splited):
        processes.append(
            Process(
                target=make_2by2_grid,
                args=(
                    grid_target_filenames,
                    2048,
                    join(output_path, f"grid-{index}.png"),
                ),
            )
        )

    for p in processes:
        p.start()

    for p in processes:
        p.join()


@command()
@argument("folder_path")
@argument("output_path", default=".")
def handler(folder_path: str, output_path: str):
    build_grids(source_path=folder_path, output_path=output_path)
