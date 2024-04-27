from absl import app
from absl import flags
import cv2

FLAGS = flags.FLAGS

flags.DEFINE_string("image1", None, "Path to the first image file.")
flags.DEFINE_string("image2", None, "Path to the second image file.")
flags.DEFINE_string("output", None, "Path to save the difference image.")
flags.DEFINE_integer("threshold", 0, "Threshold for considering pixel difference.")
flags.DEFINE_boolean("adjust_brightness", True, "Adjust brightness before comparing.")


def compare_images(
    image1_path, image2_path, output_path, threshold=10, adjust_brightness=True
):
    """
    Creates a difference image between two color images, highlighting differences above a threshold.
    Optionally adjusts brightness for better matching before comparison.

    Args:
      image1_path: Path to the first image file.
      image2_path: Path to the second image file.
      output_path: Path to save the difference image.
      threshold: Minimum pixel difference for considering a difference (default 10).
      adjust_brightness: Boolean flag to adjust brightness before comparison (default True).
    """
    try:
        image1 = cv2.imread(image1_path)  # Read in color format (BGR)
        image2 = cv2.imread(image2_path)  # Read in color format (BGR)
    except FileNotFoundError:
        print(f"Error: One or both image files not found!")
        return

    # Resize smaller image to match larger one
    height1, width1 = image1.shape[:2]
    height2, width2 = image2.shape[:2]
    if height1 < height2 or width1 < width2:
        # Resize the smaller image (image1)
        max_height = max(height1, height2)
        max_width = max(width1, width2)
        image1 = cv2.resize(image1, (max_width, max_height))
    elif height1 > height2 or width1 > width2:
        # Resize the smaller image (image2)
        max_height = max(height1, height2)
        max_width = max(width1, width2)
        image2 = cv2.resize(image2, (max_width, max_height))

    # Adjust brightness if flag is set
    if adjust_brightness:
        image1 = adjust_image_brightness(
            image1, image2
        )  # Function to adjust brightness
        image2 = adjust_image_brightness(
            image2, image1
        )  # Adjust both images for better match

    # Calculate absolute difference for each color channel
    b_diff = cv2.absdiff(image1[:, :, 0], image2[:, :, 0])
    g_diff = cv2.absdiff(image1[:, :, 1], image2[:, :, 1])
    r_diff = cv2.absdiff(image1[:, :, 2], image2[:, :, 2])

    # Combine difference channels with element-wise maximum (highlights max difference across channels)
    diff_image = cv2.max(b_diff, cv2.max(g_diff, r_diff))  # Element-wise maximum

    # Thresholding the combined difference image
    mask = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)[
        1
    ]  # Binary thresholding

    # Apply mask to all color channels of the original image
    highlighted_diff = cv2.bitwise_and(image1, image1, mask=mask)

    # Save the highlighted difference image
    cv2.imwrite(output_path, highlighted_diff)
    print(f"Difference image saved to: {output_path}")


# Function to adjust image brightness (example using average intensity)
def adjust_image_brightness(image1, image2):
    """
    Adjusts the brightness of image1 to try to match the average intensity of image2.

    Args:
      image1: The image to adjust brightness.
      image2: The reference image for average intensity.

    Returns:
      The image1 with adjusted brightness (if possible).
    """
    # Calculate average intensity of image2
    avg_intensity2 = cv2.mean(image2)[
        0
    ]  # Assuming BGR order, access blue channel for intensity

    # Calculate average intensity of image1
    avg_intensity1 = cv2.mean(image1)[0]

    # Calculate brightness adjustment factor
    brightness_factor = avg_intensity2 / (
        avg_intensity1 + 1e-7
    )  # Avoid division by zero

    # Apply brightness adjustment (avoid overflow/underflow)
    adjusted_image1 = cv2.convertScaleAbs(image1, alpha=brightness_factor, beta=0)
    return adjusted_image1


def main(_):
    """Main function to run the image comparison script."""
    compare_images(FLAGS.image1, FLAGS.image2, FLAGS.output, FLAGS.threshold, FLAGS.adjust_brightness)


if __name__ == "__main__":
    flags.mark_flag_as_required("image1")
    flags.mark_flag_as_required("image2")
    flags.mark_flag_as_required("output")
    app.run(main)
