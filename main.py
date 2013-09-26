from numpy import linalg
from GoProController import GoProController as GPC
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import urllib2
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def getImages(dir="http://10.5.5.9:8080/videos/DCIM/100GOPRO/"):
    soup = BeautifulSoup(urllib2.urlopen(dir))

    links = soup.find_all('a', attrs={'class': 'link'})
    linkList = filter(lambda x: ".JPG" in x, [y["href"] for y in links])


    print(linkList[-6:])
    for n,imageLink in enumerate(linkList[-3:]):
        imgRqst = urllib2.Request("img/"+dir+imageLink)
        imgData = urllib2.urlopen(imgRqst).read()
        outFile = open("img"+str(n+1)+".jpg","wb")
        outFile.write(imgData)
        outFile.close()


def filter_matches(matches, ratio = 0.75):
    filtered_matches = []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            filtered_matches.append(m[0])

    return filtered_matches

def imageDistance(matches):
    sumDistance = 0.0
    for match in matches:
        sumDistance += match.distance
    return sumDistance

def findDimensions(image, homography):
    base_p1 = np.ones(3, np.float32)
    base_p2 = np.ones(3, np.float32)
    base_p3 = np.ones(3, np.float32)
    base_p4 = np.ones(3, np.float32)

    (y, x) = image.shape[:2]

    base_p1[:2] = [0,0]
    base_p2[:2] = [x,0]
    base_p3[:2] = [0,y]
    base_p4[:2] = [x,y]

    max_x = None
    max_y = None
    min_x = None
    min_y = None

    for pt in [base_p1, base_p2, base_p3, base_p4]:

        hp = np.matrix(homography, np.float32) * np.matrix(pt, np.float32).T

        hp_arr = np.array(hp, np.float32)

        normal_pt = np.array([hp_arr[0]/hp_arr[2], hp_arr[1]/hp_arr[2]], np.float32)

        if ( max_x == None or normal_pt[0,0] > max_x ):
            max_x = normal_pt[0,0]

        if ( max_y == None or normal_pt[1,0] > max_y ):
            max_y = normal_pt[1,0]

        if ( min_x == None or normal_pt[0,0] < min_x ):
            min_x = normal_pt[0,0]

        if ( min_y == None or normal_pt[1,0] < min_y ):
            min_y = normal_pt[1,0]

    min_x = min(0, min_x)
    min_y = min(0, min_y)

    return (min_x, min_y, max_x, max_y)



