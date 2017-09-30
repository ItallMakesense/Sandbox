from skimage import io, transform, color, feature


pic = io.imread("/home/kirgenvall/task_2_data/posters/1.jpg")
compress = transform.resize(pic, (32,32))
gray = color.rgb2gray(pic)

raw_pic = compress.flatten()
features = feature.hog(gray, transform_sqrt=True)
