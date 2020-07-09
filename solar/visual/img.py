import matplotlib.pyplot as plt
import sunpy.map as sm
from pathlib import Path
from .base_visual import Visual_Builder


class Image_Builder(Visual_Builder):

    visual_type = "image"

    def add_annotation(self, fits, **kwargs):
        if not self.fig:
            return None
        self.fig.text(
            0.01,
            0.01,
            # (
            #    f"({round(self.im_ll_x,2)}, {round(self.im_ll_y, 2)})"
            #    f"-- ({round(self.im_ur_x, 2)}, {round(self.im_ur_y, 2)})"
            #    f"::({round(self.width, 2)}, {round(self.height, 2)})"
            self.generate_annotation(fits),
            # )
            fontsize=4,
            color="aliceblue",
        )

    def __init__(self, im_type):
        super().__init__(im_type)

    def save_visual(self, fits, save_path, clear_after=True, **kwargs):
        bbox = self.fig.get_window_extent().transformed(
            self.fig.dpi_scale_trans.inverted()
        )
        self.width, self.height = bbox.width * self.fig.dpi, bbox.height * self.fig.dpi
        (self.im_ll_x, self.im_ll_y), (self.im_ur_x, self.im_ur_y) = (
            self.fig.axes[0].get_position().get_points()
        )
        self.add_annotation(fits, **kwargs)
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.fig.savefig(save_path, metadata=self.generate_metadata(fits))
        if clear_after:
            plt.close()


class Unframed_Image(Image_Builder):
    def __init__(self, im_type):
        super().__init__(im_type)
        self.frame = False

    def create(self, file_path, cmap="hot", size=3, **kwargs):
        if not Path(file_path).is_file():
            return False
        self.map = sm.Map(file_path)
        x = self.map.meta["naxis1"]
        y = self.map.meta["naxis2"]
        larger = max(x, y)
        self.fig = plt.figure()
        self.fig.set_size_inches((x / larger) * size, (y / larger) * size)
        self.ax = plt.Axes(self.fig, [0.0, 0.0, 1.0, 1.0])
        self.ax.set_axis_off()
        self.fig.add_axes(self.ax)
        plt.set_cmap(cmap)

        data_stamp = kwargs.get("data_stamp", None)
        if data_stamp:
            self.ax.text(0.1, 0.1, data_stamp, fontsize=4, color="white")

        self.ax.imshow(self.map.data, aspect="equal", origin="lower")
        return True


class Basic_Image(Image_Builder):
    def __init__(self, im_type):
        super().__init__(im_type)
        self.frame = False

    def create(self, file_path, cmap="hot", size=3, **kwargs):
        if not Path(file_path).is_file():
            print(
                "You are asking me to create an image from a fits file that does not exist"
            )
            return False
        self.map = sm.Map(file_path)
        title_obsdate = self.map.date.strftime("%Y-%b-%d %H:%M:%S")
        self.fig = plt.figure(
            # figsize=[4.4, 4.4],
            dpi=300
        )
        self.ax = self.fig.add_subplot(1, 1, 1, projection=self.map)
        # self.fig.subplots_adjust(right = 1, left = -.2,top = 0.9, bottom=0.1)
        # self.ax.imshow(self.map.data)
        self.map.plot()
        self.ax.set_xlabel("Solar X (arcsec)")
        self.ax.set_ylabel("Solar Y (arcsec)")
        self.ax.set_title(f"SDO-AIA   {title_obsdate}")
        return True

    def show(self):
        plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
