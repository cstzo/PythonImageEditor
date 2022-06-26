import math
from PIL import Image, ImageDraw


class Filters:
    """
    This class takes as an input the parameters to be changes, having 0 as default for everything,
    the path for the image that is going to be used, and outputs the final image
    """

    def __init__(self, image_path):
        self.image_path = image_path
        self.output_path = 'last_image_ran.png'
        self.output_name = self.output_path

    def cartoon(self, num, beta = 100, bright=0.5):
        """
        Creates a cartoon effect on the image
        :param num:
        :param beta:
        :param bright:
        :return:
        """
        
        input_image = Image.open(self.image_path)
        input_pixels = input_image.load()

        # Create output image
        output_image = Image.new("RGB", input_image.size)

        draw = ImageDraw.Draw(output_image)

        for x in range(output_image.width):
            for y in range(output_image.height):
                r, g, b = input_pixels[x, y]
                for i in range(0, num):
                    if i * (256 / num) < r <= (i + 1) * (256 / num):
                        r = int((i + bright) * (256 / num))
                    if i * (256 / num) < g <= (i + 1) * (256 / num):
                        g = int((i + bright) * (256 / num))
                    if i * (256 / num) < b <= (i + 1) * (256 / num):
                        b = int((i + bright) * (256 / num))

                draw.point((x, y), (r, g, b))

        output_image.save(self.output_path)
        Image.open(self.output_path)
        return self.output_name

    def saturation(self, beta=100):
        """
        This function modifies the saturation parameters of the image being edited
        :param beta:
        :return:
        """

        input_image = Image.open(self.image_path)
        input_pixels = input_image.load()
        # Create output image
        output_image = Image.new("RGB", input_image.size)

        draw = ImageDraw.Draw(output_image)

        if beta > 254:  # default as whatever/0 will give error
            alpha = 254
        else:
            alpha = (255 + beta) / (255 - beta)

        for x in range(output_image.width):
            for y in range(output_image.height):
                r, g, b = input_pixels[x, y]

                graysc = (r + g + b) / 3

                r = int(alpha * (r - graysc) + graysc)
                g = int(alpha * (g - graysc) + graysc)
                b = int(alpha * (b - graysc) + graysc)

                draw.point((x, y), (r, g, b))

        output_image.save(self.output_path)
        Image.open(self.output_path)
        return self.output_name

    def gamma_correction(self, gamma=1.0):
        """
        This function corrects the gamma of the image being edited
        :param gamma:
        :return:
        """

        if gamma < 0.3:
            gamma = 0.3
        input_image = Image.open(self.image_path)
        input_pixels = input_image.load()
        output_image = Image.new("RGB", input_image.size)

        draw = ImageDraw.Draw(output_image)
        for x in range(output_image.width):
            for y in range(output_image.height):
                r, g, b = input_pixels[x, y]

                #graysc = (r + g + b) / 3

                r = int(255 * ((r/255)**(1/gamma)))
                g = int(255 * ((g/255)**(1/gamma)))
                b = int(255 * ((b/255)**(1/gamma)))

                draw.point((x, y), (r, g, b))
        output_image.save(self.output_path)
        Image.open(self.output_path)
        return self.output_name

    def purple(self, intensity):
        """
        This filter applies a purple, galaxy-like effect to the imag being edited
        :param intensity:
        :return:
        """

        input_image = Image.open(self.image_path)
        input_pixels = input_image.load()

        output_image = Image.new("RGB", input_image.size)

        draw = ImageDraw.Draw(output_image)

        for x in range(output_image.width):
            for y in range(output_image.height):
                r, g, b = input_pixels[x, y]
                (r, g) = (g, r)
                b = (r*g+25)//int(r)

                draw.point((x, y), (r, g, b))
        output_image.save(self.output_path)
        Image.open(self.output_path)
        return self.output_name

    def burning(self, intensity):
        """
        This function applies a burning effect to the image being edited
        :param intensity:
        :return:
        """
        input_image = Image.open(self.image_path)
        input_pixels = input_image.load()

        output_image = Image.new("RGB", input_image.size)
        draw = ImageDraw.Draw(output_image)

        for x in range(output_image.width):
            for y in range(output_image.height):
                r, g, b = input_pixels[x, y]
                r = int((4 + abs(math.cos(4 * intensity))) * r // 1.8)
                g = intensity * g // 9
                b = int(b * 1.2)

                draw.point((x, y), (r, g, b))
        output_image.save(self.output_path)
        Image.open(self.output_path)
        return self.output_name

    def perfect_undertone(self):
        """
        This function is not used but gets the image being edited's undertone color.
        :return:
        """

        a = str(self.output_path)
        input_image = Image.open(self.image_path)
        input_pixels = input_image.load()

        output_image = Image.new("RGB", input_image.size)
        draw = ImageDraw.Draw(output_image)
        r_val = 0
        g_val = 0
        b_val = 0
        points = 0
        for x in range(output_image.width):
            for y in range(output_image.height):
                r, g, b = input_pixels[x, y]
                if 60<r<200 or 60<g<200 or 60<b<200:
                    points += 1
                    r_val += r
                    g_val += g
                    b_val += b

                #draw.point((x, y), (r, g, b))
        r_avg = r_val // points
        g_avg = g_val // points
        b_avg = b_val // points
        for x in range(output_image.width):
            for y in range(output_image.height):
                draw.point((x, y), (r_avg, g_avg, b_avg))
        output_image.save(self.output_path)
        Image.open(self.output_path)
        return self.output_name