def stichImages(path = "./img"):
    imgPath = [join(path,f) for f in listdir(path) if isfile(join(path,f))]
    print(imgPath)
    rgbImg = []
    grayImgs = []
    keypoints = []
    descriptors = []
    hessian_threshold = 500
    for x in range(2):
        im = cv2.imread(imgPath[x])
        newX, newY = im.shape[1]/4,im.shape[0]/4
        newim = cv2.resize(im,(newX,newY))
        # newim = im
        rgbImg.append(newim)
        gray_im = cv2.cvtColor(newim, cv2.COLOR_BGR2GRAY)
        grayImgs.append(gray_im)

        surf = cv2.SURF(hessian_threshold)
        kp,desc = surf.detectAndCompute(gray_im, None )

        # extractor = cv2.DescriptorExtractor_create("SURF")
        # kp, desc = extractor.compute(gray_im,kp)
        #
        keypoints.append(kp)
        descriptors.append(desc)

    # FLann parameters
    index_params = dict(algorithm = 1,trees = 5)
    search_params = dict(checks=50)
    flannMatcher = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flannMatcher.knnMatch(descriptors[1], trainDescriptors=descriptors[0],k=2)
    print("Match Count {0}".format(len(matches)))

    matches_subset = filter_matches(matches)
    print("New MatchCount {0}".format(len(matches_subset)))

    plt.figure()
    plt.hist([x.distance for x in matches_subset],  50, normed=1, histtype='step')


    distance = imageDistance(matches_subset)
    kp1 =[]
    kp2 =[]
    for match in matches_subset:
        kp1.append(keypoints[0][match.trainIdx])
        kp2.append(keypoints[1][match.queryIdx])

    p1 = np.array([k.pt for k in kp1])
    p2 = np.array([k.pt for k in kp2])

    for p in p1:
        print p
    print "======================="
    for p in p2:
        print p

    # img3= cv2.drawKeypoints(grayImgs[0],matches_subset[0])
    # img4= cv2.drawKeypoints(grayImgs[1],matches_subset[1])

    # imStiched = np.concatenate((img3, img4), axis=1)
    #
    # grayImgs.append(img3)
    # grayImgs.append(img4)
    # grayImgs.append(imStiched)

    # H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 4.0)
    # print '%d / %d  inliers/matched' % (np.sum(status), len(status))
    #
    # # Diff sizes
    # H_inv = linalg.inv(H)
    # (min_x, min_y, max_x, max_y) = findDimensions(grayImgs[1], H_inv)
    # max_x = max(max_x, grayImgs[0].shape[1])
    # max_y = max(max_y, grayImgs[0].shape[0])
    #
    # move_h = np.matrix(np.identity(3), np.float32)
    #
    # if ( min_x < 0 ):
    #     move_h[0,2] += -min_x
    #     max_x += -min_x
    #
    # if ( min_y < 0 ):
    #     move_h[1,2] += -min_y
    #     max_y += -min_y
    #
    # # print "Homography: \n", H
    # # print "Inverse Homography: \n", H_inv
    # # print "Min Points: ", (min_x, min_y)
    #
    # mod_inv_h = move_h * H_inv
    #
    # img_w = int(math.ceil(max_x))
    # img_h = int(math.ceil(max_y))
    #
    # print "New Dimensions: ", (img_w, img_h)
    #
    # # Warp the new image given the homography from the old image
    # base_img_warp = cv2.warpPerspective(rgbImg[0], move_h, (img_w, img_h))
    #
    # # utils.showImage(base_img_warp, scale=(0.2, 0.2), timeout=5000)
    # # cv2.destroyAllWindows()
    #
    # next_img_warp = cv2.warpPerspective(rgbImg[1], mod_inv_h, (img_w, img_h))
    # enlarged_base_img = np.zeros((img_h, img_w, 3), np.uint8)
    #
    #
    #
    # (ret,data_map) = cv2.threshold(cv2.cvtColor(next_img_warp, cv2.COLOR_BGR2GRAY),
    #         0, 255, cv2.THRESH_BINARY)
    #
    # enlarged_base_img = cv2.add(enlarged_base_img, base_img_warp,
    #     mask=np.bitwise_not(data_map),
    #     dtype=cv2.CV_8U)
    #
    # # Now add the warped image
    # final_img = cv2.add(enlarged_base_img, next_img_warp,
    #     dtype=cv2.CV_8U)
    #
    #
    #
    # final_gray = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(final_gray, 1, 255, cv2.THRESH_BINARY)
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #
    # max_area = 0
    # best_rect = (0,0,0,0)
    #
    # for cnt in contours:
    #     x,y,w,h = cv2.boundingRect(cnt)
    #     # print "Bounding Rectangle: ", (x,y,w,h)
    #
    #     deltaHeight = h-y
    #     deltaWidth = w-x
    #
    #     area = deltaHeight * deltaWidth
    #
    #     if ( area > max_area and deltaHeight > 0 and deltaWidth > 0):
    #         max_area = area
    #         best_rect = (x,y,w,h)
    #
    # if ( max_area > 0 ):
    #     # print "Maximum Contour: ", max_area
    #     # print "Best Rectangle: ", best_rect
    #
    #     final_img_crop = final_img[best_rect[1]:best_rect[1]+best_rect[3],
    #             best_rect[0]:best_rect[0]+best_rect[2]]
    #
    #     # utils.showImage(final_img_crop, scale=(0.2, 0.2), timeout=0)
    #     # cv2.destroyAllWindows()
    #
    #     final_img = final_img_crop

    # Write out the current round
    # cv2.imshow("Final",final_img)
    # final_filename = "%s/%d.JPG" % (output, round)
    # cv2.imwrite("Shitshit.jpg", final_img)



    # matchesMask = [[0,0] for i in xrange(len(matches))]
    # for i,(m,n) in enumerate(matches):
    #     if m.distance <0.7*n.distance:
    #         matchesMask[i]= [1,0]
    #
    # draw_params = dict(matchColor = (0, 255, 0),
    #                    singlePointColor =(255, 0, 0),
    #                    matchesMask = matchesMask,
    #                    flags = 0)
    #
    # img3 = []
    # img3= cv2.drawKeypoints(grayImgs[0],keypoints[0])
    # img4= cv2.drawKeypoints(grayImgs[1],keypoints[1])
    # k = keypoints[0][0]
    # print(x[0].response for x in keypoints[0])
    # print(x[0].response for x in keypoints[1])
    #
    # k1 = np.zeros((2,len(keypoints[0])), dtype=np.int32)
    # k2 = np.zeros((2,len(keypoints[1])), dtype=np.int32)
    #
    # k1 = np.array([x.pt for x in keypoints[0]], dtype=np.int32)
    # # k1[1,:] = np.array([x.pt for x in keypoints[0]], dtype=np.int32)
    # k2= np.array([x.pt for x in keypoints[1]], dtype=np.int32)
    # # k2[1,:] = np.array([x.pt for x in keypoints[1]], dtype=np.int32)
    # imMatch , mask2= cv2.findHomography(k1, k2,cv2.RANSAC,5.0)#,mask = np.array(matchesMask))
    # # img3 = cv2.drawMatchesKnn(grayImgs[0],kp[0],grayImgs[1],kp[1],matches,None,**draw_params)
    # grayImgs.append(img3)
    # # grayImgs.append(img4)

    # for x,img in enumerate(grayImgs):
    #     cv2.imshow("BW_"+str(x),img)

    cv2.waitKey()


if __name__ == "__main__":
    gpc = GPC("wlan0")
    ssid = "theprogo"
    pw = "calculator"
    #getImages()

